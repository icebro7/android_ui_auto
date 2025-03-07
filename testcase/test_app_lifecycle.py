import pytest
from core.base_test import BaseTest
from operation.ui_operations import UIOperations
from config.config_loader import config
import yaml
import os

class TestAppLifecycle(BaseTest):
    
    def load_test_steps(self, yaml_file):
        """从YAML文件加载测试步骤
        
        Args:
            yaml_file: YAML配置文件路径
            
        Returns:
            测试步骤列表
        """
        try:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(root_dir, yaml_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                test_config = yaml.safe_load(f)
                return test_config['test_app_lifecycle']['steps']
        except Exception as e:
            self.logger.error(f"加载测试步骤配置失败：{str(e)}")
            raise
    
    def execute_test_step(self, ui_ops, step):
        """执行单个测试步骤
        
        Args:
            ui_ops: UI操作对象
            step: 测试步骤配置
        """
        operation = step['operation']
        params = step.get('params', {})
        
        # 处理参数中的变量替换
        for key, value in params.items():
            if isinstance(value, str) and value.startswith('${'):
                if value == '${app.package_name}':
                    params[key] = config.get_app_package()
        
        # 执行操作
        result = getattr(ui_ops, operation)(**params)
        
        # 处理断言
        if 'assert' in step:
            for assertion in step['assert']:
                if assertion['type'] == 'result':
                    assert result == assertion['expected'], assertion['message']
    
    @pytest.mark.smoke
    def test_app_lifecycle(self, yaml_file='data/初次开屏测试步骤.yaml'):
        """通用应用生命周期测试
        
        从YAML配置文件加载并执行测试步骤
        
        Args:
            yaml_file: 测试步骤配置文件路径
        """
        try:
            # 初始化UI操作对象
            ui_ops = UIOperations(driver=self.driver, logger=self.logger)
            
            # 加载测试步骤
            test_steps = self.load_test_steps(yaml_file)
            
            # 依次执行测试步骤
            for step in test_steps:
                self.logger.info(f"执行测试步骤：{step['name']}")
                self.execute_test_step(ui_ops, step)
                
        except Exception as e:
            self.logger.error(f"测试执行异常: {str(e)}")
            raise