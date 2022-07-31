from flask import Blueprint, current_app, request
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import OperationalError
from studio.models import PointPoints, db
from studio.utils import abort_err, dfd, dfl, dfln, listf

point_man = Blueprint("point_man", __name__, url_prefix="/point-man")  # 创建二级蓝图


@point_man.route("/", methods=["POST"])
def r_pointman():
    dictReq = dfd(request.get_json(), {"pageNum": 1, "pageSize": 30, "searchText": ""})

    searchText = dictReq["searchText"]
    queryP: BaseQuery = PointPoints.query
    sameList = []
    if searchText.isdigit():
        queryP = queryP.filter_by(stu_id=searchText)
        sameList = db.session.query(PointPoints.name).filter_by(stu_id=searchText).group_by(PointPoints.name).all()
    elif searchText != "":
        queryP = queryP.filter_by(name=searchText)
        sameList = db.session.query(PointPoints.stu_id).filter_by(name=searchText).group_by(PointPoints.stu_id).all()

    pagP = queryP.order_by(PointPoints.id.desc()).paginate(dictReq["pageNum"], dictReq["pageSize"], False, 200)
    lstP = []
    for row in pagP.items:
        row = dfln(row.__dict__, ["_sa_instance_state"])
        lstP.append(row)
    return {"total": pagP.total, "lstPoints": lstP, "sameList": listf(sameList)}


@point_man.route("/upsert", methods=["POST"])
def r_pointman_upsert():
    try:
        for dictRow in request.get_json()["list"]:
            resP = PointPoints.query.filter_by(**dfl(dictRow, ["type_id", "stu_id", "name"])).one_or_none()
            if resP is None:
                print("insert")
                db.session.add(PointPoints(**dfln(resP, ["id"])))
            else:
                print("update")
                for k in dictRow.keys():
                    setattr(resP, k, dictRow[k])  # 事件被before_flush拦截
                db.session.add(resP)
        db.session.commit()
    except TypeError as e:
        current_app.logger.error(e)
        return abort_err(472)
    except OperationalError as e:
        current_app.logger.error(e)
        return abort_err(532)
    else:
        return {"success": True}


@point_man.route("/total")
def r_pointman_total():
    return {"total": getTotal()}


def getTotal():
    return db.session.execute("select count(*) from point_points").scalar()
