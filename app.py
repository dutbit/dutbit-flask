from studio import create_app
from studio.models import UserGroups, db

app = create_app()


def db_create_all():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(UserGroups(group_name="管理员", description="管理员用户组"))
        db.session.add(UserGroups(group_name="普通用户", description="普通用户组"))
        db.session.commit()


if __name__ == "__main__":
    # db_create_all()
    app.run(debug=False)
