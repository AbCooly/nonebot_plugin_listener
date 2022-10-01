from nonebot.adapters.onebot.v11 import MessageEvent, Bot
from nonebot.plugin import on_message
from .config import contain, Config
from .log import logger
import re

configs = contain.get_contain()


# 规则检查
async def rule_checker(event: MessageEvent) -> bool:
    res = False
    for cf in configs:
        if group_checker(event, cf) and type_checker(event, cf) and qq_checker(event, cf):
            cf.state_true()
            res = True
    return res


# 检查类型
def type_checker(event: MessageEvent, cf: Config) -> bool:
    m = str(event.get_message())
    p = re.compile(r"CQ:(.*),")
    t = p.search(m)
    if t:
        t = t.group(1)
        cf.set_mg_type(t)   # 设置消息类型
    if not cf.ty:  # 不填返回true
        return True
    else:
        return t in cf.ty


# 检查群组
def group_checker(event: MessageEvent, cf: Config) -> bool:
    if not cf.obj:  # 未填返回true
        return True
    if event.message_type != "group":
        return False
    g = event.get_session_id().split('_')[1]
    return g in cf.obj


# 检查具体对象
def qq_checker(event: MessageEvent, cf: Config) -> bool:
    if not cf.qq:  # 未填返回true
        return True
    q = event.get_user_id()
    return q in cf.qq


listen = on_message(rule=rule_checker)


@listen.handle()
async def _(bot: Bot, event: MessageEvent):
    for cf in configs:
        # 判断这个config状态
        if cf.get_state():
            cf.state_false()
            for t in cf.sd:
                mg = event.get_message()
                if cf.get_mg_type() not in ["redbag"]:
                    if cf.get_mg_type() in ["record", "forward", "json"]:   # 转发不了,直接发送
                        await bot.send_group_msg(group_id=t, message=mg)
                    else:  # 转发消息
                        await bot.call_api("send_group_forward_msg", **{
                            "group_id": t,
                            "messages": {
                                "type": "node",
                                "data": {
                                    "id": event.message_id,
                                }
                            }})
                    logger.info(f"{event.get_session_id()}:{mg}")

                # 直接发送
                # await bot.send_group_msg(group_id=t, message=mg)

                # 发送消息节点
                # qq = event.get_user_id()
                # if cf.get_mg_type() in ["record", "forward", "json"]:
                #     await bot.send_group_msg(group_id=t, message=mg)
                # else:
                #     info = await bot.call_api("get_stranger_info", **{
                #         "user_id": qq
                #     })
                #     await bot.call_api("send_group_forward_msg", **{
                #         "group_id": t,
                #         "messages": {
                #             "type": "node",
                #             "data": {
                #                 "name": info["nickname"],
                #                 "uin": qq,
                #                 "content": mg
                #             }
                #         }})
