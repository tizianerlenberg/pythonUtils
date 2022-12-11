# logHandler

A logging Library for python.

Features:
- Support for multiple threads
- Support for multiple .py files
- Logging can be done to console and/or to a logfile
- Logging to the file and the console will be done in *one thread for the entire program*.
- Color coded console output


The Python file which has the \_\_name\_\_ "\_\_main\_\_" determaines the Log-Level.
Always import logHandler first, so other imported modules can see that logHandler is already imported.

Example code:

```python
import logHandler
logger = logHandler.Logger(consoleLogLevel=logHandler.DEBUG, fileLogLevel=logHandler.ERROR).start()
# YOUR IMPORTS GO HERE
# YOUR CODE GOES HERE

# EXAMPLE LOGGING
logger.debug('Log of Level: debug')
logger.info('Log of Level: info')
logger.warn('Log of Level: warn')
logger.warning('Log of Level: warning')
logger.error('Log of Level: error')
logger.critical('Log of Level: critical')
``` 

You can also make logHandler process a paramter passed to the programm.
You can now start the program with `program_name -ll debug,debug` or `program_name --log-level debug,debug`
where `debug,debug` means consoleLogLevel and fileLogLevel respectively.

```python
import logHandler
logger = logHandler.Logger(processParams=True).start()
# YOUR IMPORTS GO HERE
# YOUR CODE GOES HERE

# EXAMPLE LOGGING
logger.debug('Log of Level: debug')
logger.info('Log of Level: info')
logger.warn('Log of Level: warn')
logger.warning('Log of Level: warning')
logger.error('Log of Level: error')
logger.critical('Log of Level: critical')
``` 

If you want to use argparse, just do it like this (logHandler will process the parameters whether you use argpars or not, but
if you specify the parameters in argparse, you will get a nice "--help" output and better error handling):


```python
import logHandler
logger = logHandler.Logger(processParams=True).start()

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

	# EXAMPLE LOGGING
	logger.debug('Log of Level: debug')
	logger.info('Log of Level: info')
	logger.warn('Log of Level: warn')
	logger.warning('Log of Level: warning')
	logger.error('Log of Level: error')
	logger.critical('Log of Level: critical')

if __name__ == '__main__':
	main()
``` 
