from cat_ui import HorizontalList, Box, styles

list_of_boxes = HorizontalList()  # этот элемент нужен для отображения всех `Box`

box_1 = Box(width=10, height=5)
box_2 = Box(width=10, height=5, vertical_bar="$", horizontal_bar="~", corners=["1", "2", "3", "4"], fill="@")
box_3 = Box(width=10, height=5, **styles.pretty)
box_4 = Box(width=10, height=5, **styles.invisible)
box_5 = Box(width=10, height=5, **styles.bold_pretty)

list_of_boxes.append(box_1)
list_of_boxes.append(box_2)
list_of_boxes.append(box_3)
list_of_boxes.append(box_4)
list_of_boxes.append(box_5)

print(list_of_boxes.draw(), end="", flush=True)