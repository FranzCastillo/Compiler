from src.controller import Controller
from src.view.text_editor import TextEditor


def __main__():
    controller = Controller()
    editor = TextEditor(controller)
    editor.run()
    # The text editor will call the controller's run_file method when the user clicks on the 'Run' button.


if __name__ == "__main__":
    __main__()
