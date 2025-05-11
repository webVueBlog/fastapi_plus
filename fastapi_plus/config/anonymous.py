"""
匿名访问接口列表
格式：req.method + req.url.path，其中method为大写
"""
# 定义一个匿名路径列表
anonymous_path_list = [
    # 获取根路径
    'GET/',
    # 获取robots.txt文件
    'GET/robots.txt',
    # 获取favicon.ico文件
    'GET/favicon.ico',
    # 获取docs路径
    'GET/docs',
    # 获取oauth2-redirect路径
    'GET/docs/oauth2-redirect',
    # 获取redoc路径
    'GET/redoc',
    # 获取openapi.json文件
    'GET/openapi.json',
    # 获取sys_info路径
    'GET/sys_info',
]
