from appium.webdriver.common.appiumby import AppiumBy
from core.base_test import BaseTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from functools import wraps
import time
from selenium.webdriver.common.action_chains import ActionChains

def auto_wait(func):
    """装饰器：为UI操作添加自动等待和重试机制"""
    
    @wraps(func)
    def wrapper(self, locator_name, *args, **kwargs):
        max_retries = kwargs.pop('max_retries', 3)
        retry_interval = kwargs.pop('retry_interval', 0.5)
        timeout = kwargs.get('timeout', 10)
        
        # 确保元素存在且可交互
        if not self.wait_for_element(locator_name, timeout, 'clickable'):
            self.logger.error(f"元素[{locator_name}]等待条件不满足")
            raise NoSuchElementException(f"元素[{locator_name}]未找到或不可点击")
            
        # 添加重试机制
        for attempt in range(max_retries):
            try:
                result = func(self, locator_name, *args, **kwargs)
                return result  # 直接返回原方法的结果
            except (StaleElementReferenceException, Exception) as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"{func.__name__}操作失败(重试{max_retries}次)：{str(e)}")
                    raise  # 或根据需求返回False/None
                time.sleep(retry_interval)
        return False  # 所有重试失败后返回
    return wrapper

class UIOperations:
    """UI操作关键字封装类，提供常用的UI自动化操作方法"""

    def __init__(self, driver=None, logger=None):
        self.driver = driver
        self.logger = logger

    def find_element_safe(self, locator_name, timeout=10, log_level='error'):
        from config.config_loader import config
        try:
            # 如果locator_name是xpath表达式，直接使用
            if locator_name.startswith('//') or locator_name.startswith('(//') or locator_name.startswith('(//'):
                xpath = locator_name
            else:
                # 否则从配置中获取定位器
                locator = config.get_locator(locator_name)
                xpath = locator['xpath']
                
            wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5)
            element = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
            return element
        except TimeoutException:
            self.logger.log(log_level.upper(), f"元素[{locator_name}]查找超时")
            return None
        except Exception as e:
            self.logger.log(log_level.upper(), f"元素[{locator_name}]查找异常: {str(e)}")
            return None


    def find_element_by_locator(self, locator_name, timeout=10, log_level='error'):
        """根据yaml中定义的定位器名称或xpath查找元素
            
            Args:
                locator_name: yaml中定义的定位器名称或xpath字符串
                timeout: 超时时间（秒）
                log_level: 日志级别
                
            Returns:
                找到的元素对象，未找到返回None
            """
        try:
            # 如果是xpath字符串，直接使用
            if locator_name.startswith('//') or locator_name.startswith('(//') or locator_name.startswith('(//'):
                element = self.find_element_safe(
                    locator_name,
                    timeout=timeout,
                    log_level=log_level
                )
            else:
                # 否则从配置文件获取定位器
                from config.config_loader import config
                locator = config.get_locator(locator_name)
                element = self.find_element_safe(
                    locator_name,
                    timeout=locator.get('timeout', timeout),
                    log_level=log_level
                )
            
            if isinstance(element, bool):
                self.logger.error(f"元素[{locator_name}]返回异常布尔值: {element}")
                return None
            return element
        except Exception as e:
            self.logger.error(f"查找元素[{locator_name}]失败: {str(e)}")
            return None
    
    @auto_wait
    def input_text(self, locator_name, text, timeout=10):
        """向指定元素输入文本，带自动等待和重试机制
        
        Args:
            locator_name: yaml中定义的定位器名称
            text: 要输入的文本
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        element = self.find_element_by_locator(locator_name, timeout)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False
    
    def close_app(self, package_name, timeout=10):
        """关闭指定的应用程序
        
        Args:
            package_name: 应用程序的包名
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        try:
            self.driver.terminate_app(package_name, timeout=timeout * 1000)
            self.logger.info(f"已关闭应用[{package_name}]")
            return True
        except Exception as e:
            self.logger.error(f"关闭应用[{package_name}]失败：{str(e)}")
            return False
    
    def launch_app(self, package_name, timeout=10):
        """启动指定的应用程序
        
        Args:
            package_name: 应用程序的包名
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        try:
            self.driver.activate_app(package_name)
            self.logger.info(f"已启动应用[{package_name}]")
            return True
        except Exception as e:
            self.logger.error(f"启动应用[{package_name}]失败：{str(e)}")
            return False
    
    @auto_wait
    def click_element(self, locator_name, timeout=10):
        """点击指定元素，带自动等待和重试机制
        
        Args:
            locator_name: yaml中定义的定位器名称
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        self.logger.info(f"开始点击元素[{locator_name}]")
        element = self.find_element_by_locator(locator_name, timeout)
        
        self.logger.info(f"找到的元素类型: {type(element)}")
        if element and not isinstance(element, bool):
            try:
                self.logger.info(f"元素[{locator_name}]已找到且可点击")
                element.click()
                
                self.logger.info(f"已成功点击元素[{locator_name}]")
                return True
            except Exception as e:
                self.logger.error(f"点击元素[{locator_name}]失败：{str(e)}")
                return False
        self.logger.info(f"元素[{locator_name}]不存在或不可点击")
        return False
    
    @auto_wait
    def press_key(self, locator_name, key_code, metastate=None, timeout=10):
        """在指定元素上模拟按键操作，带自动等待和重试机制
        
        Args:
            locator_name: yaml中定义的定位器名称
            key_code: 按键代码，例如：AndroidKeyCode.BACK, AndroidKeyCode.HOME等
            metastate: 元状态，例如：0表示无修饰键，1表示Shift键，2表示Alt键
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        element = self.find_element_by_locator(locator_name, timeout)
        if element:
            try:
                # 确保元素在视图中
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                # 执行按键操作
                self.driver.press_keycode(key_code, metastate)
                self.logger.info(f"在元素[{locator_name}]上执行按键操作，按键代码：{key_code}")
                return True
            except Exception as e:
                self.logger.error(f"按键操作失败：{str(e)}")
                return False
        return False
    
    def wait_for_element(self, locator_name, timeout=10, condition='presence'):
        """等待元素满足指定条件
        
        Args:
            locator_name: yaml中定义的定位器名称或xpath表达式
            timeout: 超时时间（秒）
            condition: 等待条件，可选值：'presence'（存在）, 'visible'（可见）, 'clickable'（可点击）
            
        Returns:
            等待是否成功
        """
        try:
            # 如果locator_name是xpath表达式，直接使用
            if locator_name.startswith('//') or locator_name.startswith('(//') or locator_name.startswith('(//'):                
                xpath = locator_name
            else:
                # 否则从配置中获取定位器
                from config.config_loader import config
                locator = config.get_locator(locator_name)
                xpath = locator['xpath']
                
            wait = WebDriverWait(self.driver, timeout)
            if condition == 'visible':
                wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, xpath)))
            elif condition == 'clickable':
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath)))
            else:  # presence
                wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath)))
            return True
        except TimeoutException:
            self.logger.info(f"等待元素[{locator_name}]超时")
            return False
        except Exception as e:
            self.logger.error(f"等待元素发生错误：{str(e)}")
            return False
    
    def find_element_by_xpath(self, xpath, timeout=10, log_level='error'):
        """根据xpath直接查找元素
        
        Args:
            xpath: 元素的xpath定位表达式
            timeout: 超时时间（秒）
            log_level: 日志级别
            
        Returns:
            找到的元素对象，未找到返回None
        """
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=0.5)
            element = wait.until(
                EC.visibility_of_element_located((AppiumBy.XPATH, xpath))
            )
            return element
        except TimeoutException:
            self.logger.log(log_level.upper(), f"元素[{xpath}]查找超时")
            return None
        except Exception as e:
            self.logger.log(log_level.upper(), f"元素[{xpath}]查找异常: {str(e)}")
            return None

    def wait_for_element_by_xpath(self, locator_name, timeout=10, condition='presence'):
        """等待元素满足指定条件（使用xpath）
        
        Args:
            xpath: 元素的xpath定位表达式
            timeout: 超时时间（秒）
            condition: 等待条件，可选值：'presence'（存在）, 'visible'（可见）, 'clickable'（可点击）
            
        Returns:
            等待是否成功
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            if condition == 'visible':
                wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, locator_name)))
            elif condition == 'clickable':
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, locator_name)))
            else:  # presence
                wait.until(EC.presence_of_element_located((AppiumBy.XPATH, locator_name)))
            return True
        except TimeoutException:
            self.logger.info(f"等待元素[{locator_name}]超时")
            return False
        except Exception as e:
            self.logger.error(f"等待元素发生错误：{str(e)}")
            return False

    @auto_wait
    def click_element_by_xpath(self, xpath, timeout=10):
        """点击指定元素（使用xpath），带自动等待和重试机制
        
        Args:
            xpath: 元素的xpath定位表达式
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        self.logger.info(f"开始点击元素[{xpath}]")
        element = self.find_element_by_xpath(xpath, timeout)
        
        if element:
            try:
                self.logger.info(f"元素[{xpath}]已找到且可点击")
                element.click()
                self.logger.info(f"已成功点击元素[{xpath}]")
                return True
            except Exception as e:
                self.logger.error(f"点击元素[{xpath}]失败：{str(e)}")
                return False
        self.logger.info(f"元素[{xpath}]不存在或不可点击")
        return False

    @auto_wait
    def check_and_handle_popup(self, popup_locator_name, button_locator_name, timeout=5):
        """检查并处理弹窗，带自动等待和重试机制
        
        Args:
            popup_locator_name: 弹窗xpath或定位器名称
            button_locator_name: 按钮xpath或定位器名称
            timeout: 超时时间（秒）
            
        Returns:
            是否处理了弹窗
        """
        # 确保弹窗存在且可见
        if not self.wait_for_element_by_xpath(popup_locator_name, timeout, 'visible'):
            return False
            
        popup = self.find_element_by_xpath(popup_locator_name, timeout, log_level='info')
        if popup:
            self.logger.info(f"检测到弹窗[{popup_locator_name}]")
            if self.click_element_by_xpath(button_locator_name, timeout):
                self.logger.info("已关闭弹窗")
                return True
            else:
                self.logger.error("关闭弹窗失败")
        return False
    
    @auto_wait
    def get_element_text(self, locator_name, timeout=10):
        """获取元素文本内容，带自动等待和重试机制
        
        Args:
            locator_name: yaml中定义的定位器名称
            timeout: 超时时间（秒）
            
        Returns:
            元素文本内容，获取失败返回None
        """
        element = self.find_element_by_locator(locator_name, timeout)
        if element:
            return element.text
        return None
    
    @auto_wait
    def get_element_attribute(self, locator_name, attribute, timeout=10):
        """获取元素属性值，带自动等待和重试机制
        
        Args:
            locator_name: yaml中定义的定位器名称
            attribute: 属性名称
            timeout: 超时时间（秒）
            
        Returns:
            属性值，获取失败返回None
        """
        element = self.find_element_by_locator(locator_name, timeout)
        if element:
            return element.get_attribute(attribute)
        return None
    
    def is_element_present(self, locator_name, timeout=10):
        """判断元素是否存在
        
        Args:
            locator_name: yaml中定义的定位器名称
            timeout: 超时时间（秒）
            
        Returns:
            元素是否存在
        """
        return self.find_element_by_locator(locator_name, timeout, log_level='info') is not None
    
    def wait_and_click(self, locator_name, timeout=10):
        """等待元素可点击并点击
        
        Args:
            locator_name: yaml中定义的定位器名称
            timeout: 超时时间（秒）
            
        Returns:
            操作是否成功
        """
        if self.wait_for_element(locator_name, timeout, 'clickable'):
            return self.click_element(locator_name, 1)
        return False
    
    def long_press_element(self, locator_name, duration=1000, timeout=10):
        """长按元素（使用W3C Actions标准）"""
        element = self.find_element_by_locator(locator_name, timeout)
        if element:
            ActionChains(self.driver).click_and_hold(element).pause(duration/1000).release().perform()
            return True
        return False

    @auto_wait
    def swipe_screen(self, start_x, start_y, end_x, end_y, duration=1000):
        """滑动屏幕增强版，带自动重试和参数校验"""
        try:
            # 参数有效性检查
            if not (0 <= start_x <= 1 and 0 <= end_x <= 1 and 0 <= start_y <= 1 and 0 <= end_y <= 1):
                self.logger.error("坐标参数应在0-1之间表示屏幕比例")
                return False

            # 获取实际屏幕尺寸
            width = self.driver.get_window_size()['width']
            height = self.driver.get_window_size()['height']

            # 转换比例坐标为实际坐标
            actual_start_x = int(width * start_x)
            actual_start_y = int(height * start_y)
            actual_end_x = int(width * end_x)
            actual_end_y = int(height * end_y)

            # 执行滑动操作
            self.driver.swipe(actual_start_x, actual_start_y, 
                            actual_end_x, actual_end_y, duration)
            self.logger.info(f"成功滑动：({start_x},{start_y})→({end_x},{end_y})")
            return True
        except Exception as e:
            self.logger.error(f"滑动失败：{str(e)}")
            return False
    
    def wait_for_activity(self, activity_name, timeout=10):
        """等待指定的Activity启动
        
        Args:
            activity_name: 要等待的Activity名称
            timeout: 超时时间（秒）
            
        Returns:
            等待是否成功
        """
        try:
            self.driver.wait_activity(activity_name, timeout)
            self.logger.info(f"已等待Activity[{activity_name}]启动")
            return True
        except Exception as e:
            self.logger.error(f"等待Activity[{activity_name}]启动失败：{str(e)}")
            return False