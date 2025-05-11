from fastapi import APIRouter
from starlette.responses import Response

# 创建一个APIRouter实例
base_router = APIRouter()


# 定义一个GET请求，访问根路径
@base_router.get('/')
async def get_root():
    """
    访问根路径
    """
    # 返回一个空字符串，媒体类型为text/plain
    return Response(content='', media_type='text/plain')


# 定义一个GET请求，获取爬虫权限
@base_router.get('/robots.txt')
async def get_robots():
    """
    获取爬虫权限
    """
    # 返回一个禁止爬取的字符串，媒体类型为text/plain
    return Response(content='User-agent: * \nDisallow: /', media_type='text/plain')


# 定义一个GET请求，获取系统基本信息
@base_router.get('/sys_info')
async def get_sys_info():
    """
    获取系统基本信息
    """
    # 导入SysInfoService类
    from ..service.sys_info import SysInfoService

    # 返回系统基本信息
    return SysInfoService().get_sys_info()
