from settings import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


task_user = db.Table("task_user", db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("task_id", db.Integer, db.ForeignKey("task.id")))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    time = db.Column(db.Integer, nullable=True, default=0)
    tasks = db.relationship("Task", secondary=task_user, backref=db.backref("users"), lazy="dynamic")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "time": self.time,
            "tasks": self.tasks
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.String(1000), unique=True, nullable=False)
    result = db.Column(db.Integer, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "time": self.time,
            "result": self.result
        }


if __name__ == "__main__":
    db.create_all()
