import time
from hash_engine import generate_sha256_hash

def run_dictionary_attack(target_hash: str, wordlist: list[str]) -> str | None:
    """
    Hashes each word in the wordlist and compares it against the target hash.
    """
    print(f"[*] Starting dictionary attack against hash: {target_hash[:16]}...")
    
    for attempt_count, word in enumerate(wordlist, start=1):
        # Generate hash for the current dictionary word
        attempt_hash = generate_sha256_hash(word)
        
        # Compare hashes
        if attempt_hash == target_hash:
            print(f"[+] Match found in {attempt_count} attempts!")
            return word
            
    print("[-] Dictionary exhausted. No match found.")
    return None

if __name__ == "__main__":
    # 1. Built-in small test wordlist
    test_dictionary = [
        "123456",
        "password",
        "admin",
        "qwerty",
        "letmein",
        "iloveyou",
        "secret123", # The target we will try to crack
        "monkey",
        "dragon"
    ]
    
    # 2. Setup the target (Simulating a stolen, hashed password)
    target_password = "secret123"
    print(f"Target Password: {target_password}")
    
    target_hash = generate_sha256_hash(target_password)
    print(f"Target Hash:     {target_hash}\n")
    
    # 3. Execute the dictionary attack
    start_time = time.time()
    cracked_password = run_dictionary_attack(target_hash, test_dictionary)
    end_time = time.time()
    
    # 4. Results
    if cracked_password:
        print(f"\n[!] SUCCESS! The cracked password is: '{cracked_password}'")
    else:
        print("\n[!] FAILED to crack the password.")
        
    print(f"[*] Time taken: {end_time - start_time:.5f} seconds")