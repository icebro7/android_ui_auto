import os
import re
import subprocess
import threading
import queue
import time
from datetime import datetime
from config.config_point import LOGCAT_KEYWORDS

class LogcatFilter:
    def __init__(self):
        self.log_queue = queue.Queue()
        self.is_running = False
        self.current_log_file = None
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', 'logcat_logs')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def start_logging(self):
        """启动日志收集"""
        if self.is_running:
            return

        self.is_running = True
        # 创建新的日志文件，使用filtered_前缀明确标识
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_log_file = os.path.join(self.log_dir, f'filtered_logcat_{timestamp}.txt')

        # 启动日志收集和处理线程
        self.logcat_thread = threading.Thread(target=self._collect_logs)
        self.process_thread = threading.Thread(target=self._process_logs)
        
        self.logcat_thread.daemon = True
        self.process_thread.daemon = True
        
        self.logcat_thread.start()
        self.process_thread.start()

    def stop_logging(self):
        """停止日志收集"""
        self.is_running = False
        if hasattr(self, 'logcat_thread'):
            self.logcat_thread.join(timeout=1)
        if hasattr(self, 'process_thread'):
            self.process_thread.join(timeout=1)

    def _get_keyword_description(self, line):
        """获取日志关键字对应的中文描述
        Args:
            line: 日志行
        Returns:
            description: 中文描述
        """
        line_stripped = line.strip()
        for keyword, description in LOGCAT_KEYWORDS.items():
            if keyword in line_stripped:
                return description
        return ""

    def _collect_logs(self):
        """收集日志的线程函数"""
        try:
            # 清除之前的日志缓存
            subprocess.run(['adb', 'logcat', '-c'], check=True)
            # 启动新的日志收集进程，添加过滤参数
            process = subprocess.Popen(
                ['adb', 'logcat', '-v', 'threadtime'],  # 添加时间戳格式
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            while self.is_running:
                line = process.stdout.readline()
                if line:
                    # 在收集阶段就进行初步过滤
                    # 检查是否包含关键字
                    line_stripped = line.strip()
                    for keyword in LOGCAT_KEYWORDS.keys():
                        if keyword in line_stripped:
                            self.log_queue.put(line)
                            break

            process.terminate()
        except Exception as e:
            print(f"日志收集出错：{str(e)}")

    def _process_logs(self):
        """处理日志的线程函数"""
        try:
            with open(self.current_log_file, 'w', encoding='utf-8') as f:
                while self.is_running or not self.log_queue.empty():
                    try:
                        line = self.log_queue.get(timeout=0.1)
                        description = self._get_keyword_description(line)
                        if description:  # 只处理匹配到关键字的日志
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            # 移除原始日志中的时间戳部分
                            log_content = re.sub(r'\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3}\s+', '', line.strip())
                            formatted_log = f"[{timestamp}] {description} {log_content}\n"
                            f.write(formatted_log)
                    except queue.Empty:
                        continue
        except Exception as e:
            print(f"日志处理出错：{str(e)}")

    def filter_existing_log(self, log_file_path):
        """过滤现有的日志文件
        Args:
            log_file_path: 日志文件路径
        Returns:
            filtered_logs: 过滤后的日志列表
        """
        filtered_logs = []
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    description = self._get_keyword_description(line)
                    if description:  # 只添加匹配到关键字的日志
                        filtered_logs.append(f"{description}: {line.strip()}")
        except Exception as e:
            print(f"处理日志文件时出错：{str(e)}")
        
        return filtered_logs

    def process_log_directory(self):
        """处理日志目录下的所有日志文件"""
        try:
            for filename in os.listdir(self.log_dir):
                if filename.startswith('logcat_') and filename.endswith('.txt'):
                    log_file_path = os.path.join(self.log_dir, filename)
                    print(f"\n处理日志文件：{filename}")
                    filtered_logs = self.filter_existing_log(log_file_path)
                    
                    # 将过滤后的日志写入新文件
                    output_file = os.path.join(self.log_dir, f'filtered_{filename}')
                    with open(output_file, 'w', encoding='utf-8') as f:
                        for log in filtered_logs:
                            f.write(log + '\n')
                    print(f"已生成过滤后的日志文件：{output_file}")
                    print(f"找到 {len(filtered_logs)} 条匹配的日志")
        except Exception as e:
            print(f"处理日志目录时出错：{str(e)}")

# 创建全局的日志过滤器实例
logcat_filter = LogcatFilter()

if __name__ == '__main__':
    # 测试代码
    pass
    # 处理已有的日志文件
    if os.path.exists(logcat_filter.log_dir):
        logcat_filter.process_log_directory()
    else:
        print(f"日志目录不存在：{logcat_filter.log_dir}")