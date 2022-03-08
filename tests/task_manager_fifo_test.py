import unittest

from task_manager import TaskManagerFIFO, Process


class TaskManagerFIFOTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tm = TaskManagerFIFO(2)
        self.p1 = Process(1, "low")
        self.p2 = Process(2, "medium")
        self.p3 = Process(3, "medium")
        self.p4 = Process(4, "high")

    def test_process_is_discarded(self):
        self.tm.add(self.p1)
        self.tm.add(self.p2)
        self.tm.add(self.p3)
        self.assertEqual(self.tm.current_count(), 2)

        self.assertTrue(3 in self.tm.processes)
        self.assertTrue(1 not in self.tm.processes)

        self.tm.kill(1)
        self.assertEqual(self.tm.current_count(), 2)

    def test_kill_all(self):
        self.tm.add(self.p1)
        self.tm.kill_all()
        self.assertEqual(self.tm.current_count(), 0)

    def test_kill_group(self):
        self.tm.add(self.p1)
        self.tm.add(self.p2)
        self.tm.add(self.p3)
        self.tm.kill_group(2, 3)
        self.assertEqual(self.tm.current_count(), 0)


if __name__ == '__main__':
    unittest.main()
