import json
import os
import random
import re

class FlashcardManager:
    """
    Manages flashcard data, loading and saving .libdict files,
    and handling flashcard navigation.
    """
    
    def _normalize_word(self, word):
        """
        Normalize a word by removing text in parentheses and trimming whitespace.
        
        Args:
            word (str): The word to normalize.
        
        Returns:
            str: The normalized word.
        """
        return re.sub(r'\s*\(.*?\)', '', word).strip().lower()

    def __init__(self):
        self.current_deck = None
        self.current_index = 0
        self.cards = []
        self.filtered_cards = []
        self.active_sections = {}  # Track which sections are active for study
        self.remove_on_correct = False  # New setting to remove cards on correct answer

    def set_remove_on_correct(self, value):
        """
        Enable or disable removing cards on correct answer.
        
        Args:
            value (bool): True to enable, False to disable
        """
        self.remove_on_correct = value

    def remove_current_card(self):
        """
        Remove the current card from the filtered cards and update the index.
        """
        if self.filtered_cards:
            del self.filtered_cards[self.current_index]
            if self.current_index >= len(self.filtered_cards):
                self.current_index = max(0, len(self.filtered_cards) - 1)
    
    def load_libdict(self, file_path):
        """
        Load a .libdict file and prepare flashcards for study.
        
        Args:
            file_path (str): Path to the .libdict file.
            
        Returns:
            bool: True if successfully loaded, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Store the deck information
            self.current_deck = {
                'title': data.get('title', os.path.basename(file_path)),
                'path': file_path,
                'format_version': data.get('format_version', '1.0')
            }
            
            # Reset cards list
            self.cards = []
            
            # Process sections
            sections = data.get('sections', {})
            self.active_sections = {}
            
            for section_name, items in sections.items():
                self.active_sections[section_name] = True  # Default all sections to active
                
                for item in items:
                    card = {
                        'term': self._normalize_word(item.get('term', '')),
                        'definition': self._normalize_word(item.get('definition', '')),
                        'section': section_name
                    }
                    self.cards.append(card)
            
            # Initialize with all sections active
            self._apply_filters()
            return True
        
        except Exception as e:
            print(f"Error loading .libdict file: {str(e)}")
            return False
    
    def _apply_filters(self):
        """
        Apply section filters to the cards list to create filtered_cards.
        """
        self.filtered_cards = [
            card for card in self.cards
            if self.active_sections.get(card['section'], True)
        ]
        
        # Reset the current index if needed
        if self.filtered_cards:
            self.current_index = min(self.current_index, len(self.filtered_cards) - 1)
        else:
            self.current_index = 0
    
    def toggle_section(self, section_name):
        """
        Toggle a section on/off for study.
        
        Args:
            section_name (str): Name of the section to toggle
            
        Returns:
            bool: New state of the section (True if active)
        """
        if section_name in self.active_sections:
            self.active_sections[section_name] = not self.active_sections[section_name]
            self._apply_filters()
            return self.active_sections[section_name]
        return False
    
    def get_section_names(self):
        """
        Get the names of all available sections.
        
        Returns:
            list: Names of all sections
        """
        return list(self.active_sections.keys())
    
    def get_section_status(self, section_name):
        """
        Get the active status of a section.
        
        Args:
            section_name (str): Name of the section
            
        Returns:
            bool: True if the section is active
        """
        return self.active_sections.get(section_name, False)
    
    def get_current_card(self):
        """
        Get the current flashcard.
        
        Returns:
            dict: Current flashcard data or None if no cards
        """
        if not self.filtered_cards:
            return None
        
        return self.filtered_cards[self.current_index]
    
    def next_card(self):
        """
        Move to the next flashcard.
        
        Returns:
            dict: New current flashcard or None if no cards
        """
        if not self.filtered_cards:
            return None
            
        self.current_index = (self.current_index + 1) % len(self.filtered_cards)
        return self.get_current_card()
    
    def previous_card(self):
        """
        Move to the previous flashcard.
        
        Returns:
            dict: New current flashcard or None if no cards
        """
        if not self.filtered_cards:
            return None
            
        self.current_index = (self.current_index - 1) % len(self.filtered_cards)
        return self.get_current_card()
    
    def shuffle_cards(self):
        """
        Shuffle the filtered cards.
        """
        if self.filtered_cards:
            random.shuffle(self.filtered_cards)
            self.current_index = 0
    
    def get_deck_info(self):
        """
        Get information about the current deck.
        
        Returns:
            dict: Deck information
        """
        result = {
            'title': 'No Deck Loaded',
            'card_count': 0,
            'filtered_count': 0
        }
        
        if self.current_deck:
            result['title'] = self.current_deck['title']
            result['card_count'] = len(self.cards)
            result['filtered_count'] = len(self.filtered_cards)
            
        return result
    
    def create_empty_libdict(self, title, output_path):
        """
        Create a new empty .libdict file.
        
        Args:
            title (str): Title for the new deck
            output_path (str): Path to save the file
            
        Returns:
            str: Path to the created file
        """
        # Ensure the output path has the .libdict extension
        if not output_path.endswith('.libdict'):
            output_path += '.libdict'
            
        data = {
            'format_version': '1.0',
            'title': title,
            'sections': {
                'nouns': [],
                'adjectives': [],
                'verbs': [],
                'adverbs': []
            }
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return output_path
        except Exception as e:
            raise Exception(f"Error creating .libdict file: {str(e)}")
