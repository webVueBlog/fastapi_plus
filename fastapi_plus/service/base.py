from ..dao.event import EventDao
from ..schema.base import ListArgsSchema, RespListSchema, RespIdSchema, RespBaseSchema


class BaseService(object):
    """Base(基础)服务，用于被继承.

    CRUD基础服务类，拥有基本方法，可直接继承使用

    Attributes:
        auth_data: 认证数据，包括用户、权限等
        user_id: 当前操作用户id
        event_dao: 业务事件dao
        dao: 当前业务数据处理类
    """

    # 定义一个字典，用于存储认证数据
    auth_data: dict = {}
    # 定义一个整数，用于存储用户ID
    user_id: int = 0
    # 定义一个EventDao对象
    event_dao: EventDao
    # 定义一个dao对象
    dao = None
    # 定义一个Model对象
    Model = None

    def __init__(self, user_id: int = 0, auth_data: dict = {}):
        """Service初始化."""

        # 设置用户ID
        self.user_id = user_id
        # 设置认证数据
        self.auth_data = auth_data
        # 创建EventDao对象，传入用户ID
        self.event_dao = EventDao(user_id)

    def read(self, id: int) -> Model:
        """读取单条数据.

        Args:
            id: 数据id

        Returns:
            一个model实体
        """

        return self.dao.read(id)

    def list(self, args: ListArgsSchema) -> RespListSchema:
        """读取多条数据.

        Args:
            args: 列表请求参数，详见ListArgsSchema

        Returns:
            多个model实体组成的List
        """

        return self.dao.read_list(args)

    def create(self, schema) -> RespIdSchema:
        """创建一条数据.

        Args:
            schema: model对应的schema，详见schema中对应的实体
            model: model的实体

        Returns:
            是否创建成功，创建成功则附加数据id
        """

        # 创建一个RespIdSchema对象
        resp = RespIdSchema()
        # 创建一个Model对象
        model = self.Model()

        # 根据schema设置model的属性
        self.set_model_by_schema(schema, model)
        # 设置model的user_id属性
        model.user_id = self.user_id
        # 设置model的created_by属性
        model.created_by = self.user_id
        # 设置model的updated_by属性
        model.updated_by = self.user_id
        # 创建model
        self.dao.create(model)

        # 获取event_log
        event_log = self.event_dao.get_event_log(2, model.__tablename__)
        # 设置event_log的name属性
        event_log.name = '创建{}：{}'.format(model.__table_args__.get('comment', '数据'), model.name)
        # 设置event_log的relation_id属性
        event_log.relation_id = model.id
        # 创建event_log
        self.event_dao.create_event_log(event_log, model)

        # 设置resp的id属性
        resp.id = model.id

        # 返回resp
        return resp

    @staticmethod
    def set_model_by_schema(schema, model):
        """给model赋值，从schema.

        Args:
            schema: model对应的schema，详见schema中对应的实体
            model: model的实体

        Returns:
            是否创建成功，创建成功则附加数据id
        """

        for (key, value) in schema:
            model.__setattr__(key, value)

        if hasattr(model, 'search'):
            model.search = model.name

    def update(self, schema) -> RespBaseSchema:
        """更新一条数据.

        Args:
            schema: model对应的schema，详见schema中对应的实体
            model: model的实体

        Returns:
            是否更新成功
        """

        resp = RespBaseSchema()

        model = self.dao.read(schema.id)

        if not model:
            resp.code = -1
            resp.message = '找不到对应的：{}'.format(model.__table_args__.get('comment', '数据'))
            return resp

        event_log = self.event_dao.get_event_log(1, model.__tablename__, model)
        event_log.name = '修改{}：{}'.format(model.__table_args__.get('comment', '数据'), model.name)

        self.set_model_by_schema(schema, model)
        model.updated_by = self.user_id
        self.dao.update(model)

        self.event_dao.create_event_log(event_log, model)

        return resp

    def delete(self, id: int) -> RespBaseSchema:
        """删除单条数据.

        Args:
            id: 数据id

        Returns:
            是否删除成功
        """

        resp = RespBaseSchema()

        model = self.dao.read(id)

        # 如果model为空
        if not model:
            # 设置响应码为 -1
            resp.code = -1
            # 设置响应消息为找不到对应的：{}，其中{}为model的注释，如果没有注释则默认为数据
            resp.message = '找不到对应的：{}'.format(model.__table_args__.get('comment', '数据'))
            # 返回响应
            return resp

        # 获取事件日志
        event_log = self.event_dao.get_event_log(5, model.__tablename__, model)
        # 设置事件日志名称
        event_log.name = '删除{}：{}'.format(model.__table_args__.get('comment', '数据'), model.name)

        self.dao.delete(model)

        self.event_dao.create_event_log(event_log, model)

        return resp
