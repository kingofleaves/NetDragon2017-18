from guizero import App, Text, PushButton

def f1():
    message.value = "Function 1"

app = App(title = "GROUPR: Hardware Bazaar")
message = Text(app, text = "Welcome to ME310 Hardware Bazaar 2018")
function_1 = PushButton(app, command = f1, text = "Function 1")
app.display()