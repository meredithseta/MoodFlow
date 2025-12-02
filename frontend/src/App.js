import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

const moodGradients = {
  "very sad": ["#003B73", "#001428"],
  sad: ["#004E92", "#000428"],
  anxious: ["#5b2cff", "#2a0845"],
  tired: ["#8e2de2", "#4a00e0"],
  irritable: ["#ff512f", "#dd2476"],
  happy: ["#f7971e", "#ffd200"],
  elated: ["#ff9966", "#ff5e62"],
  neutral: ["#485563", "#29323c"],
  fine: ["#3c3b3f", "#605c3c"],
  default: ["#1c1c1c", "#0e0e0e"],
};

function App() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterMood, setFilterMood] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editingLog, setEditingLog] = useState(null);

  const [formData, setFormData] = useState({
    user_id: 1,
    mood: "",
    log_date: "",
    sleep_hours: "",
    water_intake: "",
  });

  const fetchLogs = async () => {
    setLoading(true);
    try {
      let url = `${API_BASE}/mood_logs/`;
      if (filterMood) {
        url = `${API_BASE}/mood_logs/filter?mood=${encodeURIComponent(
          filterMood
        )}`;
      }
      const res = await axios.get(url);
      setLogs(res.data || []);
    } catch (err) {
      alert("Error fetching logs");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchLogs();
  }, [filterMood]);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const resetForm = () => {
    setEditingLog(null);
    setFormData({
      user_id: 1,
      mood: "",
      log_date: "",
      sleep_hours: "",
      water_intake: "",
    });
  };

  const openCreate = () => {
    resetForm();
    setFormOpen(true);
  };

  const openEdit = (log) => {
    setEditingLog(log);
    setFormData({
      user_id: log.user_id,
      mood: log.mood,
      log_date: log.log_date,
      sleep_hours: log.sleep_hours,
      water_intake: log.water_intake,
    });
    setFormOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        user_id: Number(formData.user_id),
        mood: formData.mood,
        log_date: formData.log_date,
        sleep_hours: Number(formData.sleep_hours),
        water_intake: Number(formData.water_intake),
      };

      if (editingLog) {
        await axios.put(`${API_BASE}/mood_logs/${editingLog.mood_id}`, payload);
      } else {
        await axios.post(`${API_BASE}/mood_logs/`, payload);
      }

      setFormOpen(false);
      resetForm();
      fetchLogs();
    } catch {
      alert("Error saving log");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this entry?")) return;
    await axios.delete(`${API_BASE}/mood_logs/${id}`);
    fetchLogs();
  };

  return (
    <div className="app-root">
      <div className="app-shell">
        <div className="header-row">
          <div>
            <h1 className="app-title">moodflow</h1>
            <p className="app-subtitle">Checkpoint 2 · Mood Logs Dashboard</p>
          </div>
          <button className="primary-btn" onClick={openCreate}>
            + add mood log
          </button>
        </div>

        <div className="filter-bar">
          <label>
            Filter by mood:
            <select
              value={filterMood}
              onChange={(e) => setFilterMood(e.target.value)}
              className="filter-select"
            >
              <option value="">All moods</option>
              {Object.keys(moodGradients).map(
                (m) => m !== "default" && <option key={m}>{m}</option>
              )}
            </select>
          </label>
          <button className="ghost-btn" onClick={fetchLogs}>
            refresh
          </button>
        </div>

        <div className="cards-area">
          {loading ? (
            <p>Loading...</p>
          ) : logs.length === 0 ? (
            <p>No logs yet</p>
          ) : (
            logs.map((log) => {
              const [c1, c2] =
                moodGradients[log.mood?.toLowerCase()] ||
                moodGradients.default;

              return (
                <div
                  key={log.mood_id}
                  className="mood-card"
                  style={{
                    backgroundImage: `linear-gradient(180deg, ${c1}, ${c2})`,
                  }}
                >
                  {/* mood circle */}
                  <div
                    className="mood-circle"
                    style={{ background: c1 }}
                  ></div>

                  <div className="card-top">
                    <span className="mood-chip">{log.mood}</span>
                    <span className="mood-date">
                      {new Date(log.log_date).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="mood-stats">
                    <div className="stat-item">
                      <span>hours of sleep</span>
                      <span className="stat-value">{log.sleep_hours}</span>
                    </div>
                    <div className="stat-item">
                      <span>ounces of water</span>
                      <span className="stat-value">{log.water_intake}</span>
                    </div>
                    <div className="stat-item">
                      <span>user id</span>
                      <span className="stat-value">{log.user_id}</span>
                    </div>
                  </div>

                  <div className="mood-card-footer">
                    <button
                      className="ghost-btn small"
                      onClick={() => openEdit(log)}
                    >
                      edit
                    </button>
                    <button
                      className="danger-btn small"
                      onClick={() => handleDelete(log.mood_id)}
                    >
                      delete
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Slide-out form */}
        {formOpen && (
          <div className="form-overlay">
            <div className="form-panel">
              <div className="form-header">
                <h2>{editingLog ? "edit mood log" : "add mood log"}</h2>
                <button
                  className="icon-btn"
                  onClick={() => setFormOpen(false)}
                >
                  ✕
                </button>
              </div>

              <form className="mood-form" onSubmit={handleSubmit}>
                <label>
                  Mood
                  <select
                    name="mood"
                    value={formData.mood}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select mood</option>
                    {Object.keys(moodGradients).map(
                      (m) =>
                        m !== "default" && (
                          <option key={m} value={m}>
                            {m}
                          </option>
                        )
                    )}
                  </select>
                </label>

                <label>
                  Log date
                  <input
                    type="date"
                    name="log_date"
                    value={formData.log_date}
                    onChange={handleChange}
                    required
                  />
                </label>

                <label>
                  Hours of sleep
                  <input
                    type="number"
                    name="sleep_hours"
                    value={formData.sleep_hours}
                    onChange={handleChange}
                    required
                  />
                </label>

                <label>
                  Water intake
                  <input
                    type="number"
                    name="water_intake"
                    value={formData.water_intake}
                    onChange={handleChange}
                    required
                  />
                </label>

                <div className="form-actions">
                  <button
                    type="button"
                    className="ghost-btn"
                    onClick={() => setFormOpen(false)}
                  >
                    cancel
                  </button>
                  <button className="primary-btn" type="submit">
                    {editingLog ? "save" : "create"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
