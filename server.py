from flask import Flask, request
from models import db, Todo, IdNotFoundError

app = Flask(__name__)


@app.route("/items")
def items():
    todo_list = Todo.get()
    return {"content": [todo.serialize() for todo in todo_list]}, 200


@app.route("/create", methods=["PUT"])
def create():
    title = request.get_json().get("title")
    todo = Todo.create(title)
    return {"message": f"added '{title}'", "todo": todo.serialize()}, 201


@app.route("/update/<int:todo_id>", methods=["PUT"])
def update(todo_id):
    try:
        todo = Todo.update(todo_id)
    except IdNotFoundError:
        return '', 304
    return {"message": f"updated todo '{todo.title}'", "todo": todo.serialize()}, 200


@app.route("/delete/<int:todo_id>", methods=["DELETE"])
def delete(todo_id):
    try:
        todo = Todo.delete(todo_id)
    except IdNotFoundError:
        return '', 304
    return {"message": f"deleted todo '{todo.title}'", "todo": todo.serialize()}, 200


def run_app():
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    app.run(debug=False)


def prod_mode():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


def test_mode():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite.test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


if __name__ == "__main__":
    prod_mode()
    run_app()
