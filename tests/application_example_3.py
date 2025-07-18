from cat_ui import VerticalContainer, Label, Button, Alignment, App
import asyncio

app = App()

window = VerticalContainer(min_width=10, left_padding=2,right_padding=2, alignment=Alignment.TOP_CENTER)
window.append(Label("Pressing this button will terminate window"))

button = Button("click me", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: app.stop())
window.append(button)

app.set_screen(window)
asyncio.run(app.run())
