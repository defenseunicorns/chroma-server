import sys
from fastapi import FastAPI, Request, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import uvicorn
from document_store import DocumentStore

import os

debug = False

app = FastAPI()

doc_store = DocumentStore()
doc_store.load_pdf("./data/")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryModel(BaseModel):
    input: str
    collection_name: str

@app.post("/upload/")
async def upload(file: UploadFile):
    try:
        debug("Received file: " + file.filename)
        contents = await file.read()
        file_path = "files/" + file.filename
        if not os.path.isfile(file_path):
            new_file = open(file_path, "xb")
            new_file.write(contents)
        doc_store.ingestor.process_file(file_path)
        os.remove(file_path)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error uploading the file',
        )
    finally:
        await file.close()

    return {"filename": file.filename,
            "succeed": True}



@app.post("/query/")
def query(query_data: QueryModel):
    debug("Query received")
    outside_context = doc_store.query(query_data.input, query_data.collection_name)
    debug("The returned context is: " + outside_context)
    return {"results": outside_context}

@app.get("/health/", status_code=200)
def health():
    return {}

def debug(message):
    if debug:
        print(message)

if __name__ == '__main__':
    args = sys.argv[1:]

    if args[0] == "debug":
        debug = True

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug")
