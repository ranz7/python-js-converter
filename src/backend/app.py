from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import main

import pyflakes.api
import pyflakes.reporter
from io import StringIO

def check_python_code(code: str) -> str:
    output = StringIO()
    reporter = pyflakes.reporter.Reporter(output, output)
    
    pyflakes.api.check(code, '<input>', reporter)
    
    result = output.getvalue()
    return result

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


class ConvertCodeRequest(BaseModel):
    code: str

@app.post("/compile")
async def compile_code(code_request: ConvertCodeRequest):
    try:
        errors = check_python_code(code_request.code)
        if errors:
            print("Znaleziono błędy:")
            print(errors)
            return {"output_code": "", "error": errors}
        else:
            print("Kod jest poprawny")
            output_code = main(code_request.code)
            return {"output_code": output_code, "error": None}
    except Exception as e:
        return {"output_code": "", "error": str(e)}
