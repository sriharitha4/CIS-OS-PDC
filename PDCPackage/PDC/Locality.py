import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import display, clear_output, HTML

"""
    Logic
"""

class Memory:
    def __init__(self, len) -> None:
        self.data = np.random.randint(0, 100, len)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, key: int) -> None:
        return self.data[key]

    def __setitem__(self, key: int, value: int) -> None:
        self.data[key] = value

class Cache:
    def __init__(self, cache_len) -> None:
        self.data = [ [None, 0] ] * cache_len

    def map(self, key: int) -> int:
        return key % len(self.data)
    
    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, key: int) -> bool:
        for cell in self.data:
            if cell[0] == key:
                return True
        return False
    
    def __getitem__(self, key: int) -> int:
        return self.data[self.map(key)]
    
    def __setitem__(self, key: int, value: int) -> None:
        self.data[self.map(key)] = [key, value]

class Data:
    def __init__(self, mem_len: int, cache_len: int) -> None:
        self.memory = Memory(mem_len)
        self.cache = Cache(cache_len)
        self.total_fetches = 0
        self.total_misses = 0
        self.actions = [ ]

    def add_action(self, string: str, highlight: list[tuple[str, int, str]] = [ ]) -> tuple[str, list[tuple[str, int, str]], list[int], list[list[int]], int, int]:
        return self.actions.append((string, highlight, list(self.memory.data), list(self.cache.data), self.total_fetches, self.total_misses))

    def __len__(self) -> int:
        return len(self.memory.data)

    def __getitem__(self, key: int) -> int:
        self.total_fetches += 1
        if key in self.cache:
            self.add_action(f"Cache Hit, Address={key}", [ ("cache", key, "green"), ("memory", key, "green") ])
        else:
            self.total_misses += 1
            self.add_action(f"Cache Miss, Address={key}", [ ("memory", key, "red") ])
            self.cache[key] = self.memory[key]
            self.add_action(f"Moving Address={key} to Cache", [ ("cache", key, "green") ])
            # More of how a cache works
            #if key + 1 < len(self.memory):
            #    self.cache[(key + 1)] = self.memory[key + 1]
            #if key + 2 < len(self.memory):
            #    self.cache[(key + 2)] = self.memory[key + 2]
        return self.cache[key][1]

    def __setitem__(self, key: int, value: int) -> None:
        self.__getitem__(key)
        self.memory[key] = value
        self.cache[key] = value
        self.add_action(f"Updating Address={key} to Value={value}", [( "cache", key, "purple" ), ("memory", key, "purple")])


"""
    Rendering / User
"""

def animate(data, *fargs) -> None:
    string, highlights, memstate, cachestate, fetches, misses = data
    ax, missRateText, memoryTexts, memoryBoxes, cacheTexts, cacheBoxes = fargs

    for text, box, value in zip(memoryTexts, memoryBoxes, memstate):
        box.set_edgecolor('b')  # Reset color to blue
        text.set_color('black')
        text.set_text(str(value))

    for text, box, value in zip(cacheTexts, cacheBoxes, cachestate):
        box.set_edgecolor('b')  # Reset color to blue
        text.set_color('black')
        text.set_text(f"{value[0]}:{value[1]}" if value[0] != None else "∅")

    for (type, addr, color) in highlights:
        if type == "memory":
            memoryBoxes[addr].set_edgecolor(color)
        elif type == "cache":
            cacheBoxes[addr % len(cacheBoxes)].set_edgecolor(color)

    ax.set_title(string, fontsize=16)
    if fetches != 0:
        missRateText.set_text(f"Miss Rate: {(misses / fetches):.2f}")

    plt.draw()


def render(data: Data) -> None:
    clear_output()
    
    data.add_action("Finished")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, max(len(data.memory), 3) + 1)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    
    ax.text(-.8, 0.5, 'Memory', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(-0.7, -1.5, 'Cache', ha='center', va='center', fontsize=14, fontweight='bold')

    memoryTexts = []
    memoryBoxes = []
    cacheTexts = []
    cacheBoxes = []
    missRateText = ax.text(-0.5, 1.5, f"Miss Rate: ∅", ha='center', va='center', fontsize=14, fontweight='bold')
 
    for i in range(len(data.memory)):
        memoryText = ax.text(i + 0.5, 0.5, str(data.memory[i]), ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='b'))
        memoryBox = plt.Rectangle((i, 0), 1, 1, fill=None, edgecolor='blue')
        ax.add_patch(memoryBox)
        memoryTexts.append(memoryText)
        memoryBoxes.append(memoryBox)

    for i in range(len(data.cache)):
        cacheText = ax.text(i + 0.5, -1.5, "∅", ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', edgecolor='b'))
        cacheBox = plt.Rectangle((i, -2), 1, 1, fill=None, edgecolor='blue')
        ax.add_patch(cacheBox)
        cacheTexts.append(cacheText)
        cacheBoxes.append(cacheBox)
    
    ani = FuncAnimation(fig, animate, frames=data.actions, fargs=(ax, missRateText, memoryTexts, memoryBoxes, cacheTexts, cacheBoxes), interval=1000, repeat=False)
    plt.close(fig)
    display(HTML(ani.to_jshtml()))
    data.actions = [ ]
