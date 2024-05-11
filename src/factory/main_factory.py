class Factory:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def create_main(self):
        with open("templates/main_template.py", "r") as file:
            with open(f"{self.output_path}/main.py", "w") as main_file:
                main_file.write(file.read())
