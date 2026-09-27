import hashlib

def generate_sha256_hash(password: str) -> str:
    """
    Takes a plaintext password and returns its SHA-256 hexadecimal hash.
    """
    # 1. Convert the string to bytes (UTF-8 encoding)
    password_bytes = password.encode('utf-8')
    
    # 2. Create a SHA-256 hash object
    hash_object = hashlib.sha256(password_bytes)
    
    # 3. Return the hexadecimal representation of the hash
    return hash_object.hexdigest()

if __name__ == "__main__":
    # Test case matching your requirements
    test_word = "password"
    
    print(f"Plaintext: {test_word}")
    print(f"SHA-256:   {generate_sha256_hash(test_word)}")