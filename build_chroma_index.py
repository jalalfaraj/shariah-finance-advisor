#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 19:02:37 2025

@author: jalalfaraj
"""

import fitz  # PyMuPDF
import re
import chromadb
from chromadb.utils import embedding_functions

# === Step 1: Extract and clean PDF ===
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return re.sub(r'\s{2,}', ' ', text.strip())

# === Step 2: Chunk text ===
def chunk_text(text, max_length=500):
    sentences = text.split(". ")
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) < max_length:
            current += s + ". "
        else:
            chunks.append(current.strip())
            current = s + ". "
    if current:
        chunks.append(current.strip())
    return chunks

# === Step 3: Create Chroma Index using Persistent Client ===
def build_chroma_index(chunks):
    chroma_client = chromadb.PersistentClient(path="./chroma_db")  # ✅ NEW client
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    collection = chroma_client.get_or_create_collection(
        name="shariah_texts",
        embedding_function=embed_fn
    )

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"doc_{i}"]
        )

# === Execution ===
if __name__ == "__main__":
    pdf_path = "STOCKS AND SHARES.pdf"  # Ensure it's in the current directory
    raw_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(raw_text)
    build_chroma_index(chunks)
    print("✅ Chroma index successfully built.")
