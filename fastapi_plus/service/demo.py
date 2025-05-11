from fastapi_plus.service.base import BaseService

from ..dao.demo import DemoDao
from ..model.demo import Demo


class DemoService(BaseService):
    # 初始化DemoService类
    def __init__(self, auth_data: dict = {}):
        # 从auth_data中获取user_id，如果没有则默认为0
        user_id = auth_data.get('user_id', 0)
        # 设置Model为Demo类
        self.Model = Demo
        # 初始化DemoDao类，传入user_id
        self.dao = DemoDao(user_id)
        # 设置DemoDao类的Model为Demo类
        self.dao.Model = Demo

        # 调用父类的初始化方法，传入user_id和auth_data
        super().__init__(user_id, auth_data)
