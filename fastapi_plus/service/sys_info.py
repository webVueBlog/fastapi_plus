import platform


class SysInfoService(object):
    """信息信息服务类.

    获取服务运行系统的基础信息
    """

    # 定义一个静态方法，用于获取系统信息
    @staticmethod
    def get_sys_info():
        # 返回一个字典，包含系统信息
        return {
            'platform': platform.platform(),  # 获取操作系统名称及版本号
            'machine': platform.machine(),  # 获取计算机类型
            'node': platform.node(),  # 获取计算机的网络名称
            'processor': platform.processor(),  # 获取计算机处理器信息
            'python_version': platform.python_version(),  # 获取Python解释器的版本
        }
