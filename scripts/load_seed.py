from pathlib import Path
from app.crypto_utils import decrypt_seed

ENCRYPTED_SEED_FILE = "encrypted_seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"

DATA_DIR = Path("data")
SEED_FILE = DATA_DIR / "seed.txt"

DATA_DIR.mkdir(exist_ok=True)

# Read encrypted seed
with open(ENCRYPTED_SEED_FILE, "r") as f:
    encrypted_seed = f.read().strip()

# Decrypt seed using private key
seed_hex = decrypt_seed(encrypted_seed, PRIVATE_KEY_FILE)

if len(seed_hex) != 64:
    raise ValueError("Seed length is not 64 hex characters")

# Save seed
with open(SEED_FILE, "w") as f:
    f.write(seed_hex)

print("✅ Seed decrypted and saved to data/seed.txt")
