import ollama
from PyPDF2 import PdfReader

system_prompt="""
You are a resume-job match analyzer.

Given:
Resume:
{all_text}

Job Description:
{job_desc}

Return ONLY a valid JSON object in this exact format (no extra text, no explanations):

{{
  "match_percentage": "85%",
  "missing_skills": ["skill1", "skill2"],
  "suggested_projects": ["project1", "project2", "project3"]
}}

"""



def convert_to_text(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"
    return all_text

def analyze(all_text,job_desc):
    try:
        response = ollama.chat(
            model="mistral:latest",
            options={"temperature": 0.3},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Resume:\n{all_text}\n\nJob Description:\n{job_desc}"}
            ]
        )
        return response.get('message', {}).get('content', '').strip()
    except Exception as e:
        return f"❌ Ollama Error: {e}"