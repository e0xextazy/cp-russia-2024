# -*- coding: utf-8 -*-
import pandas as pd
from locust import HttpUser, task, between


df = pd.read_excel('case/02_Реальные_кейсы.xlsx')
questions = df['Вопрос пользователя'].tolist()


class ApiUser(HttpUser):
    wait_time = between(1, 10)  # Интервал между запросами
    q_i = 0

    @task
    def send_predict_request(self):
        payload = {
            "question": questions[self.q_i]
        }
        self.client.post("/predict", json=payload)
        self.q_i += 1

