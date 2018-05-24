import os
from guizero import App, Text, PushButton

def ask(person):
    message.value = "Asking " + person + " for help"
    if person == 'A':
        os.system('mpg123 -q A.mp3 &')
    elif person == 'B':
        os.system('mpg123 -q B.mp3 &')
    elif person == 'C':
        os.system('mpg123 -q C.mp3 &')
    elif person == 'D':
        os.system('mpg123 -q D.mp3 &')
    os.system('mpg123 -q can_you_answer.mp3 &')


app = App(title = "GROUPR: Hardware Bazaar")
message = Text(app, text = "Welcome to ME310 Hardware Bazaar 2018")
ask_a = PushButton(app, command = ask("A"), text = "Ask A")
ask_b = PushButton(app, command = ask("B"), text = "Ask B")
ask_c = PushButton(app, command = ask("C"), text = "Ask C")
ask_d = PushButton(app, command = ask("D"), text = "Ask D")
os.system('mpg123 -q hello.mp3 &')
app.display()