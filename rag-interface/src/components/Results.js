import React from 'react';
import './Results.css';

const Results = ({ results, answers, questions, onRestart }) => {
  if (!results) {
    return <div>Aucun résultat disponible</div>;
  }

  const getConfidenceColor = (confidence) => {
    switch (confidence) {
      case 'haute': return '#4CAF50';
      case 'moyenne': return '#FF9800';
      case 'basse': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FF9800';
    return '#F44336';
  };

  return (
    <div className="results">
      <div className="results-header">
        <h2>🎯 Vos Résultats d'Orientation IT</h2>
        <p className="results-summary">{results.resume_global}</p>
      </div>

      <div className="top-recommendations">
        <h3>🏆 Top 3 Recommandations</h3>
        <div className="recommendations-list">
          {results.top_3_recommandations?.map((domain, index) => (
            <div key={domain} className={`recommendation rank-${index + 1}`}>
              <span className="rank">#{index + 1}</span>
              <span className="domain-name">{domain}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="detailed-results">
        <h3>📊 Analyse Détaillée par Domaine</h3>
        {results.predictions?.map((prediction, index) => (
          <div key={prediction.domaine} className="prediction-card">
            <div className="prediction-header">
              <h4>{prediction.domaine}</h4>
              <div className="score-info">
                <div className="score">
                  <span className="score-value" style={{ color: getScoreColor(prediction.score) }}>
                    {prediction.score}/100
                  </span>
                  <span className="score-label">Score</span>
                </div>
                <div className="confidence">
                  <span
                    className="confidence-badge"
                    style={{ backgroundColor: getConfidenceColor(prediction.confiance) }}
                  >
                    {prediction.confiance}
                  </span>
                  <span className="confidence-label">Confiance</span>
                </div>
              </div>
            </div>

            <div className="prediction-details">
              <div className="reasons">
                <h5>💡 Raisons</h5>
                <ul>
                  {prediction.raisons?.map((raison, idx) => (
                    <li key={idx}>{raison}</li>
                  ))}
                </ul>
              </div>

              {prediction.points_forts && prediction.points_forts.length > 0 && (
                <div className="strengths">
                  <h5>✅ Points Forts</h5>
                  <ul>
                    {prediction.points_forts.map((point, idx) => (
                      <li key={idx}>{point}</li>
                    ))}
                  </ul>
                </div>
              )}

              {prediction.axes_amelioration && prediction.axes_amelioration.length > 0 && (
                <div className="improvements">
                  <h5>📈 À Développer</h5>
                  <ul>
                    {prediction.axes_amelioration.map((axis, idx) => (
                      <li key={idx}>{axis}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="user-answers">
        <h3>📝 Vos Réponses</h3>
        <div className="answers-list">
          {answers.map((answer, index) => {
            const question = questions.find(q => q.id === answer.question_id);
            return (
              <div key={index} className="answer-item">
                <div className="question-number">Q{index + 1}</div>
                <div className="answer-content">
                  <p className="question-text">{question?.question}</p>
                  <p className="user-answer">💬 {answer.answer}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="actions">
        <button className="restart-btn" onClick={onRestart}>
          🔄 Refaire le questionnaire
        </button>
        <div className="share-info">
          <p>Partagez vos résultats avec vos proches ou mentors !</p>
        </div>
      </div>
    </div>
  );
};

export default Results;