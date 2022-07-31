from flask import Blueprint, jsonify, request, g
from studio.models import db, UserUsers

user = Blueprint("user", __name__, url_prefix="/user")  # 创建二级蓝图


@user.route("/confirm", methods=["POST"])
def users_confirm_post():
    if request.values["code"] != g.user.validation_code:
        return jsonify({"success": False, "details": "验证码无效"})
    else:
        UserUsers.query.filter(UserUsers.id == g.user.id).update({UserUsers.confirmed: True})
        db.session.commit()
        return jsonify({"success": False, "details": "验证完成"})
