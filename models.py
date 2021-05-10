from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class IdNotFoundError(Exception):
    pass


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    done = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }

    @classmethod
    def get(cls):
        return cls.query.all()

    @classmethod
    def create(cls, title):
        new_todo = Todo(title=title, done=False)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    @classmethod
    def update(cls, todo_id):
        todo = Todo.query.filter_by(id=todo_id).first()
        if not todo:
            raise IdNotFoundError
        todo.done = not todo.done
        db.session.commit()
        return todo

    @classmethod
    def delete(cls, todo_id):
        todo = Todo.query.filter_by(id=todo_id).first()
        if not todo:
            raise IdNotFoundError
        db.session.delete(todo)
        db.session.commit()
        return todo
