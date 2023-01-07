import sys

sys.path.append("./GUI")
import GUI.main as main

# from main import setLogLabel


class Logger:

    # log a message to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def log(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Log: " + data[0], other)
        main.setLogLabel(str(" ".join(map(str, data))), "gray")
        # setLogLabel("Log: " + data[0] + str(other), "green")

    # log an error to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def error(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Error: " + data[0], other)
        main.setLogLabel(str(" ".join(map(str, data))), "red")
        # setLogLabel("Error: " + data[0] + str(other), "red")

    # log a warning to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def warn(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Warning: " + data[0], other)
        main.setLogLabel(str(" ".join(map(str, data))), "orange")
        # setLogLabel("Warning: " + data[0] + str(other), "orange")
