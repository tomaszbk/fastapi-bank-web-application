import traceback
import sys
# Create a custom exception
class CustomException(Exception):
    pass

# Define a decorator to catch and print exceptions
def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as ex:
            _, _, exc_tb = sys.exc_info()
            print("E=%s, F=%s, L=%s" % (str(ex), traceback.extract_tb(exc_tb)[-1][0], 
                                        traceback.extract_tb(exc_tb)[-1][1]))
            return None
    return wrapper

# Apply the decorator to a function
@catch_exception
def some_function():
    raise CustomException("An error occurred in some_function")

# Call the decorated function
some_function()
