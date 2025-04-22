class TimeoutItem:
    def __init__(self, callback_function, callback_time):
        self.callback_function = callback_function
        self.callback_time = callback_time
    
    def call_callback(self):
        self.callback_function()
    
    def get_callback_time(self):
        return self.callback_time
    
    def __lt__(self, rhs):
        return self.callback_time < rhs.callback_time
    
    def __le__(self, rhs):
        return self.callback_time <= rhs.callback_time
    
    def __gt__(self, rhs):
        return self.callback_time > rhs.callback_time
    
    def __ge__(self, rhs):
        return self.callback_time >= rhs.callback_time