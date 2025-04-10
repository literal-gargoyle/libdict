import sys
import os
import tkinter as tk


try:
    import PyPDF2
except ModuleNotFoundError:
    print("Installing PyPDF2...")
    sys.stdout.flush()
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
    import PyPDF2

from gui import VocabApp

def main():
    """
    Main entry point for the Vocabulary Flashcard Application.
    Initializes and runs the Tkinter GUI.
    Makes sure the PyPDF2 library is installed.

    - literal-gargoyle
    """

    root = tk.Tk()
    root.title("libdict")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Make sure window is resizable
    root.resizable(True, True)
    
    # Set the application icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets\images\icons\icon.ico")  # Replace with your .ico file name
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        print(f"Icon file not found: {icon_path}")

    # Initialize the application
    app = VocabApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()