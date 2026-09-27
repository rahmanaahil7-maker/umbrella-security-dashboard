import os
import json
import re
from google import genai
from google.genai import types

def offline_fallback_analysis(password: str) -> dict:
    """Offline heuristic engine triggered when remote API is unavailable."""
    score = 10
    weaknesses = []
    
    if len(password) >= 12:
        score -= 3
    elif len(password) >= 8:
        score -= 1
    else:
        weaknesses.append("Length is critically under 8 characters.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score -= 2
    else:
        weaknesses.append("Lacks dual-case character variety.")

    if re.search(r"\d", password):
        score -= 2
    else:
        weaknesses.append("Missing numeric digits.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score -= 2
    else:
        weaknesses.append("Missing special symbols.")

    common_patterns = ["123", "password", "admin", "qwerty", "2024", "2025", "2026"]
    if any(p in password.lower() for p in common_patterns):
        score = min(10, score + 3)
        weaknesses.append("Contains identifiable dictionary word or predictable date sequence.")

    score = max(1, min(10, score))
    return {
        "vulnerability_score": score,
        "identified_weaknesses": weaknesses if weaknesses else ["No critical structural weaknesses detected."],
        "expert_recommendation": "Adopt a multi-word passphrase with high physical entropy and store it in an encrypted password manager.",
        "engine_mode": "Offline Heuristic Fallback (API Busy)"
    }

def run_ai_analysis(password: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return offline_fallback_analysis(password)

    client = genai.Client(api_key=api_key)
    prompt = f"""
    Analyze the dummy password '{password}'. Return ONLY a JSON object:
    {{
        "vulnerability_score": (int 1-10),
        "identified_weaknesses": ["list", "of", "strings"],
        "expert_recommendation": "string"
    }}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text)
        data["engine_mode"] = "Gemini Live AI"
        return data
    except Exception:
        # Seamless failover on 503 or quota limits
        return offline_fallback_analysis(password)