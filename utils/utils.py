import time
import sys
import signal
import functools
import traceback
from rich.console import Console
console = Console()

''' lambda functions for response generation '''
generate_response = lambda text,status : {'text':[text],'status':status,'token_count':len(text)}
generate_response_chart = lambda chart=None,chart_type=None: {'chart':str(chart),'chart_type':str(chart_type)}
def test(data):
    time.sleep(2)
    return data
class TimeOutException(Exception):
    '''Raised when process more than alloted time'''

    def __init__(self,message="Operation timed out , please try again"):
        self.message = message
        super().__init__(self.message)

''' this will run the code and also if takes more time than expected then it will kill the thread '''
def kill_after(max_execution_time=30):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeOutException
            if sys.platform == 'win32':
                print("Won't be stopped in windows!")
            else:
                signal.signal(signal.SIGALRM, handle_timeout)
                signal.alarm(max_execution_time)
            try:
                result = func(*args, **kwargs)
            except TimeOutException as e:
                result = {'answer':str(e)}
            except Exception as e:

                result = {'answer':str(traceback.format_exc())}
            if sys.platform != 'win32':
                signal.alarm(0)
            return result
        return wrapper
    return decorator

def api_sleep(sleep_time=1):
    time.sleep(sleep_time)
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
        return wrapper
    return decorator
