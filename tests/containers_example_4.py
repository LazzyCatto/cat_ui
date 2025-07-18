from cat_ui import HorizontalList, Box, Alignment

horizontal_list = HorizontalList(space=0)

box_1 = Box(width=5, height=3, fill="#")
box_2 = Box(width=5, height=3, alignment=Alignment.CENTER_RIGHT, fill=":")
box_3 = Box(width=5, height=3, alignment=Alignment.BOTTOM_LEFT)
box_4 = Box(width=5, height=7, alignment=Alignment.BOTTOM_LEFT)

horizontal_list.append(box_1)
horizontal_list.append(box_2)
horizontal_list.append(box_3)
horizontal_list.append(box_4)

print(horizontal_list.draw(), end="", flush=True)