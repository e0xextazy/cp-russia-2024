from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


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

    #
    # TODO: вставить модель
    #

    answer_data = {
        "answer": f"Какой-то ответ на вопрос '{text}'",
        "class_1": "some_class",
        "class_2": "some_class"
    }

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
