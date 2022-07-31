from .base import MixinBase, db


class IssueIssues(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False, comment="反馈类型ID")
    name = db.Column(db.String(20), nullable=True, comment="姓名")
    stu_id = db.Column(db.BigInteger, nullable=True, comment="学号")
    contact = db.Column(db.Text, nullable=True, comment="联系方式")
    content = db.Column(db.Text, nullable=True, comment="反馈内容")
    user_id = db.Column(db.Integer, nullable=True, comment="用户ID")
    status = db.Column(db.SmallInteger, nullable=True, server_default=db.text("1"), comment="状态")

    def __str__(self):
        return (
            f"<IssueIssue NO {self.id}>\n"
            f"反馈类型ID：{self.type_id}\n姓名：{self.name}\n学号：{self.stu_id}\n"
            f"联系方式：{self.contact}\n反馈内容：\n{self.content}"
        )


class IssueTypes(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), nullable=False, comment="反馈类型")
    description = db.Column(db.Text, nullable=True, comment="说明")
    priority = db.Column(db.Integer, nullable=False, server_default=db.text("80"), comment="优先级")


class IssueDutyUsersRe(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False, comment="反馈类型ID")
    user_id = db.Column(db.Integer, nullable=False, comment="用户ID")
