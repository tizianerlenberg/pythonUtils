# logHandler

A logging Library for python.

Features:
- Support for multiple threads
- Support for multiple .py files
- Logging can be done to console and/or to a logfile
- Logging to the file and the console will be done in *one thread for the entire program*.
- Color coded console output


The Python file which has the \_\_name__ "\_\_main__" determaines the Log-Level.
Always import logHandler first, so other imported modules can see that logHandler is already imported.
To make sure the logging thread gets closed correctly you have to enclose your *entire code* in a try...finally block:

```python
import logHandler
logger = logHandler.Logger(consoleLogLevel=logHandler.DEBUG, fileLogLevel=logHandler.DEBUG)
try:
	logger.start()

	# EXAMPLE LOGGING
	logger.debug('Log of Level: debug')
	logger.info('Log of Level: info')
	logger.warn('Log of Level: warn')
	logger.warning('Log of Level: warning')
	logger.error('Log of Level: error')
	logger.critical('Log of Level: critical')
	
	# YOUR IMPORTS AND CODE GOES HERE
finally:
	logger.stop()
``` 

Alternatively you can use the open...as block (recommended):

```python
import logHandler
with logHandler.Logger(consoleLogLevel=logHandler.DEBUG, fileLogLevel=logHandler.DEBUG) as logger:

	# EXAMPLE LOGGING
	logger.debug('Log of Level: debug')
	logger.info('Log of Level: info')
	logger.warn('Log of Level: warn')
	logger.warning('Log of Level: warning')
	logger.error('Log of Level: error')
	logger.critical('Log of Level: critical')
	
	# YOUR IMPORTS AND CODE GOES HERE
``` 

You can also use a methode to set Log-Levels like this:


```python
import logHandler
with logHandler.Logger() as logger:

    def main():
        import argparse
        parser = argparse.ArgumentParser(description=
            """Your Program description""")
        parser.add_argument('-ll', '--log-level',
            help='Set the Log-Level. Use like this:\n' + 
            'write "--log-level debug,info" to set the level for the console at debug and for the logfile at info\n' +
            'write "--log-level none,error" to write all errors to the logfile and not write to the console',
            default = "none")
        args = parser.parse_args()
        logger.paramSetLogLevel(args.log_level)

        # EXAMPLE LOGGING
        logger.debug('Log of Level: debug')
        logger.info('Log of Level: info')
        logger.warn('Log of Level: warn')
        logger.warning('Log of Level: warning')
        logger.error('Log of Level: error')
        logger.critical('Log of Level: critical')

        # YOUR IMPORTS AND CODE GOES HERE

	if __name__ == '__main__':
		main()
``` 
