import sys
import json
import base64

# --- PASTE YOUR COPIED TOKEN BELOW ---
# It should look like "Bearer eyJhbGci..."
token_string = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk4OGQ1YTM3OWI3OGJkZjFlNTBhNDA5MTEzZjJiMGM3NWU0NTJlNDciLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiWmF5YWFuIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3NhbmRib3gtMzA5ODAzIiwiYXVkIjoic2FuZGJveC0zMDk4MDMiLCJhdXRoX3RpbWUiOjE3NjY0MDEzNjYsInVzZXJfaWQiOiJOWUVnY0F6NGFoZjhybHY1WmJ1eUtUMUkyclgyIiwic3ViIjoiTllFZ2NBejRhaGY4cmx2NVpidXlLVDFJMnJYMiIsImlhdCI6MTc2NjQwMTM2NiwiZXhwIjoxNzY2NDA0OTY2LCJlbWFpbCI6Inptb2hhbWVkQG1hdnZyaWsuYWkiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ6bW9oYW1lZEBtYXZ2cmlrLmFpIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQiLCJ0ZW5hbnQiOiJrZ2JpYm12YXN0LW1saGNoIn19.qFhKnEuo2138R4nNV6P1EJ6i36vSk_zEghcaZi_ZOMjEl-RI2A4rqpZzx7rVOPMCp6fI9B1O_O0acs36yJTP8ZHKcYOcRx2cmolUsiukLlHA7FzsYf8J0-NqhiqZixX72t13Kbi2PTsUD8bw-8KhI799trg6zMCGAwqWYDEdrYsKs_R6TqFzPr6fHdPVebaarGOHJWwyXKxQS88urZbu0eNgnK7r9opXjoA3SojHMrlzsGVg8vjgoyzciWb4hv3Od0eNaPb_lgi50Ns2TOlaLqPsz2iGA-Gv8lVL3O2p8INtInZAWzSI7btAo38sXizSzss9eV_P_TJLpyADLanxLA" 
# -------------------------------------

def get_auth_url(auth_header):
    try:
        # Clean the prefix
        if auth_header.startswith("Bearer "):
            auth_header = auth_header.split(" ")[1]
            
        # JWTs are 3 parts separated by dots. We need the middle part (Payload).
        parts = auth_header.split(".")
        if len(parts) < 2:
            print("❌ Error: Not a valid JWT token.")
            return

        # Decode the payload (add padding if needed)
        payload_b64 = parts[1]
        payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
        payload_data = base64.urlsafe_b64decode(payload_b64)
        claims = json.loads(payload_data)
        
        # The 'iss' (Issuer) claim is the URL we are looking for
        issuer = claims.get('iss')
        
        if issuer:
            print(f"\n✅ SUCCESS! FOUND AUTH URL:")
            print(f"---------------------------")
            print(f"auth_base_url = \"{issuer.rstrip('/')}\"")
            print(f"---------------------------\n")
            print("Action: Update this URL in your src/config.py file.")
        else:
            print("❌ Error: Token does not contain an 'iss' (Issuer) field.")
            
    except Exception as e:
        print(f"❌ Error decoding token: {e}")

if __name__ == "__main__":
    get_auth_url(token_string)