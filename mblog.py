from app import app


@app.shell_context_processor
def make_shell_context():
    import sqlalchemy as sa
    import sqlalchemy.orm as so

    from app import db
    from app.models import Post, User

    return {"sa": sa, "so": so, "db": db, "User": User, "Post": Post}
