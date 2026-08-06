# routers/auth.py
from dependencies import get_current_user
from fastapi import APIRouter, HTTPException, status, Depends
from models import UserCreate, UserOut, UserLogin, Token
from database import get_connection
from security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    # Check if username or email already exists
    cur.execute(
        "SELECT id FROM users WHERE username = %s OR email = %s",
        (user.username, user.email)
    )
    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed_pw = hash_password(user.password)

    cur.execute(
        """
        INSERT INTO users (username, email, hashed_password)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, created_at
        """,
        (user.username, user.email, hashed_pw)
    )
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": new_user[0],
        "username": new_user[1],
        "email": new_user[2],
        "created_at": new_user[3]
    }

@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, hashed_password FROM users WHERE email = %s",
        (credentials.email,)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not verify_password(credentials.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user[1], "user_id": user[0]})
    return {"access_token": access_token, "token_type": "bearer"}
@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user