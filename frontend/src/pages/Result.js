import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ChartComponent from "../components/ChartComponent";
import "../styles/Result.css";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const url = location.state?.url;

  useEffect(() => {
    if (!url) {
      navigate("/");
      return;
    }

    // Simulate API call to backend
    const analyzeWebsite = async () => {
      try {
        setLoading(true);
        // Replace with your actual backend endpoint
        // const response = await fetch("http://localhost:5000/analyze", {
        //   method: "POST",
        //   headers: { "Content-Type": "application/json" },
        //   body: JSON.stringify({ url }),
        // });
        // const data = await response.json();
        
        // Mock data for demonstration
        setTimeout(() => {
          setResults({
            url: url,
            overallScore: 72,
            patterns: [
              {
                name: "Scarcity",
                risk: "High",
                score: 85,
                description: "Found false scarcity messages indicating limited stock.",
                examples: ["Only 2 items left!", "Limited time offer"],
              },
              {
                name: "Urgency",
                risk: "Medium",
                score: 65,
                description: "Detected countdown timers and time pressure tactics.",
                examples: ["Offer ends in 5 minutes", "Sale ends tonight"],
              },
              {
                name: "Drip Pricing",
                risk: "High",
                score: 78,
                description: "Hidden fees revealed at later stages of purchase.",
                examples: ["Shipping costs", "Surprise fees at checkout"],
              },
              {
                name: "Visual Deception",
                risk: "Low",
                score: 45,
                description: "Misleading button colors or layouts detected.",
                examples: ["Confusing unsubscribe buttons"],
              },
            ],
            scanTime: "2.3s",
            timestamp: new Date().toLocaleString(),
          });
          setLoading(false);
        }, 2000);
      } catch (err) {
        setError("Failed to analyze website. Please try again.");
        setLoading(false);
      }
    };

    analyzeWebsite();
  }, [url, navigate]);

  if (loading) {
    return (
      <div className="result-container loading">
        <div className="loader">
          <div className="spinner"></div>
          <h2>Analyzing {url}...</h2>
          <p>Our AI is scanning for dark patterns</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-container error">
        <div className="error-box">
          <h2>Error: {error}</h2>
          <button onClick={() => navigate("/")} className="back-btn">
            ← Go Back
          </button>
        </div>
      </div>
    );
  }

  const getRiskColor = (risk) => {
    switch (risk) {
      case "High":
        return "#ef4444";
      case "Medium":
        return "#f59e0b";
      case "Low":
        return "#10b981";
      default:
        return "#6366f1";
    }
  };

  return (
    <div className="result-container">
      <header className="result-header">
        <button onClick={() => navigate("/")} className="back-btn">
          ← Analyze Another
        </button>
        <h1>Analysis Report</h1>
      </header>

      <section className="result-summary">
        <div className="summary-card main">
          <h2>Overall Risk Score</h2>
          <div className="score-display">
            <div className="score-circle">{results.overallScore}%</div>
            <div className="score-label">
              {results.overallScore > 70 ? "High Risk" : results.overallScore > 40 ? "Medium Risk" : "Safe"}
            </div>
          </div>
          <p className="url-analyzed">Website: {results.url}</p>
          <p className="scan-time">Scanned in {results.scanTime}</p>
        </div>

        <div className="summary-grid">
          {results.patterns.map((pattern, idx) => (
            <div key={idx} className="summary-card">
              <h3>{pattern.name}</h3>
              <div className="pattern-score" style={{ color: getRiskColor(pattern.risk) }}>
                {pattern.score}/100
              </div>
              <p className="risk-level" style={{ color: getRiskColor(pattern.risk) }}>
                Risk: {pattern.risk}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="chart-section">
        <h2>Risk Distribution</h2>
        <ChartComponent data={results.patterns} />
      </section>

      <section className="detailed-patterns">
        <h2>Detailed Findings</h2>
        {results.patterns.map((pattern, idx) => (
          <div key={idx} className="pattern-detail">
            <div className="pattern-header">
              <h3>{pattern.name}</h3>
              <span className="risk-badge" style={{ backgroundColor: getRiskColor(pattern.risk), color: "white" }}>
                {pattern.risk}
              </span>
            </div>
            <p className="pattern-description">{pattern.description}</p>
            <div className="pattern-examples">
              <strong>Examples Found:</strong>
              <ul>
                {pattern.examples.map((example, i) => (
                  <li key={i}>"{example}"</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </section>

      <section className="recommendations">
        <h2>Recommendations</h2>
        <div className="rec-box">
          <h3>How to Protect Yourself</h3>
          <ul>
            <li>Be cautious of sudden urgency or scarcity claims</li>
            <li>Always check full pricing before committing</li>
            <li>Look for hidden fees and charges</li>
            <li>Read terms and conditions carefully</li>
            <li>Trust your gut - if something feels suspicious, it probably is</li>
          </ul>
        </div>
      </section>

      <footer className="result-footer">
        <button onClick={() => navigate("/")} className="primary-btn">
          Analyze Another Website
        </button>
      </footer>
    </div>
  );
}

export default Result;
