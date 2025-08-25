#!/usr/bin/env python3
"""
Simplified ONDC Signing and Verification Utilities
Based on ONDC Official Reference Implementation
"""

import base64
import datetime
import json
import sys
import nacl.encoding
import nacl.hash
from nacl.bindings import crypto_sign_ed25519_sk_to_seed
from nacl.signing import SigningKey, VerifyKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

def hash_message(msg: str):
    """Hash message using BLAKE2b"""
    HASHER = nacl.hash.blake2b
    digest = HASHER(bytes(msg, 'utf-8'), digest_size=64, encoder=nacl.encoding.Base64Encoder)
    digest_str = digest.decode("utf-8")
    return digest_str

def create_signing_string(digest_base64, created=None, expires=None):
    """Create signing string for authorization header"""
    if created is None:
        created = int(datetime.datetime.now().timestamp())
    if expires is None:
        expires = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    signing_string = f"""(created): {created}
(expires): {expires}
digest: BLAKE-512={digest_base64}"""
    return signing_string

def generate_key_pairs():
    """Generate Ed25519 signing keys and X25519 encryption keys"""
    print("Generating ONDC Key Pairs...")
    
    # Generate Ed25519 signing keys
    signing_key = SigningKey.generate()
    signing_private_key = base64.b64encode(signing_key.encode()).decode()
    signing_public_key = base64.b64encode(signing_key.verify_key.encode()).decode()
    
    # Generate X25519 encryption keys
    encryption_private_key = X25519PrivateKey.generate()
    encryption_public_key = encryption_private_key.public_key()
    
    # Serialize encryption keys
    encryption_private_key_der = encryption_private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    encryption_public_key_der = encryption_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    encryption_private_key_b64 = base64.b64encode(encryption_private_key_der).decode()
    encryption_public_key_b64 = base64.b64encode(encryption_public_key_der).decode()
    
    print(f"Signing_private_key: {signing_private_key}")
    print(f"Signing_public_key: {signing_public_key}")
    print(f"Encryption_Privatekey: {encryption_private_key_b64}")
    print(f"Encryption_Publickey: {encryption_public_key_b64}")
    
    return {
        "signing_private_key": signing_private_key,
        "signing_public_key": signing_public_key,
        "encryption_private_key": encryption_private_key_b64,
        "encryption_public_key": encryption_public_key_b64
    }

def create_authorization_header(request_body_path="ondc_request_body.json", private_key=None):
    """Create authorization header for ONDC API calls"""
    try:
        # Load request body
        with open(request_body_path, 'r') as f:
            request_body = json.load(f)
        
        # Minify the payload
        request_body_str = json.dumps(request_body, separators=(',', ':'))
        
        # Hash the message
        digest = hash_message(request_body_str)
        
        # Create signing string
        created = int(datetime.datetime.now().timestamp())
        expires = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
        signing_string = create_signing_string(digest, created, expires)
        
        # Sign the string
        if private_key:
            private_key_bytes = base64.b64decode(private_key)
            seed = crypto_sign_ed25519_sk_to_seed(private_key_bytes)
            signer = SigningKey(seed)
            signed = signer.sign(bytes(signing_string, encoding='utf8'))
            signature = base64.b64encode(signed.signature).decode()
        else:
            # Use a test signature for demonstration
            signature = "test_signature_base64_encoded"
        
        # Create authorization header
        key_id = "neo-server.rozana.in|key_1755737751|ed25519"
        auth_header = f'Signature keyId="{key_id}",algorithm="ed25519",created="{created}",expires="{expires}",headers="(created) (expires) digest",signature="{signature}"'
        
        print(f"Authorization Header: {auth_header}")
        return auth_header
        
    except Exception as e:
        print(f"Error creating authorization header: {e}")
        return None

def main():
    """Main function to run ONDC utilities"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ondc_simple_utils.py generate_key_pairs")
        print("  python ondc_simple_utils.py create_auth_header [private_key]")
        return
    
    command = sys.argv[1]
    
    if command == "generate_key_pairs":
        generate_key_pairs()
    elif command == "create_auth_header":
        private_key = sys.argv[2] if len(sys.argv) > 2 else None
        create_authorization_header(private_key=private_key)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 