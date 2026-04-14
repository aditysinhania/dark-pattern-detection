import React from "react";
import "../styles/ChartComponent.css";

function ChartComponent({ data }) {
  if (!data || data.length === 0) {
    return <div className="chart-placeholder">No data available</div>;
  }

  const maxScore = Math.max(...data.map((d) => d.score));

  return (
    <div className="chart-container">
      <div className="bar-chart">
        {data.map((item, idx) => (
          <div key={idx} className="chart-bar-wrapper">
            <div className="chart-label">{item.name}</div>
            <div className="chart-bar-bg">
              <div
                className="chart-bar-fill"
                style={{
                  width: `${(item.score / 100) * 100}%`,
                  backgroundColor:
                    item.score > 70
                      ? "#ef4444"
                      : item.score > 40
                      ? "#f59e0b"
                      : "#10b981",
                }}
              >
                <span className="chart-value">{item.score}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChartComponent;
