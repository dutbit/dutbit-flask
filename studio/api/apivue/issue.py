from flask import Blueprint, g, request
from studio.models import IssueDutyUsersRe, IssueIssues, IssueTypes, UserUsers, db
from studio.utils import dfl, dfln, listf
from studio.utils.mail import send_mail

issue = Blueprint("issue", __name__, url_prefix="/issue")


@issue.route("/", methods=["GET", "POST"])
def r_issue():
    if request.method == "GET":
        dictR = {"lstdTypes": []}  # dictResp
        for row in IssueTypes.query.filter(IssueTypes.priority > 20).all():
            dictR["lstdTypes"].append(dfln(row.__dict__, ["_sa_instance_state"]))
        return dictR
    if request.method == "POST":
        dictReq = request.get_json()
        issue = IssueIssues(
            **dfl(dictReq, ["type_id", "name", "stu_id", "contact", "content"]), user_id=g.user and g.user.id
        )
        db.session.add(issue)
        db.session.commit()

        lsttUID = db.session.query(IssueDutyUsersRe.user_id).filter_by(type_id=dictReq["type_id"]).all()
        lsttEmails = db.session.query(UserUsers.email).filter(UserUsers.id.in_(listf(lsttUID))).all()
        send_mail(to=listf(lsttEmails), subject="dutbit.com 新增反馈通知", content=str(issue))
        return {"success": True}
