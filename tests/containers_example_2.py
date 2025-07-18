from cat_ui import VerticalList, Label, Alignment

labels = VerticalList(min_width=40) # этот элемент нужен для отображения всех `Label`

label_1 = Label("label_1")
label_2 = Label("lb_2", alignment=Alignment.CENTER_RIGHT)
label_3 = Label("This label will be restricted by width", width=10, alignment=Alignment.CENTER)

labels.append(label_1)
labels.append(label_2)
labels.append(label_3)

print(labels.draw(), end="", flush=True)