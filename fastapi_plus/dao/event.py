import json

from ..model.event_log import EventLog
from ..utils.db import DbUtils
from ..utils.json_custom import CustomJSONEncoder
from ..utils.obj2json import obj2json


class EventDao(object):
    """Event(事件)Dao，业务事件记录.

    用于业务事件记录，比如修改数据等

    Attributes:
        user_id: 当前操作用户id
        db: db实体
    """

    # 初始化函数，设置用户ID和数据库连接
    def __init__(self, user_id: int = 0):
        # 设置用户ID
        self.user_id = user_id
        # 创建数据库连接对象
        self.db = DbUtils()

    def get_event_log(self, event_id: int, relation_obj: str, before_data=None) -> EventLog:
        """
        生成事件记录对象并返回
        :param event_id: 事件id
        :param relation_obj: 相关对象
        :param before_data: 之前数据
        :return: 事件记录对象
        """

        # 构造数据：事件记录实例
        # 创建一个EventLog对象
        event_log = EventLog()
        # 设置event_log对象的user_id属性为self.user_id
        event_log.user_id = self.user_id
        # 设置event_log对象的event_id属性为event_id
        event_log.event_id = event_id
        # 设置event_log对象的relation_obj属性为relation_obj
        event_log.relation_obj = relation_obj

        if before_data:
            event_log.relation_id = before_data.id
            event_log.before_data = obj2json(before_data)

        return event_log

    def create_event_log(self, event_log: EventLog, after_data=None):
        """
        创建事件记录，保存在数据库中
        :param event_log: 事件记录实例
        :param after_data: 变化后的数据
        """
        # 如果after_data存在
        if after_data:
            # 将after_data转换为json格式
            event_log.after_data = obj2json(after_data)

        # 如果事件日志中没有改变的数据，则调用calculate_change方法计算改变的数据
        if not event_log.change_data:
            self.calculate_change(event_log)

        self.db.sess.add(event_log)
        self.db.sess.flush()

    def update_event_log(self, event_log: EventLog):
        """
        更新操作记录
        :param event_log:
        :return:
        """
        self.db.sess.add(event_log)
        self.db.sess.flush()

    # 定义一个静态方法，用于计算事件日志的变化
    @staticmethod
    def calculate_change(event_log: EventLog):
        """
        比较数据前后差异，计算变化部分
        :param event_log:
        """
        # 如果event_log的before_data或after_data为空，则将change_data设为None，并返回None
        if not event_log.before_data or not event_log.after_data:
            event_log.change_data = None
            return None

        # 将event_log.before_data转换为字典
        before: dict = json.loads(event_log.before_data)
        # 将event_log.after_data转换为字典
        after: dict = json.loads(event_log.after_data)
        # 创建一个空字典，用于存储变化
        change = {}

        # 遍历before字典中的所有键
        for key in before:
            # 如果键是'updated_time'，则跳过
            if key == 'updated_time':
                continue

            # 如果before字典中的键对应的值与after字典中的键对应的值不相等，则将键和对应的值添加到change字典中
            if before[key] != after[key]:
                change[key] = {
                    'before': before.get(key),
                    'after': after.get(key),
                }

        # 如果没有变化，则将event_log的change_data属性设置为None
        if not change:
            event_log.change_data = None
        # 否则，将变化数据转换为JSON格式，并设置event_log的change_data属性
        else:
            event_log.change_data = json.dumps(change, ensure_ascii=False, cls=CustomJSONEncoder)
