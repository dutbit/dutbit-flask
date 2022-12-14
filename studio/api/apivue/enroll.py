import json

import datetime
from sqlalchemy import or_, and_
from flask import Blueprint, request, send_file, g
from studio.models import EnrollCandidates, EnrollDepts, EnrollTurns, db
from studio.utils import dfl, listf

enroll = Blueprint("enroll", __name__, url_prefix="/enroll")


@enroll.route("/getDepts", methods=["GET"])
def r_get_depts():
    depts = db.session.query(EnrollDepts.id, EnrollDepts.dept_name).filter(EnrollDepts.deleted == 0).all()
    result = []
    for dept in depts:
        result.append({
            "id": dept.id,
            "deptName": dept.dept_name
        })
    return {"depts": result}


@enroll.route("/getDeletedDepts", methods=["GET"])
def r_get_deleted_depts():
    depts = db.session.query(EnrollDepts.id, EnrollDepts.dept_name).filter(EnrollDepts.deleted == 1).all()
    result = []
    for dept in depts:
        result.append({
            "id": dept.id,
            "deptName": dept.dept_name
        })
    return {"depts": result}


@enroll.route("/recoverDept", methods=["POST"])
def r_recover_dept():
    dept = request.get_json()["dept"]
    enrollDept = EnrollDepts.query.get(dept["id"])
    enrollDept.deleted = 0
    db.session.commit()
    return {"success": True}


@enroll.route("/setDept", methods=["POST"])
def r_set_dept():
    dept = request.get_json()["dept"]
    enrollDept = EnrollDepts.query.get(dept["id"])
    enrollDept.dept_name = dept["deptName"]
    db.session.commit()
    return {"success": True}


@enroll.route("/deleteDept", methods=["POST"])
def r_delete_dept():
    dept = request.get_json()["dept"]
    enrollDept = EnrollDepts.query.get(dept["id"])
    enrollDept.deleted = 1
    db.session.commit()
    return {"success": True}


@enroll.route("/createDept", methods=["POST"])
def r_create_dept():
    dictReq = request.get_json()["dept"]
    dept = EnrollDepts(dept_name=dictReq["deptName"])
    db.session.add(dept)
    db.session.commit()
    return {"success": True}


@enroll.route("/getTurns", methods=["GET"])
def r_get_turns():
    turns = db.session.query(EnrollTurns.id, EnrollTurns.turn_name, EnrollTurns.activated).filter(
        EnrollTurns.deleted == 0).all()
    result = []
    for turn in turns:
        result.append({
            "id": turn.id,
            "turnName": turn.turn_name,
            "activated": turn.activated
        })
    return {"turns": result}


@enroll.route("/getDeletedTurns", methods=["GET"])
def r_get_deleted_turns():
    turns = db.session.query(EnrollTurns.id, EnrollTurns.turn_name, EnrollTurns.activated).filter(
        EnrollTurns.deleted == 1).all()
    result = []
    for turn in turns:
        result.append({
            "id": turn.id,
            "turnName": turn.turn_name,
            "activated": turn.activated
        })
    return {"turns": result}


@enroll.route("/recoverTurn", methods=["POST"])
def r_recover_turn():
    turn = request.get_json()["turn"]
    enrollTurn = EnrollTurns.query.get(turn["id"])
    enrollTurn.deleted = 0
    db.session.commit()
    return {"success": True}


@enroll.route("/setTurn", methods=["POST"])
def r_set_turn():
    turn = request.get_json()["turn"]
    enrollTurn = EnrollTurns.query.get(turn["id"])
    enrollTurn.turnName = turn["turnName"]
    enrollTurn.activated = turn["activated"]
    db.session.commit()
    return {"success": True}


@enroll.route("/deleteTurn", methods=["POST"])
def r_delete_turn():
    turn = request.get_json()["turn"]
    enrollTurn = EnrollTurns.query.get(turn["id"])
    enrollTurn.deleted = 1
    enrollTurn.activated = 0
    db.session.commit()
    return {"success": True}


@enroll.route("/createTurn", methods=["POST"])
def r_create_turn():
    dictReq = request.get_json()["turn"]
    turn = EnrollTurns(turn_name=dictReq["turnName"])
    turn.activated = 0
    db.session.add(turn)
    db.session.commit()
    return {"success": True}


@enroll.route("/submit", methods=["POST"])
def r_submit():
    dictReq = request.get_json()
    enrollCandidate = EnrollCandidates(
        **dfl(dictReq, ["stu_id", "name", "sex", "faculty", "tel",
                        "first_choice", "second_choice", "third_choice", "allow_adjust", "info", "turn_id"])
    )
    queryCandidate = db.session.query(EnrollCandidates) \
        .filter(and_(or_(EnrollCandidates.stu_id == enrollCandidate.id, EnrollCandidates.name == enrollCandidate.name),
                     EnrollCandidates.turn_id == enrollCandidate.turn_id)).first()
    if queryCandidate is None:
        db.session.add(enrollCandidate)
        db.session.commit()
    else:
        # ?????????????????????????????????
        db.session.delete(queryCandidate)
        db.session.add(enrollCandidate)
        db.session.commit()
    return {"success": True}


@enroll.route("/verifyUnique", methods=["POST"])
def r_verify_unique():
    dictReq = request.get_json()["info"]
    stuId = dictReq["stuId"]
    name = dictReq["name"]
    turnId = dictReq["turnId"]
    queryCandidate = db.session.query(EnrollCandidates) \
        .filter(and_(or_(EnrollCandidates.stu_id == stuId, EnrollCandidates.name == name),
                     EnrollCandidates.turn_id == turnId)).first()
    if queryCandidate is None:
        return {"unique": True}
    else:
        # ?????????????????????????????????????????????
        t = queryCandidate.update_time + datetime.timedelta(hours=8)
        return {"unique": False, "time": t.strftime("%Y-%m-%d %H:%M:%S")}


@enroll.route("/getEnrollList", methods=["POST"])
def r_get_enroll_list():
    # ??????????????????????????????
    turnId = request.get_json()["turnId"]
    # turnData = db.session.query(EnrollTurns.id).filter(turnId == EnrollTurns.id)
    # if turnData.deleted:
    #     return {"enrollCandidates": []}
    # ????????????
    queryData = db.session.query(EnrollCandidates)
    # ?????????????????????????????????
    if turnId > 0:
        candidates = queryData.filter(and_(EnrollCandidates.turn_id == turnId, EnrollCandidates.deleted == 0)).all()
    else:
        candidates = queryData.filter(EnrollCandidates.deleted == 0).all()
    result = []
    for candidate in candidates:
        result.append({
            "id": candidate.id,
            "stuId": candidate.stu_id,
            "name": candidate.name,
            "sex": candidate.sex,
            "faculty": candidate.faculty,
            "tel": candidate.tel,
            "allowAdjust": candidate.allow_adjust,
            "firstChoice": candidate.first_choice,
            "secondChoice": candidate.second_choice,
            "thirdChoice": candidate.third_choice,
            "info": candidate.info,
            "turnId": candidate.turn_id
        })
    return {"enrollCandidates": result}
