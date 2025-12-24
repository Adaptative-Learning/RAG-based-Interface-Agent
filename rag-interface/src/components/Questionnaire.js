import React, { useState } from 'react';
import './Questionnaire.css';

const Questionnaire = ({ questions, onSubmit }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [showAll, setShowAll] = useState(false);

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  const handleAnswerSelect = (questionId, answer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: answer
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = () => {
    // Convertir les réponses au format attendu par l'API
    const formattedAnswers = Object.entries(userAnswers).map(([questionId, answer]) => ({
      question_id: parseInt(questionId),
      answer: answer
    }));

    onSubmit(formattedAnswers);
  };

  const isAnswered = (questionId) => userAnswers[questionId] !== undefined;
  const allQuestionsAnswered = questions.every(q => isAnswered(q.id));

  if (showAll) {
    return (
      <div className="questionnaire-all">
        <div className="questionnaire-header">
          <h2>Questionnaire Complet</h2>
          <button
            className="toggle-view-btn"
            onClick={() => setShowAll(false)}
          >
            Vue par question
          </button>
        </div>

        {questions.map((question, index) => (
          <div key={question.id} className="question-card">
            <h3>Question {index + 1}</h3>
            <p className="question-text">{question.question}</p>
            <div className="options">
              {question.options.map((option, optionIndex) => (
                <label key={optionIndex} className="option">
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value={option}
                    checked={userAnswers[question.id] === option}
                    onChange={() => handleAnswerSelect(question.id, option)}
                  />
                  <span className="option-text">{option}</span>
                </label>
              ))}
            </div>
          </div>
        ))}

        <div className="submit-section">
          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={!allQuestionsAnswered}
          >
            Analyser mes réponses
          </button>
          {!allQuestionsAnswered && (
            <p className="warning">Veuillez répondre à toutes les questions</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="questionnaire">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>
      <div className="progress-text">
        Question {currentQuestionIndex + 1} sur {questions.length}
      </div>

      <div className="question-card">
        <h2>Question {currentQuestionIndex + 1}</h2>
        <p className="question-text">{currentQuestion?.question}</p>

        <div className="options">
          {currentQuestion?.options.map((option, index) => (
            <label key={index} className="option">
              <input
                type="radio"
                name="current-question"
                value={option}
                checked={userAnswers[currentQuestion.id] === option}
                onChange={() => handleAnswerSelect(currentQuestion.id, option)}
              />
              <span className="option-text">{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="navigation">
        <button
          className="nav-btn"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          Précédent
        </button>

        <button
          className="toggle-view-btn"
          onClick={() => setShowAll(true)}
        >
          Voir tout
        </button>

        {currentQuestionIndex < questions.length - 1 ? (
          <button
            className="nav-btn"
            onClick={handleNext}
            disabled={!isAnswered(currentQuestion?.id)}
          >
            Suivant
          </button>
        ) : (
          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={!allQuestionsAnswered}
          >
            Terminer
          </button>
        )}
      </div>

      {!isAnswered(currentQuestion?.id) && (
        <p className="instruction">Sélectionnez une réponse pour continuer</p>
      )}
    </div>
  );
};

export default Questionnaire;