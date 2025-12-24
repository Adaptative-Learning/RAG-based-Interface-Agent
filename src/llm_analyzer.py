import requests
import json
from typing import List, Dict, Optional

class LLMAnalyzer:
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initialize the analyzer with Ollama.
        
        Args:
            model: Ollama model name (llama3.2, mistral, llama3.1, etc.)
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/chat"
        
    def analyze_responses(
        self, 
        responses: List[Dict[str, str]], 
        similar_domains: Dict,
        temperature: float = 0.3
    ) -> Dict:
        """
        Analyzes student responses and predicts appropriate IT domains.
        Percentages will sum to 100%.
        """
        try:
            # Extract domain names
            domain_names = []
            if similar_domains and 'metadatas' in similar_domains:
                domain_names = [m['domaine'] for m in similar_domains['metadatas'][0]]
            
            if not domain_names:
                return {
                    "error": "Aucun domaine trouvé",
                    "predictions": [],
                    "resume_global": "Impossible d'effectuer l'analyse sans domaines."
                }
            
            # Format Q&A clearly
            formatted_qa = "\n".join([
                f"Q{i+1}: {r['question']}\nR: {r['answer']}" 
                for i, r in enumerate(responses)
            ])
            
            # Format domains with their descriptions
            domain_descriptions = ""
            if similar_domains and 'documents' in similar_domains:
                domain_descriptions = "\n\n".join([
                    f"**{domain_names[i]}**:\n{doc[:400]}" 
                    for i, doc in enumerate(similar_domains['documents'][0])
                ])
            else:
                domain_descriptions = "Descriptions non disponibles"
            
            # Optimized prompt for automatic analysis
            prompt = f"""Tu es un expert en orientation IT. Analyse les réponses de cet étudiant et détermine son affinité avec chaque domaine IT.

DOMAINES À ÉVALUER :
{', '.join(domain_names)}

DESCRIPTIONS DES DOMAINES :
{domain_descriptions}

RÉPONSES DE L'ÉTUDIANT :
{formatted_qa}

INSTRUCTIONS :
1. Analyse automatiquement les réponses pour détecter :
   - Les compétences et connaissances techniques mentionnées
   - Les intérêts et passions exprimés
   - L'expérience et les projets décrits
   - Les motivations et objectifs de carrière
   - Le style d'apprentissage et de travail préféré

2. Pour CHAQUE domaine de la liste, attribue un score de 0 à 100 basé sur l'alignement global du profil de l'étudiant avec ce domaine.

3. IMPORTANT : Les scores doivent être proportionnels. Si l'étudiant correspond bien à plusieurs domaines, distribue les scores en conséquence. Les scores ne doivent PAS tous être élevés - différencie clairement.

4. Pour chaque domaine, fournis :
   - domaine : nom exact du domaine (choisi parmi la liste)
   - score : nombre entre 0 et 100 (sera normalisé pour totaliser 100%)
   - raisons : 3-5 observations concrètes tirées des réponses
   - confiance : "haute", "moyenne", ou "basse"
   - points_forts : compétences/traits alignés avec ce domaine
   - axes_amelioration : compétences à développer

5. Ajoute un résumé du profil global de l'étudiant

Réponds UNIQUEMENT en JSON valide (pas de markdown, pas de texte avant/après) :
{{
  "predictions": [
    {{
      "domaine": "nom_exact_du_domaine",
      "score": 85,
      "raisons": ["observation1", "observation2", "observation3"],
      "confiance": "haute",
      "points_forts": ["force1", "force2"],
      "axes_amelioration": ["axe1", "axe2"]
    }}
  ],
  "resume_global": "Synthèse du profil en 2-3 phrases",
  "top_3_recommandations": ["domaine1", "domaine2", "domaine3"]
}}"""

            # Call Ollama API
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un expert en orientation IT. Tu réponds toujours en JSON valide, sans markdown. Tu es précis, objectif et constructif. Tu analyses en profondeur les réponses pour comprendre le profil de l'étudiant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": temperature,
                    "num_predict": 4000
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=300)  # 5 minutes
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            response_text = response_data['message']['content']
            result = self._parse_json_response(response_text)
            
            # Normalize scores to sum to 100%
            result = self._normalize_scores(result, domain_names)
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "Erreur de connexion à Ollama",
                "details": str(e),
                "tip": "Vérifiez qu'Ollama est lancé avec 'ollama serve'"
            }
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
        """Parse JSON response handling edge cases."""
        cleaned = response_text.strip()
        
        # Clean markdown if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        return json.loads(cleaned.strip())
    
    def _normalize_scores(self, result: Dict, valid_domains: List[str]) -> Dict:
        """
        Normalize scores to sum to 100% and validate results.
        """
        if "predictions" not in result:
            return result
        
        # Normalize domain names for comparison
        valid_domains_lower = [d.lower() for d in valid_domains]
        
        # Filter and validate predictions
        valid_predictions = []
        for p in result["predictions"]:
            if p.get("domaine", "").lower() in valid_domains_lower:
                # Ensure score is within limits
                p["score"] = max(0, min(100, float(p.get("score", 0))))
                valid_predictions.append(p)
        
        if not valid_predictions:
            return result
        
        # Calculate total score
        total_score = sum(p["score"] for p in valid_predictions)
        
        # Normalize to 100%
        if total_score > 0:
            for p in valid_predictions:
                p["score"] = round((p["score"] / total_score) * 100, 1)
            
            # Adjust for rounding errors - ensure exactly 100%
            current_total = sum(p["score"] for p in valid_predictions)
            if current_total != 100.0:
                diff = 100.0 - current_total
                valid_predictions[0]["score"] = round(valid_predictions[0]["score"] + diff, 1)
        else:
            # If all scores are 0, distribute equally
            equal_score = round(100.0 / len(valid_predictions), 1)
            for i, p in enumerate(valid_predictions):
                p["score"] = equal_score
            # Adjust last one for rounding
            valid_predictions[-1]["score"] = round(100.0 - equal_score * (len(valid_predictions) - 1), 1)
        
        # Sort by score descending
        valid_predictions.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        result["predictions"] = valid_predictions
        
        # Update top_3_recommendations
        if valid_predictions:
            result["top_3_recommandations"] = [
                p["domaine"] for p in valid_predictions[:3]
            ]
        
        return result
    
    def get_top_recommendations(self, analysis_result: Dict, top_n: int = 3) -> List[Dict]:
        """
        Extract top N recommendations.
        """
        if "predictions" not in analysis_result:
            return []
        
        return analysis_result["predictions"][:top_n]
    
    def generate_detailed_report(self, analysis_result: Dict) -> str:
        """
        Generate detailed formatted text report.
        """
        if "error" in analysis_result:
            return f"❌ Erreur: {analysis_result['error']}\nDétails: {analysis_result.get('details', 'N/A')}"
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("RAPPORT D'ORIENTATION IT")
        report_lines.append("=" * 70)
        
        # Global summary
        if "resume_global" in analysis_result:
            report_lines.append(f"\n📋 PROFIL ÉTUDIANT:\n{analysis_result['resume_global']}")
        
        # Top 3
        if "top_3_recommandations" in analysis_result:
            report_lines.append(f"\n🏆 TOP 3 RECOMMANDATIONS:")
            for i, dom in enumerate(analysis_result['top_3_recommandations'], 1):
                report_lines.append(f"   {i}. {dom}")
        
        # Verify total is 100%
        total_score = sum(p['score'] for p in analysis_result.get('predictions', []))
        report_lines.append(f"\n📊 DISTRIBUTION (Total: {total_score}%)")
        report_lines.append("\nANALYSE DÉTAILLÉE PAR DOMAINE")
        
        for pred in analysis_result.get('predictions', []):
            report_lines.append(f"\n📌 {pred['domaine'].upper()}")
            report_lines.append(f"   Score: {pred['score']}% | Confiance: {pred['confiance']}")
            
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