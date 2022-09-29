from nonebot.adapters.onebot.v11 import MessageEvent, Bot
from nonebot.rule import Rule
from nonebot.plugin import on_message
from .config import config


# 检查类型
async def type_checker(event: MessageEvent) -> bool:
    if not config.type:     # 不填返回true
        return True
    m = str(event.get_message())
    for t in config.type:
        if t in m:
            return True
    return False


# 检查群组
async def group_checker(event: MessageEvent) -> bool:
    if not config.obj:   # 未填返回true
        return True
    g = event.get_session_id().split('_')[1]
    return g in config.obj


# 检查具体对象
async def qq_checker(event: MessageEvent) -> bool:
    if not config.qq:   # 未填返回true
        return True
    q = event.get_user_id()
    return q in config.qq


listen = on_message(rule=Rule(type_checker, group_checker, qq_checker))
@listen.handle()
async def _(bot: Bot, event: MessageEvent):
    for t in config.sd:
        await bot.send_group_msg(group_id=t, message=event.get_message())
