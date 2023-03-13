import nonebot
from nonebot import logger, on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from configs import *
import os

'''
    使用"/person 人名"进行人格更改
'''

chat = on_command('/persona', priority = 1, block = True)

@chat.handle()
async def _(bot:Bot, event:Event):

    # 读取persona
    per = str(event.get_message())[9:].strip()

    if per in Persona.list:
        p_file = os.path.abspath(os.path.join(os.getcwd(), './persona'))

        with open(p_file, 'w') as p_f:
            p_f.write(per)

        p_f.close()
        reply = '--{} 人格切换成功--'.format(per)

    else:
        reply = '--无指定人格--\n--可支持人格：{}--'.format('、'.join(Persona.list))

    if reply:
        await chat.send(message=MessageSegment.text(reply))
    else:
        logger.info('【ERROR】')

