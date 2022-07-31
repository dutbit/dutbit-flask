import oss2
from flask import Blueprint, current_app

dayimgO = Blueprint("dayimgO", __name__, url_prefix="/dayimg-oss")


def get_bucket():
    auth = oss2.Auth(current_app.config["OSS_ID"], current_app.config["OSS_SECRET"])
    return oss2.Bucket(auth, "https://oss-cn-qingdao.aliyuncs.com", "dutbit")


@dayimgO.route("/cata")
def dayImage_cata():
    iterObj = oss2.ObjectIteratorV2(get_bucket(), prefix="dayimg/", delimiter="/", fetch_owner=True)
    lstCata = [str(x.key).split("/")[1] for x in iterObj if x.is_prefix()]
    return {"lstCata": lstCata}


@dayimgO.route("/cont/<dirCont>")
def dayImage_cont(dirCont):
    iterObj = oss2.ObjectIteratorV2(get_bucket(), prefix=f"dayimg/{dirCont}/", delimiter="/", fetch_owner=True)
    lstCont = [str(x.key).split("/")[2] for x in iterObj if not x.is_prefix()]
    return {"lstCont": lstCont}
