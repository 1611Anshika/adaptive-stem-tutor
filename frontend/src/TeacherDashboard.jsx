
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  BookOpen,
  Brain,
  GraduationCap,
  Search,
  Target,
  TrendingUp,
  Users,
  RefreshCw
} from "lucide-react";

import "./TeacherDashboard.css";

const API_URL = "http://127.0.0.1:8000";

function TeacherDashboard({ onBack,token }) {
  const [overview, setOverview] = useState({
    total_students: 0,
    });
  const [students, setStudents] = useState([]);
  const [topics, setTopics] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = async () => {
    setLoading(true);
    setError("");

    try {
      const responses = await Promise.all([
        fetch(`${API_URL}/api/teacher/overview`, {
            headers: {
            Authorization: `Bearer ${token}`,
            },
        }),
        fetch(`${API_URL}/api/teacher/students`, {
            headers: {
            Authorization: `Bearer ${token}`,
            },
        }),
        fetch(`${API_URL}/api/teacher/topics`, {
            headers: {
            Authorization: `Bearer ${token}`,
            },
        }),
        ]);

        if (responses.some((response) => response.status === 401)) {
        localStorage.removeItem("student");
        localStorage.removeItem("access_token");
        window.location.reload();
        return;
        }

        if (responses.some((response) => response.status === 403)) {
        throw new Error("Teacher access is required for this dashboard.");
        }

        if (responses.some((response) => !response.ok)) {
        throw new Error("Unable to load teacher analytics.");
        }
        const overviewData = await responses[0].json();
        const studentsData = await responses[1].json();
        const topicsData = await responses[2].json();

        setOverview(overviewData);
        setStudents(studentsData);
        setTopics(topicsData);
    } catch (err) {
      setError(err.message || "Unable to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filteredStudents = students.filter((student) =>
    student.name.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="teacher-loading">
        <Brain size={30} />
        <p>Analyzing class performance...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="teacher-loading">
        <p>{error}</p>
        <button onClick={loadData}>Try again</button>
        <button onClick={onBack}>Back to learning</button>
      </div>
    );
  }

  return (
    <div className="teacher-page">
      <header className="teacher-header">
        <button className="teacher-back" onClick={onBack}>
          <ArrowLeft size={17} />
          Log out
        </button>

        <div className="teacher-brand">
          <Brain size={19} />
          <span>ADAPTIVE STEM</span>
          <span className="teacher-badge">TEACHER SPACE</span>
        </div>

        <button
          className="teacher-refresh"
          onClick={loadData}
          title="Refresh analytics"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </header>

      <main className="teacher-main">
        <section className="teacher-hero">
          <div>
            <span className="teacher-eyebrow">
              CLASS INTELLIGENCE / OVERVIEW
            </span>

            <h1>
              Understand your
              <br />
              <span>class at a glance.</span>
            </h1>

            <p>
              Explore learner progress, uncover knowledge gaps,
              and identify where additional support may help.
            </p>
          </div>

          <div className="teacher-hero-icon">
            <GraduationCap size={44} />
          </div>
        </section>

        <section className="teacher-metrics">
          <Metric
            icon={<Users size={19} />}
            label="REGISTERED STUDENTS"
            value={overview.total_students}
            note="Across all registered accounts"
          />

          <Metric
            icon={<BookOpen size={19} />}
            label="QUESTIONS ATTEMPTED"
            value={overview.total_questions_attempted}
            note="Recorded practice attempts"
          />

          <Metric
            icon={<Target size={19} />}
            label="CLASS ACCURACY"
            value={`${overview.class_accuracy}%`}
            note="Correct answers / attempts"
          />

          <Metric
            icon={<TrendingUp size={19} />}
            label="AVERAGE MASTERY"
            value={`${overview.average_mastery}%`}
            note="Across recorded topic profiles"
          />
        </section>

        <section className="teacher-section">
          <div className="teacher-section-heading">
            <div>
              <span>LEARNER PROFILES</span>
              <h2>Student performance</h2>
            </div>

            <label className="teacher-search">
              <Search size={16} />
              <input
                placeholder="Search students..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </label>
          </div>

          <div className="teacher-table-wrap">
            <table className="teacher-table">
              <thead>
                <tr>
                  <th>STUDENT</th>
                  <th>GRADE</th>
                  <th>QUESTIONS</th>
                  <th>ACCURACY</th>
                  <th>AVG. MASTERY</th>
                  <th>FOCUS TOPIC</th>
                </tr>
              </thead>

              <tbody>
                {filteredStudents.map((student) => (
                  <tr key={student.id}>
                    <td>
                      <div className="teacher-student-name">
                        <div className="teacher-avatar">
                          {student.name.charAt(0).toUpperCase()}
                        </div>
                        <span>{student.name}</span>
                      </div>
                    </td>

                    <td>{student.grade}</td>
                    <td>{student.questions_attempted}</td>

                    <td>
                      <span className="teacher-number">
                        {student.accuracy}%
                      </span>
                    </td>

                    <td>
                      <div className="teacher-mastery-cell">
                        <div className="teacher-mini-bar">
                          <div
                            style={{
                              width: `${student.average_mastery}%`
                            }}
                          />
                        </div>
                        <span>{student.average_mastery}%</span>
                      </div>
                    </td>

                    <td>
                      {student.weakest_topic || "Not assessed"}
                    </td>
                  </tr>
                ))}

                {filteredStudents.length === 0 && (
                  <tr>
                    <td colSpan="6" className="teacher-empty">
                      No matching students found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        <section className="teacher-section">
          <div className="teacher-section-heading">
            <div>
              <span>CURRICULUM INSIGHTS</span>
              <h2>Topic mastery map</h2>
            </div>
          </div>

          <div className="teacher-topic-grid">
            {topics.map((topic) => {
              const level =
                topic.students_assessed === 0
                  ? "Not assessed"
                  : topic.average_mastery < 40
                    ? "Needs support"
                    : topic.average_mastery < 70
                      ? "Developing"
                      : "Strong";

              return (
                <article
                  className="teacher-topic-card"
                  key={topic.topic}
                >
                  <div className="teacher-topic-top">
                    <div className="teacher-topic-icon">
                      <BookOpen size={18} />
                    </div>

                    <span className="teacher-topic-subject">
                      {topic.subject}
                    </span>
                  </div>

                  <h3>{topic.topic}</h3>

                  <div className="teacher-topic-score">
                    <strong>
                      {topic.average_mastery}%
                    </strong>
                    <span>average mastery</span>
                  </div>

                  <div className="teacher-topic-bar">
                    <div
                      style={{
                        width: `${topic.average_mastery}%`
                      }}
                    />
                  </div>

                  <div className="teacher-topic-bottom">
                    <span>{level}</span>
                    <span>
                      {topic.students_assessed} learner
                      {topic.students_assessed === 1 ? "" : "s"}
                    </span>
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <footer className="teacher-footer">
          <Brain size={16} />
          Insights are calculated from recorded assessments
          and quiz attempts. Topics with no mastery records
          have not yet been assessed.
        </footer>
      </main>
    </div>
  );
}


function Metric({ icon, label, value, note }) {
  return (
    <article className="teacher-metric">
      <div className="teacher-metric-icon">{icon}</div>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{note}</small>
    </article>
  );
}

export default TeacherDashboard;