import sys
import customtkinter

sys.path.append("./GUI")
import GUI.main as main

# from main import setLogLabel

# Macht nach jeden n ten character im String einen "\n" rein
def text_zu_mehrehren_Linien(string, n=38):
    result = []
    for i in range(len(string)):
        char = string[i]
        result.append(char)
        # Wenn durch index durch n teilbar dann kann da im neuen aerary dies erstett werden
        if (i + 1) % n == 0:
            result.append("\n")

    return "".join(result)


def calculateAdditionalHigh(string, maxAnzahlLinien=38):
    heighOneLine = 17
    return ((len(string) // maxAnzahlLinien) * heighOneLine) - heighOneLine


allWindows = []


def createErrorPopup(message, color):

    höheLabel = calculateAdditionalHigh(message)

    global window

    def onOkClick():
        allWindows[len(allWindows) - 1].destroy()
        del allWindows[len(allWindows) - 1]

    window = customtkinter.CTkToplevel()
    window.geometry("300x" + str(120 + (höheLabel if höheLabel > 0 else 0)))
    window.title("Hinweis")
    allWindows.append(window)
    label = customtkinter.CTkLabel(window, text=message, text_color=color)
    label.place(x=40, y=30)

    button = customtkinter.CTkButton(master=window, text="Ok", command=onOkClick)

    button.place(x=75, y=75 + (höheLabel if höheLabel > 0 else 0))


# TODO clear message after 5 seconds
class Logger:

    # log a message to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def log(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Log: " + data[0], other)
        x = str(" ".join(map(str, data)))
        # setLogLabel("Log: " + data[0] + str(other), "green")
        createErrorPopup(text_zu_mehrehren_Linien(x), "gray")

    # log an error to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def error(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Error: " + data[0], other)
        # main.setLogLabel(str(" ".join(map(str, data))), "red")
        # setLogLabel("Error: " + data[0] + str(other), "red")
        x = str(" ".join(map(str, data)))
        # setLogLabel("Log: " + data[0] + str(other), "green")
        createErrorPopup(text_zu_mehrehren_Linien(x), "red")

    # log a warning to the console and the GUI
    # first parameter must be a str, the rest can be further data of any printable type
    def warn(*data: list[any]) -> None:
        other = list(data)[1::]
        print("Warning: " + data[0], other)
        # main.setLogLabel(str(" ".join(map(str, data))), "orange")
        # setLogLabel("Warning: " + data[0] + str(other), "orange")
        x = str(" ".join(map(str, data)))
        # setLogLabel("Log: " + data[0] + str(other), "green")15
        createErrorPopup(text_zu_mehrehren_Linien(x), "orange")
