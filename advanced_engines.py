import hashlib
import bcrypt
import itertools
import time
import concurrent.futures

def generate_hash(password: str, algorithm: str = 'sha256') -> str:
    pw_bytes = password.encode('utf-8')
    if algorithm == 'bcrypt':
        return bcrypt.hashpw(pw_bytes, bcrypt.gensalt(rounds=10)).decode('utf-8')
    elif algorithm == 'md5':
        return hashlib.md5(pw_bytes).hexdigest()
    else:
        return hashlib.sha256(pw_bytes).hexdigest()

def verify_hash(candidate: str, target_hash: str, algorithm: str) -> bool:
    if algorithm == 'bcrypt':
        try:
            return bcrypt.checkpw(candidate.encode('utf-8'), target_hash.encode('utf-8'))
        except Exception:
            return False
    return generate_hash(candidate, algorithm) == target_hash

def _search_chunk(target_hash: str, charset: str, length: int, algorithm: str, start_char: str):
    for combo in itertools.product(charset, repeat=length - 1):
        candidate = start_char + ''.join(combo)
        if verify_hash(candidate, target_hash, algorithm):
            return candidate
    return None

def parallel_brute_force(target_hash: str, charset: str, max_length: int, algorithm: str, max_workers: int = 4):
    start_time = time.time()
    total_attempts = 0
    found_password = None

    for length in range(1, max_length + 1):
        total_attempts += len(charset) ** length
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_char = {
                executor.submit(_search_chunk, target_hash, charset, length, algorithm, c): c
                for c in charset
            }
            for future in concurrent.futures.as_completed(future_to_char):
                result = future.result()
                if result:
                    found_password = result
                    break
        if found_password:
            break

    elapsed = max(time.time() - start_time, 0.00001)
    return found_password, elapsed, total_attempts

def run_experimental_benchmark(test_password="abc"):
    """Compares the computational latency and throughput of different hash formats."""
    algorithms = ['md5', 'sha256', 'bcrypt']
    results = {}
    
    for algo in algorithms:
        target = generate_hash(test_password, algo)
        start = time.time()
        for i in range(100 if algo != 'bcrypt' else 3):
            verify_hash(test_password, target, algo)
        duration = time.time() - start
        ops = (100 if algo != 'bcrypt' else 3) / duration
        results[algo] = {"time_sec": round(duration, 4), "hashes_per_sec": round(ops, 1)}
        
    return results