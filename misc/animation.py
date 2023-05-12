from threading import Event, Thread
from time import sleep
import traceback

bigbar = [
"[        ]",
"[=       ]",
"[===     ]",
"[====    ]",
"[=====   ]",
"[======  ]",
"[======= ]",
"[========]",
"[ =======]",
"[  ======]",
"[   =====]",
"[    ====]",
"[     ===]",
"[      ==]",
"[       =]",
"[        ]",
"[        ]"
]

braille = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

def animation(stop_event : Event, end_text : str, animation : list = bigbar, break_time : int=0.4):
    i = 0
    while not stop_event.is_set():
        frame = animation[i % len(animation)]
        print('\r' + frame + ' ' + end_text, end='', flush=True)
        sleep(break_time)
        i += 1
    print() # Print a newline so anything that prints after animation is printed on a fresh line

def process(message : str="Loading...", frames : list=bigbar, break_time : float | int = 0.07):
    def container(func):
        def wrapper(*args, **kwargs):
            stop     = Event()
            thread   = Thread(target=animation, args=(stop, message, frames, break_time))
            thread.daemon = True
            thread.start()
            try:
                result   = func(*args, **kwargs)
            except Exception as e:
                stop.set()
                thread.join()
                sleep(0.2)
                print()
                print(traceback.get_exc())
            stop.set()
            thread.join()
            return result
        return wrapper
    return container

