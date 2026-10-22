
import { useState } from "react";
import { Bot, Send, User, Sparkles } from "lucide-react";
import "../App.css";

const suggestedQuestions = [
  "Summarize my portfolio performance",
  "Which of my holdings are at a loss?",
  "What market events should I watch?",
  "Explain how recent news could affect my holdings",
];

function Assistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(message = input) {
    const question = message.trim();

    if (!question || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      { role: "user", content: question },
    ]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ai/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: question }),
      });

      if (!response.ok) {
        throw new Error(
          response.status === 502
            ? "The AI assistant couldn't generate a response. Check that the AI model is running, then try again."
            : "Unable to contact the AI assistant. Please try again.",
        );
      }

      const data = await response.json();

      if (typeof data.response !== "string" || !data.response.trim()) {
        throw new Error("The AI assistant returned an empty response.");
      }

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.response },
      ]);
    } catch (err) {
      setError(
        err.message ||
          "Unable to reach the backend. Check that the API is running.",
      );
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    sendMessage();
  }

  return (
    <section className="assistant-page">
      <header className="assistant-header">
        <div className="assistant-heading-icon">
          <Bot size={25} />
        </div>

        <div>
          <p className="eyebrow">PORTFOLIO INTELLIGENCE</p>
          <h1>AI Assistant</h1>
          <p>
            Ask questions about your holdings, portfolio performance, and
            relevant market developments.
          </p>
        </div>
      </header>

      <div className="assistant-chat">
        {messages.length === 0 ? (
          <div className="assistant-welcome">
            <div className="assistant-welcome-icon">
              <Sparkles size={24} />
            </div>

            <h2>How can I help with your portfolio?</h2>
            <p>
              Ask a question to get started. Answers depend on the portfolio
              data and research available to the assistant.
            </p>

            <div className="assistant-suggestions">
              {suggestedQuestions.map((question) => (
                <button
                  className="assistant-suggestion"
                  key={question}
                  type="button"
                  disabled={loading}
                  onClick={() => sendMessage(question)}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="assistant-messages" aria-live="polite">
            {messages.map((message, index) => (
              <article
                className={`assistant-message assistant-message-${message.role}`}
                key={`${index}-${message.role}`}
              >
                <div className="assistant-message-icon">
                  {message.role === "user" ? (
                    <User size={17} />
                  ) : (
                    <Bot size={17} />
                  )}
                </div>

                <div className="assistant-message-content">
                  <span className="assistant-message-label">
                    {message.role === "user" ? "You" : "PortfolioPulse AI"}
                  </span>
                  <p>{message.content}</p>
                </div>
              </article>
            ))}

            {loading && (
              <div className="assistant-loading" role="status">
                <span className="assistant-spinner" />
                Analyzing your question...
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="assistant-error" role="alert">
            {error}
          </div>
        )}

        <form className="assistant-composer" onSubmit={handleSubmit}>
          <input
            aria-label="Ask PortfolioPulse AI"
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about your portfolio..."
            disabled={loading}
            maxLength={2000}
          />

          <button
            type="submit"
            aria-label="Send message"
            disabled={loading || !input.trim()}
          >
            <Send size={18} />
          </button>
        </form>

        <p className="assistant-disclaimer">
          AI responses may be inaccurate. Verify important financial
          information before making investment decisions.
        </p>
      </div>
    </section>
  );
}

export default Assistant;
