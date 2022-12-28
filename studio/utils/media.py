import os
import math


def gen_media(title, raw_content, img_name, file_name):
    url_prefix = "studio/utils"
    f = open(f"{url_prefix}/postcard.py", "r+", encoding="utf-8")
    code_str = ""
    for line in f.readlines():
        code_str += line
    f.close()
    lines = [raw_content[i:i + 8] for i in range(0, len(raw_content), 8)]
    content = ""
    for line in lines:
        content += line
        content += "\\n"
    # 最大8个字符，否则换行
    code_str = code_str.format(title=title, img_url=f"assets/{img_name}", content=content)
    f = open(f"studio/tmp/{file_name}.py", "w", encoding="utf-8")
    f.write(code_str)
    f.close()
    os.system(f"manimgl studio/tmp/{file_name}.py -w --file_name {file_name}.mp4 --video_dir studio/tmp")
