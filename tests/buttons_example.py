from cat_ui import VerticalContainer, HorizontalList, Label, Button, styles, Alignment, App, Window
import asyncio

app = App()
window = Window(VerticalContainer(**styles.pretty, alignment=Alignment.TOP_CENTER))

output = Label("no buttons have been pressed.", alignment=Alignment.CENTER)
window.context.append(output)

def change_output(button: Button):
    output.set_text(f"\"{button.children[0].get_text()}\" has been pressed!")

button_1 = Button("button 1", style=styles.pretty, selected_style=styles.bold_pretty)
button_2 = Button("button 2", style=styles.pretty, selected_style=styles.bold_pretty)
button_3 = Button("button 3", style=styles.pretty, selected_style=styles.bold_pretty)

button_1.add_action(change_output)
button_2.add_action(change_output)
button_3.add_action(change_output)

button_row = HorizontalList()
window.context.append(button_row)

button_row.append(button_1)
button_row.append(button_2)
button_row.append(button_3)

app.add_window(window)
asyncio.run(app.run())