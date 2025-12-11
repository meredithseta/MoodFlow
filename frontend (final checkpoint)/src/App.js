import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [logs, setLogs] = useState([]);
  const [moodTypes, setMoodTypes] = useState([]);
  const [formOpen, setFormOpen] = useState(false);
  const [editingLog, setEditingLog] = useState(null);

  const [formData, setFormData] = useState({
    user_id: 1,
    mood_type_id: "",
    log_date: "",
    mood_color_hex: "#ffaa00",
    stress_level: "",
    notes: ""
  });

  // Fetch ALL logs for a user (user_id = 1)
  const fetchLogs = async () => {
    const res = await axios.get(`${API_BASE}/mood_logs/1`);
    setLogs(res.data);
  };

  // Fetch mood types
  const fetchMoodTypes = async () => {
    const res = await axios.get(`${API_BASE}/mood_logs/types`);
    setMoodTypes(res.data);
  };

  useEffect(() => {
    fetchLogs();
    fetchMoodTypes();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const openCreate = () => {
    setEditingLog(null);
    setFormData({
      user_id: 1,
      mood_type_id: "",
      log_date: "",
      mood_color_hex: "#ffaa00",
      stress_level: "",
      notes: ""
    });
    setFormOpen(true);
  };

  const openEdit = (log) => {
    setEditingLog(log);
    setFormData({
      user_id: log.user_id,
      mood_type_id: log.mood_type_id,
      log_date: log.log_date.split("T")[0],
      mood_color_hex: log.mood_color_hex,
      stress_level: log.stress_level,
      notes: log.notes || ""
    });
    setFormOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      user_id: 1,
      mood_type_id: Number(formData.mood_type_id),
      log_date: formData.log_date,
      mood_color_hex: formData.mood_color_hex,
      stress_level: Number(formData.stress_level),
      notes: formData.notes
    };

    if (editingLog) {
      await axios.put(`${API_BASE}/mood_logs/${editingLog.mood_log_id}`, payload);
    } else {
      await axios.post(`${API_BASE}/mood_logs/`, payload);
    }

    setFormOpen(false);
    fetchLogs();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this entry?")) return;

    await axios.delete(`${API_BASE}/mood_logs/${id}`);
    fetchLogs();
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>MoodFlow – Mood Logs</h1>

      <button onClick={openCreate}>➕ Add Mood Log</button>

      <h2>Your Mood Logs</h2>
      {logs.length === 0 ? (
        <p>No logs yet.</p>
      ) : (
        logs.map((log) => (
          <div key={log.mood_log_id} style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
            <p><strong>Mood:</strong> {log.mood_name}</p>
            <p><strong>Date:</strong> {log.log_date}</p>
            <p><strong>Color:</strong> {log.mood_color_hex}</p>
            <p><strong>Stress Level:</strong> {log.stress_level}</p>
            <p><strong>Notes:</strong> {log.notes || "none"}</p>

            <button onClick={() => openEdit(log)}>✏ Edit</button>
            <button onClick={() => handleDelete(log.mood_log_id)}>🗑 Delete</button>
          </div>
        ))
      )}

      {/* ---------------------- FORM PANEL ---------------------- */}
      {formOpen && (
        <div style={{ marginTop: "20px", padding: "10px", border: "1px solid black" }}>
          <h2>{editingLog ? "Edit Mood Log" : "Create Mood Log"}</h2>

          <form onSubmit={handleSubmit}>
            <label>
              Mood Type:
              <select
                name="mood_type_id"
                value={formData.mood_type_id}
                onChange={handleChange}
                required
              >
                <option value="">Select mood type</option>
                {moodTypes.map((mt) => (
                  <option key={mt.mood_type_id} value={mt.mood_type_id}>
                    {mt.mood_name}
                  </option>
                ))}
              </select>
            </label>
            <br /><br />

            <label>
              Log Date:
              <input
                type="date"
                name="log_date"
                value={formData.log_date}
                onChange={handleChange}
                required
              />
            </label>
            <br /><br />

            <label>
              Mood Color:
              <input
                type="color"
                name="mood_color_hex"
                value={formData.mood_color_hex}
                onChange={handleChange}
                required
              />
            </label>
            <br /><br />

            <label>
              Stress Level (1–10):
              <input
                type="number"
                name="stress_level"
                value={formData.stress_level}
                onChange={handleChange}
                min="1"
                max="10"
                required
              />
            </label>
            <br /><br />

            <label>
              Notes:
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
              />
            </label>
            <br /><br />

            <button type="submit">{editingLog ? "Save Changes" : "Create"}</button>
            <button type="button" onClick={() => setFormOpen(false)}>Cancel</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;