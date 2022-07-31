from .base import MixinBase, db


class Voltime(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, comment="姓名")
    sex = db.Column(db.String(5), nullable=False, server_default="", comment="性别")
    stu_id = db.Column(db.BigInteger, nullable=False, comment="学号")
    faculty = db.Column(db.String(20), nullable=False, server_default="", comment="学院")
    date_str = db.Column(db.String(30), nullable=False, server_default="")
    date = db.Column(db.DATE, nullable=False, comment="日期")
    duration = db.Column(db.Numeric(5, 2), nullable=False, comment="时长")
    activity_name = db.Column(db.String(50), nullable=False, comment="活动名称")
    team = db.Column(db.String(50), nullable=False, comment="队名")
    duty_faculty = db.Column(db.String(20), nullable=False, comment="组织学院")
    duty_person = db.Column(db.String(20), nullable=False, comment="组织人")
    remark = db.Column(db.Text, nullable=True, comment="备注")


class VoltimeDupname(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True, comment="姓名")
    dup_num = db.Column(db.SmallInteger, nullable=False, comment="重名人数")
