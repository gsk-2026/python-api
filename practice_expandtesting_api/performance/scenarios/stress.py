from locust import LoadTestShape


class StressTestShape(LoadTestShape):
    """
    Stress test.
        Gradually increases concurrent users to observe performance degradation.
    """

    stages = [
        { "duration": 120, "users": 25, "spawn_rate": 5 },
        { "duration": 120, "users": 50, "spawn_rate": 10 },
        { "duration": 120, "users": 75, "spawn_rate": 15 },
        { "duration": 120, "users": 50, "spawn_rate": 10 },
        { "duration": 120, "users": 2, "spawn_rate": 1 }
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
