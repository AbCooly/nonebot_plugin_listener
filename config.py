# 配置文件

class Config:
    def __init__(self, ty=None, obj=None, qq=None, sd=None):
        self.ty = ty
        self.obj = obj
        self.qq = qq
        self.sd = sd
        self.state = False
        self.mg_type = "None"

    def state_true(self):
        self.state = True

    def state_false(self):
        self.state = False

    def get_state(self):
        return self.state

    def set_mg_type(self, mg_type: str):
        self.mg_type = mg_type

    def get_mg_type(self):
        return self.mg_type


class Contain:
    def __init__(self, *args: Config):
        # 存储Config
        self.contain = []
        for cf in args:
            self.contain.append(cf)

    def __call__(self, c: Config):
        self.contain.append(c)

    def get_contain(self):
        return self.contain


# 填写配置-例子
# Config
    # ty 监视类型  不填-所有类型 forward-聊天记录 image-图片 record-语音 具体参考cq码 https://docs.go-cqhttp.org/cqcode/
    # obj 监视群(不填-所有
    # qq 具体对象(不填-所有
    # sd 发送群
config = Config(["forward", "video"], ["123456", "321321"], [], ["427956626"])
config2 = Config([], ["2376567356"], ["298587827"], ["427956626"])
# 加入多个配置到容器中
contain = Contain(config, config2)
