class Logger:
  def log(*data) -> None:
    other = list(data)[1::]
    print(data[0], other)
    # TODO, add to GUI

  def error(*data) -> None:
    other = list(data)[1::]
    print("Error: " + data[0], other)
    # TODO, add to GUI

  def warn(*data) -> None:
    other = list(data)[1::]
    print("Warning: ", data[0], other)
    # TODO, add to GUI