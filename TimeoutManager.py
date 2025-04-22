from queue import PriorityQueue
from TimeoutItem import TimeoutItem

class TimeoutManager:
    def __init__(self, clock):
        # The pq attribute is the priority queue for timeout items. The
        # timeout item with the lowest callback time is the first to be
        # dequeued.
        self.pq = PriorityQueue()
        
        # The clock attribute is a clock used to get the current time in the
        # add_timeout() and update() methods
        self.clock = clock
    
    # Returns a reference to this timeout manager's internal priority queue.
    # Used only for grading purposes.
    def get_priority_queue(self):
        return self.pq
    
    # Adds a timeout item, given a callback function and delay time as
    # parameters. The added timeout expires at:
    # (clock's current time when this function is called) + (delay time)
    def add_timeout(self, callback, delay_before_callback):
        current_time = self.clock.get_time()
        callback_time = current_time + delay_before_callback
        timeout_item = TimeoutItem(callback, callback_time)
        self.pq.put(timeout_item)
    
    # Dequeues each expired timeout item from the priority queue and calls each
    # expired item's callback function.
    def update(self):
        current_time = self.clock.get_time()
        while not self.pq.empty() and self.pq.queue[0].callback_time <= current_time:
            expired_item = self.pq.get()
            expired_item.callback_function()