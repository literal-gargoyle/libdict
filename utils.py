import os

def center_window(window):
    """
    Center a tkinter window on the screen.
    
    Args:
        window: Tkinter window to center
    """
    window.update_idletasks()
    
    width = window.winfo_width()
    height = window.winfo_height()
    
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def get_default_save_directory():
    """
    Get the default directory for saving files.
    Typically returns the user's Desktop directory.
    
    Returns:
        str: Path to the default save directory
    """
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desktop):
        return desktop
    
    # Fallback to home directory if Desktop doesn't exist
    return os.path.expanduser("~")

def validate_file_extension(file_path, expected_ext):
    """
    Validate that a file has the expected extension.
    Adds the extension if missing.
    
    Args:
        file_path (str): Path to check
        expected_ext (str): Expected extension (include dot, e.g. '.libdict')
        
    Returns:
        str: Path with correct extension
    """
    if not file_path.lower().endswith(expected_ext.lower()):
        return file_path + expected_ext
    return file_path

def extract_filename(file_path):
    """
    Extract just the filename without extension from a path.
    
    Args:
        file_path (str): Full file path
        
    Returns:
        str: Filename without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]
