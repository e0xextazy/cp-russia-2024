import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class Request(BaseModel):
    question: str


class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str


app = FastAPI()


@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}


@app.post("/predict")
async def predict_sentiment(request: Request):
    answer_data = {
        "answer": "Какой-то ответ",
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
    host = "0.0.0.0"  # Сконфигурируйте host согласно настройкам вашего сервера.
    config = uvicorn.Config(app, host=host, port=8000)
    server = uvicorn.Server(config)
    loop = asyncio.get_running_loop()
    loop.create_task(server.serve())
