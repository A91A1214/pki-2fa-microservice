import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt_seed(encrypted_seed_b64: str, private_key_path: str) -> str:
    # Load private key
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )

    # Decode base64 ciphertext
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)
# Decrypt using RSA-OAEP + SHA256
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Convert bytes → hex string
    seed_hex = decrypted.hex()

    # Validate length (must be 64 hex chars)
    if len(seed_hex) != 64:
        raise ValueError("Decrypted seed must be 64 hex characters")

    return seed_hex
