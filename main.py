import flet as ft
import random
import asyncio

def get_random_post() -> int:
    return random.randint(-100, 2000)

def get_random_color() -> any:
    colors: list = ["blue", "white"]
    return random.choice(colors)

def get_random_offset() -> int:
    return random.randint(1, 5)

def get_random_wait() -> any:
    return random.randrange(500, 700, 100)

class Thing(ft.Container):
    def __init__(self) -> None:
        color: str = get_random_color()
        super(Thing, self).__init__(
            left=get_random_post(),
            top=get_random_post(),
            width=2.5,
            height=2.5,
            shape=ft.BoxShape("circle"),
            bgcolor=color,
            opacity=0,
            offset=ft.transform.Offset(0, 0),
            shadow=ft.BoxShadow(
                spread_radius=20,
                blur_radius=100,
                color=color,
            ),
        )

        self.wait: int = get_random_wait()

        self.animate_opacity = ft.Animation(self.wait, "ease")
        self.animate_offset = ft.Animation(self.wait, "ease")

    async def animate_thing(self, event=None) -> None:
        self.opacity = 1
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2, get_random_offset() ** 2,
        )

        self.update()
        await asyncio.sleep(self.wait / 1000)
        self.opacity = 0
        self.offset = ft.transform.Offset(
            get_random_offset() ** 2, get_random_offset() ** 2,
        )

        self.update()
        await asyncio.sleep(self.wait / 1000)

        await self.animate_thing()

# اصلاح: حذف 'focused_border' از دیکشنری
input_style: dict = {
    "height": 38,
    "cursor_height": 16,
    "cursor_color": "white",
    "content_padding": 1.5,
    "text_size": 12,
}


class input(ft.TextField):
    def __init__(self , password : bool) -> None:
        super().__init__(**input_style , password = password)


button_style: dict = {
    "expand" : True,
    "height" : 38,
    "bgcolor" : "blue",
    "style" : ft.ButtonStyle(shape = {"" : ft.RoundedRectangleBorder(radius = 5)}),
    "color" : "white",
}


class Button(ft.ElevatedButton):  # اصلاح نام کلاس
    def __init__(self , text : str) -> None:
        super().__init__(**button_style , text = text) 


body_style: dict = {
    "width" : 400,
    "padding" : 15,
    "bgcolor" : ft.colors.with_opacity(0.45,"white"),
    "border_radius" :10,
    "shadow" : ft.BoxShadow(
        spread_radius = 20,
        blur_radius = 45,
        color = ft.colors.with_opacity(0.45,"black"),
    ),
}


class Body(ft.Container):
    def __init__(self) -> None:
        super().__init__(**body_style)
        self.email = input(password = False)
        self.password = input(password = True)

        self.content = ft.Column(  # اصلاح نام کلاس
            controls = [
                ft.Divider(height = 10,color = "transparent"),
                ft.Text("Email", size = 10),
                self.email,
                ft.Divider(height = 10,color = "transparent"),
                ft.Text("Password", size = 10),
                self.password,
                ft.Divider(height = 10,color = "transparent"),
                ft.Row(controls = [Button("Sign in")])  # اصلاح اشتباه املایی
            ]
        )

def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.padding = 0

    background = ft.Stack(
        expand=True,
        controls=[Thing() for __ in range(75)],
    )

    stack = ft.Stack(
        expand=True,
        controls=[
            background,
            ft.Column(
                alignment = "center",
                horizontal_alignment = "center",
                controls = [
                    ft.Row(
                        alignment = "center",
                        controls = [Body()],
                   ) 
                ]
            )
        ],
    )

    page.add(stack)
    page.update()

    async def run() -> None:
        await asyncio.gather(
            *(item.animate_thing() for item in background.controls),
        )

    asyncio.run(run())

if __name__ == "__main__":
    ft.app(target=main)
