import os
import math


def gen_media(title, raw_content, img_name, file_name):
    url_prefix = "studio/utils"
    f = open(f"{url_prefix}/postcard.py", "r+", encoding="utf-8")
    code_str = ""
    for line in f.readlines():
        code_str += line
    f.close()
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
        content += line
        content += "\\n"
    # 最大8个字符，否则换行
    code_str = code_str.format(title=title, img_url=f"assets/{img_name}", content=content)
    f = open(f"studio/tmp/{file_name}.py", "w", encoding="utf-8")
    f.write(code_str)
    f.close()
    os.system(f"manimgl studio/tmp/{file_name}.py -w --file_name {file_name}.mp4 --video_dir studio/tmp")
