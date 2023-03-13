
import openai
from configs import *
import os

MODEL = OpenaiAccount.MODEL
openai.api_key = OpenaiAccount.OPENAI_API


class AskChatGPT():
    '''
        处理接受到的消息，向ChatGPT发送请求，并保存请求回复
    '''

    def __init__(self, persona):
        self.persona = persona
        self.background = Persona.background[persona]  # 人格背景
        self.user_history = []  # 记录聊天记录
        self.prompt = []

    def create_user_content(self, message):
        return {"role": "user", "content": message}

    def create_assistant_content(self, message):
        return {"role": "assistant", "content": message}

    def storage_user_content(self, message):
        self.user_history.append(self.create_user_content(message))

    def storage_assistant_content(self, message):
        self.user_history.append(self.create_assistant_content(message))

    def create_prompt(self):

        # 聊天记录超过30条，则从头开始删除
        if len(self.user_history) > 60:
            self.user_history = self.user_history[2:]

        self.prompt = self.background + self.user_history

    async def ask_chatgpt(self, message):

        # 接受消息，生成prompt
        self.storage_user_content(message)
        self.create_prompt()
        # print(self.prompt)

        # 向OpenAI发送请求
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=self.prompt
        )
        res = response['choices'][0]['message']['content'].replace('\n', '')

        # 保存请求回复
        self.storage_assistant_content(res)

        # 发送消息
        return res