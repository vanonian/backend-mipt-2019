from itsdangerous import URLSafeTimedSerializer

from web_app import app

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email)


def verify_token(token, expiration=1200):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, max_age=expiration)
    except:
        return ""
    return email
