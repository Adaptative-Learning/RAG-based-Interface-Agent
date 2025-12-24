from vector_store import VectorStore
from llm_analyzer import LLMAnalyzer
from questionnaire import Questionnaire

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def main():
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}SYSTEME DE PREDICTION DE DOMAINES IT{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.END}\n")
    
    # 1. Initialize ChromaDB and load domains
    print(f"{Colors.CYAN}[INFO] Chargement de la base de connaissances...{Colors.END}")
    vector_store = VectorStore()
    domains_loaded = vector_store.load_domains('data/domaines')
    print(f"{Colors.GREEN}[OK] {domains_loaded} domaines charges avec succes{Colors.END}\n")
    
    # 2. Launch questionnaire
    print(f"{Colors.BOLD}{Colors.BLUE}[QUESTIONNAIRE] DEBUT DU QUESTIONNAIRE{Colors.END}")
    questionnaire = Questionnaire('questionnaire.json')
    responses = questionnaire.run()
    
    # 3. Analyze responses
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}[ANALYSE] ANALYSE EN COURS...{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 70}{Colors.END}\n")
    
    # Retrieve relevant domains for all answers
    all_answers = " ".join([r['answer'] for r in responses])
    
    # Get all domains from vector store (not just similar ones)
    # This ensures we analyze ALL domains
    all_domain_names = vector_store.get_all_domains()
    
    # Still use similarity search for context
    similar_domains = vector_store.find_similar_domains(all_answers, top_k=len(all_domain_names))
    
    # Analyze with Ollama LLM
    print(f"{Colors.CYAN}[LLM] Connexion au modele Ollama...{Colors.END}")
    analyzer = LLMAnalyzer(model="llama3.2:1b")  # Much faster!
    results = analyzer.analyze_responses(responses, similar_domains)
    
    # 4. Display results
    if "error" in results:
        print(f"\n{Colors.RED}{Colors.BOLD}[ERREUR]{Colors.END}")
        print(f"{Colors.RED}   {results['error']}{Colors.END}")
        print(f"{Colors.RED}   Details: {results.get('details', 'N/A')}{Colors.END}")
        if 'tip' in results:
            print(f"\n{Colors.YELLOW}[CONSEIL] {results['tip']}{Colors.END}")
        return
    
    # Generate and display full report
    print(f"\n{analyzer.generate_detailed_report(results)}")
    
    # Display summary table
    print(f"\n{Colors.BOLD}{Colors.GREEN}[RESULTATS] RESUME DES SCORES:{Colors.END}\n")
    total = 0
    for pred in results['predictions']:
        score = pred['score']
        total += score
        bar = "#" * int(score / 2)  # Visual bar
        
        # Color code based on score
        if score >= 70:
            color = Colors.GREEN
        elif score >= 50:
            color = Colors.YELLOW
        else:
            color = Colors.CYAN
            
        print(f"{color}{pred['domaine']:30} {score:5.1f}% {bar}{Colors.END}")
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}TOTAL{' ' * 25}{total:5.1f}%{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.END}\n")

if __name__ == "__main__":
    main()