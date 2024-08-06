import time 
import timeit
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import random
from IPython.display import display, clear_output

def run_series(button_click):
    clear_output(wait=True)
    display(button)
    finite_times = []
    infinite_times = []

    for _ in range(10):
        a = random.randint(1, 10)
        r = random.random()
        n = random.randint(1, 10)
        A = random.randint(1, 10)
        R = random.random()

        start_finite = timeit.default_timer()
        time_finiteseries(a, r, n)
        end_finite = timeit.default_timer()
        finite_times.append(end_finite - start_finite)

        start_infinite = timeit.default_timer()
        time_infiniteseries(A, R)
        end_infinite = timeit.default_timer()
        infinite_times.append(end_infinite - start_infinite)
    
    tasks = []
    current_time = 0 
    
    for i, (ft, it) in enumerate(zip(finite_times, infinite_times), 1):
        tasks.append({'Task': f'Finite Series Run {i}', 'Start': current_time, 'End': current_time + ft})
        current_time += ft
        tasks.append({'Task': f'Infinite Series Run {i}', 'Start': current_time, 'End': current_time + it})
        current_time += it

    df = pd.DataFrame(tasks)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for task in df.itertuples():
        ax.barh(task.Task, task.End - task.Start, left=task.Start, color='skyblue' if 'Finite' in task.Task else 'lightgreen')
    
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Tasks')
    ax.set_title('Gantt Chart for Function Execution Times')
    ax.set_xticks(range(int(current_time) + 1))
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    total_finite_time = sum(finite_times)
    total_infinite_time = sum(infinite_times)
    total_time = total_finite_time + total_infinite_time

    labels = ['Finite Series', 'Infinite Series']
    sizes = [total_finite_time / total_time * 100, total_infinite_time / total_time * 100]
    colors = ['skyblue', 'lightgreen']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title('Total Percentage Running Time of Each Function')
    plt.show()

    a = random.randint(1, 10)
    r = random.random()
    n = random.randint(1, 10)
    A = random.randint(1, 10)
    R = random.random()

    finite_result = finiteseries(a, r, n)
    infinite_result = infiniteseries(A, R)
    
    print(f"Finite series sum: {finite_result}")
    print(f"Infinite series sum: {infinite_result}")
