import json

class Questionnaire:
    def __init__(self, questions_file):
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data['questions']
    
    def run(self):
        """Pose les questions et collecte les réponses"""
        responses = []
        
        for q in self.questions:
            print(f"\nQuestion {q['id']}: {q['question']}")
            
            # Afficher les options si elles existent
            options = q.get('options', [])
            if options:
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                
                # Boucle pour forcer à choisir une option valide
                while True:
                    try:
                        choice = int(input("Choisis une option (numéro) : "))
                        if 1 <= choice <= len(options):
                            answer = options[choice - 1]
                            break
                        else:
                            print("Numéro invalide, réessaie.")
                    except ValueError:
                        print("Merci de saisir un nombre.")
            else:
                answer = input("Ta réponse: ")
            
            responses.append({
                'question': q['question'],
                'answer': answer
            })
        
        return responses
