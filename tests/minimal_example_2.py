from cat_ui import VerticalContainer, Label, Button, Alignment, App, Window
import asyncio

app = App()
window = Window(VerticalContainer(min_width=10, left_padding=2,right_padding=2, alignment=Alignment.TOP_CENTER))

label = Label("Use Enter (↵)", alignment=Alignment.TOP_CENTER)
window.context.append(label)

button = Button("click me", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: label.set_text("Hello world!"))
window.context.append(button)

app.add_window(window)
asyncio.run(app.run())
