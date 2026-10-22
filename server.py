import os
from datetime import timedelta
from flask import abort
import agent

secret = os.environ.get('SECRET_KEY', '')
password = os.environ.get('ADMIN_PASSWORD', '')
if len(secret) < 32 or secret in {'ulug-bek-ai-secret', 'uzoq_maxfiy_kalit_yozing'}:
    raise RuntimeError('SECRET_KEY must be a new random secret of at least 32 characters.')
if len(password) < 16:
    raise RuntimeError('ADMIN_PASSWORD must be a new secret of at least 16 characters.')

app = agent.app
app.secret_key = secret
agent.ADMIN_PASSWORD = password
app.config.update(
    DEBUG=False,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    MAX_CONTENT_LENGTH=131072,
)

@app.before_request
def block_static_source_files():
    from flask import request
    if request.endpoint == 'static':
        abort(404)

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'same-origin'
    response.headers['Cache-Control'] = 'no-store'
    return response
