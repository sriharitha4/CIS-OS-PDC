import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Class to represent a Task with a name, start time, and duration
class Task:
    def __init__(self, name, start, duration):
        self.name = name
        self.start = start
        self.duration = duration

# Function to create and display the Gantt chart
def create_gantt_chart(tasks):
    fig, ax = plt.subplots(figsize=(10, 6))  
    y_labels = list(tasks.keys())  
    y_pos = range(len(y_labels))  

    # Loop through each thread and its tasks to add them to the Gantt chart
    for i, (label, task_list) in enumerate(tasks.items()):
        for task in task_list:
            # Add a bar for each task
            ax.broken_barh([(task.start, task.duration)], (i - 0.4, 0.8), facecolors=('tab:blue'))
            # Add task name text in the middle of the bar
            ax.text(task.start + task.duration / 2, i, task.name, va='center', ha='center', color='white')

    # Set the y-axis labels and positions
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time') 
    ax.set_ylabel('Thread/Process')  
    ax.grid(True)  
    plt.show()  

# Function to get task input from the user
def get_task_input(thread_id, task_id):
    print(f"\nEnter details for Task {task_id} in Thread {thread_id}:")
    name = input("Task Name: ")  
    start = int(input("Start Time: "))  
    duration = int(input("Duration: "))  
    return Task(name, start, duration)  

# Main function to gather inputs and create the Gantt chart
def main():
    num_threads = 2  # Limiting the Number of threads 
    num_tasks_per_thread = 3  # Limiting the Number of tasks per thread 
    
    tasks = {}  
    for thread_id in range(1, num_threads + 1): 
        thread_tasks = []  
        for task_id in range(1, num_tasks_per_thread + 1):  
            task = get_task_input(thread_id, task_id)  
            thread_tasks.append(task)  
        tasks[f'Thread {thread_id}'] = thread_tasks  

    create_gantt_chart(tasks)  # Create and display the Gantt chart with the collected tasks

if __name__ == "__main__":
    main()  
