from docx import Document
from openai import OpenAI
import os


def read_docx(file_path):
    try:
        document = Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        return text
    except Exception as e:
        return f"Error reading file: {e}"

def analyze_with_llm(text):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    with open('system_prompt.txt', 'r') as file:
        system_prompt = file.read()
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    file_path = 'Samples/Primary/2.docx'
    report_text = read_docx(file_path)
    analysis = analyze_with_llm(report_text)
    print("Finished Analysis")
    with open('output.txt', 'w') as file:
        file.write(analysis)
