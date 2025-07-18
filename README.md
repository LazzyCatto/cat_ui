# CAT UI

Это легковестный фрэймворк для создания интерактивных CLI программ на питоне.

![preview](https://github.com/LazzyCatto/cat_ui/tree/main/images/preview.gif)

## Установка

Установите напрямую из PyPI:

```bash
pip install cat_ui
```

Или локально из исходников:


```bash
git clone https://github.com/LazzyCatto/midichi
cd midich
pip install .
```

## Запуск

Чтобы быстро попробовать `cat_ui`, создайте файл `main.py` со следующим содержимым:

```python
from ui import Label, run, set_screen
import asyncio

set_screen(Label("Hello cat_ui!"))
asyncio.run(run())
```

Запустить можно с помощью:

```bash
python main.py
```

Чтобы выйти нажмите `Ctrl+C`.

## Документация

### Контейнеры

#### ContainerElement

Базовым класом всех элементов является `ContainerElement`. Именно он отвечает за обработку клавиатуры, а так же отрисовку.

`get_width`, `get_height` возвращают ширину и высоту контейнера соответственно (если элемент неправильной формы, то `get_width`, `get_height` должны возвращать длину и высоту описаного прямоугольника). Они отвечают за изменение размеров родительских контейнеров.

`draw` как раз и отвечает за отрисовку, он возвращает строчку, которая в дальнейшем будет печататься. У всех `ContainerElement` гарантируется, что курсор начинает и заканчивает отрисовку в левом-верхнем углу контейнера.

`draw_on_screen` применяет `alignment` для размещения контейнера. Работает соглашения `draw`: курсор начинает и заканчивает свою работу в левом-верхнем краю экрана.

`process_key` принимает строку кнопки, обрабатывает взаимодействие, а после возвращает кнопку, которая будет обрабатываться родительским контейнером. Если родительский контейнер не должен ничего обрабатывать - возвращается `""`.

`selectable` возвращает `True`, если с контейнером можно взаимодействовать и `False` иначе.

`select`, `deselect` методы отвечают за подсветку или иное обозначение выбраного контейнера (например `Button` меняет стиль своей границы, а `InputField` делает текст жирым).

#### Box

Контейнер, который отрисовывается как прямоугольник. У `Box` можно менять стиль отрисовки сторон, углов, а так же внутренности.

<details><summary>Пример.</summary>

```python
from ui import HorizontalList, Box, styles

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
```

```
*--------* 1~~~~~~~~2 ┌────────┐            ┏━━━━━━━━┓
|        | $@@@@@@@@$ │        │            ┃        ┃
|        | $@@@@@@@@$ │        │            ┃        ┃
|        | $@@@@@@@@$ │        │            ┃        ┃
*--------* 3~~~~~~~~4 └────────┘            ┗━━━━━━━━┛
```
</details>

#### Label

Тестовый контейнер. Текст может быть ограничен по ширине : тогда нужно выставить соответствующее значение `width`.

`get_text` возвращвет текущий текст.

`set_text(text, [width])` устанавливает новый текст.
> Если `width` не установлен, текст будет не ограничен по ширине

<details><summary>Пример.</summary>

```python
from ui import VerticalList, Label, Alignment

labels = VerticalList(min_width=40) # этот элемент нужен для отображения всех `Label`

label_1 = Label("label_1")
label_2 = Label("lb_2", alignment=Alignment.CENTER_RIGHT)
label_3 = Label("This label will be restricted by width", width=10, alignment=Alignment.CENTER)

labels.append(label_1)
labels.append(label_2)
labels.append(label_3)

print(labels.draw(), end="", flush=True)
```

```
label_1

                                    lb_2

               This label
                will be r
               estricted 
               by width
```
</details>

#### BoxContainer

Это Контейнер, который автоматически увеличивается, под размер содержимого. Внутри все вложеные контейнеры расположены свободно, тоесть их положение определяется их `alignment`.

---

внутренние контейнеры выбираются стрелками:
- ( ← ) / ( ↑ ) для выбора предыдущего,
- ( → ) / ( ↓ ) для выбора следующего.

---

> В случае, если внутренние контейнеры перекрываются, выше будет тот, который добавлен позже.

`min_width`, `min_height` - минимальные размеры контейнера.

`top_padding`, `left_padding`, `right_padding`, `bottom_padding` - отступы от краев контейнера (по умолчанию 1).

`append` добавляет контейнер внутрь.

<details><summary>Пример.</summary>
```python
from ui import BoxContainer, Box, Alignment

box_container = BoxContainer(min_width=40, min_height=2, bottom_padding=2, right_padding=4)

box = Box(width=5, height=7, alignment=Alignment.CENTER_RIGHT, fill="#")

box_container.append(box)

print(box_container.draw(), end="", flush=True)
input()
```

```
*--------------------------------------*
|                              *---*   |
|                              |###|   |
|                              |###|   |
|                              |###|   |
|                              |###|   |
|                              |###|   |
|                              *---*   |
|                                      |
*--------------------------------------*
```
</details>

#### VerticalList/HorizontalList

Увеличивающийся контейнер, который распологает внутри элементы по верликали (`VerticalList`) сверху вниз или по горизонтали (`HorizontalList`) слева направо.

внутренние контейнеры выбираются стрелками:
- ( ← ) - `HorizontalList` / ( ↑ ) - `VerticalList` для выбора предыдущего,
- ( → ) - `HorizontalList` / ( ↓ ) - `VerticalList` для выбора следующего.

`min_width`, `min_height` - минимальные размеры контейнера.

`space` - растояние между элементами (по умолчанию 1).

<details><summary>Пример.</summary>

```python
from ui import HorizontalList, Box, Alignment

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
```

```
*---*          *---*
|###|          |   |
*---**---*     |   |
     |:::|     |   |
     *---**---*|   |
          |   ||   |
          *---**---*
```
</details>

#### VerticalContainer/HorizontalContainer

То же самое, что и `VerticalList`/`HorizontalList` и `BoxContainer` одновременно.

<details><summary>Пример.</summary>

```python
from ui import HorizontalContainer, Box, Alignment

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
```

```
*----------------------*
|  *---*          *---*|
|  |###|          |   ||
|  *---**---*     |   ||
|       |:::|     |   ||
|       *---**---*|   ||
|            |   ||   ||
|            *---**---*|
*----------------------*
```
</details>

### Кнопки и чекбоксы

#### Button

Кнопка представляет собой `BoxContainer` с `Label` внутри. При выборе кнопки, меняется стиль отрисовки контейнера.

`style` - обычный стиль отрисовки кнопки.

`selected_style` - стиль при выделении.

---

При нажатии `Enter`(↵) срабатывают все функции, которые были привязаны к кнопке.

`add_action(action)` позволяет привязать новое действие.

> Функции, на которые подкисывается кнопка имеют вид `action(button: Button)`.

---

<details><summary>Пример.</summary>

```python
from ui import VerticalContainer, HorizontalList, Label, Button, styles, Alignment, run, set_screen
import asyncio

window = VerticalContainer(**styles.pretty, alignment=Alignment.TOP_CENTER)
output = Label("no buttons have been pressed.", alignment=Alignment.CENTER)
window.append(output)

def change_output(button: Button):
    output.set_text(f"\"{button.children[0].get_text()}\" has been pressed!")

button_1 = Button("button 1", style=styles.pretty, selected_style=styles.bold_pretty)
button_2 = Button("button 2", style=styles.pretty, selected_style=styles.bold_pretty)
button_3 = Button("button 3", style=styles.pretty, selected_style=styles.bold_pretty)

button_1.add_action(change_output)
button_2.add_action(change_output)
button_3.add_action(change_output)

button_row = HorizontalList()
window.append(button_row)

button_row.append(button_1)
button_row.append(button_2)
button_row.append(button_3)

set_screen(window)
asyncio.run(run())
```

```
                                 ┌────────────────────────────────┐
                                 │  "button 3" has been pressed!  │
                                 │                                │
                                 │┌────────┐ ┌────────┐ ┏━━━━━━━━┓│
                                 ││button 1│ │button 2│ ┃button 3┃│
                                 │└────────┘ └────────┘ ┗━━━━━━━━┛│
                                 └────────────────────────────────┘
```
</details>

#### SelectorLabel : Checkbox и Radio

`SelectorLabel` представляет из себя `Label`, который работает как кнопка, на которую можно нажимать с помощью `Enter`(↵).

`chosen_prefix` это префикс обозначающий, что данный `SelectorLabel` был выбран.

`plain_prefix` это префикс обозначающий, что данный `SelectorLabel` не был выбран.

На соответствующие действия можно подписываться.

`add_action_on(action)` - `action` будет выполнен, как только `SelectorLabel` стал выбран.

`add_action_off(action)` - `action` будет выполнен, как только `SelectorLabel` перестал быть выбран.

> Так же как и у `Button`, функция, на которые подписывается `SelectorLabel` имеет вид `action(button: Button)`.

По отдельности он мало представляет интерес, поэтому далее рассмотрим классы `VerticalCheckbox`, `HorizontalCheckbox`, `VerticalRadio`, `HorizontalRadio`.

---

`VerticalCheckbox`/`HorizontalCheckbox` представляют из себя `VerticalList`/`HorizontalList` состоящий из `SelectorLabel`.

`get_mask` позволяет получить массив `bool`, показывающий текущее состояние `SelectorLabel`.

`get_indices` возвращвет массив индексов выбраных элементов.

Можно так же привязываться к изменению состояния `VerticalCheckbox`/`HorizontalCheckbox` с помощью `add_action(action)`.

``

<details><summary>Пример.</summary>

```python
from ui import VerticalContainer, VerticalCheckbox, Button, Label, styles, Alignment, run, set_screen
import asyncio

window = VerticalContainer(
    space=2,
    left_padding=2,
    right_padding=2,
    alignment=Alignment.TOP_CENTER,
    **styles.pretty
    )
window.append(Label("THE ULTIMATE TODO LIST", alignment=Alignment.TOP_CENTER))
label = Label("")

plan_list = VerticalCheckbox(
    [
    "make cool application with cat_ui",
    "do a backflip",
    "go to sleep",
    "watch anime 24/7"
    ], chosen_prefix="🗹 ", plain_prefix="☐ ")
window.append(plan_list)

plan_list.children[-1].add_action_on(lambda sl: label.set_text("toch some grass"))
plan_list.children[-1].add_action_off(lambda sl: label.set_text("achivement unlocked: \"toch some grass\""))

done_button = Button("DONE", min_width=10, alignment=Alignment.BOTTOM_CENTER, style=styles.pretty, selected_style=styles.bold_pretty)
window.append(done_button)
window.append(label)

done_button.add_action(lambda btn: label.set_text(f"the mask list: {plan_list.get_mask()}"))

set_screen(window)
app = asyncio.run(run())
```

```
                           ┌───────────────────────────────────────────┐
                           │          THE ULTIMATE TODO LIST           │
                           │                                           │
                           │                                           │
                           │ 🗹 make cool application with cat_ui       │
                           │                                           │
                           │ ☐ do a backflip                           │
                           │                                           │
                           │ 🗹 go to sleep                             │
                           │                                           │
                           │ ☐ watch anime 24/7                        │
                           │                                           │
                           │                                           │
                           │                ┏━━━━━━━━┓                 │
                           │                ┃  DONE  ┃                 │
                           │                ┗━━━━━━━━┛                 │
                           │                                           │
                           │                                           │
                           │ the mask list: [True, False, True, False] │
                           └───────────────────────────────────────────┘
```
</details>

---

`VerticalRadio`/`HorizontalRadio` - то же, что и `VerticalCheckbox`/`HorizontalCheckbox`, только не позволяют нескольким `SelectorLabel` быть выбраными одновременно.

Вместо `get_mask` и `get_indecies` есть метод `get_index`. Он возвращает индекс выбраного элемента (-1, если не выбрано ничего).

<details><summary>Пример.</summary>

```python
from ui import VerticalContainer, VerticalRadio, Label, styles, Alignment, run, set_screen
import asyncio

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

set_screen(window)
app = asyncio.run(run())
```
```
                                  ┌─────────────────────────────┐
                                  │ What is your favorite game? │
                                  │                             │
                                  │                             │
                                  │ ○ minectart                 │
                                  │                             │
                                  │ ○ terraria                  │
                                  │                             │
                                  │ ◉ portal                    │
                                  │                             │
                                  │ ○ the witness               │
                                  │                             │
                                  │                             │
                                  │ I love portal too!          │
                                  └─────────────────────────────┘
```
</details>

### Ввод текстовых данных

`InputField` позволяет вводить текстовые данные. Изначально в текстовом поле записан `text`.

`width` - максимальная ширина текста.

`set_width(width)` выставляет новую максимальную ширину.
> можно выставить -1, чтобы текст увеличивался неограничено.

`set_text(text)` позволяет поменять содержимое текстового поля.

`get_text` возвращает написаный текст.

`alowed_char` - допустимый набор символов (по умолчанию это `ui.printable`).

---

- ( ← ) перемещает курсор влево
- ( → ) перемещает курсор вправо


При нажатии на `Enter`(↵) срабатывают все функции, которые были привязаны.

`add_action(action)` позволяет привязать новое действие.

> Так же как и у `Button`, все привязаные функции имеют вид `action(button: Button)`.

---

`PasswordInput` - то же, что и `InputField`, только все символы заменяются на `password_char` (по умолчанию `*`).

<details><summary>Пример.</summary>

```python
from ui import VerticalContainer, HorizontalList, InputField, PasswordInput, Label, styles, Alignment, run, set_screen
import asyncio

window = VerticalContainer(
    space=2,
    left_padding=2,
    right_padding=2,
    alignment=Alignment.TOP_CENTER,
    **styles.pretty
    )

window.append(Label("What is your name?"))
name_input = InputField()
name_row = HorizontalList(min_height=1)
name_row.append(Label("name:"))
name_row.append(name_input)
window.append(name_row)

greetings_label = Label("")
window.append(greetings_label)

name_input.add_action(lambda name: greetings_label.set_text(f"Hello {name.get_text()}!"))

window.append(Label("Enter secret password (only numbers)"))
password_input = PasswordInput(alowed_char="".join([str(num) for num in range(10)]))
password_row = HorizontalList(min_height=1)
password_row.append(Label("password:"))
password_row.append(password_input)
window.append(password_row)

verify_label = Label("")
window.append(verify_label)

def check_password(password: PasswordInput):
    if password.get_text() == "12345":
        verify_label.set_text("The password is correct!")
    else:
        verify_label.set_text("Wrong password!!!")

password_input.add_action(check_password)

set_screen(window)
app = asyncio.run(run())
```
```
                              ┌──────────────────────────────────────┐
                              │ What is your name?                   │
                              │                                      │
                              │                                      │
                              │ name: Akio                           │
                              │                                      │
                              │                                      │
                              │ Hello Akio!                          │
                              │                                      │
                              │                                      │
                              │ Enter secret password (only numbers) │
                              │                                      │
                              │                                      │
                              │ password: *****_                     │
                              │                                      │
                              │                                      │
                              │ The password is correct!             │
                              └──────────────────────────────────────┘
```
</details>