from fastapi_plus.model.base import *


# 定义一个名为Demo的类，继承自Base类
class Demo(Base):
    # 定义表名
    __tablename__ = 'demo'
    # 定义表注释
    __table_args__ = {'comment': 'Demo'}

    # 定义用户ID字段，类型为BIGINT(20)，不能为空，默认值为0，注释为用户ID
    user_id = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='用户ID')
    # 定义分类ID字段，类型为BIGINT(20)，不能为空，默认值为0，注释为分类ID
    category_id = Column(BIGINT(20), nullable=False, server_default=text("0"), comment='分类ID')
    # 定义分类名称字段，类型为String(255)，不能为空，默认值为空字符串，注释为分类名称
    category_name = Column(String(255), nullable=False, server_default=text("''"), comment='分类名称')
    # 定义数据字段，类型为String(1000)，不能为空，默认值为空字符串，注释为数据
    data = Column(String(1000), nullable=False, server_default=text("''"), comment='数据')
