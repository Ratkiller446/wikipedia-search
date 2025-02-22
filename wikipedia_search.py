import wikipedia
import sys

def check_quit(input_text):
    if input_text.lower() == 'quit':
        print("Goodbye!")
        sys.exit(0)

def get_wikipedia_article(title):
    try:
        # Check if user wants to quit
        check_quit(title)
        
        # First search for matching pages
        search_results = wikipedia.search(title, results=5)
        
        if not search_results:
            return "No articles found. Please try another search term."
        
        # If we have multiple results, let user choose
        if len(search_results) > 1:
            print("\nFound multiple matches. Please choose one:")
            for i, result in enumerate(search_results, 1):
                print(f"{i}. {result}")
            
            while True:
                try:
                    choice = input("\nEnter a number to choose an article (or press Enter to search again): ").strip()
                    # Check if user wants to quit
                    check_quit(choice)
                    
                    if choice == '':
                        return "Please try another search."
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(search_results):
                        title = search_results[choice_idx]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        
        # Get the page
        page = wikipedia.page(title, auto_suggest=False)
        return f"Title: {page.title}\n\n{page.content}"
    except wikipedia.exceptions.PageError:
        return "Article not found. Please try another search term."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"This topic is ambiguous. Possible matches:\n{', '.join(e.options)}"

def main():
    print("\nWelcome to Wikipedia Search!")
    print("Type 'quit' at any time to exit the program.")
    
    while True:
        # Get user input
        print("\nEnter a Wikipedia article title: ")
        search_term = input().strip()
        
        # Check if user wants to quit
        check_quit(search_term)
        
        # Get and print the article
        article = get_wikipedia_article(search_term)
        print("\n" + "="*80 + "\n")
        print(article)
        print("\n" + "="*80)
        
        # Ask if user wants to continue reading or search again
        while True:
            action = input("\nPress Enter to search again, or type 'quit' to exit: ").strip()
            if action == '' or action.lower() == 'quit':
                break
        
        check_quit(action)

if __name__ == "__main__":
    main() 