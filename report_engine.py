import datetime
from fpdf import FPDF

def sanitize_text(text) -> str:
    """Ensures text is a string and safe for standard FPDF Latin-1 fonts."""
    if text is None: 
        return ""
    text = str(text)
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "…": "..."
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    return text.encode('latin-1', 'replace').decode('latin-1')

class ExecutiveSecurityReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, 'UMBRELLA CORP: SECURITY INTEL REPORT', border=0, ln=1, align='C')
        self.set_font('Arial', 'I', 9)
        self.cell(0, 5, 'Automated Resilience Audit & Cryptographic Research Comparison', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, ln=0, align='C')

def generate_pdf_report(password: str, ai_data: dict, bench_data: dict, ml_data: dict, filepath="security_report.pdf"):
    pdf = ExecutiveSecurityReport()
    pdf.add_page()
    
    # 1. Audit Metadata
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, "1. Target Audit Metadata", border=0, ln=1)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, f"Audit Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", border=0, ln=1)
    pdf.cell(0, 5, f"Target Payload: {sanitize_text(password)}", border=0, ln=1)
    pdf.cell(0, 5, f"Protocol Tested: {bench_data.get('algorithm', 'sha256').upper()}", border=0, ln=1)
    pdf.cell(0, 5, f"Calculated Entropy: {bench_data.get('entropy', 0.0)} bits", border=0, ln=1)
    pdf.ln(3)

    # 2. Heuristics & ML Evaluation
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, "2. Red Queen Heuristic & Machine Learning Evaluation", border=0, ln=1)
    pdf.set_font('Arial', '', 9)
    pdf.cell(0, 5, f"Analysis Mode: {sanitize_text(ai_data.get('engine_mode', 'Local'))}", border=0, ln=1)
    pdf.cell(0, 5, f"Markov Perplexity: {ml_data.get('perplexity', 'N/A')} ({sanitize_text(ml_data.get('risk_level', 'N/A'))})", border=0, ln=1)
    pdf.cell(0, 5, f"Threat Level: {ai_data.get('vulnerability_score', 'N/A')}/10", border=0, ln=1)
    
    for weakness in ai_data.get('identified_weaknesses', []):
        pdf.cell(0, 5, f"- {sanitize_text(weakness)}", border=0, ln=1)
        
    rec = sanitize_text(ai_data.get('expert_recommendation', 'Maintain strict passphrase rotation.'))
    pdf.multi_cell(0, 5, f"Directive: {rec}")
    pdf.ln(3)

    # 3. Research Baseline Comparison Table
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, "3. Attack Latency Benchmark vs. Academic Baselines", border=0, ln=1)
    
    # Table Header
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(45, 6, "Hardware Infrastructure", border=1, ln=0)
    pdf.cell(30, 6, "Protocol", border=1, ln=0)
    pdf.cell(45, 6, "Measured Throughput", border=1, ln=0)
    pdf.cell(45, 6, "Est. 8-Char Exhaustion", border=1, ln=1)

    # Table Body
    pdf.set_font('Arial', '', 8)
    rows = [
        ("Active Hive Node (Local)", bench_data.get('algorithm', 'sha256').upper(), f"{bench_data.get('hash_rate', 0):,} h/s", "Real-Time Log"),
        ("Standard CPU Core", "MD5", "~4.5 MH/s", "~1.4 Days"),
        ("Dedicated GPU Array", "SHA-256", "28.5 GH/s", "~3.4 Minutes"),
        ("Dedicated GPU Array", "bcrypt (Cost 10)", "125 kH/s", "~530 Years"),
    ]
    for r in rows:
        pdf.cell(45, 6, r[0], border=1, ln=0)
        pdf.cell(30, 6, r[1], border=1, ln=0)
        pdf.cell(45, 6, r[2], border=1, ln=0)
        pdf.cell(45, 6, r[3], border=1, ln=1)

    pdf.output(filepath)
    return filepath