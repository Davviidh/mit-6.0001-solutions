'''Thread-safe version of Tkinter.
Modified for Python 3 compatibility.
'''

from tkinter import *
import tkinter as Tkinter
import sys
import queue
import threading

__all__ = Tkinter.__all__

# Create an event type for custom events
import collections
Event = collections.namedtuple('Event', 'func args kwargs response')

_main_thread = threading.current_thread()
_event_queue = queue.Queue()
_root = None

def _CheckEvents():
    global _root
    if _root is None:
        return
    
    while not _event_queue.empty():
        try:
            event = _event_queue.get_nowait()
        except queue.Empty:
            break
            
        try:
            res = event.func(*event.args, **event.kwargs)
            event.response.put((False, res))
        except SystemExit as ex:
            event.response.put((True, (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])))
            raise ex
        except Exception as ex:
            event.response.put((True, (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])))
            
    _root.after(100, _CheckEvents)

class MTProxy(object):
    def __init__(self, target):
        self.__target = target

    def __getattr__(self, name):
        attr = getattr(self.__target, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                if threading.current_thread() == _main_thread:
                    return attr(*args, **kwargs)
                else:
                    response = queue.Queue()
                    _event_queue.put(Event(attr, args, kwargs, response))
                    isException, res = response.get()
                    if isException:
                        exType, exValue, exTb = res
                        raise exValue.with_traceback(exTb)
                    return res
            return wrapper
        return attr

original_tk = Tkinter.Tk

class Tk(original_tk):
    def __init__(self, *args, **kwargs):
        global _root, _main_thread
        _main_thread = threading.current_thread()
        original_tk.__init__(self, *args, **kwargs)
        _root = self
        self.tk = MTProxy(self.tk)
        self.after(100, _CheckEvents)

Tkinter.Tk = Tk