from typing import Dict, List

import os
import httpx
import time

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory

from src.prompts import custom_instructions, timecode_prompt
from src.app_config import MODEL_NAME, TEMPERATURE
    
class GeminiModel():
    """Получить доступ к модели OpenAI"""

    def __init__(self, api_key: str, llm_model: str) -> None:
        self.model = ChatGoogleGenerativeAI(
            model=llm_model,
            google_api_key=api_key,
            temperature=TEMPERATURE,
            safety_settings={
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )

    def invoke(self, prompt: ChatPromptTemplate) -> BaseMessage:
        prompt_messages = [SystemMessage(content=custom_instructions)] + prompt.messages
        response = self.model.invoke(prompt_messages)
        return response


class LoggerChatModel:
    """
    Класс для взаимодействия с языковой моделью (LLM) и логирования всех операций.
    Этот класс обрабатывает запросы к языковой модели, парсит и логирует ответы, а также обрабатывает
    возможные ошибки, такие как превышение лимита запросов или сетевые ошибки.
    """

    def __init__(self, llm: GeminiModel):
        self.llm = llm

    def __call__(self, messages: List[Dict[str, str]]) -> str:
        """
        Выполняем вызов LLM, обрабатываем ответ и логируем весь процесс.
        """
        # logger.debug(f"Вход в метод __call__ с сообщениями: {messages}")
        while True:
            try:
                reply = self.llm.invoke(messages)
                return reply

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.headers.get("retry-after")
                    retry_after_ms = e.response.headers.get("retry-after-ms")

                    if retry_after:
                        wait_time = int(retry_after)
                        time.sleep(wait_time)
                    elif retry_after_ms:
                        wait_time = int(retry_after_ms) / 1000.0
                        time.sleep(wait_time)
                    else:
                        wait_time = 30
                        time.sleep(wait_time)
                else:
                    time.sleep(30)


def create_timecodes(input_text: str, language: str) -> str:
    """
    Create timecodes for the YouTube video.

    Examples
    --------
    >>> timecodes = create_timecodes(video_text)
    >>> print(timecodes)
    '0:00 Intro
     0:10 Journeys
     0:25 Conclusion'
    """
    llm_api_key = os.getenv("LLM_API_KEY")
    prompt_template = ChatPromptTemplate.from_template(timecode_prompt)

    llm = GeminiModel(llm_api_key, MODEL_NAME)
    llm_cheap = LoggerChatModel(llm)
    chain = prompt_template | llm_cheap
    result = chain.invoke({
        "input_language": language, 
        "input_text": input_text, 
        })

    return result.content