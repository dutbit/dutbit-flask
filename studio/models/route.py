from .base import MixinBase, db


class RouteInterceptors(db.Model, MixinBase):
    id = db.Column(db.Integer, primary_key=True)
    startswith = db.Column(db.String(100), nullable=False, comment="URL前缀")
    group_id = db.Column(db.Integer, nullable=False, comment="用户组ID")
    description = db.Column(db.Text, nullable=True, comment="说明")
