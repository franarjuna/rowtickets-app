import functools
import time

from django.db import connection


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f'Function : {func.__name__}')
        print(f'Number of Queries : {end_queries - start_queries}')
        print(f'Finished in : {(end - start):.2f}s')
        return result

    return inner_func


def query_debugger_detailed(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        print(f'Function : {func.__name__}')

        for query in connection.queries:
            print(query)

        print(f'Finished in : {(end - start):.2f}s')
        return result

    return inner_func
