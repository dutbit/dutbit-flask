from werkzeug.security import check_password_hash, generate_password_hash

from .base import MixinBase, db


class UserUsers(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, comment="用户名")
    email = db.Column(db.String(100), nullable=False, unique=True, comment="邮箱")
    password_hash = db.Column(db.String(150), nullable=False, comment="密码Hash")
    confirmed = db.Column(db.Boolean, nullable=False, server_default=db.text("0"), comment="邮箱是否已验证")
    last_login_ip = db.Column(db.String(50), nullable=True, comment="最后登录IP")
    last_login_time = db.Column(db.DateTime, nullable=True, comment="最后登录时间")

    @property
    def password(self):
        raise AttributeError("明文密码不可读")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserGroups(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20), nullable=True, comment="用户组名称")
    description = db.Column(db.Text, nullable=True, comment="说明")


class UserGroupMembersRe(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, comment="用户ID")
    group_id = db.Column(db.Integer, nullable=False, comment="用户组ID")
