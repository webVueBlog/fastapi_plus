from fastapi import APIRouter, Depends
from fastapi_plus.schema.base import ListArgsSchema, RespBaseSchema, RespIdSchema, RespListSchema
from fastapi_plus.utils.auth import get_auth_data
from fastapi_plus.utils.custom_route import CustomRoute

from ..schema.demo import DemoInfoSchema, DemoRespDetailSchema
from ..service.demo import DemoService

# 创建一个APIRouter实例，并指定路由类为CustomRoute
router = APIRouter(route_class=CustomRoute)


# 定义一个POST请求，用于获取列表数据
@router.post('/list', response_model=RespListSchema)
async def list(*, args: ListArgsSchema, auth_data: dict = Depends(get_auth_data)):
    # 从auth_data中获取user_id，并将其赋值给args
    args.user_id = auth_data.get('user_id')
    # 调用DemoService的list方法，传入args，并返回结果
    return DemoService(auth_data).list(args)


# 定义一个GET请求，用于获取指定id的数据
@router.get('/{id}', response_model=DemoRespDetailSchema)
async def read(id: int, auth_data: dict = Depends(get_auth_data)):
    # 创建一个DemoRespDetailSchema实例
    resp = DemoRespDetailSchema()
    # 调用DemoService的read方法，传入id，并将结果赋值给resp的detail属性
    resp.detail = DemoService(auth_data).read(id)
    # 返回resp
    return resp


# 定义一个POST请求，用于创建数据
@router.post('', response_model=RespIdSchema, response_model_exclude_none=True)
async def create(*, info: DemoInfoSchema, auth_data: dict = Depends(get_auth_data)):
    # 调用DemoService的create方法，传入info，并返回结果
    return DemoService(auth_data).create(info)


# 定义一个PUT请求，用于更新数据
@router.put('/{id}', response_model=RespBaseSchema)
async def update(*, info: DemoInfoSchema, auth_data: dict = Depends(get_auth_data)):
    # 调用DemoService的update方法，传入info，并返回结果
    return DemoService(auth_data).update(info)


# 定义一个DELETE请求，用于删除数据
@router.delete('/{id}', response_model=RespBaseSchema)
async def delete(id: int, auth_data: dict = Depends(get_auth_data)):
    # 调用DemoService的delete方法，传入id，并返回结果
    return DemoService(auth_data).delete(id)
