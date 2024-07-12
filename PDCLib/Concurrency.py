import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from time import sleep, time
from threading import Thread, Event, Lock

# https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval
class SetInterval:
    def __init__(self,interval,action) :
        self.interval = interval
        self.action = action
        self.stopEvent = Event()
        thread = Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime= time()+self.interval
        while not self.stopEvent.wait(nextTime-time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()

# ============================================

class Screen:
    focus = None
    render_interval = None

    @staticmethod
    def redraw_task():
        if Screen.focus == None:
            return
        clear_output(True)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, Screen.focus.width() - 1)
        ax.set_ylim(0, Screen.focus.height() - 1)
        ax.axis('off')
        ax.imshow(Screen.focus.pixels)
        plt.show()
        if Screen.focus.is_drawn():
            Screen.render_interval.cancel()
            Screen.focus = None

    def __init__(self) -> None:
        self.pixels = np.zeros((35, 60, 3), dtype=np.uint8)
        self.drawn = np.zeros((35, 60), dtype=np.bool8)
        self.complete = False
        self.mutex = Lock()
        Screen.focus = self
        Screen.render_interval = SetInterval(.25, Screen.redraw_task)

    def __getitem__(self, pos: tuple[int, int]) -> tuple[int, int, int]:
        return self.pixels[pos[1], pos[0]]
    
    def __setitem__(self, pos: tuple[int, int], rgb: tuple[int, int, int]) -> None:
        self.pixels[pos[1], pos[0]] = rgb
        self.drawn[pos[1], pos[0]] = 1
        sleep(.25)

    def is_drawn(self) -> bool:
        for x in self.drawn:
            for y in x:
                if y == 0:
                    return False
        return True

    def width(self) -> int:
        return 60
    
    def height(self) -> int:
        return 35