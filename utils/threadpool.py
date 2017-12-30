""" This is a threadpool module with some workers predefined. """

import time
import uuid

from queue import Queue

from threading import Thread, Lock

TASK_UUID = "task_uuid"
TASK_LOCK = Lock()


def get_uuid():
    """ Grab a UUID in string form """
    return str(uuid.uuid1())


class Worker(Thread):
    def __init__(self, queue, results):
        super(Worker, self).__init__()
        self.stop = False
        self.shutdown = False

        self.queue = queue
        self.results = results

    def run(self):

        while not self.stop:
            func, args, kwargs = self.queue.get()
            task_uuid = kwargs[TASK_UUID]

            try:
                val = func(args, **kwargs)
                with TASK_LOCK:
                    self.results[task_uuid] = val

            except Exception:
                print(e)
            finally:
                self.queue.task_done()

        # Bool to check and make sure thread is complete
        self.shutdown = True

    def shutdown(self, wait_time=60):
        self.stop = True

        # Only wait a minute before
        if wait_time > 0:
            elapsed = 0
            while not self.shutdown:
                if elapsed == wait_time:
                    break

                time.sleep(1)
                elapsed += 1


class ThreadPool(object):
    def __init__(self, num_workers):
        self.queue = Queue(num_workers)
        self.results = {}
        self.workers = [Worker(self.queue, self.results) for _ in range(num_workers)]
        self._shutdown = False

    @property
    def shutdown(self):
        return self._shutdown

    def add_task(self, func, *args, **kwargs):
        """ Create an id to stash the return value from the task added to the queue. """

        # Create a unique index for this job
        task_uuid = get_uuid()
        kwargs[TASK_UUID] = task_uuid

        # Add task tuple
        self.queue.put((func, args, kwargs))
        return task_uuid

    def wait_and_shutdown(self):
        """ Wait for all tasks to complete, and shutdown workers. """
        self.queue.join()
        [w.shutdown() for w in self.workers]
        self._shutdown = True

    def get_results(self, uuid):
        """ Get the results for a given UUID. """
        return self.results[uuid]

