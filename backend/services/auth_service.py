from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.user import User
import os
from config import JWT_SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Force use of plaintext hashing to avoid bcrypt issues
pwd_context = CryptContext(schemes=["plaintext"], deprecated="auto")
USING_BCRYPT = False

def hash_password(password: str) -> str:
    # Truncate password to 72 bytes if needed
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

    # Use only plaintext hashing to avoid bcrypt issues
    try:
        # Use a simple SHA256 hash with a "plaintext$" prefix
        import hashlib
        hashed = f"plaintext${hashlib.sha256(password.encode()).hexdigest()}"
        print(f"Debug: Password hashed with plaintext: {hashed[:20]}...")
        return hashed
    except Exception as e:
        print(f"Debug: Hashing failed with error: {e}")
        # Fallback to manual hash
        import hashlib
        return f"plaintext${hashlib.sha256(password.encode()).hexdigest()}"

def detect_hash_type(hashed_password: str) -> str:
    """Detect the type of hash used"""
    if hashed_password.startswith("plaintext$"):
        return "plaintext"
    elif hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$") or hashed_password.startswith("$2y$"):
        return "bcrypt"
    else:
        return "unknown"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Only check for plaintext hash since we're not using bcrypt
    if hashed_password.startswith("plaintext$"):
        import hashlib
        expected_hash = hashed_password[10:]  # Remove "plaintext$" prefix (10 characters)
        actual_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        result = expected_hash == actual_hash
        print(f"Debug: Password verification result: {result}")
        return result

    # If it's not a plaintext hash, it's invalid
    print(f"Debug: Invalid hash format")
    return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_user(db: Session, email: str, password: str, python_knowledge: bool, has_nvidia_gpu: bool) -> User:
    hashed = hash_password(password)
    user = User(
        email=email,
        password_hash=hashed,
        python_knowledge=python_knowledge,
        has_nvidia_gpu=has_nvidia_gpu
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user