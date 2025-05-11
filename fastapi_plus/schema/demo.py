from datetime import datetime

from fastapi_plus.schema.base import InfoSchema, RespDetailSchema


# 定义一个DemoInfoSchema类，继承自InfoSchema类
class DemoInfoSchema(InfoSchema):
    # 定义一个parent_name属性，类型为字符串
    parent_name: str


# 定义一个DemoDetailSchema类，继承自DemoInfoSchema类
class DemoDetailSchema(DemoInfoSchema):
    # 定义一个created_time属性，类型为datetime
    created_time: datetime
    # 定义一个updated_time属性，类型为datetime
    updated_time: datetime


# 定义一个DemoRespDetailSchema类，继承自RespDetailSchema类
class DemoRespDetailSchema(RespDetailSchema):
    # 定义一个detail属性，类型为DemoDetailSchema，默认值为None
    detail: DemoDetailSchema = None
