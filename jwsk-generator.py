from jwcrypto import jwk
import json

# Step 1: Generate RSA key pair
key = jwk.JWK.generate(kty='RSA', size=2048)

# Export private key
private_pem = key.export_to_pem(private_key=True, password=None)
with open("private.key", "wb") as f:
    f.write(private_pem)

# Export public key
public_pem = key.export_to_pem()
with open("public.pem", "wb") as f:
    f.write(public_pem)

# Step 2: Create JWKS
key_dict = json.loads(key.export_public())
key_dict["kid"] = "d2l-test-key"
key_dict["use"] = "sig"
key_dict["alg"] = "RS256"

jwks = {"keys": [key_dict]}

# Save JWKS
with open("jwks.json", "w") as f:
    json.dump(jwks, f, indent=2)

print("Files created:")
print("- private.key")
print("- public.pem")
print("- jwks.json")