import unittest

from task_manager import TaskManagerMaxSize, Process, Priority


class TaskManagerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tm = TaskManagerMaxSize(2)
        self.p1 = Process(1, Priority.low)
        self.p2 = Process(2, Priority.medium)
        self.p3 = Process(3, Priority.medium)
        self.p4 = Process(4, Priority.high)

    def test_process_is_discarded(self):
        self.tm.add(self.p1)
        self.tm.add(self.p2)
        self.tm.add(self.p3)
        self.assertEqual(self.tm.current_count(), 2)
        print(self.tm.processes)

        self.tm.kill(1)
        print(self.tm.processes)
        self.assertEqual(self.tm.current_count(), 1)

    def test_kill_all(self):
        self.tm.add(self.p1)
        self.tm.kill_all()
        self.assertEqual(self.tm.current_count(), 0)

    def test_kill_group(self):
        self.tm.add(self.p1)
        self.tm.add(self.p2)
        self.tm.add(self.p3)
        self.tm.kill_group(2,3)
        self.assertEqual(self.tm.current_count(), 1)


if __name__ == '__main__':
    unittest.main()
