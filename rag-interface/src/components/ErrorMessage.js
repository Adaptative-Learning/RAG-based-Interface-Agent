import React from 'react';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-message">
      <div className="error-icon">⚠️</div>
      <h3>Oups ! Une erreur est survenue</h3>
      <p className="error-text">{message}</p>
      <div className="error-actions">
        <button className="retry-btn" onClick={onRetry}>
          🔄 Réessayer
        </button>
      </div>
      <div className="error-help">
        <p>Si le problème persiste :</p>
        <ul>
          <li>Vérifiez que le serveur API est démarré</li>
          <li>Vérifiez votre connexion internet</li>
          <li>Actualisez la page</li>
        </ul>
      </div>
    </div>
  );
};

export default ErrorMessage;