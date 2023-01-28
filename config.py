from typing import Literal, List
from pydantic import BaseModel, Extra

# https://docs.go-cqhttp.org/cqcode/
CQ_TYPE = Literal[
    "face", "record", "video", "at", "share",
    "music", "image", "reply", "redbag", "poke",
    "gift", "forward", "node", "xml", "json",
    "cardimage", "tts",
    "plain"  # 纯文本
]


class Config:
    def __init__(
            self,
            listen_type: List["CQ_TYPE"] = None,
            listen_groups: List[int] = None,
            listen_users: List[int] = None,
            listen_content: List[str] = None,
            send_groups: List[int] = None
    ):
        """
        :param listen_type: 监听消息类型，为空则所有消息类型都监听
        :param listen_groups: 监听群，为空则所有群都监听
        :param listen_users: 监听用户，为空则所有用户都监听
        :param listen_content: 监听消息内容，为空则所有消息内容都监听
        :param send_groups: 发送群
        """
        self._listen_type = listen_type
        self._listen_groups = listen_groups
        self._listen_users = listen_users
        self._listen_content = listen_content
        self._send_groups = send_groups

        self._state = False
        self._msg_type = None
        
    @property
    def listen_type(self) -> List["CQ_TYPE"]:
        return self._listen_type
        
    @property
    def listen_groups(self) -> List[int]:
        return self._listen_groups
        
    @property
    def listen_users(self) -> List[int]:
        return self._listen_users

    @property
    def listen_content(self) -> List[str]:
        return self._listen_content

    @property
    def send_groups(self) -> List[int]:
        return self._send_groups

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, status: bool = False):
        self._state = status

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, type_: str = None):
        self._msg_type = type_


class ConfigContain:
    def __init__(self, *cfgs: Config):
        self._contains = list(cfgs)

    def __call__(self, cfg: Config):
        self._contains.append(cfg)

    @property
    def contains(self) -> List["Config"]:
        return self._contains


config = Config(
    listen_type=[],
    listen_groups=[533904524],
    listen_users=[],
    listen_content=[],
    send_groups=[310945892]
)
# config2 = Config([], [2376567356], [298587827], ["群主"], [427956626])


config_contain = ConfigContain(config)
# config_contain = ConfigContain(config, config2)


__all__ = [
    "Config",
    "ConfigContain",
    
    "config",
    "config_contain"
]
