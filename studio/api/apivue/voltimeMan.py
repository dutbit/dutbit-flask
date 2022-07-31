from flask import Blueprint, current_app, request
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import NoResultFound, OperationalError
from studio.models import Voltime, db
from studio.utils import abort_err, dfd, dfln, listf

voltime_man = Blueprint("voltime_man", __name__, url_prefix="/voltime-man")


@voltime_man.route("/", methods=["POST"])
def r_voltimeman():
    dictReq = dfd(request.get_json(), {"pageNum": 1, "pageSize": 30, "searchText": ""})

    searchText = dictReq["searchText"]
    queryV: BaseQuery = Voltime.query
    sameList = []
    if searchText.isdigit():
        queryV = queryV.filter_by(stu_id=searchText)
        sameList = db.session.query(Voltime.name).filter_by(stu_id=searchText).group_by(Voltime.name).all()
    elif searchText != "":
        queryV = queryV.filter_by(name=searchText)
        sameList = db.session.query(Voltime.stu_id).filter_by(name=searchText).group_by(Voltime.stu_id).all()

    pagV = queryV.order_by(Voltime.date.desc()).paginate(dictReq["pageNum"], dictReq["pageSize"], False, 200)
    lstV = []
    for row in pagV.items:
        row = dfln(row.__dict__, ["_sa_instance_state"])
        row["date"] = row["date"].strftime("%Y-%m-%d")
        lstV.append(row)
    return {"total": pagV.total, "lstVoltimes": lstV, "sameList": listf(sameList)}


@voltime_man.route("/insert", methods=["POST"])
def r_voltimeman_insert():
    nRows_old = getTotal()
    try:
        for row in request.get_json()["list"]:
            db.session.add(Voltime(**dfln(row)))
        db.session.commit()
    except TypeError as e:
        current_app.logger.error(e)
        return abort_err(472)
    except OperationalError as e:
        current_app.logger.error(e)
        return abort_err(532)
    else:
        intNew = getTotal() - nRows_old
        strInfo = f"操作成功，插入{intNew}条新记录"
        current_app.logger.info(strInfo)
        return {"success": True, "details": strInfo, "intNew": intNew}


@voltime_man.route("/update", methods=["POST"])
def r_voltimeman_update():
    try:
        dictReq = dfln(request.get_json())
        resV = Voltime.query.filter_by(id=dictReq["id"]).one()
        for k in dictReq.keys():
            setattr(resV, k, dictReq[k])  # 事件被before_flush拦截
        db.session.add(resV)

        # 以下事件被do_orm_execute拦截
        # db.session.query(Voltime).filter_by(id=dictReq["id"]).update(dfl(dictReq, ["stu_id", "name"]))
        db.session.commit()
    except NoResultFound as e:
        current_app.logger.error(e)
        return abort_err(541)
    else:
        return {"success": True}


@voltime_man.route("/delete", methods=["POST"])
def r_voltimeman_delete():
    for intID in request.get_json()["lstIDs"]:
        row = Voltime.query.filter_by(id=intID).one_or_none()
        if row is not None:
            db.session.delete(row)
    db.session.commit()
    return {"success": True}


@voltime_man.route("/total")
def r_voltimeman_total():
    return {"total": getTotal()}


def getTotal():
    return db.session.execute("select count(*) from voltime").scalar()
