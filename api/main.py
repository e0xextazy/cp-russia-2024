import logging
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from logger import file_handler, console_handler


from model import get_predicts
from rag import rag


logger = logging.getLogger('api')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = FastAPI()


@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}


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

    class1, class2 = get_predicts(text)
    answer = rag.predict(text)

    answer_data = {
        "answer": answer,
        "class_1": class1,
        "class_2": class2
    }

    logger.info({'response_text': answer_data})

    response = Response(
        answer=answer_data['answer'],
        class_1=answer_data['class_1'],
        # Классификатор оценивается опционально; при отсутствии можно задать константное значение.
        class_2=answer_data['class_2'],
        # Классификатор оценивается опционально; при отсутствии можно задать константное значение.
    )
    return response


if __name__ == "__main__":
    # host = "0.0.0.0"
    host = "localhost"
    uvicorn.run(app, host=host, port=8000)
