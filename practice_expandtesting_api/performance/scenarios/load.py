from locust import LoadTestShape


class LoadTestShape(LoadTestShape):
    """
    Normal load test.
        Stage 1: 10 users
        Stage 2: 25 users
    """

    stages = [
        { "duration": 120, "users": 10, "spawn_rate": 5 },
        { "duration": 120, "users": 25, "spawn_rate": 10 },
        { "duration": 60, "users": 2, "spawn_rate": 1 }
    ]

    def tick(self):
        run_time = self.get_run_time()
        total_duration = 0
        for stage in self.stages:
            total_duration += stage["duration"]
            if run_time < total_duration:
                return (
                    stage["users"],
                    stage["spawn_rate"]
                )
        return None
