from datetime import UTC, datetime
from hashlib import md5

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

followers = sa.Table(
    "followers",
    db.metadata,
    sa.Column("follower_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("followed_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
)


class User(UserMixin, db.Model):  # ty: ignore[unsupported-base]
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.Text(), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.Text(), index=True, unique=True)
    password_hash: so.Mapped[str | None] = so.mapped_column(sa.Text())
    about_me: so.Mapped[str | None] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[datetime | None] = so.mapped_column(
        default=lambda: datetime.now(UTC)
    )

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    # following/followers mapping through the `followers` table
    following: so.WriteOnlyMapped["User"] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates="followers",
    )
    followers: so.WriteOnlyMapped["User"] = so.relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates="following",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int = 128) -> str:
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def follow(self, user: "User") -> None:
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user: "User") -> None:
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user: "User") -> bool:
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self) -> int:
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery()
        )
        return db.session.scalar(query) or 0

    def following_count(self) -> int:
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery()
        )
        return db.session.scalar(query) or 0

    def following_posts(self) -> sa.Select["Post"]:
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(
                sa.or_(
                    Follower.id == self.id,
                    Author.id == self.id,
                )
            )
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )

    def __repr__(self):
        return f"<User {self.id}, {self.username}>"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Post(db.Model):  # ty: ignore[unsupported-base]
    __tablename__ = "posts"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text())
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(UTC)
    )

    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.id}, {self.body}>"
