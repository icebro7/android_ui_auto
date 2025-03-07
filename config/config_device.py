from appium.options.common import AppiumOptions

# 后续修改为可从yaml文件中读取
class AndroidDeviceConfig:
    """Android 设备配置类"""
    @staticmethod
    def get_options():
        """获取Appium配置选项"""
        options = AppiumOptions()  # 使用 AppiumOptions
        options.set_capability("platformName", "Android")
        options.set_capability("platformVersion", "13")
        options.set_capability("deviceName", "Pixel 7")
        options.set_capability("udid", "emulator-5554")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("noReset", True)
        return options
    
    @staticmethod
    def get_server_url():
        """获取Appium服务器URL"""
        return 'http://localhost:4723'