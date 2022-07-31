from flask import Blueprint, request
from studio.models import PointPoints
from studio.utils import dfl, dfln

point = Blueprint("point", __name__, url_prefix="/point")  # 创建二级蓝图


@point.route("/", methods=["POST"])
def pointsQuery():
    dictReq = dfl(request.get_json(), ["type_id", "stu_id", "name"])
    resPoints = PointPoints.query.filter_by(**dictReq).one_or_none()
    if resPoints is not None:
        dictRow = dfln(resPoints.__dict__, ["_sa_instance_state", "id"])
        return {**dictReq, "dictRow": dictRow}

    return {"success": False, "details": "无查询结果"}
