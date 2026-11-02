import jwt
import datetime

SECRET = "super-secret-key-12345"
payload = {
    "sub": "student_user",
    "name": "Student",
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print(f"Generated Token:\n{token}")