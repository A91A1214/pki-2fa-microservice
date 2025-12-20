from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from app.crypto_utils import decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code, get_seconds_remaining

app = FastAPI()

SEED_FILE = "data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"


# Pydantic models for POST requests
class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: DecryptRequest):
    """
    Decrypts the RSA-encrypted seed and saves it to data/seed.txt
    """
    try:
        seed_hex = decrypt_seed(request.encrypted_seed, PRIVATE_KEY_FILE)
        os.makedirs("data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(seed_hex)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa_endpoint():
    """
    Generates the current TOTP code using the stored seed
    """
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not loaded")

    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    code = generate_totp_code(seed_hex)
    valid_for = get_seconds_remaining()
    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa_endpoint(request: VerifyRequest):
    """
    Verifies the submitted TOTP code
    """
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not loaded")

    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    valid = verify_totp_code(seed_hex, request.code)
    return {"valid": valid}
