from cat_ui import HorizontalContainer, Box, Alignment

horizontal_container = HorizontalContainer(space=0, left_padding=3)

box_1 = Box(width=5, height=3, fill="#")
box_2 = Box(width=5, height=3, alignment=Alignment.CENTER_RIGHT, fill=":")
box_3 = Box(width=5, height=3, alignment=Alignment.BOTTOM_LEFT)
box_4 = Box(width=5, height=7, alignment=Alignment.BOTTOM_LEFT)

horizontal_container.append(box_1)
horizontal_container.append(box_2)
horizontal_container.append(box_3)
horizontal_container.append(box_4)

print(horizontal_container.draw(), end="", flush=True)