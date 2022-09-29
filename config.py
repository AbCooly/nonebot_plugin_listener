# 配置文件

class Config:
    # 监视类型  不填-所有类型 forward-聊天记录 image-图片 record-语音 具体参考cq码 https://docs.go-cqhttp.org/cqcode/
    type = ["forward", "video"]
    # 监视群(不填-所有
    obj = ["427956626", "1234567"]
    # 具体对象(不填-所有
    qq = []
    # 发送群
    sd = ["1234567"]


config = Config()
