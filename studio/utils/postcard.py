from manim import *


class PostcardText(Scene):
    def construct(self) -> None:
        title = Text("{title}", font="宋体", font_size=25)
        title.set_width(2.2)
        title.set_max_height(0.5)
        title.set_color(RED_B).set_x(3.95).set_y(0.75)
        content = Text("{content}", font="宋体", font_size=16, color=GREY_D)
        content.set_width(2.2)
        content.next_to(title, DOWN)
        img = ImageMobject("{img_url}")
        img.scale(1.25)
        self.play(FadeIn(img))
        self.play(Write(title))
        self.play(FadeIn(content, shift=UP))
        self.wait(3)



