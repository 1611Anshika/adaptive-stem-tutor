import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Brain,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  Loader2,
  Sparkles,
  Target,
  XCircle,
  ArrowUpRight,
  Zap
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function Quiz({ studentId = 1, onBack,token }) {
  const [question, setQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  
const [selectedSubject, setSelectedSubject] = useState("Mathematics");
const [started, setStarted] = useState(false);
const [error, setError] = useState("");

const subjects = [
  "Mathematics",
  "Physics",
  "Chemistry",
  "Biology",
  "Computer Science",
];

  

const fetchQuestion = async (subject = selectedSubject) => {
  setError("");
  setLoading(true);
  setFeedback(null);
  setSelectedAnswer("");

  try {
    const response = await fetch(
      `${API_URL}/api/quiz/next/${studentId}?subject=${encodeURIComponent(subject)}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch question: ${response.status}`);
    }

    const data = await response.json();
    setQuestion(data);
  } catch (err) {
    console.error("Quiz question fetch failed:", err);
    setError("Unable to load the next question. Please try again.");
    setQuestion(null);
  } finally {
    setLoading(false);
  }
};

  

  const submitAnswer = async () => {
    if (!selectedAnswer || submitting) {
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(
        `${API_URL}/api/quiz/answer`,
        {
            method: "POST",
            headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            },
            body: JSON.stringify({
            student_id: studentId,
            question_id: question.question_id,
            selected_answer: selectedAnswer,
            }),
        }
        );

        if (!response.ok) {
        throw new Error(`Failed to submit answer: ${response.status}`);
        }

        const data = await response.json();
        setFeedback(data);
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  const getDifficultyClass = () => {
    if (!question?.difficulty) return "";

    return `difficulty-${question.difficulty}`;
  };

  

if (!started) {
  const subjectDetails = {
    Mathematics: {
      icon: "∑",
      description: "Strengthen your logic & problem solving",
      color: "math"
    },
    Physics: {
      icon: "⚛",
      description: "Understand concepts through practice",
      color: "physics"
    },
    Chemistry: {
      icon: "⚗",
      description: "Build confidence in reactions & bonding",
      color: "chemistry"
    },
    Biology: {
      icon: "❧",
      description: "Reinforce life science concepts",
      color: "biology"
    },
    "Computer Science": {
      icon: "</>",
      description: "Sharpen logic & algorithmic thinking",
      color: "computer"
    }
  };

  return (
    <div className="assessment-page subject-select-page">
      <header className="assessment-header">
        <button className="back-button" onClick={onBack}>
          <ArrowLeft size={17} />
          Dashboard
        </button>

        <div className="assessment-brand">
          <div className="brand-mark">
            <Brain size={22} />
          </div>
          <div>
            <strong>
              ADAPTIVE <span className="brand-highlight">STEM TUTOR</span>
            </strong>
            <span>Your personal learning space</span>
          </div>
        </div>

        <div className="session-badge">
          <span className="session-dot" />
          CONTINUE LEARNING
        </div>
      </header>

      <main className="assessment-container subject-select-container">
        <div className="assessment-intro subject-select-intro">
          <div className="assessment-label">
            <Sparkles size={15} />
            YOUR NEXT LEARNING SESSION
          </div>

          <h1>
            Where will you <span>grow today?</span>
          </h1>

          <p>
            Choose a subject and continue building your skills.
            Your practice adapts to your progress and performance.
          </p>
        </div>

        <div className="subject-grid">
          {subjects.map((subject, index) => {
            const details = subjectDetails[subject];

            return (
              <button
                key={subject}
                className={`subject-card subject-${details.color} ${
                  selectedSubject === subject ? "active-subject" : ""
                }`}
                style={{ "--card-index": index }}
                onClick={() => setSelectedSubject(subject)}
                aria-pressed={selectedSubject === subject}
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
                  {selectedSubject === subject
                    ? "Subject selected"
                    : "Explore subject"}
                  <ArrowRight size={16} />
                </div>
              </button>
            );
          })}
        </div>

        <div className="subject-start-row">
          <div className="subject-select-footer">
            <Target size={16} />
            <span>
              {selectedSubject
                ? `${selectedSubject} selected — you're ready to practice.`
                : "Choose a subject to begin your adaptive learning session."}
            </span>
          </div>

          <button
            className="primary-button subject-start-button"
            disabled={!selectedSubject}
            onClick={() => {
              setStarted(true);
              fetchQuestion(selectedSubject);
            }}
          >
            Start Learning
            <ChevronRight size={17} />
          </button>
        </div>
      </main>
    </div>
  );
}

  if (loading) {
    return (
      <div className="quiz-loading">
        <div className="loading-orb">
          <Brain size={34} />
        </div>

        <h2>Finding your next challenge...</h2>

        <p>
          Your adaptive engine is selecting a question
          based on your current mastery.
        </p>
      </div>
    );
  }


if (error) {
  return (
    <div className="quiz-page">
      <button className="back-button" onClick={onBack}>
        <ArrowLeft size={17} />
        Dashboard
      </button>

      <div className="quiz-empty">
        <CircleAlert size={45} />
        <h2>Couldn't load your next question</h2>
        <p>{error}</p>

        <button
          className="primary-button"
          onClick={() => fetchQuestion(selectedSubject)}
        >
          Try Again
        </button>
      </div>
    </div>
  );
}

if (question && !question.message) {

  return (
    <div className="quiz-page">

      <header className="quiz-header">

        <button
          className="back-button"
          onClick={onBack}
        >
          <ArrowLeft size={17} />
          Dashboard
        </button>

        <div className="quiz-brand">
          <div className="brand-mark">
            <Brain size={20} />
          </div>

          <div>
            <strong>ADAPTIVE SESSION</strong>
            <span>Question selected for you</span>
          </div>
        </div>

        <div className="quiz-live">
          <span></span>
          AI adaptation active
        </div>

      </header>

      <main className="quiz-container">

        <div className="quiz-meta">

          <div className="quiz-topic">
            <Target size={16} />
            {question.topic}
          </div>

          <div className={`difficulty ${getDifficultyClass()}`}>
            <Zap size={14} />
            {question.difficulty}
          </div>

        </div>

        <div className="adaptive-message">

          <Sparkles size={16} />

          <span>
            {question.adaptive_reason}
          </span>

        </div>

        <section className="question-card">

          <div className="question-number">
            ADAPTIVE QUESTION
          </div>

          <h1>
            {question.question}
          </h1>

          <div className="options-grid">

            {Object.entries(question.options).map(
              ([key, value]) => {

                const isSelected =
                  selectedAnswer === key;

                const isCorrect =
                  feedback &&
                  key === feedback.correct_answer;

                const isWrong =
                  feedback &&
                  isSelected &&
                  !feedback.correct;

                let className = "answer-option";

                if (isSelected) {
                  className += " selected";
                }

                if (isCorrect) {
                  className += " correct";
                }

                if (isWrong) {
                  className += " incorrect";
                }

                return (
                  <button
                    key={key}
                    className={className}
                    onClick={() =>
                      !feedback &&
                      setSelectedAnswer(key)
                    }
                    disabled={!!feedback}
                  >

                    <span className="option-key">
                      {key}
                    </span>

                    <span className="option-text">
                      {value}
                    </span>

                    {isCorrect && (
                      <CheckCircle2 size={20} />
                    )}

                    {isWrong && (
                      <XCircle size={20} />
                    )}

                  </button>
                );
              }
            )}

          </div>

          {!feedback ? (

            <button
              className="submit-answer"
              onClick={submitAnswer}
              disabled={!selectedAnswer || submitting}
            >

              {submitting ? (
                <>
                  <Loader2
                    size={17}
                    className="spin"
                  />
                  Checking...
                </>
              ) : (
                <>
                  Check Answer
                  <ChevronRight size={17} />
                </>
              )}

            </button>

          ) : (

            <div
              className={`feedback-box ${
                feedback.correct
                  ? "feedback-correct"
                  : "feedback-incorrect"
              }`}
            >

              <div className="feedback-icon">

                {feedback.correct ? (
                  <CheckCircle2 size={25} />
                ) : (
                  <CircleAlert size={25} />
                )}

              </div>

              <div className="feedback-content">

                <strong>
                  {feedback.correct
                    ? "Correct! Great work."
                    : "Not quite this time."}
                </strong>

                <p>
                  {feedback.feedback}
                </p>
                {feedback.tutor && (
                <div className="tutor-guidance">
                    <div className="tutor-guidance-header">
                    <Brain size={15} />
                    <span>ADAPTIVE TUTOR</span>
                    </div>

                    <p>
                    {feedback.tutor.message}
                    </p>

                    {!feedback.correct && feedback.tutor.explanation && (
                    <div className="tutor-explanation">
                        <strong>Let's understand it:</strong>
                        <p>{feedback.tutor.explanation}</p>
                    </div>
                    )}
                </div>
                )}

                {feedback.mastery_score !== undefined && (
                <div className="mastery-update">
                    <Zap size={14} />
                    <span>
                    {feedback.topic} mastery is now{" "}
                    <strong>{feedback.mastery_score}%</strong>
                    </span>
                </div>
                )}

                {!feedback.correct && (
                  <small>
                    Correct answer:{" "}
                    <strong>
                      {feedback.correct_answer}
                    </strong>
                  </small>
                )}

              </div>

              <button
                className="next-question"
                onClick={() => fetchQuestion()}
              >
                Next Question
                <ChevronRight size={17} />
              </button>

            </div>

          )}

        </section>

        <div className="quiz-footer">

          <div>
            <Sparkles size={15} />
            Difficulty adapts after every response
          </div>

          <span>
            Your performance shapes what comes next.
          </span>

        </div>

      </main>

    </div>
  );
}
 return (
    <div className="quiz-page">
      <button className="back-button" onClick={onBack}>
        <ArrowLeft size={17} />
        Dashboard
      </button>

      <div className="quiz-empty">
        <Brain size={45} />
        <h2>You're All Caught Up!</h2>
        <p>
          {question?.message ||
            `There are no more ${selectedSubject} questions available right now.`}
        </p>

        <button
          className="primary-button"
          onClick={() => {
            setStarted(false);
            setQuestion(null);
            setFeedback(null);
            setSelectedAnswer("");
          }}
        >
          Choose Another Subject
          <ChevronRight size={17} />
        </button>
      </div>
    </div>
  );
}

export default Quiz;
