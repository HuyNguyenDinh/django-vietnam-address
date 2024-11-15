from locust import HttpUser, task, between

class LoadTest(HttpUser):
    # Simulates a wait time between each user action
    wait_time = between(1, 3)

    @task
    def get_ward(self):
        # Perform a GET request to the specified URL
        self.client.get("/vietnam/ward/")

    @task
    def get_province(self):
        # Perform a GET request to the specified URL
        self.client.get("/vietnam/province/")

    @task
    def get_district(self):
        # Perform a GET request to the specified URL
        self.client.get("/vietnam/district/")

    @task
    def get_administrative_unit(self):
        # Perform a GET request to the specified URL
        self.client.get("/vietnam/administrative_unit/")

    @task
    def get_administrative_region(self):
        # Perform a GET request to the specified URL
        self.client.get("/vietnam/administrative_region/")
