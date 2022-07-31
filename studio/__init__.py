from dotenv import load_dotenv
from flask import Flask

from studio.models import db

from .api.apivue import apivue
from .utils import cache, logger_handler
from .utils.interceptor import global_interceptor


def create_app():
    app = Flask(__name__)

    # 从环境变量加载初始配置
    load_dotenv()
    app.config.from_prefixed_env()

    # 根据运行环境, 从配置文件加载对应配置
    from config import dictConfig

    app.config.from_object(dictConfig[app.config["ENV"]])

    # 插件初始化
    db.init_app(app)
    cache.init_app(app)

    # 配置日志记录器
    app.logger.addHandler(logger_handler())

    # 添加拦截器, 进行用户鉴权
    app.before_request(global_interceptor)

    # 注册一级蓝图
    app.register_blueprint(apivue)

    # 添加根路由
    app.add_url_rule("/", view_func=lambda: "This is homepage.")

    return app
