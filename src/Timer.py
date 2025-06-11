import time

class Timer:
    def __init__(self):
        self.start = time.time()
        self.start_wall = time.time()

    def restart(self):
        self.start = time.time()
        self.start_wall = time.time()

    def elapsed(self) -> float:
        now = time.time()
        return round((now - self.start_wall) * 100, 2) / 100

    def elapsed_process(self) -> float:
        # Python does not provide a direct way to get process times like C++.
        # This is a placeholder for demonstration purposes.
        return 0.0

    def elapsed_user(self) -> float:
        # Placeholder for user time
        return 0.0

    def elapsed_system(self) -> float:
        # Placeholder for system time
        return 0.0