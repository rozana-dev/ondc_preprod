"""
ONDC Cryptography Module
Handles encryption, decryption, signing, and verification for ONDC protocol
"""

import base64
import json
import logging
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os

logger = logging.getLogger(__name__)


class ONDCCrypto:
    """ONDC Cryptography handler"""
    
    def __init__(self):
        self.credentials = self._load_credentials()
        self.signing_private_key = self._load_signing_private_key()
        self.encryption_private_key = self._load_encryption_private_key()
    
    def _load_credentials(self) -> Dict[str, Any]:
        """Load ONDC credentials from file"""
        try:
            with open("secrets/ondc_credentials.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("ONDC credentials file not found. Generate keys first.")
            return {}
        except Exception as e:
            logger.error(f"Error loading ONDC credentials: {e}")
            return {}
    
    def _load_signing_private_key(self) -> Optional[Ed25519PrivateKey]:
        """Load Ed25519 signing private key"""
        if not self.credentials:
            return None
        
        try:
            private_key_b64 = self.credentials['signing_keys']['private_key']
            private_key_bytes = base64.b64decode(private_key_b64)
            return Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        except Exception as e:
            logger.error(f"Error loading signing private key: {e}")
            return None
    
    def _load_encryption_private_key(self) -> Optional[X25519PrivateKey]:
        """Load X25519 encryption private key"""
        if not self.credentials:
            return None
        
        try:
            private_key_b64 = self.credentials['encryption_keys']['private_key']
            private_key_bytes = base64.b64decode(private_key_b64)
            return X25519PrivateKey.from_private_bytes(private_key_bytes)
        except Exception as e:
            logger.error(f"Error loading encryption private key: {e}")
            return None
    
    def get_ondc_public_key(self, environment: str = "staging") -> Optional[X25519PublicKey]:
        """Get ONDC public key for the specified environment"""
        if not self.credentials:
            return None
        
        try:
            ondc_public_key_b64 = self.credentials['ondc_public_keys'][environment]
            # ONDC public key is in DER format, need to decode it
            ondc_public_key_der = base64.b64decode(ondc_public_key_b64)
            return serialization.load_der_public_key(ondc_public_key_der)
        except Exception as e:
            logger.error(f"Error loading ONDC public key for {environment}: {e}")
            return None
    
    def create_shared_key(self, environment: str = "staging") -> Optional[bytes]:
        """Create shared key for encryption/decryption"""
        if not self.encryption_private_key:
            logger.error("Encryption private key not available")
            return None
        
        ondc_public_key = self.get_ondc_public_key(environment)
        if not ondc_public_key:
            logger.error(f"ONDC public key not available for {environment}")
            return None
        
        try:
            # Perform X25519 key exchange
            shared_key = self.encryption_private_key.exchange(ondc_public_key)
            
            # Use HKDF to derive a 32-byte key for AES-256
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'',
            ).derive(shared_key)
            
            return derived_key
        except Exception as e:
            logger.error(f"Error creating shared key: {e}")
            return None
    
    def decrypt_challenge(self, encrypted_challenge: str, environment: str = "staging") -> Optional[str]:
        """Decrypt ONDC challenge using shared key"""
        try:
            # Get shared key
            shared_key = self.create_shared_key(environment)
            if not shared_key:
                return None
            
            # Decode base64 encrypted challenge
            encrypted_data = base64.b64decode(encrypted_challenge)
            
            # Extract IV (first 16 bytes) and ciphertext
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # Decrypt using AES-256-CBC
            cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove PKCS7 padding
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error decrypting challenge: {e}")
            return None
    
    def sign_data(self, data: str) -> Optional[str]:
        """Sign data using Ed25519 private key"""
        if not self.signing_private_key:
            logger.error("Signing private key not available")
            return None
        
        try:
            signature = self.signing_private_key.sign(data.encode('utf-8'))
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            logger.error(f"Error signing data: {e}")
            return None
    
    def verify_signature(self, data: str, signature: str, public_key_b64: str) -> bool:
        """Verify signature using Ed25519 public key"""
        try:
            public_key_bytes = base64.b64decode(public_key_b64)
            public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
            
            signature_bytes = base64.b64decode(signature)
            public_key.verify(signature_bytes, data.encode('utf-8'))
            return True
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
    
    def get_signing_public_key(self) -> Optional[str]:
        """Get base64 encoded signing public key"""
        if not self.credentials:
            return None
        return self.credentials['signing_keys']['public_key']
    
    def get_encryption_public_key(self) -> Optional[str]:
        """Get base64 encoded encryption public key"""
        if not self.credentials:
            return None
        return self.credentials['encryption_keys']['public_key']
    
    def get_unique_key_id(self) -> Optional[str]:
        """Get unique key ID"""
        if not self.credentials:
            return None
        return self.credentials['unique_key_id']
    
    def get_request_id(self) -> Optional[str]:
        """Get request ID"""
        if not self.credentials:
            return None
        return self.credentials['request_id']
    
    def get_signed_request_id(self) -> Optional[str]:
        """Get signed request ID"""
        if not self.credentials:
            return None
        return self.credentials['signed_request_id']


# Global crypto instance
crypto = ONDCCrypto()