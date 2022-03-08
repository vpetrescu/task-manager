# task-manager
Task Manager implementation

The Process class implements the less than method
which is used in sorting a collections of Process objects.
The processes will be sorted by priority and in case they
have the same priority by timestamp.

The TaskManagerInterface defines the methods

#### Task 1
TaskManagerMaxSize implements a fixed size TaskManager which drops
new processes when capacity is reached. The processes are
stored in a dictionary which maps pid -> Process

Time complexity

add() -> O(1)
kill() -> O(1)

#### Task 2
TaskManagerFIFO implements a fixed size TaskManager which
drops last processes. The processes are stored in an OrderedDict.
Unlike a regular dict, OrderedDict remembers the insertion order of the 
keys.

Time complexity

add() -> O(1)
kill() -> O(1)

#### Task 3
TaskManagerPriorityBased implements priority based manager.
It holds the processes both in a priority queue and in a dictionary.
Unlike the previous two methods it has O(2N) space complexity.
Time Complexity

add() -> O(logN) given by the push method
kill() -> O(N) given by the heapify method

Note: The priority queue was chosen such that time complexity
of add is not O(NlogN)

#### Task 4