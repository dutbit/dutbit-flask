from .base import MixinBase, db


class EnrollTurns(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    turn_name = db.Column(db.String(40), nullable=False, comment="招新批次名称")
    activated = db.Column(db.Integer, nullable=False, comment="是否为当前批次", server_default=db.text("0"))


class EnrollCandidates(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    stu_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(5), nullable=False)
    faculty = db.Column(db.String(20), nullable=False)
    politic = db.Column(db.String(20), nullable=False, server_default="群众")
    major = db.Column(db.Text, nullable=True)
    major_class = db.Column(db.Text, nullable=True)
    advantage = db.Column(db.Text, nullable=True)
    other_advantage = db.Column(db.Text, nullable=True)
    birth_date = db.Column(db.Text, nullable=True)
    role = db.Column(db.Text, nullable=True)
    first_choice = db.Column(db.String(20), nullable=False, comment="第一志愿")
    second_choice = db.Column(db.String(20), nullable=True, comment="第二志愿")
    third_choice = db.Column(db.String(20), nullable=True, comment="第三志愿")
    tel = db.Column(db.String(20), nullable=False, comment="联系电话")
    allow_adjust = db.Column(db.Boolean, nullable=False, comment="是否服从调剂")
    student_exp = db.Column(db.Text, nullable=True)
    info = db.Column(db.Text, nullable=True, comment="特长等详细信息")
    turn_id = db.Column(db.Integer, db.ForeignKey("enroll_turns.id"))


class EnrollDepts(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(20), nullable=False, comment="部门名称")
