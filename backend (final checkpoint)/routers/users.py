from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.connection import get_connection, log_audit_action
import hashlib

router = APIRouter(prefix="/users", tags=["Users"])

def hash_password(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


# SIGNUP
@router.post("/signup")
def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    hashed_pw = hash_password(user.password)

    try:
        cur.execute("""
            INSERT INTO Users (username, email, password_hash)
            VALUES (%s, %s, %s)
        """, (user.username, user.email, hashed_pw))

        conn.commit()
        user_id = cur.lastrowid

        log_audit_action(user_id, "SIGNUP", "Users", user_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

    cur.close()
    conn.close()

    return {"message": "User created successfully", "user_id": user_id}


# LOGIN
@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM Users WHERE email = %s", (user.email,))
    record = cur.fetchone()

    if not record:
        raise HTTPException(status_code=404, detail="User not found")

    if record["password_hash"] != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # AUDIT LOG — user logged in
    log_audit_action(record["user_id"], "LOGIN", "Users", record["user_id"])

    return {"message": "Login successful", "user_id": record["user_id"]}
