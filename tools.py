def file_reader_tool(file_path: str) -> str:
    """
    පහත ගොනුව (txt) කියවා එහි අන්තර්ගතය ලබා දෙයි. [cite: 26]
    
    Args:
        file_path (str): කියවිය යුතු ගොනුවේ මාර්ගය (Path).
        
    Returns:
        str: ගොනුවේ ඇති සම්පූර්ණ පෙළ (text).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"