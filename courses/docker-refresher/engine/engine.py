class DockerRefresherEngine:
    def __init__(self):
        self.modules = {
            1: "Docker Basics",
            2: "Images & Containers",
            3: "Volumes & Networks",
            4: "Docker Compose",
            5: "Security & Hardening"
        }

    def run_module(self, module_id):
        if module_id in self.modules:
            print(f"Running Docker Module {module_id}: {self.modules[module_id]}")
        else:
            print("Invalid module ID")
