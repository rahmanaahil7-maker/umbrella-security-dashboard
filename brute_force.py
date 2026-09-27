import itertools
import time
from hash_engine import generate_sha256_hash

def run_brute_force(target_hash: str, charset: str, max_length: int):
    """
    Generates every possible combination of characters from the charset
    up to max_length and compares their hashes to the target.
    """
    print(f"[*] Starting brute force attack...")
    print(f"[*] Character set: '{charset}' | Max length: {max_length}")
    
    attempts = 0
    
    # Iterate through lengths 1 to max_length
    for length in range(1, max_length + 1):
        # Generate all possible combinations for the current length
        for guess_tuple in itertools.product(charset, repeat=length):
            attempts += 1
            
            # Join the tuple into a single string (e.g., ('a', 'b') -> 'ab')
            guess = ''.join(guess_tuple)
            guess_hash = generate_sha256_hash(guess)
            
            if guess_hash == target_hash:
                return guess, attempts
                
    return None, attempts

if __name__ == "__main__":
    # 1. Setup constraints for demonstration
    test_charset = "abc123"
    target_password = "c2"  # A short password within our constraints
    
    # 2. Setup the target hash
    target_hash = generate_sha256_hash(target_password)
    print(f"Target Password: {target_password}")
    print(f"Target Hash:     {target_hash}\n")
    
    # 3. Execute
    start_time = time.time()
    cracked_pw, total_attempts = run_brute_force(target_hash, test_charset, max_length=3)
    end_time = time.time()
    
    # 4. Results
    if cracked_pw:
        print(f"\n[+] SUCCESS! Password is: '{cracked_pw}'")
    else:
        print("\n[-] Brute force exhausted. No match found.")
        
    print(f"[*] Attempts: {total_attempts} | Time: {end_time - start_time:.4f}s")