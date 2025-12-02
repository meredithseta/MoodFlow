import tkinter as tk
from tkinter import messagebox
from mood_log_crud import (
    create_mood_log,
    read_mood_logs,
    update_mood_log, 
    delete_mood_log,
    filter_mood_logs
)

def show_results(title, rows):
    win = tk.Toplevel(root)
    win.title(title)
    text = tk.Text(win, width=80, height=20)
    text.pack(fill="both", expand=True)
    for row in rows:
        text.insert(tk.END, str(row) + "\n")

def gui_create():
    try:
        new_id = create_mood_log(
            int(user_id_entry.get()),
            int(mood_type_id_entry.get()),
            color_entry.get(),
            int(stress_entry.get()),
            notes_entry.get()
        )
        messagebox.showinfo("Created", f"Mood Log Created (ID: {new_id})")

        user_id_entry.delete(0, tk.END)
        mood_type_id_entry.delete(0, tk.END)
        color_entry.delete(0, tk.END)
        stress_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def gui_read():
    rows = read_mood_logs()
    show_results("All Mood Logs", rows)

def gui_update():
    try:
        update_mood_log(
            int(update_id_entry.get()),
            update_notes_entry.get()
        )
        messagebox.showinfo("Updated", "Mood Log updated!")

        update_id_entry.delete(0, tk.END)
        update_notes_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def gui_delete():
    try:
        delete_mood_log(int(delete_id_entry.get()))
        messagebox.showinfo("Deleted", "Mood Log deleted!")

        delete_id_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def gui_filter():
    try:
        rows = filter_mood_logs(int(filter_stress_entry.get()))
        show_results("Filtered Mood Logs", rows)

        filter_stress_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))

### GUI Layout ###
root = tk.Tk()
root.resizable(True, True)
root.title("MoodFlow CRUD + Filter GUI")
root.geometry("600x550")

title = tk.Label(root, text="MoodFlow CRUD + Filter Demo", font=("Arial", 18))
title.pack(pady=10)

### Create ###
frame_create = tk.LabelFrame(root, text="Create Mood Log")
frame_create.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_create, text="User ID:").grid(row=0, column=0)
user_id_entry = tk.Entry(frame_create); user_id_entry.grid(row=0, column=1)

tk.Label(frame_create, text="Mood Type ID:").grid(row=1, column=0)
mood_type_id_entry = tk.Entry(frame_create); mood_type_id_entry.grid(row=1, column=1)

tk.Label(frame_create, text="Color HEX:").grid(row=2, column=0)
color_entry = tk.Entry(frame_create); color_entry.grid(row=2, column=1)

tk.Label(frame_create, text="Stress Level (1-10):").grid(row=3, column=0)
stress_entry = tk.Entry(frame_create); stress_entry.grid(row=3, column=1)

tk.Label(frame_create, text="Notes:").grid(row=4, column=0)
notes_entry = tk.Entry(frame_create); notes_entry.grid(row=4, column=1)

tk.Button(frame_create, text="Create", command=gui_create).grid(row=5, column=0, columnspan=2, pady=5)

### Read ###
tk.Button(root, text="Read All Mood Logs", command=gui_read).pack(pady=10)

### Update ###
frame_update = tk.LabelFrame(root, text="Update Mood Log")
frame_update.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_update, text="Mood Log ID:").grid(row=0, column=0)
update_id_entry = tk.Entry(frame_update); update_id_entry.grid(row=0, column = 1)

tk.Label(frame_update, text="New Notes:").grid(row=1, column=0)
update_notes_entry = tk.Entry(frame_update); update_notes_entry.grid(row=1, column = 1)

tk.Button(frame_update, text="Update", command=gui_update).grid(row=2, column=0, columnspan=2, pady=5)

### Delete ###
frame_delete = tk.LabelFrame(root, text="Delete Mood Log")
frame_delete.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_delete, text="Mood Log ID:").grid(row=0, column=0)
delete_id_entry = tk.Entry(frame_delete); delete_id_entry.grid(row=0, column=1)

tk.Button(frame_delete, text="Delete", command=gui_delete).grid(row=1, column=0, columnspan=2, pady=5)

### Filter ###
frame_filter = tk.LabelFrame(root, text="Filter Mood Logs (stress >= X)")
frame_filter.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame_filter, text="Min Stress:").grid(row=0, column=0)
filter_stress_entry = tk.Entry(frame_filter); filter_stress_entry.grid(row=0, column=1)

tk.Button(frame_filter, text="Filter", command=gui_filter).grid(row=1, column=0, columnspan=2, pady=5)

root.mainloop()

