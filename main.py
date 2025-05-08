from fastapi import FastAPI, File, UploadFile
from docx import Document

app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Book Report Grader API'}

@app.post('/grade_report')
async def grade_report(file: UploadFile = File(...)):
    if file.filename.endswith('.docx'):
        document = Document(file.file)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        return {'text': text}
    else:
        return {'error': 'File must be a .docx file'}
