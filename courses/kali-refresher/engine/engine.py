class KaliRefresherEngine:
    def __init__(self):
        self.modules = {
            1: "Kali Basics",
            2: "Networking & Tools",
            3: "Recon & Enumeration",
            4: "Exploitation Frameworks",
            5: "Post-Exploitation & Reporting"
        }

    def run_module(self, module_id):
        if module_id in self.modules:
            print(f"Running Kali Module {module_id}: {self.modules[module_id]}")
        else:
            print("Invalid module ID")
