def file_reader_tool(file_path: str) -> str:
    """
    Reads the following file (txt) and returns its content.
    
    Args:
        file_path (str): The path of the file to be read.
        
    Returns:
        str: The full text content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"