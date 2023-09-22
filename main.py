from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from document_store import DocumentStore

import os

app = FastAPI()

doc_store = DocumentStore()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file: UploadFile):
    print(file.filename)
    contents = await file.read()
    file_path = "files/" + file.filename
    if not os.path.isfile(file_path):
        new_file = open(file_path, "xb")
        new_file.write(contents)
    doc_store.ingestor.process_file(file_path)
    os.remove(file_path)
    return {"filename": file.filename,
            "succeed": True}

@app.post("/query/")
def query(input: str, collection_name: str):
    outside_context = doc_store.query(input, collection_name)
    return {"results": outside_context}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug")
