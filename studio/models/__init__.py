from flask import current_app, g
from sqlalchemy import event, inspect, not_
from sqlalchemy.orm import (
    InstanceState,
    ORMExecuteState,
    Session,
    attributes,
    make_transient,
    with_loader_criteria,
)

from .base import EditHistory, MixinBase, db  # noqa: F401
from .issue import IssueDutyUsersRe, IssueIssues, IssueTypes  # noqa: F401
from .point import PointPoints, PointTypes  # noqa: F401
from .route import RouteInterceptors  # noqa: F401
from .user import UserGroupMembersRe, UserGroups, UserUsers  # noqa: F401
from .voltime import Voltime, VoltimeDupname  # noqa: F401
from .enroll import EnrollCandidates, EnrollDepts, EnrollTurns
from .media import MediaList


@event.listens_for(Session, "before_flush")
def before_flush(session: Session, _flush_context, _instances):
    current_app.logger.info("before_flush")
    current_app.logger.info(f"insert: {session.new}")
    current_app.logger.info(f"update: {session.dirty}")  # 拦截条件: 查询获取->修改类成员->add->commit
    current_app.logger.info(f"delete: {session.deleted}")  # 拦截条件: 查询获取->delete->commit
    for instance in session.dirty:
        if not session.is_modified(instance):  # 导致dirty的原因不止是“修改”
            continue
        if not attributes.instance_state(instance).has_identity:  # ??
            continue

        # 此处可以修改属性值, 同样会使has_changes()为True, 例如
        # instance.team = 'before_flush'

        # /orm/internals.html#sqlalchemy.orm.InstanceState
        # /orm/internals.html#sqlalchemy.orm.AttributeState
        # /orm/session_api.html#sqlalchemy.orm.attributes.History
        state: InstanceState = inspect(instance)
        for attr in state.attrs:
            if attr.history.has_changes():
                edit = EditHistory(
                    type="modified",
                    table_name=instance.__tablename__,
                    row_id=instance.id,
                    attr_name=attr.key,
                    details=str(attr.history),
                    edit_by=g.user.id,
                )
                session.add(edit)
        instance.update_cnt += 1  # 版本号加1

    for instance in session.deleted:
        make_transient(instance)  # 取消当前操作
        session.query(instance.__class__).filter_by(id=instance.id).update({"deleted": True})  # 添加删除标记
        print(g.user)
        edit = EditHistory(type="deleted", table_name=instance.__tablename__, row_id=instance.id, edit_by=g.user.id)
        session.add(edit)


@event.listens_for(Session, "do_orm_execute")
def do_orm_execute(orm_execute_state: ORMExecuteState):
    # /orm/session_api.html#sqlalchemy.orm.ORMExecuteState
    current_app.logger.info("do_orm_execute")
    current_app.logger.info(
        f"is_delete: {orm_execute_state.is_delete}; "
        f"is_insert: {orm_execute_state.is_insert}; "
        f"is_select: {orm_execute_state.is_select}; "
        f"is_update: {orm_execute_state.is_update}"  # 拦截条件: 查询获取.update()
    )

    # 文档: /orm/session_events.html#adding-global-where-on-criteria
    if (
        orm_execute_state.is_select
        and not orm_execute_state.is_column_load
        and not orm_execute_state.is_relationship_load
    ):
        orm_execute_state.statement = orm_execute_state.statement.options(
            with_loader_criteria(
                MixinBase, lambda cls: not_(cls.deleted), include_aliases=True, propagate_to_loaders=False
            )
        )
        # orm_execute_state.statement = orm_execute_state.statement.filter_by(deleted=False)

    print(orm_execute_state.statement)
