import time
import random

class LoadGenerator:
    def __init__(self, master):
        self.master = master

    def send_requests(self):
        request_id = 0
        while True:
            self.master.balance_requests(request_id)
            request_id += 1
            time.sleep(random.randint(1,1))

