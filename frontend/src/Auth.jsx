import { useState } from "react";
import {
  ArrowRight,
  Brain,
  Eye,
  EyeOff,
  Sparkles,
  Target,
  Zap
} from "lucide-react";

const API_URL = "http://127.0.0.1:8000";

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [role, setRole] = useState("student");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [grade, setGrade] = useState("10");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    const endpoint =
      mode === "login"
        ? "/api/auth/login"
        : "/api/auth/register";

    const body =
      mode === "login"
        ? {
            email,
            password
          }
        : {
            name,
            email,
            password,
            grade: Number(grade)
          };

    try {
      const response = await fetch(
        `${API_URL}${endpoint}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(body)
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Something went wrong"
        );
      }

      if (!data.access_token || !data.student) {
        throw new Error(
            "Authentication response is missing a token. Please check the backend."
        );
        }
     if (data.student.role !== role) {
        throw new Error(
            `This account is not registered as a ${role}. Please select the correct role.`
        );
        }

        localStorage.setItem(
        "student",
        JSON.stringify(data.student)
        );

        localStorage.setItem(
        "access_token",
        data.access_token
        );

        onLogin(data.student, data.access_token);

    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-background-glow glow-one" />
      <div className="auth-background-glow glow-two" />

      <div className="auth-layout">

        {/* LEFT SIDE */}
        <section className="auth-intro">

          <div className="auth-brand">
            <div className="auth-brand-icon">
              <Brain size={20} />
            </div>

            <span>ADAPTIVE STEM</span>
          </div>

          <div className="auth-copy">

            <div className="auth-eyebrow">
              <Sparkles size={14} />
              PERSONALIZED LEARNING
            </div>

            <h1>
              Learn smarter.
              <br />
              <span>At your own pace.</span>
            </h1>

            <p>
              An adaptive learning system that understands
              your strengths, identifies your gaps, and
              continuously adjusts your learning path.
            </p>

          </div>

          <div className="auth-features">

            <div className="auth-feature">
              <div>
                <Target size={17} />
              </div>

              <span>
                <strong>Identify gaps</strong>
                <small>Know exactly what needs practice.</small>
              </span>
            </div>

            <div className="auth-feature">
              <div>
                <Zap size={17} />
              </div>

              <span>
                <strong>Adapt instantly</strong>
                <small>Questions change with your performance.</small>
              </span>
            </div>

          </div>

        </section>

        {/* AUTH CARD */}
        <section className="auth-card">

          <div className="auth-card-header">

            <div>
              <span className="auth-label">
                {mode === "login"
                  ? "WELCOME BACK"
                  : "GET STARTED"}
              </span>

              <h2>
                {mode === "login"
                  ? "Continue learning"
                  : "Create your account"}
              </h2>

              <p>
                {mode === "login"
                  ? "Pick up where your learning journey left off."
                  : "Build your personalized STEM learning profile."}
              </p>
            </div>

          </div>

          
            <div className="auth-tabs">
            <button
                className={role === "student" ? "active" : ""}
                onClick={() => {
                setRole("student");
                setError("");
                }}
                type="button"
            >
                Student
            </button>

            <button
                className={role === "teacher" ? "active" : ""}
                onClick={() => {
                setRole("teacher");
                setError("");
                }}
                type="button"
            >
                Teacher
            </button>
            </div>

            <div className="auth-tabs">
            <button
                className={mode === "login" ? "active" : ""}
                onClick={() => {
                setMode("login");
                setError("");
                }}
                type="button"
            >
                Login
            </button>

            <button
                className={mode === "register" ? "active" : ""}
                onClick={() => {
                setMode("register");
                setError("");
                }}
                type="button"
            >
                Register
            </button>
            </div>


          
            <form onSubmit={handleSubmit}>
            {mode === "register" && (
                <>
                <label>
                    Your name

                    <input
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                    />
                </label>

                {role === "student" && (
                    <label>
                    Grade

                    <select
                        value={grade}
                        onChange={(e) => setGrade(e.target.value)}
                    >
                        <option value="8">Grade 8</option>
                        <option value="9">Grade 9</option>
                        <option value="10">Grade 10</option>
                        <option value="11">Grade 11</option>
                        <option value="12">Grade 12</option>
                    </select>
                    </label>
                )}
                </>
            )}

            <label>
                Email

                <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                />
            </label>

            <label>
                Password

                <div className="password-input">
                <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                >
                    {showPassword ? (
                    <EyeOff size={17} />
                    ) : (
                    <Eye size={17} />
                    )}
                </button>
                </div>
            </label>

            {error && (
                <div className="auth-error">
                {error}
                </div>
            )}

            <button
                className="auth-submit"
                type="submit"
                disabled={loading}
            >
                {loading
                ? "Please wait..."
                : mode === "login"
                    ? role === "teacher"
                    ? "Enter Teacher Dashboard"
                    : "Enter Learning Space"
                    : role === "teacher"
                    ? "Create Teacher Account"
                    : "Create Learning Profile"}

                {!loading && <ArrowRight size={17} />}
            </button>
            </form>



          <p className="auth-footer">
            Your learning journey is personalized around
            your performance.
          </p>

        </section>

      </div>

    </div>
  );
}

export default Auth;