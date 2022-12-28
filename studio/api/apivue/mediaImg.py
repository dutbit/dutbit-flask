import os
import flask
import hashlib
from flask import Blueprint, send_from_directory, request
from studio.models import MediaList, db
from studio.utils.media import gen_media

media_img = Blueprint("media_img", __name__, url_prefix="/media-img")


@media_img.route("/download-media", methods=["GET"])
def r_download_media():
    media_id = request.values.get("mediaId")
    print(media_id)
    if media_id is None:
        return {"success": False, "detail": "请求非法"}

    temp_dir = os.getcwd() + "/studio/tmp/videos/"
    media = MediaList.query.filter(MediaList.media_id == media_id).first()
    if media is None:
        return {"success": False, "detail": "请求非法"}
    if media.status == 0:
        return {"success": False, "detail": "视频尚未制作完成，请耐心等待~"}
    return send_from_directory(temp_dir, media.file_name, as_attachment=True)


@media_img.route("/gen-media", methods=["POST"])
def r_gen_media():
    req = request.get_json()
    name = req.get("name")  # 姓名
    title = req.get("title")  # 标题
    img_name = req.get("imgName")  # 图片名称，前后端保持一致
    wish_texts = req.get("wishTexts")  # 新年祝福文本
    if name is None or wish_texts is None or title is None:
        return {"success": False, "detail": "参数非法"}
    name_md5 = hashlib.md5(name.encode("utf8")).hexdigest()
    print("md5", name_md5)
    media_query = MediaList.query.filter(MediaList.name == name).first()
    if media_query is None:
        media = MediaList(name=name, file_name=name_md5 + ".mp4", media_id=name_md5, status=0)
        db.session.add(media)
        db.session.commit()
    # 如果不为空，则有 2 种情况，一种情况是制作完成，此时可以重新启动新进程，另一种则为正在制作
    elif media_query.status == 0:
        return {"success": False, "detail": "视频尚未制作完成，请耐心等待~"}
    elif media_query.status == 1:
        # 重新制作
        media_query.status = 0
        db.session.add(media_query)
        db.session.commit()
    # 在这里启动视频制作
    gen_media(title, wish_texts, img_name, name_md5)
    # 视频制作完成，更新数据库
    media_query = MediaList.query.filter(MediaList.name == name).first()
    media_query.status = 1
    db.session.add(media_query)
    print("已经更新数据库")
    db.session.commit()
    return {"success": True, "mediaId": media_query.media_id}
