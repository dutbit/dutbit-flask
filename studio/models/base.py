from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MixinBase:
    create_time = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), comment="创建时间")
    update_time = db.Column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now(), comment="更新时间"
    )
    update_cnt = db.Column(db.SmallInteger, nullable=False, server_default=db.text("1"), comment="更新次数")
    deleted = db.Column(db.Boolean, nullable=False, server_default=db.text("0"), comment="删除标记")


class EditHistory(db.Model, MixinBase):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    table_name = db.Column(db.String(30), nullable=False)
    row_id = db.Column(db.Integer, nullable=False)
    rows_total = db.Column(db.SmallInteger, nullable=False, server_default=db.text("1"))
    attr_name = db.Column(db.String(30), nullable=False, server_default="")
    details = db.Column(db.Text, nullable=True)
    edit_by = db.Column(db.Integer, nullable=False)
