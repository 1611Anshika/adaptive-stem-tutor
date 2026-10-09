import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  CheckCircle2,
  Loader2,
  Sparkles,
  ArrowUpRight,
  Target
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function Assessment({ studentId = 1, onComplete, onBack , token }) {
  
  const [questions, setQuestions] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  
  const subjects = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science"
  ];

  
  useEffect(() => {
    if (!selectedSubject) {
      return;
    }

    setLoading(true);
    setQuestions([]);
    setCurrentIndex(0);
    setAnswers({});
    setResult(null);

    fetch(
      `${API_URL}/api/assessment/questions?subject=${encodeURIComponent(selectedSubject)}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to load assessment questions");
        }
        return response.json();
      })
      .then((data) => {
        setQuestions(data);
      })
      .catch((error) => {
        console.error(error);
        setQuestions([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedSubject, token]);

  const currentQuestion = questions[currentIndex];

  const selectAnswer = (answer) => {
    setAnswers((previous) => ({
      ...previous,
      [currentQuestion.id]: answer
    }));
  };

  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((previous) => previous + 1);
    }
  };

  const previousQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex((previous) => previous - 1);
    }
  };

  const submitAssessment = async () => {
    setSubmitting(true);

    const formattedAnswers = questions.map((question) => ({
      question_id: question.id,
      selected_answer: answers[question.id]
    }));

    try {
      const response = await fetch(
        `${API_URL}/api/assessment/submit`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            },
          body: JSON.stringify({
            student_id: studentId,
            answers: formattedAnswers
          })
        }
      );

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };
  

  if (!selectedSubject) {
    const subjectDetails = {
      Mathematics: {
        icon: "∑",
        description: "Patterns, logic & problem solving",
        color: "math"
      },
      Physics: {
        icon: "⚛",
        description: "Understand how the world works",
        color: "physics"
      },
      Chemistry: {
        icon: "⚗",
        description: "Explore matter & reactions",
        color: "chemistry"
      },
      Biology: {
        icon: "❧",
        description: "Life, cells & ecosystems",
        color: "biology"
      },
      "Computer Science": {
        icon: "</>",
        description: "Algorithms & computational thinking",
        color: "computer"
      }
    };

    return (
      <div className="assessment-page subject-select-page">
        <header className="assessment-header">
          <div className="assessment-brand">
            <div className="brand-mark">
              <Brain size={22} />
            </div>
            <div>
              <strong>ADAPTIVE <span className="brand-highlight">STEM TUTOR</span></strong>
              <span>Your personal learning space</span>
            </div>
          </div>

          <div className="session-badge">
            <span className="session-dot" />
            PERSONALIZED SESSION
          </div>
        </header>

        <main className="assessment-container subject-select-container">
          <div className="assessment-intro subject-select-intro">
            <div className="assessment-label">
              <Sparkles size={15} />
              PERSONALIZED KNOWLEDGE CHECK
            </div>

            <h1>
              Choose your <span>subject.</span>
            </h1>

            <p>
              Focus on one subject at a time. Discover your strengths
              and what to practice next.
            </p>
          </div>

          <div className="subject-grid">
            {subjects.map((subject, index) => {
              const details = subjectDetails[subject];

              return (
                <button
                  key={subject}
                  className={`subject-card subject-${details.color}`}
                  style={{ "--card-index": index }}
                  onClick={() => setSelectedSubject(subject)}
                >
                  <div className="subject-card-top">
                    <div className="subject-symbol">
                      {details.icon}
                    </div>
                    <ArrowUpRight size={19} className="subject-arrow" />
                  </div>

                  <h2>{subject}</h2>
                  <p>{details.description}</p>

                  <div className="subject-explore">
                    Explore subject
                    <ArrowRight size={16} />
                  </div>
                </button>
              );
            })}
          </div>

          <div className="subject-select-footer">
            <Target size={16} />
            <span>Choose one subject to begin your diagnostic assessment.</span>
          </div>
        </main>
      </div>
    );
  }
  if (loading) {
    return (
      <div className="assessment-loading">
        <div className="loading-orb">
          <Brain size={34} />
        </div>

        <h2>Preparing your assessment...</h2>

        <p>
          We are selecting questions to understand
          your current knowledge level.
        </p>
      </div>
    );
  }

  if (result) {
    const topicResults = result.topic_results || [];

    const weakestTopic =
        topicResults.length > 0
        ? [...topicResults].sort(
            (a, b) => a.score - b.score
            )[0]
        : null;

    return (
        <div className="assessment-page">

        <main className="result-container">

            <div className="result-header">

            <div className="result-icon">
                <CheckCircle2 size={38} />
            </div>

            <span className="result-label">
                ASSESSMENT COMPLETE
            </span>

            <h1>
                Your learning profile is ready.
            </h1>

            <p>
                We've analyzed your responses and identified
                where your learning journey should begin.
            </p>

            </div>

            <section className="result-overview">

            <div className="score-panel">

                <span>OVERALL MASTERY</span>

                <strong>
                {result.overall_score ?? 0}%
                </strong>

                <small>
                Initial assessment score
                </small>

            </div>

            <div className="focus-panel">

                <div className="focus-panel-icon">
                <Target size={21} />
                </div>

                <div>
                <span>FIRST FOCUS AREA</span>

                <strong>
                    {weakestTopic
                    ? weakestTopic.topic
                    : "No weak topic identified"}
                </strong>

                {weakestTopic && (
                    <small>
                    {weakestTopic.score}% mastery
                    </small>
                )}
                </div>

            </div>

            </section>

            <section className="topic-results">

            <div className="result-section-heading">

                <div>
                <span>01</span>

                <div>
                    <h2>Knowledge Snapshot</h2>

                    <p>
                    Your starting point across different concepts.
                    </p>
                </div>
                </div>

                <Brain size={21} />

            </div>

            <div className="result-topic-list">

                {topicResults.map((topic) => (

                <div
                    className="result-topic"
                    key={topic.topic}
                >

                    <div className="result-topic-info">

                    <strong>
                        {topic.topic}
                    </strong>

                    <span className={
                        topic.level === "Strong"
                        ? "status-strong"
                        : topic.level === "Weak"
                        ? "status-weak"
                        : "status-practice"
                    }>
                        {topic.level}
                    </span>

                    </div>

                    <div className="result-topic-bar">

                    <div
                        style={{
                        width: `${topic.score}%`
                        }}
                    />

                    </div>

                    <strong className="result-topic-score">
                    {topic.score}%
                    </strong>

                </div>

                ))}

            </div>

            </section>

            {weakestTopic && (
            <section className="result-insight">

                <div className="insight-icon">
                <Sparkles size={22} />
                </div>

                <div>

                <span>ADAPTIVE INSIGHT</span>

                <h2>
                    We'll focus first on {weakestTopic.topic}.
                </h2>

                <p>
                    Your assessment shows this is currently
                    your biggest opportunity for improvement.
                    Your next learning activities will adapt
                    around this result.
                </p>

                </div>

            </section>
            )}

            <button
            className="result-continue"
            onClick={() => onComplete(result)}
            >
            Open My Personalized Learning Space
            <ArrowRight size={18} />
            </button>

            <div className="result-footer-note">
            <Sparkles size={14} />
            Your learning path will adapt as you continue practicing.
            </div>

        </main>

        </div>
    );
    }

  if (!currentQuestion) {
    return null;
  }

  const selectedAnswer = answers[currentQuestion.id];

  const progress =
    ((currentIndex + 1) / questions.length) * 100;

  const isLastQuestion =
    currentIndex === questions.length - 1;

  return (
    <div className="assessment-page">

      <header className="assessment-header">

        <button
          className="back-button"
          onClick={onBack}
        >
          <ArrowLeft size={17} />
          Back
        </button>

        <div className="assessment-brand">
          <div className="brand-mark">
            <Brain size={20} />
          </div>

          <div>
            <strong>INITIAL ASSESSMENT</strong>
            <span>Building your learning profile</span>
          </div>
        </div>

        <div className="assessment-count">
          {currentIndex + 1} / {questions.length}
        </div>

      </header>

      <main className="assessment-container">

        <div className="assessment-intro">

          <div className="assessment-label">
            <Sparkles size={15} />
            DIAGNOSTIC LEARNING CHECK
          </div>

          <h1>
            Let's understand
            <span> what you know.</span>
          </h1>

          <p>
            This isn't about getting everything right.
            Your answers help Adaptive STEM Tutor understand
            where you need more practice.
          </p>

        </div>

        <div className="assessment-progress">

          <div
            className="assessment-progress-bar"
            style={{ width: `${progress}%` }}
          />

        </div>

        <section className="assessment-card">

          <div className="assessment-question-meta">

            <div className="assessment-topic">
              <Target size={15} />
              {currentQuestion.topic}
            </div>

            <span>
              {currentQuestion.difficulty}
            </span>

          </div>

          <div className="assessment-question-number">
            QUESTION {String(currentIndex + 1).padStart(2, "0")}
          </div>

          <h2>
            {currentQuestion.question_text}
          </h2>

          <div className="assessment-options">

            {Object.entries({
              A: currentQuestion.option_a,
              B: currentQuestion.option_b,
              C: currentQuestion.option_c,
              D: currentQuestion.option_d
            }).map(([key, value]) => (

              <button
                key={key}
                className={`assessment-option ${
                  selectedAnswer === key
                    ? "selected"
                    : ""
                }`}
                onClick={() => selectAnswer(key)}
              >

                <span className="assessment-key">
                  {key}
                </span>

                <span>
                  {value}
                </span>

              </button>

            ))}

          </div>

          <div className="assessment-navigation">

            <button
              className="secondary-button"
              onClick={previousQuestion}
              disabled={currentIndex === 0}
            >
              <ArrowLeft size={16} />
              Previous
            </button>

            {!isLastQuestion ? (

              <button
                className="primary-button"
                onClick={nextQuestion}
                disabled={!selectedAnswer}
              >
                Next Question
                <ArrowRight size={16} />
              </button>

            ) : (

              <button
                className="primary-button"
                onClick={submitAssessment}
                disabled={!selectedAnswer || submitting}
              >
                {submitting ? (
                  <>
                    <Loader2
                      size={17}
                      className="spin"
                    />
                    Analyzing...
                  </>
                ) : (
                  <>
                    Finish Assessment
                    <CheckCircle2 size={17} />
                  </>
                )}
              </button>

            )}

          </div>

        </section>

        <div className="assessment-note">
          <Sparkles size={14} />
          Your results will be used to personalize your learning path.
        </div>

      </main>

    </div>
  );
}

export default Assessment;