from cat_ui import BoxContainer, Box, Alignment

box_container = BoxContainer(min_width=40, min_height=2, bottom_padding=2, right_padding=4)

box = Box(width=5, height=7, alignment=Alignment.CENTER_RIGHT, fill="#")

box_container.append(box)

print(box_container.draw(), end="", flush=True)