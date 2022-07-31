from flask import Blueprint, request
from studio.models import Voltime, VoltimeDupname, db
from studio.utils import cache, dfl, dfln

voltime = Blueprint("voltime", __name__, url_prefix="/voltime")


@voltime.route("/", methods=["POST"])
def r_voltime():
    req = dfl(request.get_json(), ["stu_id", "name"])  # dictReq
    dictR = {**req, "lstVoltimes": [], "totalDuration": 0}  # dictResp

    resV = Voltime.query.filter_by(**req).order_by(Voltime.date.desc()).all()
    for row in resV:
        row = dfln(row.__dict__, ["_sa_instance_state", "id"])
        row["date"] = row["date"].strftime("%Y-%m-%d") if row["date"].year > 2005 else row["date_str"]
        dictR["lstVoltimes"].append(row)
        dictR["totalDuration"] += float(row["duration"])

    dictR["numSameID"] = db.session.query(Voltime.name).filter_by(stu_id=req["stu_id"]).group_by(Voltime.name).count()
    dictR["numSameName"] = db.session.query(Voltime.stu_id).filter_by(name=req["name"]).group_by(Voltime.stu_id).count()

    resD = db.session.query(VoltimeDupname).filter_by(name=req["name"]).one_or_none()
    dictR["numDupName"] = 1 if resD is None else resD.dup_num
    return dictR


@voltime.route("/lastdate")
@cache.memoize(2000)
def r_voltime_lastdate():
    lastDate = db.session.query(Voltime.date).order_by(Voltime.date.desc()).limit(1).scalar()
    lastDate = lastDate.strftime("%Y-%m-%d")
    return {"lastDate": lastDate}


@voltime.route("/top")
@cache.memoize(3600)
def r_voltime_top():
    strSQL = (
        "SELECT CONCAT(LEFT(stu_id, 6), '***') AS stu_id, `name`, SUM(duration) AS total "
        "FROM voltime GROUP BY stu_id, `name` ORDER BY total DESC LIMIT 1,100"
    )  # 仅Mysql
    res = db.session.execute(strSQL).all()
    return {"lstTop": [x._asdict() for x in res]}
