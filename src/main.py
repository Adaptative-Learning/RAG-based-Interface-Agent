from vector_store import VectorStore
from llm_analyzer import LLMAnalyzer
from questionnaire import Questionnaire
import os
from dotenv import load_dotenv

def main():
    # Charger les variables d'environnement
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')
    
    print("Système de prédiction de domaines IT")
    
    # 1. Initialiser ChromaDB et charger les domaines
    print("\nChargement de la base de connaissances...")
    vector_store = VectorStore()
    vector_store.load_domains('data/domaines')
    
    # 2. Lancer le questionnaire
    print("\nDébut du questionnaire")
    questionnaire = Questionnaire('questionnaire.json')
    responses = questionnaire.run()
    
    # 3. Analyser les réponses
    print("\nAnalyse en cours...")
    
    # Récupérer les domaines pertinents pour chaque réponse
    all_answers = " ".join([r['answer'] for r in responses])
    similar_domains = vector_store.find_similar_domains(all_answers)
    
    # Analyser avec le LLM
    analyzer = LLMAnalyzer(api_key)
    results = analyzer.analyze_responses(responses, similar_domains)
    
    # 4. Afficher les résultats
    print("RÉSULTATS")
    
    # Vérifier s'il y a une erreur
    if "error" in results:
        print(f"❌ Erreur lors de l'analyse: {results['error']}")
        print(f"Détails: {results.get('details', 'N/A')}")
        return
    
    # Vérifier que les prédictions existent
    if "predictions" not in results:
        print("❌ Aucune prédiction trouvée dans les résultats")
        return
    
    for pred in results['predictions']:
        print(f"\n{pred['domaine']} : {pred['score']}%")
        print(f"   Confiance : {pred['confiance']}")
        print(f"   Raisons :")
        for raison in pred['raisons']:
            print(f"   ✓ {raison}")

if __name__ == "__main__":
    main()