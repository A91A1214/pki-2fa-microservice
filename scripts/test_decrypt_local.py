from app.crypto_utils import decrypt_seed

# Paths
PRIVATE_KEY_FILE = "student_private.pem"
ENCRYPTED_FILE = "encrypted_seed.txt"

# Read encrypted seed
with open(ENCRYPTED_FILE, "r") as f:
    encrypted_seed = f.read().strip()

# Decrypt
try:
    seed_hex = decrypt_seed(encrypted_seed, PRIVATE_KEY_FILE)
    print("✅ Decrypted seed:", seed_hex)
except Exception as e:
    print("❌ Decryption failed:", e)
