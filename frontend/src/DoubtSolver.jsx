
import { useState } from "react";
import "./DoubtSolver.css";

const API_URL = "http://127.0.0.1:8000";

const TOPICS = [
  "Algebra",
  "Geometry",
  "Probability",
  "Statistics",
];

export default function DoubtSolver({ token, student }) {
  const [question, setQuestion] = useState("");
  const [topic, setTopic] = useState("Algebra");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk(event) {
    event.preventDefault();

    if (!question.trim()) {
      setError("Please enter your question first.");
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await fetch(
        `${API_URL}/api/doubt-solver/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question: question.trim(),
            topic,
            grade: student?.grade
              ? `Grade ${student.grade}`
              : "school level",
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to get an explanation. Please try again."
        );
      }

      setAnswer(data.answer);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the AI tutor. Check that your backend and Ollama are running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="doubt-solver">
      <div className="doubt-header">
        <div className="doubt-icon">✦</div>
        <div>
          <h2>AI Doubt Solver</h2>
          <p>
            Ask questions, understand concepts, and learn step by step.
          </p>
        </div>
      </div>

      <form onSubmit={handleAsk} className="doubt-form">
        <label htmlFor="doubt-topic">Choose a topic</label>

        <select
          id="doubt-topic"
          value={topic}
          onChange={(event) => setTopic(event.target.value)}
        >
          {TOPICS.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>

        <label htmlFor="doubt-question">What are you stuck on?</label>

        <textarea
          id="doubt-question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="For example: Explain how to solve 2x + 5 = 15..."
          rows={5}
          maxLength={2000}
          required
        />

        <div className="doubt-form-footer">
          <span>{question.length}/2000 characters</span>

          <button type="submit" disabled={loading || !question.trim()}>
            {loading ? "Thinking..." : "✦ Explain this"}
          </button>
        </div>
      </form>

      {loading && (
        <div className="doubt-status" role="status">
          Your AI tutor is preparing a step-by-step explanation. This may take
          a little time while the local model generates its answer.
        </div>
      )}

      {error && (
        <div className="doubt-error" role="alert">
          {error}
        </div>
      )}

      {answer && (
        <div className="doubt-answer" aria-live="polite">
          <h3>Your explanation</h3>
          <div className="doubt-answer-text">{answer}</div>

          <button
            type="button"
            className="doubt-followup"
            onClick={() => {
              setQuestion("");
              setAnswer("");
              setError("");
            }}
          >
            Ask another question
          </button>
        </div>
      )}

      <p className="doubt-note">
        Powered by a locally running AI model. Review important answers with
        your course material.
      </p>
    </section>
  );
}