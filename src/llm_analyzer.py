from groq import Groq
import json
from typing import List, Dict, Optional
import os

class LLMAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise l'analyseur avec l'API Groq.
        
        Args:
            api_key: Clé API Groq (optionnel, peut utiliser GROQ_API_KEY env var)
        """
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        
    def _build_context(self, responses: List[Dict], similar_domains: Dict) -> str:
        """
        Construit un contexte enrichi à partir des réponses et domaines similaires.
        
        Args:
            responses: Liste des réponses [{question, answer}]
            similar_domains: Résultats de recherche vectorielle
            
        Returns:
            Contexte formaté pour le prompt
        """
        context_parts = []
        
        # Extraire tous les textes de réponses
        all_answers = " ".join([r['answer'] for r in responses])
        
        # Analyser les compétences techniques mentionnées
        technical_keywords = {
            'langages': ['python', 'java', 'javascript', 'c++', 'go', 'rust', 'php', 'ruby'],
            'outils': ['docker', 'kubernetes', 'git', 'jenkins', 'ansible', 'terraform'],
            'domaines': ['cloud', 'data', 'sécurité', 'réseau', 'web', 'mobile', 'ia', 'ml'],
            'concepts': ['api', 'microservices', 'devops', 'agile', 'ci/cd', 'testing']
        }
        
        found_keywords = {}
        answer_lower = all_answers.lower()
        
        for category, keywords in technical_keywords.items():
            found = [k for k in keywords if k in answer_lower]
            if found:
                found_keywords[category] = found
        
        if found_keywords:
            for category, keywords in found_keywords.items():
                context_parts.append(f"{category.capitalize()}: {', '.join(keywords)}")
        
        # Analyser le niveau d'expérience
        experience_levels = {
            'débutant': ['débutant', 'nouveau', 'apprendre', 'découvrir'],
            'intermédiaire': ['intermédiaire', 'quelques projets', 'pratique'],
            'avancé': ['avancé', 'expérimenté', 'expert', 'professionnel', 'années']
        }
        
        detected_level = None
        for level, indicators in experience_levels.items():
            if any(ind in answer_lower for ind in indicators):
                detected_level = level
                break
        
        if detected_level:
            context_parts.append(f"Niveau estimé: {detected_level}")
        
        # Ajouter les domaines similaires trouvés
        if similar_domains and 'metadatas' in similar_domains:
            domains_found = [m['domaine'] for m in similar_domains['metadatas'][0]]
            context_parts.append(f"Domaines pertinents identifiés: {', '.join(domains_found)}")
        
        return "\n".join(context_parts) if context_parts else "Analyse basée sur les réponses directes."

    def analyze_responses(
        self, 
        responses: List[Dict[str, str]], 
        similar_domains: Dict,
        temperature: float = 0.2
    ) -> Dict:
        """
        Analyse les réponses de l'étudiant et prédit les domaines IT appropriés.
        
        Args:
            responses: Liste de {question, answer}
            similar_domains: Résultats de recherche vectorielle ChromaDB
            temperature: Contrôle la créativité (0-1, plus bas = plus déterministe)
            
        Returns:
            Dictionnaire avec les prédictions et scores
        """
        try:
            context = self._build_context(responses, similar_domains)
            
            # Extraire les noms de domaines
            domain_names = []
            if similar_domains and 'metadatas' in similar_domains:
                domain_names = [m['domaine'] for m in similar_domains['metadatas'][0]]
            
            # Formater les Q&A de manière claire
            formatted_qa = "\n".join([
                f"Q{i+1}: {r['question']}\nR: {r['answer']}\n" 
                for i, r in enumerate(responses)
            ])
            
            # Formater les domaines avec leurs descriptions si disponibles
            formatted_domains = "\n".join([
                f"- {name}" for name in domain_names
            ])
            
            if similar_domains and 'documents' in similar_domains:
                domain_descriptions = "\n\n".join([
                    f"**{domain_names[i]}**:\n{doc[:300]}..." 
                    for i, doc in enumerate(similar_domains['documents'][0])
                ])
            else:
                domain_descriptions = "Aucune description disponible"
            
            # Prompt optimisé
            prompt = f"""Tu es un conseiller d'orientation IT expert avec 15 ans d'expérience. Analyse les réponses de cet étudiant pour recommander les domaines IT les plus appropriés.

DOMAINES IT À ÉVALUER :
{formatted_domains}

DESCRIPTIONS DES DOMAINES :
{domain_descriptions}

RÉPONSES DE L'ÉTUDIANT :
{formatted_qa}

CONTEXTE TECHNIQUE DÉTECTÉ :
{context}

INSTRUCTIONS D'ANALYSE :
1. Évalue CHAQUE domaine de la liste avec un score de 0 à 100 basé sur :
   - Adéquation des compétences techniques mentionnées (40%)
   - Intérêts et passions exprimés (30%)
   - Expérience et projets pertinents (20%)
   - Motivations et objectifs de carrière (10%)

