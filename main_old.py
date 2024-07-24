from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import PyPDF2
import re
import random
from collections import Counter

app = FastAPI()

class Flashcard(BaseModel):
    question: str
    answer: str

def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

def extract_key_phrases(text, num_phrases=20):
    words = preprocess_text(text).split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_phrases) if len(word) > 3]

def create_question(sentence, key_phrase):
    # Replace the key phrase with a blank in the sentence
    question = re.sub(r'\b' + re.escape(key_phrase) + r'\b', '________', sentence, flags=re.IGNORECASE)
    return f"Fill in the blank: {question}"

@app.post("/create_flashcards/", response_model=List[Flashcard])
async def create_flashcards(file: UploadFile = File(...)):
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Extract key phrases
    key_phrases = extract_key_phrases(text)

    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Create flashcards
    flashcards = []
    for sentence in sentences:
        for phrase in key_phrases:
            if phrase in sentence.lower():
                question = create_question(sentence, phrase)
                answer = phrase
                flashcards.append(Flashcard(question=question, answer=answer))
                break  # Move to the next sentence after creating a flashcard

    # Shuffle and limit the number of flashcards
    random.shuffle(flashcards)
    return flashcards[:10]  # Return the first 10 flashcards

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)