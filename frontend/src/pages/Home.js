import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

function Home() {
  const [url, setUrl] = useState("");
  const [expandedFaq, setExpandedFaq] = useState(null);
  const navigate = useNavigate();

  const handleCheck = () => {
    if (!url) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    navigate("/result", { state: { url } });
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleCheck();
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const features = [
    {
      icon: "⚡",
      title: "Scarcity Detection",
      desc: "Identifies false urgency and artificial scarcity tactics.",
    },
    {
      icon: "⏰",
      title: "Time Pressure",
      desc: "Detects countdown timers and false time limits.",
    },
    {
      icon: "💸",
      title: "Drip Pricing",
      desc: "Uncovers hidden costs revealed at checkout.",
    },
    {
      icon: "🎭",
      title: "Visual Deception",
      desc: "Spots misleading buttons and confusing layouts.",
    },
  ];

  const steps = [
    { num: "1", title: "Enter URL", desc: "Provide the website you want to analyze" },
    { num: "2", title: "AI Analysis", desc: "Our AI scans for deceptive patterns" },
    { num: "3", title: "Get Report", desc: "Receive a detailed analysis report" },
    { num: "4", title: "Take Action", desc: "Learn how to avoid these tricks" },
  ];

  const faqs = [
    {
      q: "What are dark patterns?",
      a: "Dark patterns are deceptive UI/UX designs that trick users into doing things they don't intend, like hidden fees or forced subscriptions.",
    },
    {
      q: "How accurate is your detection?",
      a: "Our AI model has been trained on thousands of patterns and achieves 92%+ accuracy in identifying common dark patterns.",
    },
    {
      q: "Is my data secure?",
      a: "Yes! We only analyze the website structure and don't store personal data. Your privacy is our priority.",
    },
    {
      q: "Can I use this for mobile apps?",
      a: "Yes, our tool supports both websites and mobile app interfaces! Just provide the app's URL or package name.",
    },
  ];

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Dark Pattern Detection</h1>
          <p className="hero-subtitle">
            Protect yourself from deceptive design. Analyze any website and uncover hidden dark patterns
            trying to manipulate your decisions.
          </p>

          <div className="search-box">
            <input
              type="text"
              placeholder="Enter website URL..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyPress={handleKeyPress}
              className="search-input"
            />
            <button onClick={handleCheck} className="analyze-btn">
              Analyze Now
            </button>
          </div>

          <p className="hero-note">Free & instant analysis powered by AI</p>
          
          <div className="scroll-indicator">
            <p className="scroll-text">Scroll down for more details</p>
          </div>
        </div>

        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>What We Detect</h2>
        <div className="features-grid">
          {features.map((feature, idx) => (
            <div key={idx} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-container">
          {steps.map((step, idx) => (
            <div key={idx} className="step">
              <div className="step-number">{step.num}</div>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
              {idx < steps.length - 1 && <div className="step-arrow">|</div>}
            </div>
          ))}
        </div>
      </section>

      {/* Demo Section */}
      <section className="demo-section">
        <h2>See It In Action</h2>
        <div className="demo-container">
          <div className="demo-placeholder">
            <div className="demo-mockup">
              <div className="mockup-header"></div>
              <div className="mockup-content"></div>
              <div className="mockup-footer"></div>
            </div>
          </div>
          <div className="demo-text">
            <h3>Instant Insights</h3>
            <p>Our AI analyzes website designs and provides detailed reports on each dark pattern found, with explanations and recommendations.</p>
            <button className="cta-btn" onClick={handleCheck}>Try It Now</button>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-container">
          {faqs.map((faq, idx) => (
            <div key={idx} className="faq-item">
              <button
                className="faq-question"
                onClick={() => setExpandedFaq(expandedFaq === idx ? null : idx)}
              >
                <span>{faq.q}</span>
                <span className="faq-toggle">{expandedFaq === idx ? "−" : "+"}</span>
              </button>
              {expandedFaq === idx && <div className="faq-answer">{faq.a}</div>}
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="final-cta">
        <h2>Ready to Spot Dark Patterns?</h2>
        <p>Start protecting yourself today with AI-powered analysis</p>
        <div className="final-cta-buttons">
          <button className="primary-btn" onClick={handleCheck}>
            Analyze a Website
          </button>
          <button className="secondary-btn" onClick={scrollToTop}>Learn More</button>
        </div>
      </section>
    </div>
  );
}

export default Home;