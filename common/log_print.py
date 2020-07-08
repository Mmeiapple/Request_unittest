import os
import logging

current=os.path.dirname(__file__)
loginfopath=os.path.join(current,'../log/info_logs.txt')

class LogPrint:
    def __init__(self):
        """
        创建一个日志对象

        """
        self.looger=logging.getLogger(__name__)

        """
        给日志设置级别

        """
        self.looger.setLevel(level=logging.INFO)

        """
        创建一个日志格式对象
        
        """
        self.formater=logging.Formatter('Info:%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        """
        创建一个FileHandler的对象
        
        """
        console=logging.FileHandler(loginfopath)

        """
        给日志设置格式

        """

        console.setFormatter(self.formater)

        """
        logger日志对象加载FileHandler对象
        
        """
        self.looger.addHandler(console)

    def logsinfo(self,message):

        """
        日志输出

        """
        self.looger.info(message)

Log=LogPrint()
if __name__=="__main__":
    Log.logsinfo('dudu')
