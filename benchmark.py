import time
import itertools
from hash_engine import generate_sha256_hash

def run_benchmark(target_hash: str, charset: str, max_length: int):
    """
    Runs a brute force attack and calculates performance metrics.
    """
    print(f"[*] Benchmarking SHA-256 Brute Force...")
    print(f"[*] Charset: a-z (lowercase) | Max length: {max_length}\n")
    
    start_time = time.time()
    attempts = 0
    match_found = None
    
    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(charset, repeat=length):
            attempts += 1
            guess = ''.join(guess_tuple)
            
            if generate_sha256_hash(guess) == target_hash:
                match_found = guess
                break 
                
        if match_found:
            break
            
    end_time = time.time()
    
    # Calculate metrics
    elapsed_time = end_time - start_time
    speed = attempts / elapsed_time if elapsed_time > 0 else 0
    
    # Print Dashboard
    print("========== BENCHMARK RESULTS ==========")
    print(f"Status:       {'Match Found' if match_found else 'Exhausted'}")
    if match_found:
        print(f"Password:     {match_found}")
    print(f"Total Time:   {elapsed_time:.4f} seconds")
    print(f"Attempts:     {attempts:,}")
    print(f"Speed:        {speed:,.0f} hashes / second")
    print("=======================================")

if __name__ == "__main__":
    # We will use the full lowercase alphabet. 
    # Target "zzz" forces the script to test every combination up to 3 characters.
    full_charset = "abcdefghijklmnopqrstuvwxyz"
    target_password = "zzz" 
    target_hash = generate_sha256_hash(target_password)
    
    run_benchmark(target_hash, full_charset, max_length=3)