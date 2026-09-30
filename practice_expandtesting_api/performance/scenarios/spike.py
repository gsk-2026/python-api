from locust import LoadTestShape


class SpikeTestShape(LoadTestShape):
    """
    Spike test.
        Normal: 5, 10 users
        Spike: 100 users
        Recovery: 10, 5 users
    """

    stages = [
        { "duration": 120, "users": 2,  "spawn_rate": 1 },
        { "duration": 120, "users": 10, "spawn_rate": 2 },
        { "duration": 120, "users": 100, "spawn_rate": 50 },
        { "duration": 120, "users": 10, "spawn_rate": 2 },
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
