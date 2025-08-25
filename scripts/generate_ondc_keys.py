#!/usr/bin/env python3
"""
ONDC Key Generation Script
Generates Ed25519 signing keys and X25519 encryption keys as per ONDC requirements
"""

import base64
import json
import os
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def generate_ed25519_keypair():
    """Generate Ed25519 signing key pair"""
    private_key = Ed25519PrivateKey.generate()
    
    # Get private key in raw format (32 bytes) and base64 encode
    private_key_raw = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_b64 = base64.b64encode(private_key_raw).decode('utf-8')
    
    # Get public key in raw format (32 bytes) and base64 encode
    public_key = private_key.public_key()
    public_key_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    public_key_b64 = base64.b64encode(public_key_raw).decode('utf-8')
    
    return {
        'private_key': private_key_b64,
        'public_key': public_key_b64,
        'private_key_obj': private_key,
        'public_key_obj': public_key
    }


def generate_x25519_keypair():
    """Generate X25519 encryption key pair"""
    private_key = X25519PrivateKey.generate()
    
    # Get private key in raw format and base64 encode
    private_key_raw = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_b64 = base64.b64encode(private_key_raw).decode('utf-8')
    
    # Get public key in ASN.1 DER format and base64 encode (as required by ONDC)
    public_key = private_key.public_key()
    public_key_der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_b64 = base64.b64encode(public_key_der).decode('utf-8')
    
    return {
        'private_key': private_key_b64,
        'public_key': public_key_b64,
        'private_key_obj': private_key,
        'public_key_obj': public_key
    }


def generate_unique_request_id():
    """Generate unique request ID"""
    import uuid
    return str(uuid.uuid4())


def sign_request_id(request_id: str, signing_private_key_obj):
    """Sign request ID using Ed25519 private key (without hashing)"""
    signature = signing_private_key_obj.sign(request_id.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')


def main():
    """Generate all required keys and credentials for ONDC"""
    print("🔐 Generating ONDC Keys...")
    
    # Generate signing key pair (Ed25519)
    print("📝 Generating Ed25519 signing key pair...")
    signing_keys = generate_ed25519_keypair()
    
    # Generate encryption key pair (X25519)
    print("🔒 Generating X25519 encryption key pair...")
    encryption_keys = generate_x25519_keypair()
    
    # Generate unique request ID
    request_id = generate_unique_request_id()
    print(f"🆔 Generated request ID: {request_id}")
    
    # Sign the request ID
    signed_request_id = sign_request_id(request_id, signing_keys['private_key_obj'])
    print(f"✍️  Signed request ID: {signed_request_id}")
    
    # Create credentials object
    credentials = {
        "generated_at": datetime.utcnow().isoformat(),
        "subscriber_id": "neo-server.rozana.in",
        "request_id": request_id,
        "signed_request_id": signed_request_id,
        "signing_keys": {
            "private_key": signing_keys['private_key'],
            "public_key": signing_keys['public_key']
        },
        "encryption_keys": {
            "private_key": encryption_keys['private_key'],
            "public_key": encryption_keys['public_key']
        },
        "unique_key_id": f"key_{int(datetime.utcnow().timestamp())}",
        "ondc_public_keys": {
            "prod": "MCowBQYDK2VuAyEAvVEyZY91O2yV8w8/CAwVDAnqIZDJJUPdLUUKwLo3K0M=",
            "pre_prod": "MCowBQYDK2VuAyEAa9Wbpvd9SsrpOZFcynyt/TO3x0Yrqyys4NUGIvyxX2Q=",
            "staging": "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="
        }
    }
    
    # Create secrets directory if it doesn't exist
    os.makedirs("secrets", exist_ok=True)
    
    # Save credentials to file
    credentials_file = "secrets/ondc_credentials.json"
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print(f"💾 Credentials saved to: {credentials_file}")
    
    # Create site verification file
    verification_content = f"""<!-- Contents of ondc-site-verification.html -->
<html>
    <head>
        <meta name='ondc-site-verification' content='{signed_request_id}' />
    </head>
    <body>
        ONDC Site Verification Page
        <br>
        Subscriber ID: neo-server.rozana.in
        <br>
        Generated: {datetime.utcnow().isoformat()}
    </body>
</html>"""
    
    with open("ondc-site-verification.html", 'w') as f:
        f.write(verification_content)
    
    print("📄 Created ondc-site-verification.html")
    
    # Display summary
    print("\n" + "="*60)
    print("🎉 ONDC Keys Generated Successfully!")
    print("="*60)
    print(f"Subscriber ID: neo-server.rozana.in")
    print(f"Request ID: {request_id}")
    print(f"Unique Key ID: {credentials['unique_key_id']}")
    print(f"Signing Public Key: {signing_keys['public_key']}")
    print(f"Encryption Public Key: {encryption_keys['public_key']}")
    print("\n📋 Next Steps:")
    print("1. Host ondc-site-verification.html at https://neo-server.rozana.in/ondc-site-verification.html")
    print("2. Update your application to use these keys")
    print("3. Test the /on_subscribe endpoint with challenge decryption")
    print("4. Submit /subscribe request to ONDC registry")
    print("="*60)


if __name__ == "__main__":
    main()