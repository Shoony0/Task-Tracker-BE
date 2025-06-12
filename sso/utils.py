
import random
import string

def generate_random_string(length=32):
    """
    Utility function to generate a random alphanumeric string.

    The generated string includes uppercase letters, lowercase letters, and digits (a-z, A-Z, 0-9).

    Args:
        length (int, optional): Length of the generated string. Default is 32.

    Returns:
        str: A random alphanumeric string of the specified length.

    Example:
        >>> generate_random_string(16)
        'a8F2zX7bQpL1Ns9D'
    """
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(characters, k=length))
