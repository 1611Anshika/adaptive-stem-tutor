import { useEffect, useState } from "react";
import {
  ArrowUpRight,
  Brain,
  ChevronRight,
  ChevronDown,
  Clock3,
  Flame,
  LockKeyhole,
  Moon,
  Play,
  Sparkles,
  Sun,
  Target,
  Trophy,
  Zap
} from "lucide-react";
import { GraduationCap } from "lucide-react";

import "./App.css";
import Quiz from "./Quiz";
import Assessment from "./Assessment";
import Auth from "./Auth";
import TeacherDashboard from "./TeacherDashboard";
import DoubtSolver from "./DoubtSolver";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [student, setStudent] = useState(() => {
    try {
      const savedStudent = localStorage.getItem("student");
      const savedToken = localStorage.getItem("access_token");

        return savedStudent && savedToken
          ? JSON.parse(savedStudent)
          : null;
      } catch {
        return null;
      }
    });

    const [token, setToken] = useState(
      () => localStorage.getItem("access_token")
    );

  const [dashboard, setDashboard] = useState(null);
  const [learningDNA, setLearningDNA] = useState(null);
  const [dnaError, setDnaError] = useState("");
  const [showQuiz, setShowQuiz] = useState(false);
  const [showAssessment, setShowAssessment] = useState(false);
  
  const [revisionData, setRevisionData] = useState(null);
  const [revisionError, setRevisionError] = useState("");
  const [updatingTaskId, setUpdatingTaskId] = useState(null);
  const [showTeacher, setShowTeacher] = useState(false);
  const [darkMode, setDarkMode] = useState(
          localStorage.getItem("theme") !== "light"
        );

        useEffect(() => {
          document.body.classList.toggle("light-mode", !darkMode);
          localStorage.setItem("theme", darkMode ? "dark" : "light");
        }, [darkMode]);

        useEffect(() => {
          if (!student || student.role === "teacher") {
            return;
          }

          fetch(`${API_URL}/api/dashboard/${student.id}`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Unable to load your dashboard.");
              }
              return response.json();
            })
            .then((data) => setDashboard(data))
            .catch((error) => console.error(error));
        }, [student]);
        
        useEffect(() => {
          if (!student || !token || student.role === "teacher") {
            return;
          }

          fetch(`${API_URL}/api/dashboard/${student.id}/learning-dna`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Unable to load Learning DNA.");
              }
              return response.json();
            })
            .then((data) => {
              setLearningDNA(data.learning_profile);
              setDnaError("");
            })
            .catch((error) => {
              console.error(error);
              setDnaError(error.message);
            });
        }, [student, token]);
        
          useEffect(() => {
            if (!student?.id || !token || student.role === "teacher") {
              setRevisionData(null);
              return;
            }

            let cancelled = false;

            async function loadRevisionTasks() {
              try {
                const response = await fetch(
                  `${API_URL}/api/revision/${student.id}`,
                  {
                    headers: {
                      Authorization: `Bearer ${token}`,
                    },
                  }
                );

                if (!response.ok) {
                  throw new Error("Unable to load revision tasks.");
                }

                const data = await response.json();

                if (!cancelled) {
                  setRevisionData(data);
                  setRevisionError("");
                }
              } catch (error) {
                if (!cancelled) {
                  setRevisionError(error.message);
                }
              }
            }

            loadRevisionTasks();

            return () => {
              cancelled = true;
            };
          }, [student, token]);
        if (!student || !token) {
          return (
            <Auth
              onLogin={(loggedInStudent, accessToken) => {
                setStudent(loggedInStudent);
                setToken(accessToken);
                setDashboard(null);
              }}
            />
          );
        }
        if (student.role === "teacher" || showTeacher) {
          return (
          <TeacherDashboard
            token={token}
            onBack={() => {
              if (student.role === "teacher") {
                localStorage.removeItem("student");
                localStorage.removeItem("access_token");
                setStudent(null);
                setToken(null);
                setDashboard(null);
                setShowTeacher(false);
              } else {
                setShowTeacher(false);
              }
            }}
          />
        );
      }

  if (showAssessment) {
    return (
      <Assessment token={token}
        studentId={student.id}
        onComplete={() => {
          setShowAssessment(false);
          window.location.reload();
        }}
        onBack={() => setShowAssessment(false)}
      />
    );
  }
  if (showQuiz) {
    return (
      <Quiz
        studentId={student.id}
        token={token}
        onBack={() => {
          setShowQuiz(false);

          fetch(`${API_URL}/api/dashboard/${student.id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
            .then((response) => response.json())
            .then((data) => setDashboard(data))
            .catch((error) => console.error(error));
        }}
      />
    );
  }

  if (!dashboard) {
    return (
      <div className="loading">
        <div className="loading-orb">
          <Brain size={34} />
        </div>
        <h2>Building your learning profile...</h2>
        <p>Connecting to your adaptive learning engine</p>
      </div>
    );
  }

  const performance = dashboard.overall_performance;

  const mastery = performance.overall_mastery;
  
  const toggleLearningPathTask = async (item) => {
    if (!item.revision_task_id) {
      setRevisionError(
        "This topic has no revision task yet. Open the Revision Tracker first."
      );
      return;
    }

    const revisionTask = {
      id: item.revision_task_id,
      topic_id: item.topic_id,
      topic: item.topic,
      subject: item.subject,
      is_completed: item.is_completed,
    };

    await toggleRevisionTask(revisionTask);
  };
  
  
  
const toggleRevisionTask = async (task) => {
  if (updatingTaskId !== null) return;

  setUpdatingTaskId(task.id);

  try {
    const nextCompleted = !task.is_completed;

    const response = await fetch(
      `${API_URL}/api/revision/${student.id}/${task.id}?is_completed=${nextCompleted}`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Could not update revision progress.");
    }

    // Update the Revision Tracker.
    setRevisionData((previous) => {
      if (!previous) return previous;

      const tasks = previous.tasks.map((item) =>
        item.id === task.id
          ? { ...item, is_completed: nextCompleted }
          : item
      );

      const completed = tasks.filter(
        (item) => item.is_completed
      ).length;

      return {
        ...previous,
        tasks,
        completed_tasks: completed,
        total_tasks: tasks.length,
        progress_percentage: tasks.length
          ? Math.round((completed / tasks.length) * 1000) / 10
          : 0,
      };
    });

    // Update the Learning Path.
    setDashboard((previous) => {
      if (!previous || !Array.isArray(previous.study_plan)) {
        return previous;
      }

      return {
        ...previous,
        study_plan: previous.study_plan.map((item) =>
          item.revision_task_id === task.id
            ? { ...item, is_completed: nextCompleted }
            : item
        ),
      };
    });

    setRevisionError("");
  } catch (error) {
    setRevisionError(error.message);
  } finally {
    setUpdatingTaskId(null);
  }
};
  return (
    <div className="command-center">

      {/* Ambient background */}
      <div className="ambient ambient-one"></div>
      <div className="ambient ambient-two"></div>

      {/* Top navigation */}
      <header className="top-nav">

        <div className="brand">
          <div className="brand-mark">
            <Brain size={22} />
          </div>

          <div>
            <strong>AST</strong>
            <span>Adaptive STEM Tutor</span>
          </div>
        </div>

        <div className="nav-center">
          <span className="nav-active">Learning Space</span>
          <span>Progress</span>
          <span>Challenges</span>
        </div>

        <div className="profile">

          <div className="streak">
            <Flame size={16} />
            4 day streak
          </div>

          <button
            className="theme-toggle"
            title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle theme"
          >
            {darkMode ? (
              <Sun size={17} />
            ) : (
              <Moon size={17} />
            )}
          </button>

          <button
            className="logout-button"
            title="Logout"
            onClick={() => {
              localStorage.removeItem("student");
              localStorage.removeItem("access_token");
              setStudent(null);
              setToken(null);
              setDashboard(null);
              setShowTeacher(false);
              setShowQuiz(false);
              setShowAssessment(false);
            }}
          >
            Logout
          </button>

          {student.role === "teacher" && (
              <button
                className="secondary-button"
                onClick={() => setShowTeacher(true)}
              >
                <GraduationCap size={17} />
                Teacher Space
              </button>
            )}

        <div className="profile-avatar">
            {dashboard.student.name
              .split(" ")
              .map((word) => word[0])
              .join("")
              .slice(0, 2)}
          </div>
        </div>

      </header>


      {/* Hero */}
      <section className="hero">

        <div className="hero-copy">

          <div className="micro-label">
            <span className="live-dot"></span>
            PERSONALIZED SESSION
          </div>

          <h1>
            Learn at your
            <span> own pace.</span>
          </h1>

          <p>
            Your learning path is adapting continuously based on
            what you know, what you struggle with, and what you
            should learn next.
          </p>

          <div className="hero-actions">

          <button
            className="primary-button"
            onClick={() => setShowQuiz(true)}
          >
            <Play size={17} fill="currentColor" />
            Continue Learning
            <ArrowUpRight size={16} />
          </button>

          <button
            className="secondary-button"
            onClick={() => setShowAssessment(true)}
          >
            <Target size={17} />
            Take Assessment
          </button>

          <div className="ai-status">
            <Sparkles size={16} />
            AI adaptation active
          </div>

        </div>
        </div>


        {/* Mastery Orb */}
        <div className="mastery-orb-wrapper">

          <div className="orbit orbit-one"></div>
          <div className="orbit orbit-two"></div>

          <div className="mastery-orb">

            <div className="orb-glow"></div>

            <div className="orb-content">
              <Brain size={30} />
              <span>MASTERY</span>
              <strong>{mastery}%</strong>
              <small>overall</small>
            </div>

          </div>

          <div className="orb-tag tag-top">
            <Zap size={13} />
            Adaptive
          </div>

          <div className="orb-tag tag-bottom">
            <Target size={13} />
            {dashboard.topic_performance.length} topics
          </div>

        </div>

      </section>


      {/* Metrics */}
      <section className="metric-strip">

        <div className="metric">
          <span>ACCURACY</span>
          <strong>{performance.quiz_accuracy}%</strong>
          <small>quiz performance</small>
        </div>

        <div className="metric">
          <span>QUESTIONS</span>
          <strong>{performance.questions_attempted}</strong>
          <small>attempted so far</small>
        </div>

        <div className="metric">
          <span>SUCCESS</span>
          <strong>{performance.correct_answers}</strong>
          <small>correct answers</small>
        </div>

        <div className="metric highlight">
          <span>STATUS</span>
          <strong>Learning</strong>
          <small>system adapting</small>
        </div>

      </section>


      {/* Main grid */}
      <main className="content-grid">



{/* Topic constellation — Collapsible Knowledge Map */}
<details className="glass-card topics-card collapsible-section">

  <summary className="section-heading collapsible-heading">
    <div>
      <span className="section-number">01</span>
      <div>
        <h2>Your Knowledge Map</h2>
        <p>How strong are you across different concepts?</p>
      </div>
    </div>

    <ChevronDown size={21} className="collapse-chevron" />
  </summary>

  {/* Content appears when the section is expanded */}
  <div className="knowledge-map">

    <div className="knowledge-map-summary">
      <div>
        <span className="map-eyebrow">YOUR PROGRESS</span>
        <h3>Topic mastery</h3>
      </div>

      <span className="map-topic-count">
        {dashboard.topic_performance.length} topics
      </span>
    </div>

    <div className="knowledge-topic-grid">
      {dashboard.topic_performance.map((topic) => {
        const score = Math.max(
          0,
          Math.min(100, Number(topic.mastery_score) || 0)
        );

        const level =
          score >= 80
            ? "Strong"
            : score >= 60
            ? "Developing"
            : "Needs practice";

        return (
          <div className="knowledge-topic" key={topic.topic}>
            <div className="knowledge-topic-top">
              <div className="knowledge-topic-name">
                <span className="knowledge-topic-dot" />
                <strong title={topic.topic}>
                  {topic.topic}
                </strong>
              </div>

              <span className="knowledge-topic-score">
                {score}%
              </span>
            </div>

            <div
              className="knowledge-progress-track"
              role="progressbar"
              aria-label={`${topic.topic} mastery`}
              aria-valuenow={score}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <div
                className="knowledge-progress-fill"
                style={{ width: `${score}%` }}
              />
            </div>

            <div className="knowledge-topic-bottom">
              <span>{topic.status || level}</span>
              <span>{level}</span>
            </div>
          </div>
        );
      })}
    </div>

  </div>
</details>
        

{/* Focus Zone — Collapsible */}
<details className="focus-zone collapsible-section">

  <summary className="focus-top collapsible-heading">
    <div>
      <span className="section-number">02</span>
      <h2>Focus Zone</h2>
    </div>

    <ChevronDown size={21} className="collapse-chevron" />
  </summary>

  {/* Focus Zone content appears when expanded */}
  <p className="focus-description">
    Your personalized improvement plan, based on your topic mastery
    and learning progress.
  </p>

  {dashboard.weak_topics?.length > 0 ? (
    <>
      <div className="focus-topic-list">
        {dashboard.weak_topics.map((topic, index) => {
          const topicName =
            typeof topic === "string" ? topic : topic.topic;

          const topicData = dashboard.topic_performance?.find(
            (item) =>
              item.topic?.toLowerCase() === topicName?.toLowerCase()
          );

          const score = Number(topicData?.mastery_score);
          const hasScore = Number.isFinite(score);

          const priority =
            hasScore && score < 40
              ? "High priority"
              : hasScore && score < 60
              ? "Needs attention"
              : "Recommended practice";

          return (
            <div className="focus-topic" key={topicName}>
              <div className="focus-icon">
                <Target size={18} />
              </div>

              <div className="focus-topic-text">
                <strong>{topicName}</strong>
                <span>
                  {index === 0 ? "Top priority" : priority}
                </span>
              </div>

              <div className="focus-topic-action">
                {hasScore && (
                  <strong className="focus-topic-score">
                    {score}%
                  </strong>
                )}
                <ChevronRight size={18} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="focus-footer">
        <span>Recommended next step</span>

        <button
          type="button"
          className="focus-practice-button"
          onClick={() => setShowQuiz(true)}
        >
          Start practice
          <ArrowUpRight size={15} />
        </button>
      </div>
    </>
  ) : (
    <>
      <div className="all-good">
        <Trophy size={25} />
        <strong>Everything is on track.</strong>
      </div>

      <p className="focus-description">
        Keep practising to maintain your progress and strengthen
        your understanding.
      </p>

      <div className="focus-footer">
        <span>Recommended next step</span>

        <button
          type="button"
          className="focus-practice-button"
          onClick={() => setShowQuiz(true)}
        >
          Continue learning
          <ArrowUpRight size={15} />
        </button>
      </div>
    </>
  )}

</details>

       
{/* Study Path — Collapsible */}
<details className="glass-card study-path collapsible-section">

  <summary className="section-heading collapsible-heading">
    <div>
      <span className="section-number">03</span>
      <div>
        <h2>Today's Learning Path</h2>
        <p>A route generated from your current mastery.</p>
      </div>
    </div>

    <div className="study-path-heading-right">
      <div className="path-time">
        <Clock3 size={15} />
        Adaptive plan
      </div>

      <ChevronDown size={20} className="collapse-chevron" />
    </div>
  </summary>

  {/* Learning timeline appears when expanded */}
  <div className="learning-timeline">
    {dashboard.study_plan.map((item, index) => (
      <div className="timeline-item" key={item.topic}>
        <div className="timeline-marker">
          {item.priority === "High" ? (
            <Zap size={15} />
          ) : (
            <span>{index + 1}</span>
          )}
        </div>

        <div className="timeline-content">
          <div>
            <span className="timeline-sub">
              {item.priority === "High"
                ? "HIGH PRIORITY"
                : item.priority === "Medium"
                ? "NEEDS PRACTICE"
                : "MAINTAIN PROGRESS"}
            </span>

            <h3>
              {item.sequence ? `${item.sequence}. ` : ""}
              {item.topic}
            </h3>

            <small>
              {item.subject} ·{" "}
              {item.learning_stage || "Personalized practice"}
            </small>
          </div>

          <div className="timeline-right">
            <span
              className={`timeline-status priority-${(
                item.priority || item.status || ""
              )
                .toLowerCase()
                .replace(/\s+/g, "-")}`}
            >
              {item.priority || item.status}
            </span>

            <span className="timeline-time">
              {item.recommended_time_minutes} min
            </span>
          </div>
        </div>

        <div className="timeline-details">
          <p>
            {item.recommendation_reason || item.recommended_action}
          </p>

          {item.recommended_action && (
            <p>{item.recommended_action}</p>
          )}

          <button
            type="button"
            className="learning-complete-button"
            disabled={
              !item.revision_task_id ||
              updatingTaskId === item.revision_task_id
            }
            onClick={() => toggleLearningPathTask(item)}
          >
            {updatingTaskId === item.revision_task_id
              ? "Saving..."
              : item.is_completed
              ? "Studied ✓"
              : "Mark as Studied"}
          </button>

          <div className="timeline-progress-info">
            <span>Mastery: {item.mastery_score}%</span>

            <span>
              Overall accuracy:{" "}
              {item.accuracy == null
                ? "Not enough data"
                : `${item.accuracy}%`}
            </span>

            <span>
              Recent accuracy:{" "}
              {item.recent_accuracy == null
                ? "Not enough data"
                : `${item.recent_accuracy}%`}
            </span>

            <span>
              Target mastery: {item.target_mastery ?? 75}%
            </span>

            <span>Attempts: {item.total_attempts ?? 0}</span>

            {item.performance_trend && (
              <span>Trend: {item.performance_trend}</span>
            )}
          </div>
        </div>

        <div className="timeline-line" />
      </div>
    ))}
  </div>

</details>

            {/* AI Doubt Solver */}
            <DoubtSolver token={token} student={student} />

        
{/* Revision Completion Tracker — Collapsible */}
<details className="glass-card revision-tracker collapsible-section">

  <summary className="section-heading collapsible-heading">
    <div>
      <span className="section-number">05</span>
      <div>
        <h2>Revision Tracker</h2>
        <p>Track the topics you have revised.</p>
      </div>
    </div>

    <div className="revision-heading-right">
      <span className="revision-count">
        {revisionData
          ? `${revisionData.completed_tasks}/${revisionData.total_tasks} completed`
          : "Loading progress"}
      </span>

      <ChevronDown size={20} className="collapse-chevron" />
    </div>
  </summary>

  {/* Tracker details appear when expanded */}
  <div className="revision-tracker-content">

    {revisionError ? (
      <p role="alert">{revisionError}</p>
    ) : !revisionData ? (
      <p>Loading your revision tasks...</p>
    ) : (
      <>
        <div
          className="revision-progress-track"
          role="progressbar"
          aria-label="Revision completion"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={revisionData.progress_percentage}
        >
          <div
            className="revision-progress-fill"
            style={{
              width: `${revisionData.progress_percentage}%`
            }}
          />
        </div>

        <p className="revision-progress-label">
          {revisionData.progress_percentage}% of your revision plan
          completed
        </p>

        {revisionData.streaks && (
          <div className="streak-stats">
            <div className="streak-card">
              <span>🔥</span>
              <h3>{revisionData.streaks.current_streak}</h3>
              <p>Current Streak (days)</p>
            </div>

            <div className="streak-card">
              <span>🏆</span>
              <h3>{revisionData.streaks.longest_streak}</h3>
              <p>Longest Streak (days)</p>
            </div>

            <div className="streak-card">
              <span>📅</span>
              <h3>{revisionData.streaks.total_active_days}</h3>
              <p>Active Revision Days</p>
            </div>
          </div>
        )}

        {revisionData.tasks.length === 0 ? (
          <p>Complete a quiz to build your revision plan.</p>
        ) : (
          <div className="revision-task-list">
            {revisionData.tasks.map((task) => (
              <div
                className={`revision-task ${
                  task.is_completed ? "is-completed" : ""
                }`}
                key={task.id}
              >
                <label className="revision-task-check">
                  <input
                    type="checkbox"
                    checked={task.is_completed}
                    disabled={updatingTaskId !== null}
                    onChange={() => toggleRevisionTask(task)}
                  />

                  <span>
                    <strong>{task.topic}</strong>
                    <small>
                      {task.subject} · {task.priority} priority ·{" "}
                      {task.recommended_time_minutes} min
                    </small>
                  </span>
                </label>

                <p>{task.recommended_action}</p>

                <small>Mastery: {task.mastery_score}%</small>
              </div>
            ))}
          </div>
        )}
      </>
    )}

  </div>
</details>

        
        {/* Learning DNA */}
        <section className="glass-card learning-dna-card">
          <div className="section-heading">
            <div>
              <span className="section-number">04</span>
              <div>
                <h2>Your Learning DNA</h2>
                <p>Patterns from your actual quiz performance.</p>
              </div>
            </div>
            <Brain size={22} />
          </div>

          {dnaError ? (
            <p role="alert">{dnaError}</p>
          ) : !learningDNA ? (
            <p>Analyzing your learning patterns...</p>
          ) : (
            <>
              <div className="dna-metrics">
                <div className="dna-metric">
                  <span>TOTAL ATTEMPTS</span>
                  <strong>{learningDNA.total_attempts}</strong>
                </div>

                <div className="dna-metric">
                  <span>RECENT ACCURACY</span>
                  <strong>
                    {learningDNA.recent_accuracy == null
                      ? "—"
                      : `${learningDNA.recent_accuracy}%`}
                  </strong>
                </div>

                <div className="dna-metric">
                  <span>RECURRING MISTAKES</span>
                  <strong>{learningDNA.recurring_mistakes.length}</strong>
                </div>
              </div>

              <h3>Topic performance</h3>

              {learningDNA.topic_profiles.length === 0 ? (
                <p>Complete a quiz to start building your profile.</p>
              ) : (
                <div className="dna-topic-list">
                  {learningDNA.topic_profiles.map((topic) => (
                    <div className="dna-topic" key={topic.topic}>
                      <div className="dna-topic-heading">
                        <strong>{topic.topic}</strong>
                        <span>{topic.accuracy}% accuracy</span>
                      </div>

                      <div
                        className="dna-progress-track"
                        role="progressbar"
                        aria-label={`${topic.topic} accuracy`}
                        aria-valuemin={0}
                        aria-valuemax={100}
                        aria-valuenow={topic.accuracy}
                      >
                        <div
                          className="dna-progress-fill"
                          style={{ width: `${topic.accuracy}%` }}
                        />
                      </div>

                      <small>
                        {topic.attempts} attempts ·{" "}
                        {topic.mastery == null
                          ? "Mastery not yet recorded"
                          : `${topic.mastery}% mastery`}
                      </small>
                    </div>
                  ))}
                </div>
              )}

              <h3>Recurring mistakes</h3>

              {learningDNA.recurring_mistakes.length === 0 ? (
                <p>No repeated incorrect answers detected yet.</p>
              ) : (
                <div className="dna-mistake-list">
                  {learningDNA.recurring_mistakes.map((mistake) => (
                    <div
                      className="dna-mistake"
                      key={mistake.question_id}
                    >
                      <strong>{mistake.topic}</strong>
                      <p>{mistake.question}</p>
                      <small>
                        Incorrect attempts: {mistake.incorrect_attempts}
                      </small>
                    </div>
                  ))}
                </div>
              )}

              <h3>Personalized recommendations</h3>

              {learningDNA.recommendations.length === 0 ? (
                <p>Keep practicing to generate more personalized insights.</p>
              ) : (
                <ul className="dna-recommendations">
                  {learningDNA.recommendations.map((item, index) => (
                    <li key={`${item.topic}-${index}`}>
                      <strong>{item.topic}:</strong> {item.reason}
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </section>
        {/* AI insight */}
        <section className="ai-card">

          <div className="ai-symbol">
            <Sparkles size={24} />
          </div>

          <div className="ai-content">

            <span>ADAPTIVE INSIGHT</span>

            <h2>
              Your next question will be selected
              based on your latest performance.
            </h2>

            <p>
              Instead of following a fixed difficulty level,
              Adaptive STEM Tutor continuously updates your
              learning path after every response.
            </p>

          </div>

          <div className="ai-lock">
            <LockKeyhole size={17} />
            Live
          </div>

        </section>

      </main>

      <footer>
        <span>ADAPTIVE STEM TUTOR</span>
        <span>AI-powered personalized learning • SDG 4</span>
      </footer>

    </div>
  );
}

export default App;