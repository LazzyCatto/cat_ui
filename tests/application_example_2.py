from cat_ui import VerticalContainer, Button, Label, Alignment, App
import asyncio

app = App()

window_1 = VerticalContainer(alignment=Alignment.TOP_CENTER)
window_2 = VerticalContainer(alignment=Alignment.TOP_CENTER)

button = Button("next window", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: app.set_screen(window_2))

window_1.append(Label("This is window 1"))
window_1.append(button)

window_2.append(Label("This is window 2"))

app.set_screen(window_1)
asyncio.run(app.run())