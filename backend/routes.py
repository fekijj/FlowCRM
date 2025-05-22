from flask import jsonify, render_template, request, redirect, url_for
import os
import threading
from datetime import date
from sqlalchemy import func
from backend.models import SessionLocal, PC, Sale
from backend.utils import wake_on_lan

def register_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/shutdown", methods=["POST"])
    def shutdown():
        def stop():
            os._exit(0)
        threading.Thread(target=stop).start()
        return "Сервер выключается..."

    @app.route("/api/pcs", methods=["GET"])
    def get_pcs():
        db = SessionLocal()
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
        db = SessionLocal()
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
    def map_view():
        db = SessionLocal()
        pcs = db.query(PC).order_by(PC.position).all()
        return render_template("map.html", title="Карта клуба", pcs=pcs)

    @app.route("/map/update-order", methods=["POST"])
    def update_pc_order():
        data = request.get_json()
        order = data.get("order", [])
        db = SessionLocal()
        for index, pc_id in enumerate(order):
            pc = db.query(PC).filter(PC.id == int(pc_id)).first()
            if pc:
                pc.position = index
        db.commit()
        return jsonify({"status": "ok"})

    @app.route("/map/<int:pc_id>/wake", methods=["POST"])
    def wake_pc(pc_id):
        db = SessionLocal()
        pc = db.query(PC).filter(PC.id == pc_id).first()
        if pc:
            wake_on_lan(pc.mac_address)
        return redirect(url_for('map_view'))
