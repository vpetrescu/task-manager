# task-manager  library
    
# How To Run tests  locally
Checkout the GitHub actions in .github/workflows/main.yml.  
1. Checkout the code  and go to task-manager folder
`cd task-manager`
2. In the folder task-manager run the command  
`docker build --build-arg python_src=${pwd} -f Dockerfile -t task_manager_pipeline . `
3. Run individual unittest
 `docker run --entrypoint python3 -t taskm -m pytest task_manager_max_size_test.py`

# How to use the task manager as a library
The taskmanager Python library is installed in the image that is build using the provided Dockerfile. Start a container from task_manager_pipeline image:

    docker run -it task_manager_pipeline /bin/bash

You can check the version of the library

    pip3 show taskmanager

You can start python3 on the console and run some commands:

    from task_manager import TaskManagerMaxSize
    tm = TaskManagerMaxSize(3)

# Implementation details & Complexity
The Process class implements the *less than* method  
which is used in sorting a collections of Process objects.  
The processes will be sorted by priority and in case they  
have the same priority by timestamp.  
    
#### Task 1  
TaskManagerMaxSize implements a fixed size TaskManager which drops  
new processes when capacity is reached. The processes are  
stored in a dictionary which maps *pid* -> *Process*  
  
Time complexity : add() -> O(1) , kill() -> O(1)  
  
#### Task 2  
TaskManagerFIFO implements a fixed size TaskManager which  
drops the oldest process. The processes are stored in an OrderedDict.  
Unlike a regular dict, OrderedDict in Python remembers the insertion order of the  keys.  
  
Time complexity:  add() -> O(1), kill() -> O(1)  
  
#### Task 3  
TaskManagerPriorityBased implements priority based manager.  
It holds the processes both in a priority queue and in a dictionary.  
Unlike the previous two methods it has O(2N) space complexity.  

Time Complexity : 
add() -> O(logN) given by the push method  
kill() -> O(N) given by the heapify method  
  
Note: The priority queue was chosen such that time complexity  
of add is not O(NlogN)  
  
#### Task 4  
The list method has O(NlogN)  complexity given by the sorting of the elements.