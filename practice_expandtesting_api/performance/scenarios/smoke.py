from locust import LoadTestShape


class SmokeTestShape(LoadTestShape):
    """
    Smoke Test
        Load: 2 users
        Ramp-up: 1 user / second
        Duration:  5 minutes
    """

    stages = [ { "duration": 300,  "users": 2,  "spawn_rate": 1, } ]

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
