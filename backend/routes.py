from flask import jsonify, render_template, request, redirect, url_for, session, flash
import os
import threading
from datetime import date
from sqlalchemy import func
from functools import wraps
from backend.models import get_session, PC, Sale, User
from backend.utils import wake_on_lan

def register_routes(app):

    def login_required(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            return f(*args, **kwargs)
        return wrapper

    def admin_required(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("user_role") != "admin":
                return "Доступ запрещён", 403
            return f(*args, **kwargs)
        return wrapper

    @app.route("/")
    @login_required
    def index():
        return render_template("home.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            login = request.form.get("login")
            password = request.form.get("password")
            with get_session() as db:
                user = db.query(User).filter(User.login == login).first()
                if user and user.check_password(password):
                    session["user_id"] = user.id
                    session["user_role"] = user.role
                    return redirect("/")
            flash("Неверный логин или пароль", "error")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    @app.route("/shutdown", methods=["POST"])
    def shutdown():
        def stop():
            os._exit(0)
        threading.Thread(target=stop).start()
        return "Сервер выключается..."

    @app.route("/api/pcs", methods=["GET"])
    def get_pcs():
        with get_session() as db:
            pcs = db.query(PC).all()
            return jsonify([
                {
                    "id": pc.id,
                    "name": pc.name,
                    "ip": pc.ip_address,
                    "mac": pc.mac_address,
                    "is_online": pc.is_online,
                    "in_use": pc.in_use,
                    "position": pc.position or 0
                } for pc in pcs
            ])

    @app.route("/api/stats", methods=["GET"])
    def get_stats():
        with get_session() as db:
            today = date.today()
            sales_today = db.query(func.count(Sale.id))\
                .filter(func.date(Sale.created_at) == today)\
                .scalar()
            total_revenue = db.query(func.coalesce(func.sum(Sale.total_price), 0.0)).scalar()
            return jsonify({
                "sales_today": sales_today,
                "total_revenue": total_revenue
            })

    @app.route("/map")
    @login_required
    def map_view():
        with get_session() as db:
            pcs = db.query(PC).order_by(PC.position).all()
            return render_template("map.html", pcs=pcs)

    @app.route("/map/update-position", methods=["POST"])
    @login_required
    def update_position():
        data = request.get_json()
        with get_session() as db:
            pc = db.query(PC).filter_by(id=int(data["id"])).first()
            if pc:
                pc.pos_x = int(data["x"])
                pc.pos_y = int(data["y"])
        return jsonify({"status": "ok"})


    @app.route("/map/<int:pc_id>/wake", methods=["POST"])
    @login_required
    def wake_pc(pc_id):
        with get_session() as db:
            pc = db.query(PC).filter(PC.id == pc_id).first()
            if pc:
                wake_on_lan(pc.mac_address)
        return redirect(url_for('map_view'))

    @app.route("/admin/employees")
    @admin_required
    def admin_employees():
        with get_session() as db:
            employees = db.query(User).all()
            return render_template("admin_employees.html", employees=employees)
