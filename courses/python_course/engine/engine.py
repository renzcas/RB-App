class PythonCourseEngine:
    def run_module(self, module_id):
        try:
            module = __import__(f"courses.python_course.modules.module_{module_id}", fromlist=["run"])
            return module.run()
        except ModuleNotFoundError:
            print(f"Module {module_id} not found.")
