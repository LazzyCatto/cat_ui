from ui import VerticalContainer, Label, Button, Alignment, run, set_screen
import asyncio

window = VerticalContainer(min_width=10, left_padding=2,right_padding=2, alignment=Alignment.TOP_CENTER)
label = Label("Use Enter (↵)", alignment=Alignment.TOP_CENTER)
window.append(label)

button = Button("click me", alignment=Alignment.BOTTOM_CENTER)
button.add_action(lambda btn: label.set_text("Hello world!"))
window.append(button)

set_screen(window)
asyncio.run(run())
