import threading
import time
import queue
from typing import List, Any

class SlaveProcessor(threading.Thread):
    def __init__(self, slave_id: int, task_queue: queue.Queue, timeout: float = 1.0):
        threading.Thread.__init__(self)
        self.slave_id = slave_id
        self.task_queue = task_queue
        self.timeout = timeout
        self.running = True
    
    def run(self) -> None:
        while self.running:
            try:
                task = self.task_queue.get(timeout=self.timeout)
                print(f"🟢 Slave {self.slave_id} starts: {task}")
                time.sleep(2) 
                print(f"🔴 Slave {self.slave_id} finish: {task}")
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Slave {self.slave_id} error: {e}")
    
    def stop(self) -> None:
        self.running = False


class MasterProcessor:
    def __init__(self, num_slaves: int):
        self.task_queue = queue.Queue()
        self.slaves = [SlaveProcessor(i, self.task_queue) for i in range(num_slaves)]
    
    def assign_tasks(self, tasks: List[Any]) -> None:
        print("Master: Starting slaves...")
        for slave in self.slaves:
            slave.start()
        
        print("Master: Assigning tasks...")
        for task in tasks:
            self.task_queue.put(task)
        
        self.task_queue.join() 
        
        print("Master: Stopping slaves...")
        for slave in self.slaves:
            slave.stop()
            slave.join()  
        
        print("✅ All tasks completed!")


if __name__ == "__main__":
    tasks = ["Task1", "Task2", "Task3", "Task4", "Task5"]
    master = MasterProcessor(num_slaves=3)
    master.assign_tasks(tasks)