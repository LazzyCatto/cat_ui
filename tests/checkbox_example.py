from cat_ui import VerticalContainer, VerticalCheckbox, Button, Label, styles, Alignment, App, Window
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
window.context.append(Label("THE ULTIMATE TODO LIST", alignment=Alignment.TOP_CENTER))
label = Label("")

plan_list = VerticalCheckbox(
    [
    "make cool application with cat_ui",
    "do a backflip",
    "go to sleep",
    "watch anime 24/7"
    ], chosen_prefix="🗹 ", plain_prefix="☐ ")
window.context.append(plan_list)

plan_list.children[-1].add_action_on(lambda sl: label.set_text("toch some grass"))
plan_list.children[-1].add_action_off(lambda sl: label.set_text("achivement unlocked: \"toch some grass\""))

done_button = Button("DONE", min_width=10, alignment=Alignment.BOTTOM_CENTER, style=styles.pretty, selected_style=styles.bold_pretty)
window.context.append(done_button)
window.context.append(label)

done_button.add_action(lambda btn: label.set_text(f"the mask list: {plan_list.get_mask()}"))

app.add_window(window)
asyncio.run(app.run())