2. Pour chaque domaine, fournis :
   - domaine : nom exact du domaine
   - score : nombre entre 0 et 100
   - raisons : 3-5 facteurs concrets qui justifient le score
   - confiance : "haute" (>75), "moyenne" (50-75), ou "basse" (<50)
   - points_forts : compétences alignées avec ce domaine
   - axes_amelioration : compétences à développer pour ce domaine

3. Ajoute un résumé global du profil

Réponds UNIQUEMENT avec un objet JSON valide (sans markdown) :
{{
  "predictions": [
    {{
      "domaine": "nom_exact_du_domaine",
      "score": 85,
      "raisons": ["raison1", "raison2", "raison3"],
      "confiance": "haute",
      "points_forts": ["compétence1", "compétence2"],
      "axes_amelioration": ["compétence à développer"]
    }}
  ],
  "resume_global": "Synthèse du profil en 2-3 phrases",
  "top_3_recommandations": ["domaine1", "domaine2", "domaine3"]
}}"""

            # Appel à l'API Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert en orientation IT. Tu réponds toujours en JSON valide, sans markdown ni texte supplémentaire. Tu es précis, objectif et constructif dans tes analyses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            # Parser la réponse
            response_text = response.choices[0].message.content
            result = self._parse_json_response(response_text)
            
            # Validation et tri des résultats
            result = self._validate_and_sort_results(result, domain_names)
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "error": "Erreur de parsing JSON",
                "details": str(e),
                "raw_response": response_text if 'response_text' in locals() else None
            }
        except Exception as e:
            return {
                "error": "Erreur lors de l'analyse",
                "details": str(e),
                "type": type(e).__name__
            }
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse la réponse JSON en gérant les cas limites."""
        cleaned = response_text.strip()
        
        # Nettoyer les markdown si présents
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        return json.loads(cleaned.strip())
    
    def _validate_and_sort_results(
        self, 
        result: Dict, 
        valid_domains: List[str]
    ) -> Dict:
        """Valide et trie les résultats."""
        if "predictions" not in result:
            return result
        
        # Normaliser les noms de domaines pour la comparaison
        valid_domains_lower = [d.lower() for d in valid_domains]
        
        # Filtrer et valider les prédictions
        valid_predictions = []
        for p in result["predictions"]:
            if p.get("domaine", "").lower() in valid_domains_lower:
                # S'assurer que le score est dans les limites
                p["score"] = max(0, min(100, p.get("score", 0)))
                valid_predictions.append(p)
        
        # Trier par score décroissant
        valid_predictions.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        result["predictions"] = valid_predictions
        
        # Mettre à jour top_3_recommandations
        if valid_predictions:
            result["top_3_recommandations"] = [
                p["domaine"] for p in valid_predictions[:3]
            ]
        
        return result
    
    def get_top_recommendations(
        self, 
        analysis_result: Dict, 
        top_n: int = 3
    ) -> List[Dict]:
        """
        Extrait les N meilleures recommandations.
        
        Args:
            analysis_result: Résultat de analyze_responses()
            top_n: Nombre de recommandations à retourner
            
        Returns:
            Liste des top N domaines recommandés
        """
        if "predictions" not in analysis_result:
            return []
        
        return analysis_result["predictions"][:top_n]
    
    def generate_detailed_report(self, analysis_result: Dict) -> str:
        """
        Génère un rapport détaillé en texte formaté.
        
        Args:
            analysis_result: Résultat de analyze_responses()
            
        Returns:
            Rapport formaté en texte
        """
        if "error" in analysis_result:
            return f"❌ Erreur: {analysis_result['error']}\nDétails: {analysis_result.get('details', 'N/A')}"
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("RAPPORT D'ORIENTATION IT")
        report_lines.append("=" * 70)
        
        # Résumé global
        if "resume_global" in analysis_result:
            report_lines.append(f"\n📋 PROFIL ÉTUDIANT:\n{analysis_result['resume_global']}")
        
        # Top 3
        if "top_3_recommandations" in analysis_result:
            report_lines.append(f"\n🏆 TOP 3 RECOMMANDATIONS:")
            for i, dom in enumerate(analysis_result['top_3_recommandations'], 1):
                report_lines.append(f"   {i}. {dom}")
        
        # Détails par domaine
        report_lines.append("ANALYSE DÉTAILLÉE PAR DOMAINE")
        
        for pred in analysis_result.get('predictions', []):
            report_lines.append(f"\n📌 {pred['domaine'].upper()}")
            report_lines.append(f"   Score: {pred['score']}/100 | Confiance: {pred['confiance']}")
            
            report_lines.append(f"\n   💡 Raisons:")
            for raison in pred.get('raisons', []):
                report_lines.append(f"      • {raison}")
            
            if 'points_forts' in pred and pred['points_forts']:
                report_lines.append(f"\n   ✅ Points forts:")
                for pf in pred['points_forts']:
                    report_lines.append(f"      • {pf}")
            
            if 'axes_amelioration' in pred and pred['axes_amelioration']:
                report_lines.append(f"\n   📈 À développer:")
                for aa in pred['axes_amelioration']:
                    report_lines.append(f"      • {aa}")
            
            report_lines.append("")
        
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)