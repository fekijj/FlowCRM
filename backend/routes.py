from flask import jsonify, render_template, request
import os
import threading
import sys

def register_routes(app):
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/api/ping')
    def ping():
        return jsonify({"status": "pong"})

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        def stop():
            os._exit(0)
        threading.Thread(target=stop).start()
        return "Сервер выключается..."
