class Logger:
    # log a message to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def log(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Log: " + data[0], other)
        # TODO, add to GUI

    # log an error to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def error(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Error: " + data[0], other)
        # TODO, add to GUI

    # log a warning to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def warn(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Warning: " + data[0], other)
        # TODO, add to GUI
