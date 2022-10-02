from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from flask_caching import Cache

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


def logger_handler():
    Path.mkdir(Path("log"), exist_ok=True)
    handler = TimedRotatingFileHandler("log/studio.log", when="W0", delay=True)
    formatter = Formatter("[%(asctime)s] %(levelname)s:%(name)s - %(pathname)s:%(lineno)s in %(funcName)s: %(message)s")
    handler.setFormatter(formatter)
    return handler


def abort_err(code: int, details: str = None, **kwargs):
    dictDesc = {
        401: "需要登录",
        403: "权限不足",
        461: "账号需要验证",
        462: "登录失败",
        463: "登录过期",
        471: "参数错误",
        472: "参数未知",
        532: "数据库数据错误",
        533: "数据库完整性错误",
        541: "数据库查询应有但没有结果",
    }
    return {"success": False, "details": details or dictDesc[code], **kwargs}, code


def dfc(dictA: dict, classK: object):
    """Utils: dict filter by class."""
    return {k: v for k, v in dictA.items() if hasattr(classK, k)}


def dfd(dictA: dict, dictK: dict):
    """Utils: dict filter by dict with default value."""
    return {k: dictA.get(k) or v for k, v in dictK.items()}


def dfl(dictA: dict, lstK: list):
    """Utils: dict filter by list."""
    return {k: v for k, v in dictA.items() if k in lstK}


def dfln(dictA: dict, lstK: list = []):
    """Utils: dict filter by not list."""
    lstK += ["create_time", "update_time", "update_cnt", "deleted"]
    return {k: v for k, v in dictA.items() if k not in lstK}


def listf(lstA: list):
    return [x[0] for x in lstA]
