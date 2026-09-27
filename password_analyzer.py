import math
import string
import re

def calculate_entropy(password: str) -> float:
    """Calculates password entropy in bits."""
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26
    if any(c.isupper() for c in password): pool_size += 26
    if any(c.isdigit() for c in password): pool_size += 10
    if any(c in string.punctuation for c in password): pool_size += len(string.punctuation)
    
    if pool_size == 0 or len(password) == 0:
        return 0.0
        
    return len(password) * math.log2(pool_size)

def analyze_password(password: str) -> dict:
    """Performs static analysis on the password structure."""
    analysis = {
        "password": password,
        "length": len(password),
        "has_lower": any(c.islower() for c in password),
        "has_upper": any(c.isupper() for c in password),
        "has_digit": any(c.isdigit() for c in password),
        "has_symbol": any(c in string.punctuation for c in password),
        "entropy": round(calculate_entropy(password), 2),
        "patterns_found": []
    }
    
    # Pattern Detection
    lower_pass = password.lower()
    common_sequences = ["123", "qwer", "pass", "abc", "admin"]
    
    for seq in common_sequences:
        if seq in lower_pass:
            analysis["patterns_found"].append(f"Common sequence '{seq}' detected")
            
    # Check for repeated characters (3 or more of the same character in a row)
    if re.search(r'(.)\1{2,}', password):
        analysis["patterns_found"].append("Repeated characters detected")
        
    return analysis

if __name__ == "__main__":
    test_passwords = ["password123", "Tr0ub4dour&3", "correcthorsebatterystaple"]
    
    print("========== PASSWORD ANALYSIS ==========")
    for pw in test_passwords:
        result = analyze_password(pw)
        print(f"\nTarget: {result['password']}")
        print(f"Length: {result['length']} | Entropy: {result['entropy']} bits")
        print(f"Classes: Upper:{result['has_upper']} | Lower:{result['has_lower']} | Num:{result['has_digit']} | Sym:{result['has_symbol']}")
        if result['patterns_found']:
            print(f"Flags:  {', '.join(result['patterns_found'])}")