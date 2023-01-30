from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.plugin import on_message
from .log import logger
from .config import config_contain, Config
from .rule import rule_checker
from asyncio import sleep

CONFIGS = config_contain.contains
DANGER = {"xml", "cardimage"}  # xml, cardimage 易风控
MAPPING = {
    "record": "语音",
    "video": "视频",
    "music": "音乐",
    "json": "分享",
    "forward": "合并",
}

listen = on_message(rule=rule_checker)


@listen.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.message
    user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
    group_info = await bot.get_group_info(group_id=event.group_id)

    for cfg in CONFIGS:
        if not cfg.state:
            continue

        cfg.state = False
        for group in cfg.send_groups:
            if cfg.msg_type == "redbag":
                await bot.send_group_msg(
                    group_id=group,
                    message=f"!!!红包提醒!!! <{group_info['group_name']}({event.group_id})> [{user_info['nickname']}({event.user_id})]"
                )

            elif cfg.msg_type in DANGER:
                continue

            elif cfg.msg_type in MAPPING:
                await bot.send_group_msg(group_id=group, message=f"={MAPPING[cfg.msg_type]}消息= <{group_info['group_name']}({event.group_id})> [{user_info['nickname']}({event.user_id})]")
                await sleep(0.1)
                await bot.send_group_msg(group_id=group, message=msg)

            else:
                await bot.send_group_msg(
                    group_id=group,
                    message=f"<{group_info['group_name']}({event.group_id})> [{user_info['nickname']}({event.user_id})]:\n{msg}"
                )
            logger.info(f"{event.get_session_id()}: {msg}")

