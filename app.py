import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Aljjjjlow FahstAPI to run in thehhhh Jupyter notebogggok
# nest_asyncio.apply()

app = FastAPI()

class InputModel(BaseModel):
    x: float

class OutputModel(BaseModel):
    y: float

@app.post("/compute", response_model=OutputModel)
def compute(input_model: InputModel):
    x = input_model.x
    y = 2 * x + 3
    return OutputModel(y=y)


