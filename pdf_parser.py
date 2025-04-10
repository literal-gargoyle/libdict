import re
import json
import os
from PyPDF2 import PdfReader

class PDFParser:
    """
    Handles parsing of PDF files containing vocabulary lists
    and converts them to the .libdict format.
    """
    
    def __init__(self):
        # Define section patterns to identify different parts of the vocabulary
        self.section_patterns = {
            'nouns': r'^Nouns\s*:',
            'adjectives': r'^Adjectives\s*:',
            'adverbs': r'^Adverbs\s*:',
            'prepositions': r'^Preposition\s*s?\s*:',
            'conjunctions': r'^Conjunction\s*s?\s*:',
            'verbs': r'^Verbs\s*:'  # Keep verbs last to avoid false matches
        }
        
        # Pattern to match vocabulary entries - this will be more complex
        # and is handled in the _process_text method
        
    def parse_pdf(self, pdf_path):
        """
        Parse a PDF file to extract vocabulary entries.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: Parsed vocabulary data organized by sections
        """
        try:
            print(f"Starting to parse PDF: {pdf_path}")
            reader = PdfReader(pdf_path)
            text = ""
            
            # Extract text from all pages
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                print(f"Page {i+1} contains {len(page_text)} characters")
                text += page_text + "\n"
            
            result = self._process_text(text)
            
            # Print a summary of what was found
            total_entries = sum(len(entries) for entries in result.values())
            print(f"Found {total_entries} vocabulary entries:")
            for section, entries in result.items():
                print(f"  - {section}: {len(entries)} entries")
                
            return result
        except Exception as e:
            error_msg = f"Error parsing PDF: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
    
    def _process_text(self, text):
        """
        Process extracted text to identify vocabulary entries.
        
        Args:
            text (str): Extracted text from PDF
            
        Returns:
            dict: Organized vocabulary data
        """
        lines = text.split('\n')
        vocabulary = {
            'nouns': [],
            'adjectives': [],
            'verbs': [],
            'adverbs': [],
            'prepositions': [],
            'conjunctions': []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            section_found = False
            for section, pattern in self.section_patterns.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    current_section = section
                    section_found = True
                    print(f"Found section header: '{line}' -> {section}")
                    break
                    
            if section_found:
                continue
                
            # If we have an active section, try to parse vocabulary entries
            if current_section:
                # Remove multiple spaces and normalize the line
                line = re.sub(r'\s+', ' ', line)
                
                # Look for entries with Latin terms and English definitions
                # Split the line by spaces and look for potential term-definition pairs
                
                # Check for patterns based on the current section
                matched = False
                
                # Special pattern for adjectives (they often have multiple forms)
                if current_section == 'adjectives':
                    adj_match = re.search(r'^([^,]+),\s+([^,]+),\s+([^\s]+)\s+(.*)', line)
                    if adj_match:
                        masculine = adj_match.group(1).strip()
                        feminine = adj_match.group(2).strip()
                        neuter = adj_match.group(3).strip()
                        definition = adj_match.group(4).strip()
                        
                        # Format the term with all forms
                        latin_term = f"{masculine}, {feminine}, {neuter}"
                        
                        vocabulary[current_section].append({
                            'term': latin_term,
                            'definition': definition
                        })
                        matched = True
                
                # Special pattern for prepositions (they often have case information in parentheses)
                if current_section == 'prepositions' and not matched:
                    prep_match = re.search(r'^(\S+)\s+\((.*?)\)\s+(.*)', line)
                    if prep_match:
                        latin_term = prep_match.group(1).strip()
                        case_info = prep_match.group(2).strip()
                        definition = prep_match.group(3).strip()
                        
                        # Include the case information in the definition
                        full_definition = f"{definition} ({case_info})"
                        
                        vocabulary[current_section].append({
                            'term': latin_term,
                            'definition': full_definition
                        })
                        matched = True
                        
                # Special pattern for verbs (they often have present tense form in parentheses)
                if current_section == 'verbs' and not matched:
                    verb_match = re.search(r'^(\S+)\s+\((.*?)\)\s+(.*)', line)
                    if verb_match:
                        infinitive = verb_match.group(1).strip()
                        present_form = verb_match.group(2).strip()
                        definition = verb_match.group(3).strip()
                        
                        vocabulary[current_section].append({
                            'term': infinitive,
                            'definition': f"{definition} (present: {present_form})"
                        })
                        matched = True
                
                # Special pattern for nouns with gender information
                if current_section == 'nouns' and not matched:
                    # Format like: "avārus, avārī m. miser"
                    noun_match = re.search(r'^([^,]+(?:,\s*[^,]+)?)\s+(m\.|f\.|n\.|\[.*?\])\s+(.*)', line)
                    if noun_match:
                        latin_term = noun_match.group(1).strip()
                        gender_info = noun_match.group(2).strip()
                        definition = noun_match.group(3).strip()
                        
                        vocabulary[current_section].append({
                            'term': latin_term,
                            'definition': f"{definition} ({gender_info})"
                        })
                        matched = True
                
                # Generic pattern for any other entries with grammatical info
                if not matched:
                    term_match = re.search(r'^([^,]+(?:,\s*[^,]+)?)\s+(?:m\.|f\.|n\.|adj\.|adv\.|v\.|prep\.|\[.*?\])?\s+(.*)', line)
                    
                    if term_match:
                        latin_term = term_match.group(1).strip()
                        definition = term_match.group(2).strip()
                        
                        vocabulary[current_section].append({
                            'term': latin_term,
                            'definition': definition
                        })
                        matched = True
                
                # Fallback pattern for simpler entries (like adverbs)
                if not matched:
                    parts = line.split(maxsplit=1)
                    if len(parts) >= 2:
                        latin_term = parts[0].strip()
                        definition = parts[1].strip()
                        
                        vocabulary[current_section].append({
                            'term': latin_term,
                            'definition': definition
                        })
        
        return vocabulary
    
    def save_to_libdict(self, vocabulary, output_path):
        """
        Save parsed vocabulary to a .libdict file (JSON format).
        
        Args:
            vocabulary (dict): Parsed vocabulary data
            output_path (str): Path to save the .libdict file
            
        Returns:
            str: Path to the saved file
        """
        # Ensure the output path has the .libdict extension
        if not output_path.endswith('.libdict'):
            output_path += '.libdict'
            
        # Prepare data for saving
        data = {
            'format_version': '1.0',
            'title': os.path.basename(output_path).replace('.libdict', ''),
            'sections': vocabulary
        }
        
        # Save to JSON file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return output_path
        except Exception as e:
            raise Exception(f"Error saving .libdict file: {str(e)}")
