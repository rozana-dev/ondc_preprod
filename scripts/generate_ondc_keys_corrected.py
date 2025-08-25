#!/usr/bin/env python3
"""
ONDC Key Generation Script - CORRECTED VERSION
Generates Ed25519 signing keys and X25519 encryption keys as per ONDC requirements
with proper domain verification logic
"""

import base64
import json
import os
import hashlib
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


def sign_request_id_corrected(request_id: str, signing_private_key_obj, subscriber_id: str):
    """
    Sign request ID using Ed25519 private key with proper ONDC verification logic
    Based on ONDC specification for domain verification
    """
    # Create the verification string as per ONDC specification
    # Format: subscriber_id + "|" + request_id
    verification_string = f"{subscriber_id}|{request_id}"
    
    # Sign the verification string
    signature = signing_private_key_obj.sign(verification_string.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')


def sign_request_id_simple(request_id: str, signing_private_key_obj):
    """
    Simple signing - just sign the request ID directly
    This is the original method that might be expected
    """
    signature = signing_private_key_obj.sign(request_id.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')


def sign_request_id_hash(request_id: str, signing_private_key_obj):
    """
    Sign hashed request ID - some implementations expect this
    """
    # Hash the request ID first
    request_hash = hashlib.sha256(request_id.encode('utf-8')).digest()
    signature = signing_private_key_obj.sign(request_hash)
    return base64.b64encode(signature).decode('utf-8')


def main():
    """Generate all required keys and credentials for ONDC with corrected verification"""
    print("🔐 Generating ONDC Keys - CORRECTED VERSION...")
    
    subscriber_id = "neo-server.rozana.in"
    
    # Generate signing key pair (Ed25519)
    print("📝 Generating Ed25519 signing key pair...")
    signing_keys = generate_ed25519_keypair()
    
    # Generate encryption key pair (X25519)
    print("🔒 Generating X25519 encryption key pair...")
    encryption_keys = generate_x25519_keypair()
    
    # Generate unique request ID
    request_id = generate_unique_request_id()
    print(f"🆔 Generated request ID: {request_id}")
    
    # Generate multiple verification signatures using different methods
    print("✍️  Generating verification signatures...")
    
    # Method 1: Simple signing (original)
    signed_request_id_simple = sign_request_id_simple(request_id, signing_keys['private_key_obj'])
    
    # Method 2: ONDC specification format
    signed_request_id_ondc = sign_request_id_corrected(request_id, signing_keys['private_key_obj'], subscriber_id)
    
    # Method 3: Hash-based signing
    signed_request_id_hash = sign_request_id_hash(request_id, signing_keys['private_key_obj'])
    
    print(f"Simple signature: {signed_request_id_simple[:20]}...")
    print(f"ONDC signature: {signed_request_id_ondc[:20]}...")
    print(f"Hash signature: {signed_request_id_hash[:20]}...")
    
    # Create credentials object with all signatures
    credentials = {
        "generated_at": datetime.utcnow().isoformat(),
        "subscriber_id": subscriber_id,
        "request_id": request_id,
        "verification_signatures": {
            "simple": signed_request_id_simple,
            "ondc_format": signed_request_id_ondc,
            "hash_based": signed_request_id_hash
        },
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
    credentials_file = "secrets/ondc_credentials_corrected.json"
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print(f"💾 Credentials saved to: {credentials_file}")
    
    # Create multiple verification files for testing
    verification_files = {
        "simple": signed_request_id_simple,
        "ondc_format": signed_request_id_ondc,
        "hash_based": signed_request_id_hash
    }
    
    for method, signature in verification_files.items():
        verification_content = f"""<!-- Contents of ondc-site-verification.html ({method}) -->
<html>
    <head>
        <meta name='ondc-site-verification' content='{signature}' />
    </head>
    <body>
        ONDC Site Verification Page ({method})
        <br>
        Subscriber ID: {subscriber_id}
        <br>
        Request ID: {request_id}
        <br>
        Method: {method}
        <br>
        Generated: {datetime.utcnow().isoformat()}
    </body>
</html>"""
        
        filename = f"ondc-site-verification-{method}.html"
        with open(filename, 'w') as f:
            f.write(verification_content)
        
        print(f"📄 Created {filename}")
    
    # Create the main verification file (using ONDC format as default)
    main_verification_content = f"""<!-- Contents of ondc-site-verification.html -->
<html>
    <head>
        <meta name='ondc-site-verification' content='{signed_request_id_ondc}' />
    </head>
    <body>
        ONDC Site Verification Page
        <br>
        Subscriber ID: {subscriber_id}
        <br>
        Request ID: {request_id}
        <br>
        Method: ONDC Format
        <br>
        Generated: {datetime.utcnow().isoformat()}
    </body>
</html>"""
    
    with open("ondc-site-verification.html", 'w') as f:
        f.write(main_verification_content)
    
    print("📄 Created ondc-site-verification.html (main file)")
    
    # Display summary
    print("\n" + "="*60)
    print("🎉 ONDC Keys Generated Successfully - CORRECTED!")
    print("="*60)
    print(f"Subscriber ID: {subscriber_id}")
    print(f"Request ID: {request_id}")
    print(f"Unique Key ID: {credentials['unique_key_id']}")
    print(f"Signing Public Key: {signing_keys['public_key']}")
    print(f"Encryption Public Key: {encryption_keys['public_key']}")
    
    print("\n🔍 Verification Methods Generated:")
    print(f"1. Simple: {signed_request_id_simple[:30]}...")
    print(f"2. ONDC Format: {signed_request_id_ondc[:30]}...")
    print(f"3. Hash-based: {signed_request_id_hash[:30]}...")
    
    print("\n📋 Next Steps:")
    print("1. Test each verification file with ONDC registry")
    print("2. Upload the working verification file to your server")
    print("3. Update your application to use the new keys")
    print("4. Test the /on_subscribe endpoint with challenge decryption")
    print("5. Submit /subscribe request to ONDC registry")
    
    print("\n🧪 Testing Commands:")
    print("curl https://neo-server.rozana.in/ondc-site-verification.html")
    print("python3 ondc_subscribe_with_schema.py")
    
    print("="*60)


if __name__ == "__main__":
    main() 