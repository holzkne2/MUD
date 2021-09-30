import time

class ElapsedTimer:
    def __init__(self, amount):
        self.start_time = time.time()
        self.time = amount

    def Elapsed(self):
        return self.time <= time.time() - self.start_time

    def Sleep(self):
        amount = self.time - (time.time() - self.start_time)
        if (amount > 0):
            time.sleep(amount)