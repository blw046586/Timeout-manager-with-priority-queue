# Timeout-manager-with-priority-queue
Timeout manager overview
A timeout manager stores a priority queue of timeout items, each a (callback function, callback time) pair. Each callback function is called approximately N milliseconds after the timeout is set, where N is the delay specified when adding the timeout item. Ex:

At time t = 0, a 500 millisecond timeout is set for function A
At time t = 100, a 3000 millisecond timeout is set for function B
At time t = 2000, a 1000 millisecond timeout is set for function C
So the timeout manager should call the callbacks as follows:

Call function A at time t = 0 + 500 = 500
Call function C at time t = 2000 + 1000 = 3000
Call function B at time t = 100 + 3000 = 3100
A timeout item with a callback time ≤ the current time is said to be "expired".

Millisecond-level callback precision is often unfeasible. So a timeout manager typically has an update function that is called by external code every so often, ex: every 100 milliseconds. The manager's update function calls each expired timeout's callback function.


Step 1: Inspect TimeoutItem.py
Inspect the TimeoutItem class declaration in the read-only TimeoutItem.py file. The callback_time attribute stores the time the item was added plus the item's delay. Ex: A TimeoutItem created at t = 500 with a delay of 1000 has callbackTime = 500 + 1000 = 1500. The callback_function attribute is the function to call after the timeout expires.

TimeoutItem's comparison operators are implemented so that TimeoutItems can be put in a priority queue that gives higher priority to lesser callback_time values.


Step 2: Inspect Clocks.py
Inspect class declarations in the read-only Clocks.py file. MillisecondClock is a base class for a clock. The get_time() method returns an integer indicating the clock's current time, in milliseconds.

Times are simulated during grading using the TestClock class. TestClock inherits from MillisecondClock and allows the clock's time to be set via the set_time() method.


Step 3: Implement TimeoutManager's add_timeout() and update() methods
Complete the TimeoutManager class implementation in TimeoutManager.py. add_timeout() must add a new TimeoutItem to the priority queue that expires delay_before_callback milliseconds after the current time. update() must dequeue and call the callback function for each expired timeout item. Use TimeoutManager's self.clock object to get the current time.


Step 4: Test code, then submit
File main.py contains two automated tests. Each adds timeouts and invokes updates at various times, then verifies that the proper callback functions are called during each update. Additional tests can be added, if desired. Run your code and ensure that the two tests in main.py pass before submitting code for grading.
