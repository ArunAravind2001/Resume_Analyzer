from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import requests
import uvicorn
import os
from io import BytesIO
from fastapi import Form
from analyze import convert_to_text,analyze

class getjobdesc(BaseModel):
    description: str


app=FastAPI()
@app.post("/analyze/")
async def results(file:UploadFile, description: str=Form(...)):
    file_bytes = await file.read()
    pdf_text=convert_to_text(BytesIO(file_bytes))
    result = analyze(pdf_text, description)
    return {"analysis_result": result}


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
        
        

    


