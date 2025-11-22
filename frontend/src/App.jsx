import React, { useState } from "react";

const RUBRIC = "/mnt/data/8f022ef2-4456-4b09-a530-565c68df177d.png";

export default function App() {
  const [transcript, setTranscript] = useState("");
  const [duration, setDuration] = useState(52);
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);

  async function scoreText(e) {
    e.preventDefault();
    setErr(null);
    setResult(null);
    setLoading(true);
    try {
      const res = await fetch("/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript, duration_sec: Number(duration) }),
      });
      const data = await res.json();
      setResult({ transcript, score: data });
    } catch (error) {
      setErr(error.message || "Error");
    } finally {
      setLoading(false);
    }
  }

  async function scoreAudio(e) {
    e.preventDefault();
    setErr(null);
    setResult(null);
    if (!audioFile) {
      setErr("Please choose an audio file first.");
      return;
    }
    setLoading(true);
    try {
      const form = new FormData();
      form.append("file", audioFile);
      form.append("duration_sec", Number(duration));

      const res = await fetch("/score_audio", {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const t = await res.text();
        throw new Error(t || "Server error");
      }

      const data = await res.json();
      setResult(data);
      setTranscript(data.transcript || "");
    } catch (error) {
      setErr(error.message || "Error uploading audio");
    } finally {
      setLoading(false);
    }
  }

  function handleAudioChange(e) {
    const f = e.target.files[0];
    setAudioFile(f);
  }

  return (
    <div className="container">
      <h1>Nirmaan — Transcript Scorer (Audio + Text)</h1>

      <section>
        <h3>1) Upload audio file</h3>
        <input type="file" accept="audio/*" onChange={handleAudioChange} />
        <div style={{ marginTop: 8 }}>
          <label>Duration (seconds): </label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            style={{ width: 100 }}
          />
        </div>
        <button onClick={scoreAudio} disabled={loading} style={{ marginTop: 8 }}>
          {loading ? "Transcribing & Scoring..." : "Upload & Score Audio"}
        </button>
      </section>

      <hr style={{ margin: "16px 0" }} />

      <section>
        <h3>2) Or paste transcript directly</h3>
        <textarea
          rows={8}
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          style={{ width: "100%" }}
        />
        <div style={{ marginTop: 8 }}>
          <label>Duration (seconds): </label>
          <input
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            style={{ width: 100 }}
          />
          <button onClick={scoreText} disabled={loading} style={{ marginLeft: 12 }}>
            {loading ? "Scoring..." : "Score Text"}
          </button>
        </div>
      </section>

      <hr />

      {/* <div>
        <h4>Rubric preview</h4>
        <img src={RUBRIC} alt="rubric" style={{ maxHeight: 200 }} />
      </div> */}

      {err && <div style={{ color: "red", marginTop: 12 }}>{err}</div>}

      {result && (
        <div style={{ marginTop: 12 }}>
          <h3>Result</h3>
          <pre style={{ maxHeight: 400, overflow: "auto", background: "#f5f7fb", padding: 12 }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
