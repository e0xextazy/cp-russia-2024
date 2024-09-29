import logging
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from logger import file_handler, console_handler


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
    logger.info({'request_text': text})
    #
    # TODO: вставить модель
    #

    answer_data = {
        "answer": f"Какой-то ответ на вопрос {text}",
        "class_1": "some_class",
        "class_2": "some_class"
    }

    logger.info({'response_text': answer_data})

    response = Response(
        answer=answer_data['answer'],
        class_1=answer_data['class_1'],
        class_2=answer_data['class_2'],
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
