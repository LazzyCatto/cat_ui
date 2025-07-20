from cat_ui import VerticalContainer, HorizontalList, InputField, PasswordInput, Label, styles, Alignment, App, Window
import asyncio

app = App()
window = Window(
    VerticalContainer(
        space=2,
        left_padding=2,
        right_padding=2,
        alignment=Alignment.TOP_CENTER,
        **styles.pretty
    )
)

window.context.append(Label("What is your name?"))
name_input = InputField()
name_row = HorizontalList(min_height=1)
name_row.append(Label("name:"))
name_row.append(name_input)
window.context.append(name_row)

greetings_label = Label("")
window.context.append(greetings_label)

name_input.add_action(lambda name: greetings_label.set_text(f"Hello {name.get_text()}!"))

window.context.append(Label("Enter secret password (only numbers)"))
password_input = PasswordInput(alowed_char="".join([str(num) for num in range(10)]))
password_row = HorizontalList(min_height=1)
password_row.append(Label("password:"))
password_row.append(password_input)
window.context.append(password_row)

verify_label = Label("")
window.context.append(verify_label)

def check_password(password: PasswordInput):
    if password.get_text() == "12345":
        verify_label.set_text("The password is correct!")
    else:
        verify_label.set_text("Wrong password!!!")

password_input.add_action(check_password)

app.add_window(window)
asyncio.run(app.run())