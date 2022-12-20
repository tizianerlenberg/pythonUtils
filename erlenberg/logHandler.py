#!/usr/bin/env python3

import sys, threading, queue, inspect, datetime, pathlib

DEBUG = 10
INFO = 20
WARN = 30
WARNING = 30
ERROR = 40
CRITICAL = 50
NONE = 60

logger=None

class Logger():
    green = '\x1b[32m'
    blue = '\x1b[34m'
    yellow = '\x1b[93m'
    red = '\x1b[35m'
    bold_red = '\x1b[91;5;4m'
    reset = '\x1b[0m'
    def __init__(self, consoleLogLevel=NONE, fileLogLevel=NONE, processParams=False, pp=None, color=True):
        global logger
        if inspect.getmodule(inspect.stack()[1][0]).__name__ == '__main__':
            logger = self
        if not not pp:
            processParams=pp
        self.consoleLogLevel=consoleLogLevel
        self.fileLogLevel=fileLogLevel
        if processParams:
            self.paramProcessingFun()
        self.pendingMessages = queue.Queue()
        self.loggingThread = threading.Thread(target=self.threadFun)
        self.filename='tmp.log'
        self.color=color
    def paramProcessingFun(self):
        if inspect.getmodule(inspect.stack()[2][0]).__name__ == '__main__':
            userInput='none,none'
            if '-ll' in sys.argv:
                userInput=sys.argv[sys.argv.index('-ll')+1]
            elif '--log-level' in sys.argv:
                userInput=sys.argv[sys.argv.index('--log-level')+1]
            else:
                return
            self.paramSetLogLevelInternal(userInput)
    def threadFun(self):
        logFile=None
        try:
            while(True):
                if self.fileLogLevel >= NONE:
                    try:
                        pending = self.pendingMessages.get(timeout=0.02)
                    except queue.Empty:
                        if not threading.main_thread().is_alive():
                            break
                        continue
                    if pending[0] >= self.consoleLogLevel:
                        print(self.colorMod(self.formatMsg(pending[1], pending[2], fullDate=False), pending[0]))
                else:
                    if not logFile:
                        logFile = open(self.filename + '.log', 'a')
                    try:
                        pending = self.pendingMessages.get(timeout=0.02)
                    except queue.Empty:
                        if not threading.main_thread().is_alive():
                            break
                        continue
                    if pending[0] >= self.consoleLogLevel:
                        print(self.colorMod(self.formatMsg(pending[1], pending[2], fullDate=False), pending[0]))
                    if pending[0] >= self.fileLogLevel:
                        logFile.write(self.formatMsg(pending[1], pending[2], fullDate=True) + '\n')
        finally:
            try:
                logFile.close()
            except:
                pass
    def colorMod(self, message, logLevel):
        if not self.color:
            return message
        if logLevel <= DEBUG:
            return self.green + message + self.reset
        if logLevel <= INFO:
            return self.blue + message + self.reset
        if logLevel <= WARN:
            return self.yellow + message + self.reset
        if logLevel <= WARNING:
            return self.yellow + message + self.reset
        if logLevel <= ERROR:
            return self.red + message + self.reset
        if logLevel <= CRITICAL:
            return self.bold_red + message + self.reset
    def start(self):
        global logger
        if inspect.getmodule(inspect.stack()[1][0]).__name__ == '__main__':
            self.filename = pathlib.Path(inspect.getframeinfo(inspect.stack()[1][0]).filename).stem
            self.loggingThread.start()
        return logger
    def formatMsg(self, message, meta, fullDate=False):
        time, filename, lineo, threadName = meta
        if fullDate:
            timeStr= time.strftime("%d.%m.%y %H:%M:%S")
        else:
            timeStr= time.strftime("%H:%M:%S")
        return f'[ {timeStr} - {filename} {lineo} - {threadName} ] {message}'
    def getMeta(self):
        caller = inspect.getframeinfo(inspect.stack()[2][0])
        
        time = datetime.datetime.now()
        threadName = threading.current_thread().getName()
        filename = pathlib.Path(caller.filename).name
        lineo = caller.lineno
        return [time, filename, lineo, threadName]
    def setLogLevel(self, consoleLogLevel=NONE, fileLogLevel=NONE):
        if inspect.getmodule(inspect.stack()[1][0]).__name__ == '__main__':
            self.consoleLogLevel=consoleLogLevel
            self.fileLogLevel=fileLogLevel
    def paramSetLogLevelInternal(self, userInput):
        def determineLevel(s):
            toMatch=s.lower()
            if toMatch == 'debug':
                return DEBUG
            elif toMatch == 'info':
                return INFO
            elif toMatch == 'warn':
                return WARN
            elif toMatch == 'warning':
                return WARNING
            elif toMatch == 'error':
                return ERROR
            elif toMatch == 'critical':
                return CRITICAL
            else:
                return NONE
        inputList = userInput.split(',')
        if len(inputList) >= 2:
            self.consoleLogLevel = determineLevel(inputList[0])
            self.fileLogLevel = determineLevel(inputList[1])
        elif len(inputList) == 1:
            self.consoleLogLevel = determineLevel(inputList[0])
            self.fileLogLevel = NONE
        else:
            pass
    def paramSetLogLevel(self, userInput):
        if inspect.getmodule(inspect.stack()[1][0]).__name__ == '__main__':
            paramSetLogLevelInternal(userInput)
    def debug(self, message):
        self.pendingMessages.put([DEBUG, message, self.getMeta()])
    def info(self, message):
        self.pendingMessages.put([INFO, message, self.getMeta()])
    def warn(self, message):
        self.pendingMessages.put([WARN, message, self.getMeta()])
    def warning(self, message):
        self.pendingMessages.put([WARNING, message, self.getMeta()])
    def error(self, message):
        self.pendingMessages.put([ERROR, message, self.getMeta()])
    def critical(self, message):
        self.pendingMessages.put([CRITICAL, message, self.getMeta()])
