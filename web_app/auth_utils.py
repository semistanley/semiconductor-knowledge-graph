from __future__ import annotations

from functools import wraps

from flask import jsonify, redirect, request, session, url_for

from database import db
from models import User


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "请先登录", "code": "UNAUTHORIZED"}), 401
            return redirect(url_for("login_page", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def get_current_user() -> User | None:
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)


def register_user(username: str, email: str, password: str) -> tuple[User | None, str | None]:
    username = (username or "").strip()
    email = (email or "").strip().lower()
    password = password or ""

    if len(username) < 3:
        return None, "用户名至少 3 个字符"
    if "@" not in email:
        return None, "邮箱格式不正确"
    if len(password) < 6:
        return None, "密码至少 6 个字符"
    if User.query.filter_by(username=username).first():
        return None, "用户名已存在"
    if User.query.filter_by(email=email).first():
        return None, "邮箱已注册"

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None


def authenticate_user(username_or_email: str, password: str) -> tuple[User | None, str | None]:
    key = (username_or_email or "").strip()
    user = User.query.filter(
        (User.username == key) | (User.email == key.lower())
    ).first()
    if not user or not user.check_password(password):
        return None, "用户名或密码错误"
    return user, None
