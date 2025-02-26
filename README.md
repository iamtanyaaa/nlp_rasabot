# Recruitment bot using RASA framework

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contacts">Contacts</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Мы представляем чат-бота для автоматизации процесса рекрутмента, который помогает HR-специалистам собирать информацию о кандидатах, анализировать их опыт и принимать решения о дальнейшем взаимодействии. Чат-бот использует библиотеку Rasa для обработки естественного языка и управления диалогами, а также модели машинного обучения для анализа текстовых данных.

Чат-бот способен:
- Собирать информацию о кандидатах (имя, возраст, контактные данные, опыт работы, ожидания по зарплате).
- Анализировать опыт кандидата с использованием предобученных моделей (RuBERT) для сравнения с требованиями вакансии.
- Принимать решения о соответствии кандидата на основе анализа его опыта и ожиданий.

Стек решения: Python, Rasa, RuBERT, PyTorch, Transformers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

**Для запуска чат-бота**:

1. Установите необходимые зависимости:
   ```bash
   pip install rasa 
   ```
2. Инициализируйте проект с примерами:
   ```bash
   rasa init
  
3. Запустите сервер действий (actions server):
   ```bash
   rasa run actions
   ```
   
4. Обучите модель Rasa:
   ```bash
   rasa train
   ```

4. Начните диалог:
   ```bash
   rasa shell
   ```

### Структура проекта:

- **domain:**
  - `domain.yml` - описание всех компонентов бота.

- **data:**
  - `nlu.yml` - данные для обучения.
  - `stories.yml` - сценарии диалогов.
  - `rules.yml` - правила для управления диалогами.

- **actions:**
  - `actions.py` - пользовательские действия, в нашем случае анализ опыта и оценка кандидата.
 
- **best_jobs_descriptions:**
  - `*best_jobs_descriptions.json` - эмбеддинги для эталонных описаний кандидатов на разные роли

- **tests:**
  - `test_stories.yml` - примеры диалогов для тестирования.

- **models:**
  - Обученные модели.

- **config:**
  - `config.yml` - pipeline и политики для обучения и работы модели.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contacts

Project Link: [https://github.com/juliachirkova/nlp_rasabot](https://github.com/juliachirkova/nlp_rasabot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
