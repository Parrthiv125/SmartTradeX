from fastapi import APIRouter
from smarttradex_core.database.postgres_db import PostgresDB
import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "smarttradex_secret"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth")


# =========================================
# REGISTER
# =========================================
@router.post("/register")
def register_user(data: dict):

    try:

        # FIELD MAPPING
        name = (
            data.get("name")
            or data.get("full_name")
        )

        email = (
            data.get("email")
            or data.get("email_address")
        )

        password = data.get("password")

        confirm = (
            data.get("confirm")
            or data.get("confirm_password")
        )

        # VALIDATION
        if not password:
            return {"error": "Password missing"}

        if password != confirm:
            return {"error": "Passwords do not match"}

        # HASH PASSWORD
        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        # DB INSERT
        db = PostgresDB()
        conn = db.conn
        cursor = conn.cursor()

        query = """
        INSERT INTO users
        (name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, hashed)
        )

        conn.commit()

        return {"status": "User registered"}

    except Exception as e:

        print("REGISTER ERROR:", e)

        return {"error": str(e)}

# =========================================
# LOGIN
# =========================================
# =========================================
@router.post("/login")
def login_user(data: dict):

    try:

        email = data.get("email")
        password = data.get("password")

        db = PostgresDB()
        conn = db.conn
        cursor = conn.cursor()

        query = """
        SELECT id, password
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))
        row = cursor.fetchone()

        if not row:
            return {"error": "User not found"}

        user_id = row[0]
        stored_hash = row[1].encode()

        if not bcrypt.checkpw(
            password.encode(),
            stored_hash
        ):
            return {"error": "Invalid password"}

        # -----------------------------
        # CREATE TOKEN
        # -----------------------------
        payload = {

            "user_id": user_id,
            "exp": datetime.utcnow()
                   + timedelta(hours=24)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {

            "status": "Login success",
            "token": token
        }

    except Exception as e:

        return {"error": str(e)}