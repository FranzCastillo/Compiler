from src.controller import Controller
from src.view.text_editor import TextEditor


def __main__():
    controller = Controller()
    editor = TextEditor(controller)
    editor.run()


if __name__ == "__main__":
    __main__()
