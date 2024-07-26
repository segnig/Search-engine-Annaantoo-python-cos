import tkinter as tk
from tkinter import messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import shutil
import os
from similarity_measure import * 
from remove_stopping_words import *
from weighter import * 
from weight_to_file import *
from query_proccesor import *

"""
Sure! Here are more color codes with their corresponding names:

- `"#f44336"` is red
- `"#e91e63"` is pink
- `"#9c27b0"` is purple
- `"#673ab7"` is deep purple
- `"#3f51b5"` is indigo
- `"#2196f3"` is blue
- `"#03a9f4"` is light blue
- `"#00bcd4"` is cyan
- `"#009688"` is teal
- `"#4caf50"` is green
- `"#8bc34a"` is light green
- `"#cddc39"` is lime
- `"#ffeb3b"` is yellow
- `"#ffc107"` is amber
- `"#ff9800"` is orange
- `"#ff5722"` is deep orange
- `"#795548"` is brown
- `"#9e9e9e"` is gray
- `"#607d8b"` is blue gray

These should give you a wide range of options for customizing your UI.
"""

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AnnaanToo Search Engine")
        self.root.geometry("800x800")
        self.root.configure(bg="#f0f0f0")

        # Enable drag and drop support
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop)

        # Create the menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Search", command=self.new_search)
        self.file_menu.add_command(label="Upload File", command=self.upload_file)  # Add Upload File option
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Add help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # Create a header label
        self.header_label = tk.Label(root, text="AnnaanToo Search Engine", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#673ab7")
        self.header_label.pack(pady=20)

        # Add a stylish frame around the entry and button
        self.top_frame = tk.Frame(root, bg="#4CAF50", bd=5)
        self.top_frame.pack(pady=10)

        # Create the search entry widget
        self.search_entry = tk.Entry(self.top_frame, width=40, font=("Helvetica", 14))
        self.search_entry.pack(side=tk.LEFT, padx=10)

        # Create the search button
        self.search_button = tk.Button(self.top_frame, text="Search", font=("Helvetica", 12, "bold"), bg="#ff9800", command=self.perform_search)
        self.search_button.pack(side=tk.LEFT)

        # Add a stylish frame around the listbox
        self.middle_frame = tk.Frame(root, bg="#f0f0f0", bd=5)
        self.middle_frame.pack(pady=10)

        # Create the listbox to display search results with a scrollbar
        self.scrollbar = tk.Scrollbar(self.middle_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_listbox = tk.Listbox(self.middle_frame, width=50, height=10, font=("Helvetica", 12), yscrollcommand=self.scrollbar.set, bg="#ffffff", selectbackground="#4CAF50", selectforeground="#ffffff")
        self.results_listbox.pack(pady=10)
        self.results_listbox.bind("<<ListboxSelect>>", self.show_details)

        self.scrollbar.config(command=self.results_listbox.yview)

        # Add a detail frame
        self.detail_frame = tk.Frame(root, bg="#f0f0f1", bd=5)
        self.detail_frame.pack(pady=10)

        self.detail_text = tk.Text(self.detail_frame, width=120, height=15, font=("Helvetica", 12), bg="#ffffff")
        self.detail_text.pack(pady=10)

        # Add a status bar
        self.status_bar = tk.Label(root, text="Welcome to AnnaanToo Search Engine", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Helvetica", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Add a footer frame with a label
        self.footer_frame = tk.Frame(root, bg="#4CAF50", bd=5)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.footer_label = tk.Label(self.footer_frame, text="© 2024 AnnaanToo Search Engine Inc.", font=("Helvetica", 10), bg="#4CAF50", fg="#ffffff")
        self.footer_label.pack()

        # Define the target directory for uploaded files
        self.target_directory = "corpus"
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)

    def perform_search(self):
        # Clear the current contents of the listbox and detail text
        self.results_listbox.delete(0, tk.END)
        self.detail_text.delete("1.0", tk.END)

        # Get the search query from the entry widget
        query = self.search_entry.get()

        if query:
            self.status_bar.config(text=f"Searching for {query}...")

            # Perform search operations here using the provided functions
            results = QueryProcessor(query).process_results()
            # Insert the search results into the listbox
            for result in results:
                result_title = result["title"].ljust(70)
                
                self.results_listbox.insert(tk.END,result_title)
            # Store the details for each result
            self.result_details = {result["title"]: result["content"] for result in results}
            # Update status bar
            self.status_bar.config(text=f"Found {len(results)} results for '{query}'")
        else:
            messagebox.showwarning("Input Error", "Please enter a search query")
            self.status_bar.config(text="Search query is empty. Please enter a query.")

    def show_details(self, event):
        # Get the selected result
        selected_index = self.results_listbox.curselection()
        if selected_index:
            selected_result = self.results_listbox.get(selected_index)
            details = self.result_details.get(selected_result, "No details available")
            self.detail_text.delete("1.0", tk.END)
            self.detail_text.insert(tk.END, details)

    def new_search(self):
        # Clear the search entry, listbox, and detail text
        self.search_entry.delete(0, tk.END)
        self.results_listbox.delete(0, tk.END)
        self.detail_text.delete("1.0", tk.END)
        self.status_bar.config(text="Ready for a new search")

    def show_about(self):
        # Show about dialog
        messagebox.showinfo("About", "SearchApp Version 1.0\n© 2024 AnnaanToo Search Engine Inc.")

    def drop(self, event):
        # Handle file drop event
        file_paths = self.root.tk.splitlist(event.data)
        for file_path in file_paths:
            print(file_path)
            self.process_file(file_path)
            self.status_bar.config(text=f"File '{file_path}' dropped")

    def upload_file(self):
        # Handle file upload event
        file_path = filedialog.askopenfilename()
        if file_path and file_path.endswith(".txt"):
            print(file_path)
            self.save_file(file_path)
            self.process_file(file_path)
            messagebox.YES
        else:
            messagebox.showerror("Invalid file format", "Please upload a text file.")

    def save_file(self, file_path):
        # Save the uploaded file to the corpus directory
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)

        uploaded_files = set()
        with open(r"indexed_file/Uploaded_file.txt") as f:
            uploaded_files = {line.strip()[14:-15] + ".txt" for line in f}

        base_name = os.path.basename(file_path)
        target_path = os.path.join(self.target_directory, base_name)

        # Check if the file has already been indexed before saving it to the corpus directory. If not, save it.
        if base_name not in uploaded_files:
            try: 
                shutil.copy(file_path, target_path)
                
            except Exception as e:
                messagebox.showwarning("Error occurred while saving file '{base_name}': {str(e)}")

        else:
            messagebox.showwarning("File Already Indexed", f"The file '{base_name}' has already been indexed.")
            self.status_bar.config(text=f"File '{base_name}' has already been indexed.")

        if base_name not in uploaded_files: 
            try:
                is_failed = not bool(StopWords(target_path))
                if is_failed:
                    messagebox.showwarning("Process Failed")
                else:
                    stemmed_file_path = f"Stemmed-words\\{base_name[:-4]}__stemmed__.txt"
                    Weights_TF_Matrix(stemmed_file_path)
                    self.status_bar.config(text=f"File '{base_name}' processed and weights updated.")
            except Exception as e:
                self.status_bar.config(text=f"Error occurred while processing file '{base_name}': {str(e)}")

    def process_file(self, file_path):
        # Perform specific operations on the dropped or uploaded file
        self.save_file(file_path)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SearchApp(root)
    root.mainloop()
