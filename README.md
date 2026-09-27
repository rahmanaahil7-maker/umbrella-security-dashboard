# 🛡️ Red Queen Cryptographic Resilience Engine
### Umbrella Corporation — Applied Cryptography Division

An enterprise-grade, high-end cybersecurity analytics dashboard themed around the **Umbrella Corporation**. This platform combines parallel processing, machine learning heuristics, multi-format hashing, and generative AI security audits into a unified, dark-themed operational interface.

> *"Our business is life itself."*

---

## 🚀 Key Features

* **Multi-Format Cryptographic Analysis:** Supports high-speed legacy hashes (`MD5`), standard cryptographic algorithms (`SHA-256`), and memory-hard adaptive hashing (`bcrypt`).
* **Multithreaded Parallel Engine:** Distributes brute-force and dictionary search spaces across concurrent worker threads to evaluate password resilience under load.
* **Machine Learning Predictability (Markov Model):** Calculates n-gram transition probabilities and perplexity scores to measure human predictability patterns in passwords.
* **Generative AI Heuristics (Google Gemini SDK):** Automated security vulnerability scoring with a seamless **offline heuristic fallback** to guarantee zero downtime during network or rate-limit anomalies.
* **Search-Space Visualization:** Interactive logarithmic trajectory charts powered by `Chart.js` illustrating exponential combinatorial explosion.
* **Role-Based Access Control (RBAC) & Guest Mode:** Secure session management via `Flask-Login`. Unauthenticated users operate in Guest Mode, while administrative and analyst accounts manage database audit logs.
* **Executive PDF Intelligence Export:** Compiles live telemetry, ML analysis, and cryptographic benchmarks into a downloadable professional security audit report.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask, SQLAlchemy, Flask-Login, Werkzeug
* **Engines:** Multithreading (`concurrent.futures`), `bcrypt`, `hashlib`, Custom Markov Chain Model, Google GenAI SDK
* **Reporting:** `fpdf` (Safe UTF-8 text sanitization)
* **Frontend:** HTML5, CSS3 (Custom Dark Cyberpunk Theme), Chart.js, JavaScript (Async Fetch API)

---

## ⚙️ Installation & Deployment

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/umbrella-security-dashboard.git](https://github.com/YOUR_USERNAME/umbrella-security-dashboard.git)
   cd umbrella-security-dashboard
