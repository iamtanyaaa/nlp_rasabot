from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from gensim.models import KeyedVectors
import json
import torch
from scipy.spatial.distance import cosine
from transformers import AutoTokenizer, AutoModel
import numpy as np

# model.cuda()  # uncomment it if you have a GPU

class ActionEvaluateCandidate(Action):
    def name(self) -> Text:
        return "action_evaluate_candidate"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
        self.model = AutoModel.from_pretrained("cointegrated/rubert-tiny")
        with open('best_jobs_descriptions.json', 'r', encoding='utf-8') as f:
            self.best_job_descriptions = json.load(f)
        self.THRESHOLD = 0.05

    def embed_bert_cls(self, text, model, tokenizer):
        t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**{k: v.to(model.device) for k, v in t.items()})
        embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings[0].cpu().numpy()

    def get_embedding(self, job_title):
        # Проверяем, существует ли вакансия в файле
        if job_title in self.best_job_descriptions:
            # Извлекаем эмбеддинг и преобразуем его в numpy массив
            embed = np.array(self.best_job_descriptions[job_title]['embed'])
            return embed
        else:
            raise ValueError(f"Вакансия '{job_title}' не найдена в JSON файле.")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        age = int(tracker.get_slot("age"))
        role = tracker.get_slot("role").lower()
        experience_text = tracker.get_slot("experience")
        salary = int(tracker.get_slot("salary"))

        if age and age < 18:
            dispatcher.utter_message(text="К сожалению, мы нанимаем сотрудников только с 18 лет.")
            return []

        if salary > 300000:
            dispatcher.utter_message(text="К сожалению, мы не можем столько платить")

        evaluation_result = self.evaluate_candidate(role, experience_text)

        if evaluation_result["fit"]:
            dispatcher.utter_message(text=f"{name}, вы подходите на роль {role}. {evaluation_result['message']}")
        else:
            dispatcher.utter_message(text=f"{name}, к сожалению, вы не подходите на роль {role}. {evaluation_result['message']}")

        return []

    def evaluate_candidate(self, role: Text, experience_text: Text) -> Dict[Text, Any]:
        """
        Оценивает кандидата на основе роли, опыта, навыков и зарплаты.
        Возвращает словарь с результатом оценки и сообщением.
        """

        result = {"fit": False, "message": ""}
        if not experience_text:
            result["message"] = "Пожалуйста, расскажите подробнее о вашем опыте работы."
            return result

            # Проверка на краткость описания
        if len(experience_text.split()) < 10:
            result[
                "message"] = "Пожалуйста, опишите ваш опыт работы более подробно. Расскажите о ваших обязанностях и достижениях."
            return result

            # Анализ опыта

        d = {'project manager': 'PM', 'data analyst': 'DA', 'data engineer': 'DE', 'data scientist': 'DS',
             'mlops engineer': 'MLOPS'}
        job_title = d[role]

        best_embed = self.get_embedding(job_title)


        embed_from_candidate = self.embed_bert_cls(experience_text, self.model, self.tokenizer)

        if cosine(best_embed, embed_from_candidate) < self.THRESHOLD:
            result["fit"] = True
            result["message"] = "Скоро с вами свяжется HR для назначения собеседования."
            return result
        else:
            result["message"] = "Ваш опыт работы не соответствует требованиям роли."
            return result



        # Если мало ключевых слов о ролях и доменах
        # if len(experience_info["roles"]) + len(experience_info["domains"]) < 2:
        #     result["message"] = "Пожалуйста, расскажите подробнее о ваших должностях и сферах деятельности."
        #     return result

