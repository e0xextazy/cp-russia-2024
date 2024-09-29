import logging
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from logger import file_handler, console_handler


from model import get_predicts


logger = logging.getLogger('api')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


class Request(BaseModel):
    question: str


class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str


@app.post("/predict")
async def predict_sentiment(request: Request):
    text = request.question
    logger.info(f"Q: {text}")

    # TODO вставить RAG
    answer = f"Какой-то ответ на вопрос {text}"
    class1, class2 = get_predicts(text)

    logger.info(f"A: {answer}|{class1}|{class2}")

    response = Response(
        answer=answer,
        class_1=class1,
        class_2=class2,
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8975)
