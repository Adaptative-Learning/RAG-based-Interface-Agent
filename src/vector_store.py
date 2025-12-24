import chromadb
import os

class VectorStore:
    def __init__(self, collection_name="domaine_it"):
        """
        Initialise le store vectoriel avec ChromaDB.
        
        Args:
            collection_name: Nom de la collection ChromaDB
        """
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)

    def load_domains(self, domain_folder):
        """
        Charge tous les domaines depuis un dossier.
        
        Args:
            domain_folder: Chemin vers le dossier contenant les fichiers .txt
            
        Returns:
            Nombre de domaines chargés
        """
        if not os.path.exists(domain_folder):
            raise FileNotFoundError(f"Le dossier {domain_folder} n'existe pas")
        
        loaded_count = 0
        
        for filename in os.listdir(domain_folder):
            if filename.endswith(".txt"):
                domain_name = filename.replace(".txt", "")
                filepath = os.path.join(domain_folder, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    if content:  # Ne charger que si le fichier n'est pas vide
                        self.collection.add(
                            documents=[content],
                            metadatas=[{"domaine": domain_name}],
                            ids=[domain_name]
                        )
                        loaded_count += 1
                        print(f"   ✓ {domain_name}")
                    else:
                        print(f"   ⚠ {domain_name} (fichier vide, ignoré)")
                        
                except Exception as e:
                    print(f"   ✗ Erreur lors du chargement de {domain_name}: {e}")
        
        return loaded_count

    def find_similar_domains(self, answer_text, top_k=3):
        """
        Trouve les domaines les plus similaires à un texte donné.
        
        Args:
            answer_text: Texte à analyser (réponses du questionnaire)
            top_k: Nombre de domaines à retourner
            
        Returns:
            Résultats de la requête ChromaDB avec documents, metadatas, distances
        """
        if not answer_text or not answer_text.strip():
            return {
                'documents': [[]],
                'metadatas': [[]],
                'distances': [[]]
            }
        
        try:
            results = self.collection.query(
                query_texts=[answer_text],
                n_results=min(top_k, self.collection.count())
            )
            return results
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return {
                'documents': [[]],
                'metadatas': [[]],
                'distances': [[]]
            }
    
    def get_all_domains(self):
        """
        Récupère tous les domaines disponibles.
        
        Returns:
            Liste des noms de domaines
        """
        try:
            all_data = self.collection.get()
            return [meta['domaine'] for meta in all_data['metadatas']]
        except Exception as e:
            print(f"Erreur lors de la récupération des domaines: {e}")
            return []
    
    def get_domain_content(self, domain_name):
        """
        Récupère le contenu complet d'un domaine.
        
        Args:
            domain_name: Nom du domaine
            
        Returns:
            Contenu du domaine ou None si non trouvé
        """
        try:
            result = self.collection.get(ids=[domain_name])
            if result['documents']:
                return result['documents'][0]
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de {domain_name}: {e}")
            return None
    
    def clear_collection(self):
        """Vide la collection (utile pour réinitialiser)."""
        try:
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.get_or_create_collection(self.collection.name)
            print("Collection vidée avec succès")
        except Exception as e:
            print(f"Erreur lors du vidage de la collection: {e}")