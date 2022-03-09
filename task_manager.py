from collections import OrderedDict
from enum import Enum
import heapq
import logging
import time
from typing import List


Priority = Enum("Priority", ["low", "medium", "high"])


class Process(object):
    def __init__(self, pid: int, priority: Priority):
        self.priority = priority
        self.timestamp = time.time()
        self.pid = pid

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.timestamp < other.timestamp
        return self.priority < other.priority

    def kill(self):
        pass


class TaskManagerInterface(object):
    def __init__(self, max_capacity: int):
        self.max_capacity = max_capacity
        self.processes = {}

    def add(self, process: Process):
        pass

    def kill(self, pid: int):
        pass

    def kill_all(self):
        self.processes = {}

    def kill_group(self, *argv):  # O(n)
        for pid in argv:
            self.kill(pid)
        else:
            logging.warning("Process with pid {} was not found".format(pid))

    def list(self):
        print("Timestamp\t ProcessId\t Priority")
        for pid in sorted(self.processes):
            print("{}\t {}\t {}".format(self.processes[pid].timestamp,
                                        pid,
                                        self.processes[pid].priority))

    def current_count(self):
        return len(self.processes)


class TaskManagerMaxSize(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        super().__init__(max_capacity)
        self.processes: dict[int, Process] = {}

    def add(self, process: Process):  # O(1)
        if len(self.processes) == self.max_capacity:
            logging.warning("Process with pid {} was discarded.".format(process.pid))
        elif process.pid in self.processes:
            logging.warning("Process with pid {} already exists.".format(process.pid))
        else:
            self.processes[process.pid] = process

    def kill(self, pid):  # O(1)
        if pid in self.processes:
            del self.processes[pid]
        else:
            logging.warning("Process with pid {} was not found".format(pid))


class TaskManagerFIFO(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        super().__init__(max_capacity)
        self.processes: OrderedDict[int, Process] = OrderedDict({})

    def add(self, process: Process):  # O(1)
        if len(self.processes) == self.max_capacity:
            self.processes.popitem(last=False)
        self.processes[process.pid] = process

    def kill(self, pid):  # O(1)
        if pid in self.processes:
            del self.processes[pid]
        else:
            logging.warning("Process with pid {} was not found".format(pid))


class TaskManagerPriorityBased(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        super().__init__(max_capacity)
        self.processes: dict[int, Process] = {}
        self.priority_queue: List[Process] = []

    def add(self, process: Process):  # O(logN)
        if len(self.processes) == self.max_capacity:
            if self.priority_queue[0].priority < process.priority:
                p = heapq.heappop(self.priority_queue)
                del self.processes[p.pid]
            else:
                logging.warning("Process {} was discarded.".format(process.pid))
                return
        heapq.heappush(self.priority_queue, process)
        self.processes[process.pid] = process

    def kill(self, pid):  # O(n) due to heapify method
        if pid in self.processes:
            for i in range(len(self.priority_queue)):
                if self.priority_queue[i].pid == pid:
                    self.priority_queue[i], self.priority_queue[-1] = self.priority_queue[-1], self.priority_queue[i]
                    heapq.heappop(self.priority_queue)
                    heapq.heapify(self.priority_queue)
                    break
            del self.processes[pid]
        else:
            logging.warning("Process with pid {} was not found".format(pid))

    def kill_all(self):
        super().kill_all()
        self.priority_queue = []
