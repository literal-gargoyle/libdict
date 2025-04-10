import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_parser import PDFParser
from flashcard_manager import FlashcardManager
from utils import center_window

class VocabApp:
    """
    Main application class for the Vocabulary Flashcard Study Tool.
    Manages the GUI interface and integrates the various components.
    """
    
    def __init__(self, root):
        self.root = root
        
        # Set app theme colors
        self.colors = {
            'primary': '#2C3E50',    # Navy blue
            'secondary': '#ECF0F1',  # Light grey
            'accent': '#E74C3C',     # Coral red
            'text': '#34495E'        # Dark grey
        }
        
        # Initialize components
        self.parser = PDFParser()
        self.manager = FlashcardManager()
        
        # Create main application UI
        self.setup_styles()
        self.create_ui()
        
        # Center the window on screen
        center_window(root)
        
    def setup_styles(self):
        """Configure ttk styles with our color scheme"""
        self.style = ttk.Style()
        
        # Configure common styles
        self.style.configure('TFrame', background=self.colors['secondary'])
        self.style.configure('TButton', 
                            background=self.colors['primary'],
                            foreground=self.colors['text'],  # Use text color
                            padding=10)
        self.style.configure('Accent.TButton',
                            background=self.colors['accent'],
                            foreground=self.colors['text'],  # Use text color
                            padding=10)
        self.style.configure('TLabel', 
                            background=self.colors['secondary'],
                            foreground=self.colors['text'],
                            font=('Helvetica', 10))
        self.style.configure('Header.TLabel', 
                            background=self.colors['primary'],
                            foreground='white',
                            font=('Helvetica', 14, 'bold'),
                            padding=10)
        self.style.configure('Title.TLabel', 
                            background=self.colors['secondary'],
                            foreground=self.colors['primary'],
                            font=('Helvetica', 18, 'bold'),
                            padding=5)
        
    def create_ui(self):
        """Create the main user interface"""
        # Configure the root window
        self.root.configure(bg=self.colors['secondary'])
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create the header
        header_frame = ttk.Frame(self.main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                  text="libdict - Vocabulary Flashcard Study Tool", 
                  style='Title.TLabel').pack(side=tk.LEFT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create converter tab
        self.converter_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.converter_tab, text="PDF Converter")
        self._create_converter_tab()
        
        # Create study tab
        self.study_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.study_tab, text="Flashcard Study")
        self._create_study_tab()
        
        # Create the status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_frame = ttk.Frame(self.main_frame, style='TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(status_frame, 
                  textvariable=self.status_var,
                  style='TLabel').pack(side=tk.LEFT)
    
    def _create_converter_tab(self):
        """Create the PDF to .libdict converter tab"""
        # Top section - Input file selection
        input_frame = ttk.Frame(self.converter_tab, style='TFrame')
        input_frame.pack(fill=tk.X, pady=10)
        input_frame.columnconfigure(1, weight=1)  # Make the entry column expandable
        
        ttk.Label(input_frame, 
                  text="Input PDF:", 
                  style='TLabel').grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.input_path_var = tk.StringVar()
        ttk.Entry(input_frame, 
                  textvariable=self.input_path_var).grid(row=0, column=1, padx=(0, 10), sticky="ew")
        
        ttk.Button(input_frame, 
                   text="Browse...", 
                   command=self.browse_input_file).grid(row=0, column=2, sticky="e")
        
        # Middle section - Output file selection
        output_frame = ttk.Frame(self.converter_tab, style='TFrame')
        output_frame.pack(fill=tk.X, pady=10)
        output_frame.columnconfigure(1, weight=1)  # Make the entry column expandable
        
        ttk.Label(output_frame, 
                  text="Output Location:", 
                  style='TLabel').grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, 
                  textvariable=self.output_path_var).grid(row=0, column=1, padx=(0, 10), sticky="ew")
        
        ttk.Button(output_frame,
                   text="Browse...", 
                   command=self.browse_output_location).grid(row=0, column=2, sticky="e")
        
        # Bottom section - Convert button
        button_frame = ttk.Frame(self.converter_tab, style='TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, 
                   text="Convert PDF to Flashcards", 
                   style='Accent.TButton',
                   command=self.convert_pdf).pack(pady=10)
        
        # Conversion status
        self.conversion_result_var = tk.StringVar()
        self.conversion_result_var.set("")
        
        ttk.Label(self.converter_tab, 
                  textvariable=self.conversion_result_var,
                  style='TLabel').pack(pady=10)
    
    def _create_study_tab(self):
        """Create the flashcard study tab"""
        # Top section - Load flashcards
        load_frame = ttk.Frame(self.study_tab, style='TFrame')
        load_frame.pack(fill=tk.X, pady=10)
        load_frame.columnconfigure(1, weight=1)  # Make the entry column expandable
        
        ttk.Label(load_frame, 
                  text="Flashcard File:", 
                  style='TLabel').grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.flashcard_path_var = tk.StringVar()
        ttk.Entry(load_frame, 
                  textvariable=self.flashcard_path_var).grid(row=0, column=1, padx=(0, 10), sticky="ew")
        
        ttk.Button(load_frame, 
                   text="Browse...", 
                   command=self.browse_flashcard_file).grid(row=0, column=2, padx=(0, 10), sticky="e")
        
        ttk.Button(load_frame, 
                   text="Load", 
                   command=self.load_flashcards).grid(row=0, column=3, sticky="e")
        self.remove_on_correct_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.study_tab, 
                        text="Remove card on correct answer",
                        variable=self.remove_on_correct_var,
                        command=self.toggle_remove_on_correct,
                        style='TCheckbutton').pack(anchor=tk.W, pady=(0, 10))
        # Section filters (only show when deck is loaded)
        self.filters_frame = ttk.Frame(self.study_tab, style='TFrame')
        self.filters_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.filters_frame, 
                  text="Show sections:", 
                  style='TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.section_vars = {}  # Will hold checkbutton variables
        self.section_buttons = {}  # Will hold checkbutton widgets
        
        # Flashcard display area
        self.deck_title_var = tk.StringVar()
        self.deck_title_var.set("No Deck Loaded")
        
        title_frame = ttk.Frame(self.study_tab, style='TFrame')
        title_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(title_frame, 
                  textvariable=self.deck_title_var,
                  style='Title.TLabel').pack(side=tk.LEFT)
        
        self.card_count_var = tk.StringVar()
        self.card_count_var.set("Cards: 0")
        ttk.Label(title_frame, 
                  textvariable=self.card_count_var,
                  style='TLabel').pack(side=tk.RIGHT)
        
        # Card display
        card_frame = ttk.Frame(self.study_tab, style='TFrame')
        card_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create the flashcard display
        self.flashcard_frame = tk.Frame(card_frame, 
                                      bg=self.colors['primary'],
                                      bd=2,
                                      relief=tk.RAISED)
        self.flashcard_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Make the flashcard and its labels clickable for flipping
        self.flashcard_frame.bind("<Button-1>", self.flip_card)
        self.flashcard_frame.bind("<Configure>", self.on_flashcard_resize)
        
        self.card_front = True  # Track which side is showing
        
        # Term (front of card)
        self.term_var = tk.StringVar()
        self.term_var.set("Click 'Load' to begin studying")
        
        self.term_label = tk.Label(self.flashcard_frame,
                                 textvariable=self.term_var,
                                 bg='white',
                                 fg=self.colors['text'],
                                 font=('Helvetica', 24),
                                 wraplength=400,
                                 cursor="hand2")  # Change cursor to indicate clickable
        self.term_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.term_label.bind("<Button-1>", self.flip_card)  # Bind click to term label
        
        # Definition (back of card) - hidden initially
        self.definition_var = tk.StringVar()
        self.definition_label = tk.Label(self.flashcard_frame,
                                       textvariable=self.definition_var,
                                       bg=self.colors['secondary'],
                                       fg=self.colors['text'],
                                       font=('Helvetica', 20),
                                       wraplength=400,
                                       cursor="hand2")  # Change cursor to indicate clickable
        self.definition_label.bind("<Button-1>", self.flip_card)  # Bind click to definition label
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.study_tab, style='TFrame')
        nav_frame.pack(fill=tk.X, pady=10)
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.columnconfigure(3, weight=1)
        
        self.answer_var = tk.StringVar()
        ttk.Entry(self.study_tab, 
                textvariable=self.answer_var).pack(fill=tk.X, pady=(10, 5))
        ttk.Button(self.study_tab, 
               text="Check Answer", 
               command=lambda: self.check_answer(self.answer_var.get())).pack(pady=(0, 10))
        ttk.Button(nav_frame, 
                   text="Previous", 
                   command=self.previous_card).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ttk.Button(nav_frame, 
                   text="Flip Card", 
                   command=lambda: self.flip_card(None)).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Button(nav_frame, 
                   text="Shuffle", 
                   command=self.shuffle_cards).grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        
        ttk.Button(nav_frame, 
                   text="Next", 
                   command=self.next_card).grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        # Instructions label
        ttk.Label(self.study_tab, 
                  text="Click on a card to flip it",
                  style='TLabel').pack(pady=(0, 10))
    
    def check_answer(self, user_input):
        """
        Check the user's input against the current card's term or definition.
        
        Args:
            user_input (str): The text entered by the user.
        """
        current_card = self.manager.get_current_card()
        if not current_card:
            return

        # Normalize the user's input and the card's term/definition
        normalized_input = self.manager._normalize_word(user_input)
        normalized_term = self.manager._normalize_word(current_card['term'])
        normalized_definition = self.manager._normalize_word(current_card['definition'])

        # Check if the input matches the term or definition
        if normalized_input in (normalized_term, normalized_definition):
            messagebox.showinfo("Correct!", "You answered correctly!")
            
            # Remove the card if the setting is enabled
            if self.manager.remove_on_correct:
                self.manager.remove_current_card()
            
            # Show the next card
            self.manager.next_card()
            self.show_current_card()
        else:
            messagebox.showerror("Incorrect", "Try again!")

    def toggle_remove_on_correct(self):
        """
        Toggle the 'Remove on Correct' setting in the FlashcardManager.
        """
        self.manager.set_remove_on_correct(self.remove_on_correct_var.get())
        
    # --- Converter tab methods ---
    
    def browse_input_file(self):
        """Open file dialog to select input PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.input_path_var.set(file_path)
            
            # Set a default output filename based on the input
            base_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(base_name)[0]
            
            # Suggest the desktop as the default save location
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            suggested_output = os.path.join(desktop, f"{name_without_ext}.libdict")
            self.output_path_var.set(suggested_output)
    
    def browse_output_location(self):
        """Open file dialog to select output location for .libdict file"""
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".libdict",
            filetypes=[("Flashcard Files", "*.libdict"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.output_path_var.set(file_path)
    
    def convert_pdf(self):
        """Convert PDF to .libdict flashcard format"""
        input_path = self.input_path_var.get().strip()
        output_path = self.output_path_var.get().strip()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input PDF file.")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output location.")
            return
        
        try:
            self.status_var.set("Converting PDF...")
            self.conversion_result_var.set("Processing...")
            self.root.update_idletasks()  # Force UI update
            
            # Parse the PDF
            vocabulary = self.parser.parse_pdf(input_path)
            
            # Save to .libdict format
            output_file = self.parser.save_to_libdict(vocabulary, output_path)
            
            # Update UI
            self.conversion_result_var.set(f"Conversion successful! File saved to:\n{output_file}")
            self.status_var.set("Ready")
            
            # Ask if user wants to study this file now
            if messagebox.askyesno("Conversion Complete", 
                                   "Would you like to study this flashcard deck now?"):
                self.flashcard_path_var.set(output_file)
                self.notebook.select(1)  # Switch to study tab
                self.load_flashcards()
                
        except Exception as e:
            self.conversion_result_var.set(f"Error: {str(e)}")
            self.status_var.set("Error during conversion")
            messagebox.showerror("Conversion Error", str(e))
    
    # --- Study tab methods ---
    
    def browse_flashcard_file(self):
        """Open file dialog to select .libdict file"""
        file_path = filedialog.askopenfilename(
            title="Select Flashcard File",
            filetypes=[("Flashcard Files", "*.libdict"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.flashcard_path_var.set(file_path)
    
    def load_flashcards(self):
        """Load flashcards from a .libdict file"""
        file_path = self.flashcard_path_var.get().strip()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a flashcard file.")
            return
        
        try:
            self.status_var.set("Loading flashcards...")
            self.root.update_idletasks()  # Force UI update
            
            # Load the flashcard file
            success = self.manager.load_libdict(file_path)
            
            if success:
                # Update deck info display
                deck_info = self.manager.get_deck_info()
                self.deck_title_var.set(deck_info['title'])
                self.card_count_var.set(f"Cards: {deck_info['filtered_count']}")
                
                # Reset the card display
                self.card_front = True
                self.show_current_card()
                
                # Update section filters
                self._update_section_filters()
                
                self.status_var.set("Flashcards loaded successfully")
            else:
                self.status_var.set("Error loading flashcards")
                messagebox.showerror("Load Error", "Failed to load flashcard file.")
                
        except Exception as e:
            self.status_var.set("Error loading flashcards")
            messagebox.showerror("Load Error", str(e))
    
    def _update_section_filters(self):
        """Update the section filter checkboxes based on loaded deck"""
        # Clear existing checkbuttons
        for widget in self.section_buttons.values():
            widget.destroy()
        
        self.section_vars.clear()
        self.section_buttons.clear()
        
        # Get sections from the loaded deck
        sections = self.manager.get_section_names()
        
        # Create new checkbuttons for each section
        for section in sections:
            var = tk.BooleanVar(value=self.manager.get_section_status(section))
            self.section_vars[section] = var
            
            # Capitalize section name for display
            display_name = section.capitalize()
            
            cb = ttk.Checkbutton(
                self.filters_frame, 
                text=display_name,
                variable=var,
                command=lambda s=section: self.toggle_section(s)
            )
            cb.pack(side=tk.LEFT, padx=(0, 10))
            self.section_buttons[section] = cb
    
    def toggle_section(self, section_name):
        """Toggle a section on/off and update the study cards"""
        if self.section_vars[section_name].get():
            # User checked the box
            self.manager.toggle_section(section_name)
        else:
            # User unchecked the box
            self.manager.toggle_section(section_name)
        
        # Update card display
        deck_info = self.manager.get_deck_info()
        self.card_count_var.set(f"Cards: {deck_info['filtered_count']}")
        self.show_current_card()
    
    def show_current_card(self):
        """Update the display with the current flashcard"""
        card = self.manager.get_current_card()
        
        if card:
            self.term_var.set(card['term'])
            self.definition_var.set(card['definition'])
            
            # Make sure we're showing the front
            if not self.card_front:
                self.flip_card(None)
        else:
            self.term_var.set("No cards available")
            self.definition_var.set("")
    
    def flip_card(self, event):
        """Flip the flashcard to show term or definition"""
        if self.card_front:
            # Switch to back (definition)
            self.term_label.pack_forget()
            self.definition_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            self.card_front = False
        else:
            # Switch to front (term)
            self.definition_label.pack_forget()
            self.term_label.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            self.card_front = True
    
    def next_card(self):
        """Move to the next flashcard"""
        self.manager.next_card()
        self.show_current_card()
    
    def previous_card(self):
        """Move to the previous flashcard"""
        self.manager.previous_card()
        self.show_current_card()
    
    def shuffle_cards(self):
        """Shuffle the flashcards"""
        self.manager.shuffle_cards()
        self.show_current_card()
        
    def on_flashcard_resize(self, event):
        """Adjust flashcard properties when the window is resized"""
        # Update the wraplength for both labels to match the new width
        # Leave a small margin on each side
        new_width = event.width - 20
        if new_width > 100:  # Ensure we don't get too small
            self.term_label.configure(wraplength=new_width)
            self.definition_label.configure(wraplength=new_width)
