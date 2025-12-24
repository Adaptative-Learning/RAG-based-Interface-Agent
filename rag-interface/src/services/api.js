import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const questionnaireAPI = {
  // Récupérer toutes les questions
  getQuestions: async () => {
    try {
      const response = await api.get('/questions');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des questions:', error);
      throw error;
    }
  },

  // Analyser les réponses
  analyzeResponses: async (answers) => {
    try {
      const response = await api.post('/analyze', { answers });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de l\'analyse des réponses:', error);
      throw error;
    }
  },

  // Vérifier l'état de l'API
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Erreur lors du health check:', error);
      throw error;
    }
  },
};

export default api;