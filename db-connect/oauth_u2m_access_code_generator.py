import hashlib, base64, secrets, string

# Allowed characters for the code verifier, per PKCE spec
allowed_chars = string.ascii_letters + string.digits + "-._~"

# Generate a secure code verifier (43–128 characters)
code_verifier = ''.join(secrets.choice(allowed_chars) for _ in range(64))

# Create the SHA256 hash of the code verifier
sha256_hash = hashlib.sha256(code_verifier.encode()).digest()

# Base64-url-encode the hash and strip any trailing '=' padding
code_challenge = base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")

# Output values
print(f"code_verifier:  {code_verifier}")
print(f"code_challenge: {code_challenge}")