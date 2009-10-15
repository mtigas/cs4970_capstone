# coding=utf-8
"""
Provides a call_in_bg wrapper function that allows calling a function
in the background of a Django view. When used in a view, the response
can be returned while the given task continues to operate.
"""
from threading import Thread
from django.db.connection import close as close_db

def db_threadsafe(func):
    """
    Close active Django DB connection inherited from parent
    (forces the next DB request to create a new connection).
    Allows multiple child threads/processes to access DB
    concurrently since they will all have to create their own
    separate connections to the DB.
    """
    
    def wrapped_func(*args, **kwargs):
        try:
            close_db()
        except db.InterfaceError:
            # Connection is already dead
            pass
        return func(*args, **kwargs)
    
    return wrapped_func

def call_in_bg(function,args=[],kwargs={}):
    """
    Similar API to Python's threading.Thread.
    Calls function in the background. Wraps function in a decorator that
    causes Django DB connection (inherited from parent) to close, so that
    the child creates it's own connection -- this is utterly required for
    thread/process safety since the parent DB connection cannot be shared.
    
    Would use multiprocessing.Process, but Process appears to block the calling
    thread, no matter what, which defeats any attempt at pushing tasks to
    the background.
    """
    thread = Thread(
        target=db_threadsafe(function),
        args=args,
        kwargs=kwargs
    )
    thread.daemon = False
    thread.start()
    return None
