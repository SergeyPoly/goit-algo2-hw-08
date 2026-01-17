import time
from collections import deque
from typing import Dict


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.user_requests: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id not in self.user_requests:
            return

        window = self.user_requests[user_id]

        while window and current_time - window[0] >= self.window_size:
            window.popleft()

        if not window:
            del self.user_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if user_id not in self.user_requests:
            return True

        return len(self.user_requests[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if not self.can_send_message(user_id):
            return False

        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()

        self.user_requests[user_id].append(current_time)
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        if user_id not in self.user_requests:
            return 0.0

        window = self.user_requests[user_id]

        if len(window) < self.max_requests:
            return 0.0

        earliest_time = window[0]
        wait_time = self.window_size - (current_time - earliest_time)
        return max(0.0, wait_time)
