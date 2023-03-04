import nonebot
from nonebot import logger, on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from . import askchat

chat = on_message()

@chat.handle()
async def _(bot:Bot, event:MessageEvent):

    msg = str(event.get_message()).strip()
    reply = await askchat.answer(msg)
    if reply:
        await chat.send(message=MessageSegment.text(reply))
    else:
        logger.info('【ERROR】')

# sixty = on_command("60s", aliases={"早报", "六十"}, priority=2, block=True)

# @sixty.handle()
# async def _(bot: Bot, event: MessageEvent):
#     img_url = (await askjson.get_url())
#     if img_url:
#         await sixty.send(message=MessageSegment.image(img_url["imageUrl"]))
#     else:
#         logger.info('获取时出现错误')