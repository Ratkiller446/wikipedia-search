import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
import wikipedia
import sys

# Add language dictionary at the top
LANGUAGES = {
    "English": "en",
    "Norwegian": "no",
    "Swedish": "sv",
    "Danish": "da",
    "Finnish": "fi",
    "Icelandic": "is",
    "Russian": "ru"
}

class MultipleChoiceDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options):
        self.options = options
        self.choice = None
        super().__init__(parent, title)

    def body(self, frame):
        # Configure dark theme for dialog
        frame.configure(bg='black')
        label = tk.Label(frame, text="Multiple matches found. Please choose one:",
                        bg='black', fg='white')
        label.pack(pady=10)
        
        # Create buttons for each option
        for i, option in enumerate(self.options, 1):
            btn = tk.Button(frame, text=f"{i}. {option}",
                          command=lambda x=i-1: self.set_choice(x),
                          bg='gray20', fg='white', activebackground='gray40')
            btn.pack(fill=tk.X, padx=20, pady=2)
        
        return frame

    def set_choice(self, idx):
        self.choice = idx
        self.destroy()

    def buttonbox(self):
        # Add custom buttons
        box = tk.Frame(self, bg='black')
        box.pack()
        
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel,
                     bg='gray20', fg='white', activebackground='gray40')
        w.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

class WikipediaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Search GUI")
        self.root.configure(bg='black')
        
        # Configure the dark theme
        style = ttk.Style()
        style.configure("Dark.TFrame", background="black")
        style.configure("Dark.TLabel", background="black", foreground="white")
        style.configure("Dark.TEntry", fieldbackground="gray20", foreground="white")
        style.configure("Dark.TMenubutton", background="gray20", foreground="white")
        
        # Main container
        self.main_frame = ttk.Frame(root, style="Dark.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Search and Article
        self.left_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Search frame
        self.search_frame = ttk.Frame(self.left_frame, style="Dark.TFrame")
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda e: self.search())
        
        # Search button
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search,
                                     bg="gray20", fg="white", activebackground="gray40")
        self.search_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Find frame (initially hidden)
        self.find_frame = ttk.Frame(self.left_frame, style="Dark.TFrame")
        self.find_var = tk.StringVar()
        self.find_var.trace('w', lambda *args: self.highlight_text())
        
        self.find_entry = ttk.Entry(self.find_frame, textvariable=self.find_var)
        self.find_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.close_find_button = tk.Button(self.find_frame, text="×", command=self.toggle_find,
                                         bg="gray20", fg="white", activebackground="gray40")
        self.close_find_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Article text area (read-only)
        self.text_area = scrolledtext.ScrolledText(self.left_frame, wrap=tk.WORD, 
                                                  bg="black", fg="white",
                                                  insertbackground="white")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.configure(state='disabled')  # Make it read-only
        
        # Configure text tags for highlighting
        self.text_area.tag_configure("highlight", background="yellow", foreground="black")
        
        # Right side - Keybindings and Language
        self.right_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Keybindings title
        self.keys_label = ttk.Label(self.right_frame, text="Keybindings:",
                                   style="Dark.TLabel")
        self.keys_label.pack(anchor=tk.W)
        
        # Keybindings list
        keybindings = [
            "Enter - Search",
            "Ctrl+L - Clear",
            "Ctrl+Q - Quit",
            "Ctrl+F - Toggle find",
            "↑/↓ - Scroll",
            "PgUp/PgDn - Page scroll"
        ]
        
        for kb in keybindings:
            label = ttk.Label(self.right_frame, text=kb, style="Dark.TLabel")
            label.pack(anchor=tk.W)
            
        # Add separator
        ttk.Separator(self.right_frame, orient='horizontal').pack(fill='x', pady=10)
            
        # Language selector
        self.lang_label = ttk.Label(self.right_frame, text="Language:",
                                   style="Dark.TLabel")
        self.lang_label.pack(anchor=tk.W, pady=(10, 5))
        
        # Language variable and menu
        self.current_lang = tk.StringVar(value="English")
        self.lang_menu = tk.OptionMenu(self.right_frame, self.current_lang, *LANGUAGES.keys(),
                                     command=self.change_language)
        self.lang_menu.configure(bg="gray20", fg="white", activebackground="gray40",
                               highlightbackground="black")
        self.lang_menu["menu"].configure(bg="gray20", fg="white", activebackground="gray40")
        self.lang_menu.pack(anchor=tk.W)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-l>', lambda e: self.clear_search())
        self.root.bind('<Control-f>', lambda e: self.toggle_find())
        
        # Set focus to search entry
        self.search_entry.focus()
        
        # Track find frame visibility
        self.find_visible = False

    def set_text(self, text):
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state='disabled')
    
    def toggle_find(self, event=None):
        if self.find_visible:
            self.find_frame.pack_forget()
            self.text_area.tag_remove("highlight", "1.0", tk.END)
            self.search_entry.focus()
            self.find_visible = False
        else:
            self.find_frame.pack(fill=tk.X, pady=(0, 10))
            self.find_entry.focus()
            self.highlight_text()
            self.find_visible = True
    
    def highlight_text(self):
        # Remove existing highlights
        self.text_area.tag_remove("highlight", "1.0", tk.END)
        
        # Get the search term
        find_text = self.find_var.get().strip().lower()
        if not find_text:
            return
            
        # Get the text content
        content = self.text_area.get("1.0", tk.END).lower()
        
        # Find all occurrences
        start_idx = "1.0"
        while True:
            start_idx = self.text_area.search(find_text, start_idx, tk.END, nocase=True)
            if not start_idx:
                break
                
            end_idx = f"{start_idx}+{len(find_text)}c"
            self.text_area.tag_add("highlight", start_idx, end_idx)
            start_idx = end_idx
    
    def search(self):
        query = self.search_var.get().strip()
        if not query:
            return
            
        try:
            # Set the language before searching
            lang_code = LANGUAGES[self.current_lang.get()]
            wikipedia.set_lang(lang_code)
            
            # Clear previous content
            self.set_text("Searching...\n")
            self.root.update()
            
            # Search Wikipedia
            search_results = wikipedia.search(query, results=5)
            
            if not search_results:
                self.set_text("No results found.")
                return
            
            # If we have multiple results, let user choose
            if len(search_results) > 1:
                dialog = MultipleChoiceDialog(self.root, "Choose Article", search_results)
                if dialog.choice is None:  # User cancelled
                    self.set_text("Search cancelled.")
                    return
                selected_title = search_results[dialog.choice]
            else:
                selected_title = search_results[0]
            
            # Get the selected page
            try:
                page = wikipedia.page(selected_title, auto_suggest=False)
                # Get full article content without references and links
                content = [
                    f"Title: {page.title}",
                    f"\nURL: {page.url}",
                    f"\nSummary:\n{page.summary}",
                    f"\nContent:\n{page.content}"
                ]
                
                self.set_text("\n".join(content))
                
                # Reapply highlighting if find bar is visible
                if self.find_visible and self.find_var.get():
                    self.highlight_text()
                    
            except wikipedia.exceptions.DisambiguationError as e:
                options = "\n".join([f"• {opt}" for opt in e.options[:10]])
                self.set_text(f"Multiple matches found:\n\n{options}\n\nPlease refine your search.")
            except wikipedia.exceptions.PageError:
                self.set_text("Article not found. Please try another search term.")
                
        except Exception as e:
            self.set_text(f"An error occurred: {str(e)}")
    
    def clear_search(self):
        self.search_var.set("")
        self.set_text("")
        self.search_entry.focus()
        if self.find_visible:
            self.toggle_find()

    def change_language(self, *args):
        lang_code = LANGUAGES[self.current_lang.get()]
        wikipedia.set_lang(lang_code)
        self.search()  # Refresh the current search with new language

def main():
    root = tk.Tk()
    root.geometry("1000x600")  # Set initial window size
    app = WikipediaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 