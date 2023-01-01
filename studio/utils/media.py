import os
import math

postcard = """
from manim import *


class PostcardText(Scene):
    def construct(self) -> None:
        title = Text("{title}", font="Source Han Serif CN", font_size=25)
        title.set_width(2.2)
        title.set_max_height(0.5)
        title.set_color(RED_B).set_x(3.95).set_y(0.75)
        content = Text("{content}", font="Source Han Serif CN", font_size=16, color=GREY_D, line_spacing=0.3)
        content.set_width(2.2)
        content.next_to(title, DOWN)
        img = ImageMobject("{img_url}")
        img.scale(1.25)
        self.play(FadeIn(img))
        self.play(Write(title))
        self.play(FadeIn(content, shift=UP))
        self.wait(3)

"""


def gen_media(title, raw_content, img_name, file_name):
    # url_prefix = "studio/utils"
    # f = open(f"{url_prefix}/postcard.py", "r+", encoding="utf-8")
    code_str = postcard
    # for line in f.readlines():
    #     code_str += line
    # f.close()
    lines = []
    count = 0
    start = 0
    end = 0
    for i in range(len(raw_content)):
        end += 1
        count += 1
        c = raw_content[i]
        if c == '\n':
            lines.append(raw_content[start:end])
            start = end
            count = 0
        if count % 8 == 0:
            lines.append(raw_content[start:end])
            start = end
        if i + 1 == len(raw_content):
            lines.append(raw_content[start:end])
    lines = [line.replace("\n", "") for line in lines if line != '']
    content = ""
    for line in lines:
        # 空行跳过
        if line == '':
            continue
        content += line
        content += "\\n"
    # 最大8个字符，否则换行
    code_str = code_str.format(title=title, img_url=f"assets/{img_name}", content=content)
    f = open(f"studio/tmp/{file_name}.py", "w", encoding="utf-8")
    f.write(code_str)
    f.close()
    os.system(f"manim studio/tmp/{file_name}.py -q m --format mp4 -o {file_name}.mp4 --media_dir studio/tmp")
