from cat_ui import VerticalContainer, Label, Button, Alignment, App, Window
import asyncio

app = App()
window = Window(VerticalContainer(min_width=10, left_padding=2,right_padding=2, alignment=Alignment.TOP_CENTER))

window.context.append(Label("Pressing this button will terminate window"))

button = Button("click me", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: btn.window.close())
window.context.append(button)

app.add_window(window)
asyncio.run(app.run())
