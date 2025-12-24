import React, { useState, useEffect } from 'react';
import './App.css';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import Loading from './components/Loading';
import ErrorMessage from './components/ErrorMessage';
import { questionnaireAPI } from './services/api';

function App() {
  const [currentStep, setCurrentStep] = useState('loading'); // 'loading', 'questionnaire', 'results', 'error'
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      setCurrentStep('loading');
      const questionnaireData = await questionnaireAPI.getQuestions();
      setQuestions(questionnaireData.questions || []);
      setCurrentStep('questionnaire');
    } catch (err) {
      console.error('Erreur lors du chargement des questions:', err);
      setError('Impossible de charger les questions. Vérifiez que le serveur API est démarré.');
      setCurrentStep('error');
    }
  };

  const handleAnswerSubmit = async (userAnswers) => {
    try {
      setCurrentStep('loading');
      setAnswers(userAnswers);

      const analysisResults = await questionnaireAPI.analyzeResponses(userAnswers);
      setResults(analysisResults);
      setCurrentStep('results');
    } catch (err) {
      console.error('Erreur lors de l\'analyse:', err);
      setError('Erreur lors de l\'analyse des réponses. Veuillez réessayer.');
      setCurrentStep('error');
    }
  };

  const handleRestart = () => {
    setAnswers([]);
    setResults(null);
    setError(null);
    setCurrentStep('questionnaire');
  };

  const renderContent = () => {
    switch (currentStep) {
      case 'loading':
        return <Loading />;
      case 'questionnaire':
        return (
          <Questionnaire
            questions={questions}
            onSubmit={handleAnswerSubmit}
          />
        );
      case 'results':
        return (
          <Results
            results={results}
            answers={answers}
            questions={questions}
            onRestart={handleRestart}
          />
        );
      case 'error':
        return (
          <ErrorMessage
            message={error}
            onRetry={loadQuestions}
          />
        );
      default:
        return <div>État inconnu</div>;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Système d'Orientation IT - RAG</h1>
        <p>Découvrez votre voie dans les technologies de l'information</p>
      </header>
      <main className="App-main">
        {renderContent()}
      </main>
      <footer className="App-footer">
        <p>Propulsé par l'IA et l'analyse RAG</p>
      </footer>
    </div>
  );
}

export default App;
