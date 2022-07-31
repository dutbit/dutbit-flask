from .base import MixinBase, db


class PointPoints(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False, comment="积分类型ID")
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    sex = db.Column(db.String(5), nullable=False, server_default="", comment="性别")
    stu_id = db.Column(db.BigInteger, nullable=False, comment="学号")
    faculty = db.Column(db.String(20), nullable=False, server_default="", comment="学院")
    points = db.Column(db.Integer, nullable=False, server_default=db.text("0"), comment="积分")
    remark = db.Column(db.Text, nullable=True, comment="备注")


class PointTypes(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), nullable=False, comment="积分类型")
    description = db.Column(db.Text, nullable=True, comment="说明")
