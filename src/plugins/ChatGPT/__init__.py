import nonebot
from nonebot import logger, on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from . import AskChatGPT
import os

chat = on_message(priority = 2)

user_history = {}

@chat.handle()
async def _(bot:Bot, event:MessageEvent):

    # 查询人格配置
    p_file = os.path.abspath(os.path.join(os.getcwd(), './persona'))
    persona = open(p_file, 'r').read()

    # 对方QQ号
    user_id = str(event.get_user_id())

    # 对不同的QQ号，单独记录聊天记录，如果人格更改，则删除重建
    if user_id in user_history.keys():
        ask = user_history[user_id]
        if ask.persona != persona:
            user_history[user_id] = AskChatGPT.AskChatGPT(persona)
            ask = user_history[user_id]
    else:
        user_history[user_id] = AskChatGPT.AskChatGPT(persona)
        ask = user_history[user_id]

    msg = str(event.get_message()).strip()

    reply = await ask.ask_chatgpt(msg)

    if reply:
        await chat.send(message=MessageSegment.text(reply))
    else:
        logger.info('【ERROR】')

