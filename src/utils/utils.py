import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f'Executing {args[0].__class__.__name__} {func.__name__}')
        output = func(*args, **kwargs)
        print(f"Time taken by {func.__name__} : {(time.time() - start)/60:.2f} mins")
        return output
    return wrapper