"""
server.py — Dripp Media Backend
Run: python3 server.py

Endpoints:
  POST /api/contact       — Save lead + send emails
  POST /api/community     — Save community sign-up
  GET  /admin             — Admin dashboard (password protected)
  GET  /admin/login       — Login page
  POST /admin/login       — Authenticate
  GET  /admin/logout      — Clear session
  POST /admin/status      — Update lead status
"""

import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ─── Load .env ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("[ENV] Loaded .env")
else:
    print("[ENV] No .env found — using environment variables / defaults")
    print("[ENV] Copy .env.example to .env and fill in your SMTP credentials.")

# ─── Flask App ────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None)
app.secret_key = os.getenv("SECRET_KEY", "dripp-secret-key-change-me")

# Allow requests from the HTML file opened locally (file://) and localhost
CORS(app, origins=["http://localhost", "http://127.0.0.1",
                   "http://localhost:5000", "http://127.0.0.1:5000",
                   "http://localhost:5001", "http://127.0.0.1:5001",
                   "null"],  # 'null' origin = file:// in browsers
     supports_credentials=True)

# ─── Database Init ────────────────────────────────────────────────────────────
sys.path.insert(0, BASE_DIR)
from db import init_db
init_db()

# ─── Register Blueprints ──────────────────────────────────────────────────────
from routes.contact   import contact_bp
from routes.community import community_bp
from routes.admin     import admin_bp

app.register_blueprint(contact_bp)
app.register_blueprint(community_bp)
app.register_blueprint(admin_bp)

# ─── Serve the main site HTML ─────────────────────────────────────────────────
SITE_DIR = os.path.join(BASE_DIR, "..", "Final Dripp")

@app.route("/")
def serve_site():
    return send_from_directory(SITE_DIR, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(SITE_DIR, filename)

# ─── Health Check ─────────────────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Dripp Media Backend"})

# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"""
╔══════════════════════════════════════════════╗
║          DRIPP MEDIA BACKEND                 ║
╠══════════════════════════════════════════════╣
║  Site    →  http://localhost:{port}             ║
║  Admin   →  http://localhost:{port}/admin        ║
║  Health  →  http://localhost:{port}/api/health   ║
╚══════════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=port, debug=True)
