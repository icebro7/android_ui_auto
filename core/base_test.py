import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import subprocess
import os
import threading
from datetime import datetime
from config.config_device import AndroidDeviceConfig

class BaseTest:
    """测试基类"""
    @pytest.fixture(autouse=True)
    def setup_test(self):
        # 初始化日志相关属性
        self.logcat_process = None
        self.logcat_file = None
        self.logcat_file_handle = None
        self.log_thread = None
        self._logging_enabled = False
        self._thread_lock = threading.Lock()
        
        # 初始化日志配置
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 初始化设备配置
        self.driver = webdriver.Remote(
            AndroidDeviceConfig.get_server_url(),
            options=AndroidDeviceConfig.get_options()
        )
        self.actions = ActionChains(self.driver)

        # 启动logcat日志收集
        self.start_logcat()
        
        yield
        
        # 停止logcat日志收集
        self.stop_logcat()

        if self.driver:
            self.driver.quit()


    def start_logcat(self):
        """启动logcat日志收集"""
        try:
            with self._thread_lock:
                if self._logging_enabled:
                    self.logger.warning("Logcat日志收集已在运行中")
                    return

                # 创建日志目录
                log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', 'logcat_logs')
                os.makedirs(log_dir, exist_ok=True)

                # 创建日志文件
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                self.logcat_file = os.path.join(log_dir, f'logcat_{timestamp}.txt')
                
                # 清除之前的logcat缓冲区
                subprocess.run(['adb', 'logcat', '-c'])
                
                # 创建文件句柄并设置为行缓冲模式
                self.logcat_file_handle = open(self.logcat_file, 'w', encoding='utf-8', buffering=1)
                
                # 启动logcat进程并将输出重定向到文件
                self.logcat_process = subprocess.Popen(
                    ['adb', 'logcat', '-v', 'threadtime'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    bufsize=1
                )

                self._logging_enabled = True

                # 创建日志处理线程
                def process_log():
                    try:
                        while self._logging_enabled and self.logcat_process and self.logcat_process.poll() is None:
                            try:
                                line = self.logcat_process.stdout.readline()
                                if not line:
                                    break
                                
                                with self._thread_lock:
                                    if self.logcat_file_handle and not self.logcat_file_handle.closed:
                                        self.logcat_file_handle.write(line)
                                        self.logcat_file_handle.flush()
                            except IOError as e:
                                self.logger.error(f"日志写入错误：{str(e)}")
                                break
                    except Exception as e:
                        if hasattr(self, 'logger'):
                            self.logger.error(f"日志处理线程异常：{str(e)}")
                    finally:
                        self._safe_close_resources()

                self.log_thread = threading.Thread(target=process_log, daemon=True)
                self.log_thread.start()
                
                self.logger.info(f"Logcat日志收集已启动，日志文件：{self.logcat_file}")
        except Exception as e:
            self._safe_close_resources()
            self.logger.error(f"启动Logcat失败：{str(e)}")

    def _safe_close_resources(self):
        """安全地关闭资源"""
        with self._thread_lock:
            if self.logcat_file_handle and not self.logcat_file_handle.closed:
                try:
                    self.logcat_file_handle.flush()
                    self.logcat_file_handle.close()
                except Exception as e:
                    self.logger.error(f"关闭日志文件句柄失败：{str(e)}")
                finally:
                    self.logcat_file_handle = None

            if self.logcat_process:
                try:
                    if self.logcat_process.stdout:
                        self.logcat_process.stdout.close()
                    if self.logcat_process.stderr:
                        self.logcat_process.stderr.close()
                    
                    self.logcat_process.terminate()
                    try:
                        self.logcat_process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.logcat_process.kill()
                except Exception as e:
                    self.logger.error(f"终止logcat进程失败：{str(e)}")
                finally:
                    self.logcat_process = None

    def stop_logcat(self):
        """停止logcat日志收集"""
        try:
            with self._thread_lock:
                self._logging_enabled = False
                
            if self.log_thread and self.log_thread.is_alive():
                self.log_thread.join(timeout=5)

            self._safe_close_resources()
            self.logger.info("Logcat日志收集已停止")
        except Exception as e:
            self.logger.error(f"停止Logcat失败：{str(e)}")