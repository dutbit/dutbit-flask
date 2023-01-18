from .base import MixinBase, db


class MediaList(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, comment="姓名")
    file_name = db.Column(db.String(60), nullable=False, comment="视频文件路径")
    media_id = db.Column(db.String(1024), nullable=False, comment="视频ID")
    status = db.Column(db.Integer, nullable=False, comment="视频状态, 如果为1表明制作完成")
