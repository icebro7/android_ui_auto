import yaml
import os
from typing import Dict, Any

class ConfigLoader:
    """配置加载器类，用于加载和管理测试配置"""
    
    def __init__(self, config_file: str = 'data/function_basis.yaml'):
        """初始化配置加载器
        
        Args:
            config_file (str): 配置文件路径，默认为'data/function_basis.yaml'
        """
        # 获取项目根目录路径
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(root_dir, config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载YAML配置文件
        
        Returns:
            Dict[str, Any]: 配置数据字典
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise Exception(f'加载配置文件失败：{str(e)}')
    
    def get_app_package(self) -> str:
        """获取应用包名
        
        Returns:
            str: 应用包名
        """
        return self.config['app']['package_name']
    
    def get_locator(self, element_name: str) -> Dict[str, Any]:
        """获取UI元素定位信息
        
        Args:
            element_name (str): 元素名称
            
        Returns:
            Dict[str, Any]: 元素定位信息，包含xpath和timeout
        """
        return self.config['locators'][element_name]
    
    def get_wait_time(self, wait_type: str) -> int:
        """获取等待时间配置
        
        Args:
            wait_type (str): 等待类型
            
        Returns:
            int: 等待时间（秒）
        """
        return self.config['wait_times'][wait_type]
    
    def get_max_loading_wait_time(self) -> int:
        """获取最大加载等待时间
        
        Returns:
            int: 最大等待时间（秒）
        """
        return self.config['max_loading_wait_time']

# 创建全局配置加载器实例
config = ConfigLoader()