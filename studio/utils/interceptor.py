from flask import current_app, g, request
from studio.models import RouteInterceptors, UserUsers, db
from studio.utils import cache, abort_err
from studio.utils.jwt import load_token


def global_interceptor():
    payload = load_token(request.headers.get("Authorization"))
    if payload == "ExpiredSignature":
        return abort_err(463, login_target=request.path)

    if payload is None:
        g.user = None
    else:
        g.user = get_user(payload["id"])
        current_app.logger.info(f"user id: {g.user.id}")

    rules = get_all_rules()
    for r in rules:
        if not request.path.startswith(r.startswith):
            continue
        if g.user is None:
            return abort_err(401, login_target=request.path)
        if not g.user.confirmed:
            return abort_err(461, login_target=request.path)
        if not (1 in payload["lstGIDs"] or r.group_id in payload["lstGIDs"]):
            # 不是【root用户 或者 有该权限的用户】
            return abort_err(403)
        break

    return None


@cache.memoize(30)
def get_all_rules() -> list[RouteInterceptors]:
    return RouteInterceptors.query.all()


@cache.memoize(60)
def get_user(user_id) -> UserUsers:
    return UserUsers.query.filter(UserUsers.id == user_id).first()


@cache.memoize(60)
def get_startswiths(lstGIDs) -> list[int]:
    tupSWs = db.session.query(RouteInterceptors.startswith).filter(RouteInterceptors.group_id.in_(lstGIDs)).all()
    return [x[0] for x in tupSWs]
