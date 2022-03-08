from enum import Enum
from collections import OrderedDict
from typing import List
import time
import heapq
import logging

Priority = Enum("Priority", ["low", "medium", "high"])


class Process(object):
    def __init__(self, pid: int, priority: Priority):
        self._priority = priority
        self._timestamp = time.time()
        self._pid = pid

    def __lt__(self, other):
        if self._priority == other.priority:
            return self._timestamp < other.timestamp
        return self._priority < other.priority

    def kill(self):
        pass


class TaskManagerInterface:
    def add(self, process: Process):
        pass

    def kill(self, pid:int):
        pass

    def kill_all(self):
        pass

    def kill_group(self, *argv):  # O(n)
        for pid in argv:
            self.kill(pid)
        else:
            logging.warn("Process with pid {} was not found".format(pid))

    def list(self):
        print("Timestamp\t ProcessId\t Priority")
        for pid in sorted(self.processes.items()):
            print("{}\t {}\t {}".format(self.processes[pid].timestamp,
                                        pid,
                                        self.processes[pid].priority))


class TaskManagerMaxSize(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        self.processes: dict[int, Process] = {}
        self.max_capacity = max_capacity

    def add(self, process: Process):
        if len(self.processes) < self.max_capacity:
            self.processes[process.pid] = process
        else:
            logging.warn("Process was discarded.")

    def kill(self, pid):  # O(n)
        if pid in self.processes:
            del self.processes[pid]
        else:
            logging.warn("Process with pid {} was not found".format(pid))


class TaskManagerFIFO(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        self.processes: OrderedDict = {}
        self.max_capacity = max_capacity

    def add(self, process: Process):  # O(1)
        if len(self.processes) < self.max_capacity:
            self.process.popitem()
        self.processes[process.pid] = process

    def kill(self, pid):  # O(n)
        if pid in self.processes:
            del self.processes[pid]
        else:
            logging.warn("Process with pid {} was not found".format(pid))


class TaskManagerPriorityBased(TaskManagerInterface):
    def __init__(self, max_capacity: int):
        self.processes: dict[int, Process] = {}
        self.priority_queue: List[Process] = []
        self.max_capacity = max_capacity

    def add(self, process: Process):  # O(1)
        if len(self.processes) < self.max_capacity:
            self.processes[process.pid] = process
            heapq.heappush(self.priority_queue, process)
        else:
            logging.warn("Process was discarded.")

    def kill(self, pid):  # O(n)
        if pid in self.processes:
            heapq.heappop(self.priority_queue)
            del self.processes[pid]
        else:
            logging.warn("Process with pid {} was not found".format(pid))

    def kill_all(self):
        super().kill_all()
        self.priority_queue = []
