class PowerShellRefresherEngine:
    def __init__(self):
        self.modules = {
            1: "PowerShell Fundamentals",
            2: "Objects & Pipelines",
            3: "Scripting Essentials",
            4: "Windows Internals",
            5: "Offensive & Defensive PowerShell"
        }

    def run_module(self, module_id):
        if module_id in self.modules:
            print(f"Running PowerShell Module {module_id}: {self.modules[module_id]}")
        else:
            print("Invalid module ID")
