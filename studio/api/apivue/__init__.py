from flask import Blueprint, current_app, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from studio.models import UserGroupMembersRe, UserUsers, db
from studio.utils import abort_err, dfl, listf
from studio.utils.jwt import create_token
from studio.utils.mail import send_mail

# from .dayImage import dayImage
from .dayimgO import dayimgO
from .issue import issue
from .point import point
from .pointMan import point_man
from .user import user
from .voltime import voltime
from .voltimeMan import voltime_man
from .enroll import enroll
from .mediaImg import media_img

apivue = Blueprint("apivue", __name__, url_prefix="/apivue")
apivue.register_blueprint(dayimgO)
apivue.register_blueprint(issue)
apivue.register_blueprint(point)
apivue.register_blueprint(point_man)
apivue.register_blueprint(user)
apivue.register_blueprint(voltime)
apivue.register_blueprint(voltime_man)
apivue.register_blueprint(enroll)
apivue.register_blueprint(media_img)
CORS(apivue)


@apivue.route("/login", methods=["POST"])
def users_login():
    dicForm = request.get_json()
    userNow = UserUsers.query.filter_by(email=dicForm["email"]).one_or_none()
    if userNow is None:
        return abort_err(462, "Incorrect.")
    if not userNow.check_password(dicForm["password"]):
        return abort_err(462, "Incorrect!")

    lsttGIDs = db.session.query(UserGroupMembersRe.group_id).filter_by(user_id=userNow.id).all()
    strToken = create_token({"id": userNow.id, "lstGIDs": listf(lsttGIDs)})
    return {"success": True, "details": "登录成功", "token": strToken}


@apivue.route("/register", methods=["POST"])
def register():
    dicForm: dict = request.get_json()
    try:
        userNew = UserUsers(**dfl(dicForm, ["username", "email", "password"]))
        db.session.add(userNew)
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error(e)
        return abort_err(533)
    else:
        return {"success": True, "details": "注册成功"}


@apivue.route("/mail")
def mail():
    send_mail("1968189277@qq.com", "test1", "test2")
    return {"success": True}
