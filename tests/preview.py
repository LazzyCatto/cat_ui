from cat_ui import VerticalContainer, HorizontalList, BoxContainer, Button, ButtonText, VerticalRadio, InputField, PasswordInput, Label, Alignment, styles, App, Window
import asyncio

app = App()

window_index = 0
windows = [Window(VerticalContainer(min_width=40, alignment=Alignment.TOP_CENTER, **styles.pretty)) for _ in range(3)]

def go_back(button: Button):
    global window_index
    window_index -= 1
    app.close_all_windows()
    app.add_window(windows[window_index])

def go_forward(button: Button):
    global window_index
    window_index += 1
    app.close_all_windows()
    app.add_window(windows[window_index])

# window 0

windows[0].context.append(Label("THIS IS CAT_UI!", alignment=Alignment.TOP_CENTER))
windows[0].context.append(Label("What is your name?"))
name_input = InputField(max_length=10)
name_row = HorizontalList(min_height=1)
name_row.append(Label("name:"))
name_row.append(name_input)
windows[0].context.append(name_row)

greetings_label = Label("")
windows[0].context.append(greetings_label)

name_input.add_action(lambda name: greetings_label.set_text(f"Hello {name.get_text()}!"))

windows[0].context.append(Label("Enter secret password (only numbers)"))
password_input = PasswordInput(alowed_char="".join([str(num) for num in range(10)]), max_length=10)
password_row = HorizontalList(min_height=1)
password_row.append(Label("password:"))
password_row.append(password_input)
windows[0].context.append(password_row)

verify_label = Label("")
windows[0].context.append(verify_label)

def check_password(password: PasswordInput):
    if password.get_text() == "12345":
        verify_label.set_text("The password is correct!")
    else:
        verify_label.set_text("Wrong password!!!")

password_input.add_action(check_password)

footer = BoxContainer(min_width=windows[0].context.get_width(), min_height=1, left_padding=0, right_padding=0, top_padding=0, bottom_padding=0, alignment=Alignment.BOTTOM_CENTER, **styles.invisible)
next_page = ButtonText("next", alignment=Alignment.BOTTOM_RIGHT)
next_page.add_action(go_forward)
footer.append(next_page)
windows[0].context.append(footer)

# window 1

windows[1].context.append(Label("What is your favorite game?"))
label = Label("")

game_list = ["minecraft", "terraria", "portal", "the witness"]
game_radio = VerticalRadio(game_list, chosen_prefix="◉ ", plain_prefix="○ ")
windows[1].context.append(game_radio)

def on_change(radio: VerticalRadio):
    if radio.get_index() == -1:
        label.set_text("")
    else:
        label.set_text(f"I love {game_list[radio.get_index()]} too!")

game_radio.add_action(on_change)

windows[1].context.append(label)

footer = BoxContainer(min_width=windows[0].context.get_width(), min_height=1, left_padding=0, right_padding=0, top_padding=0, bottom_padding=0, alignment=Alignment.BOTTOM_CENTER, **styles.invisible)
prev_page = ButtonText("back", alignment=Alignment.BOTTOM_LEFT)
prev_page.add_action(go_back)
footer.append(prev_page)
next_page = ButtonText("next", alignment=Alignment.BOTTOM_RIGHT)
next_page.add_action(go_forward)
footer.append(next_page)
windows[1].context.append(footer)

# window 2

windows[2].context.append(Label("THANK YOU FOR USING CAT_UI", alignment=Alignment.TOP_CENTER))
windows[2].context.append(Label("to leave use (Ctrl+C).", alignment=Alignment.TOP_CENTER))

footer = BoxContainer(min_width=windows[0].context.get_width(), min_height=1, left_padding=0, right_padding=0, top_padding=0, bottom_padding=0, alignment=Alignment.BOTTOM_CENTER, **styles.invisible)
prev_page = ButtonText("back", alignment=Alignment.BOTTOM_LEFT)
prev_page.add_action(go_back)
footer.append(prev_page)
windows[2].context.append(footer)

app.add_window(windows[0])
asyncio.run(app.run())