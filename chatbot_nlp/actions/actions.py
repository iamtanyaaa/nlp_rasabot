from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from gensim.models import KeyedVectors
import numpy as np

class ActionEvaluateCandidate(Action):
    def name(self) -> Text:
        return "action_evaluate_candidate"

    def __init__(self):
        # Загрузка предобученной модели Word2Vec (например, из файла)
        self.word2vec_model = KeyedVectors.load_word2vec_format("cc.ru.300.vec")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Получаем слоты
        name = tracker.get_slot("name")
        age = int(tracker.get_slot("age"))
        role = tracker.get_slot("role")
        experience_role = tracker.get_slot("experience_role")
        experience_years = int(tracker.get_slot("experience_years"))
        skills = tracker.get_slot("skills")
        salary = int(tracker.get_slot("salary"))

        # Проверка возраста
        if age and age < 18:
            dispatcher.utter_message(text="К сожалению, мы нанимаем сотрудников только с 18 лет.")
            return []

        # Логика оценки кандидата
        evaluation_result = self.evaluate_candidate(role, experience_role, experience_years, skills, salary)

        # Формируем ответ
        if evaluation_result["fit"]:
            dispatcher.utter_message(text=f"{name}, вы подходите на роль {role}. {evaluation_result['message']}")
        else:
            dispatcher.utter_message(text=f"{name}, к сожалению, вы не подходите на роль {role}. {evaluation_result['message']}")

        return []

    def evaluate_candidate(self, role: Text, experience_role: Text, experience_years: float, skills: Text, salary: float) -> Dict[Text, Any]:
        """
        Оценивает кандидата на основе роли, опыта, навыков и зарплаты.
        Возвращает словарь с результатом оценки и сообщением.
        """
        result = {"fit": False, "message": ""}

        # Базовые требования для каждой роли
        role_requirements = {
            "data scientist": {
                "min_experience": 2,
                "required_skills": ["python", "sql", "машинное обучение"],
                "salary_range": [80000, 150000],
                "related_experience": ["анализ данных", "ml", "искусственный интеллект"]
            },
            "data engineer": {
                "min_experience": 3,
                "required_skills": ["python", "sql", "etl", "большие данные"],
                "salary_range": [70000, 130000],
                "related_experience": ["разработка данных", "базы данных", "инфраструктура данных"]
            },
            "data analyst": {
                "min_experience": 1,
                "required_skills": ["sql", "аналитика", "статистика"],
                "salary_range": [50000, 100000],
                "related_experience": ["анализ данных", "визуализация данных", "отчетность"]
            },
            "project manager": {
                "min_experience": 5,
                "required_skills": ["управление проектами", "коммуникация"],
                "salary_range": [90000, 160000],
                "related_experience": ["управление командами", "планирование", "бюджетирование"]
            },
            "mlops engineer": {
                "min_experience": 2,
                "required_skills": ["devops", "ci/cd", "машинное обучение"],
                "salary_range": [85000, 140000],
                "related_experience": ["ML-инфраструктура", "автоматизация", "контейнеризация"]
            }
        }

        # Проверка, что роль существует в требованиях
        if role not in role_requirements:
            result["message"] = "У нас нет такой роли."
            return result

        requirements = role_requirements[role]

        # Проверка опыта работы
        if experience_years < requirements["min_experience"]:
            result["message"] = f"Для этой роли требуется минимум {requirements['min_experience']} лет опыта."
            return result

        # Проверка зарплаты
        if salary and (salary < requirements["salary_range"][0] or salary > requirements["salary_range"][1]):
            result["message"] = f"Ваши ожидания по зарплате не соответствуют нашему диапазону: {requirements['salary_range'][0]} - {requirements['salary_range'][1]} рублей."
            return result

        # Проверка навыков
        if skills:
            similarity_score = self.calculate_similarity(skills, requirements["required_skills"])
            if similarity_score < 0.5:  # Порог схожести
                result["message"] = "Вам не хватает навыков."
                return result

        # Проверка опыта работы с использованием ML
        if experience_role:
            similarity_score = self.calculate_similarity(experience_role, requirements["related_experience"])
            if similarity_score < 0.5:  # Порог схожести
                result["message"] = "Ваш опыт работы не соответствует требованиям роли."
                return result

        # Если все проверки пройдены
        result["fit"] = True
        result["message"] = "Скоро с вами свяжется HR для назначения собеседования."
        return result

    def calculate_similarity(self, text: Text, role_requirements: List[Text]) -> float:
        """
        Вычисляет семантическую близость между текстом опыта кандидата и списком связанного опыта.
        Использует модель Word2Vec для оценки схожести.
        """
        text_tokens = text.lower().split()
        max_similarity = 0.0

        for exp in role_requirements:
            exp_tokens = exp.lower().split()
            similarity = self.word2vec_model.n_similarity(text_tokens, exp_tokens)
            if similarity > max_similarity:
                max_similarity = similarity

        return max_similarity


PS C:\Users\olegt\Downloads\Telegram Desktop\chatbot_nlp> git remote remove origin
PS C:\Users\olegt\Downloads\Telegram Desktop\chatbot_nlp> Remove-Item -Recurse -Force .git
