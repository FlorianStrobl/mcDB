import sys
import customtkinter
sys.path.append("./GUI")
import GUI.main as main

# from main import setLogLabel

def createErrorPopup(message,color):
    window = customtkinter.CTkToplevel()
    window.geometry("400x200")
    window.title("Minecraft Database | Fehler ")
    label = customtkinter.CTkLabel(window, text=message)
    label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
# TODO clear message after 5 seconds
class Logger:

    # log a message to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def log(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Log: " + data[0], other)
        x  = str(" ".join(map(str, data)))
        #setLogLabel("Log: " + data[0] + str(other), "green")
        createErrorPopup(x, "gray")
    # log an error to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def error(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Error: " + data[0], other)
        #main.setLogLabel(str(" ".join(map(str, data))), "red")
        # setLogLabel("Error: " + data[0] + str(other), "red")
        x  = str(" ".join(map(str, data)))
        #setLogLabel("Log: " + data[0] + str(other), "green")
        createErrorPopup(x, "red")


    # log a warning to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def warn(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Warning: " + data[0], other)
        #main.setLogLabel(str(" ".join(map(str, data))), "orange")
        # setLogLabel("Warning: " + data[0] + str(other), "orange")
        x  = str(" ".join(map(str, data)))
        #setLogLabel("Log: " + data[0] + str(other), "green")
        createErrorPopup(x, "green")
