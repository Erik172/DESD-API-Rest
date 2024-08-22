import random
import string
from datetime import datetime

def generate_text(name_length: int = 6) -> str:
    """
    Generate a random string of lowercase letters.

    Parameters:
        name_length (int): The length of the generated string. Default is 6.

    Returns:
        str: The randomly generated string.

    Example:
        >>> generate_text(4)
        'abcd'
    """
    return ''.join(random.choices(string.ascii_lowercase, k=name_length))

from datetime import datetime

def generate_id(name_length: int = 6) -> str:
    """
    Generates a unique ID by combining a generated text and the current datetime.

    Args:
        name_length (int): The length of the generated text. Default is 6.

    Returns:
        str: The generated ID in the format "{generated_text}_{current_datetime}".
    """
    return f"{generate_text(name_length)}_{datetime.now().strftime('%Y.%m.%d-%H.%M.%S')}"