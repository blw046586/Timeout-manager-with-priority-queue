class MillisecondClock:
    # Returns an integer representing the clock's current time, in milliseconds
    def get_time(self):
        pass

# TestClock implements a clock that stores a time set by code external to the
# class.
class TestClock(MillisecondClock):
    def __init__(self):
        self.current_time = 0
    
    def get_time(self):
        return self.current_time
    
    # Sets this clock's current time, provided the new time is greater than the
    # previously set time.
    def set_time(self, new_time):
        # Only allow time to move forward
        if new_time > self.current_time:
            self.current_time = new_time
            return True
        return False