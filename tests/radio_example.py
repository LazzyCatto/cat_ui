from cat_ui import VerticalContainer, VerticalRadio, Label, styles, Alignment, App
import asyncio

app = App()

window = VerticalContainer(
    space=2,
    left_padding=2,
    right_padding=2,
    alignment=Alignment.TOP_CENTER,
    **styles.pretty
    )
window.append(Label("What is your favorite game?"))
label = Label("")

game_list = ["minectart", "terraria", "portal", "the witness"]
game_radio = VerticalRadio(game_list, chosen_prefix="◉ ", plain_prefix="○ ")
window.append(game_radio)

def on_change(radio: VerticalRadio):
    if radio.get_index() == -1:
        label.set_text("")
    else:
        label.set_text(f"I love {game_list[radio.get_index()]} too!")

game_radio.add_action(on_change)

window.append(label)

app.set_screen(window)
asyncio.run(app.run())