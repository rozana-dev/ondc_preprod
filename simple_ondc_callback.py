#!/usr/bin/env python3
"""
Simple ONDC Callback Handler
Handles /on_subscribe endpoint for ONDC subscription challenges
"""

import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ONDCCallbackHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to /on_subscribe"""
        if self.path == '/on_subscribe':
            try:
                # Get content length
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                # Parse JSON
                body = json.loads(post_data.decode('utf-8'))
                logger.info(f"Received ONDC callback: {json.dumps(body, indent=2)}")
                
                # Handle ONDC challenge
                if "challenge" in body and "subscriber_id" in body:
                    challenge = body.get("challenge")
                    subscriber_id = body.get("subscriber_id")
                    
                    logger.info(f"Processing challenge for subscriber: {subscriber_id}")
                    logger.info(f"Encrypted challenge: {challenge}")
                    
                    # For now, return a simple response
                    # In a real implementation, you would decrypt the challenge
                    response = {
                        "answer": f"decrypted_challenge_{challenge[:10]}",
                        "status": "ACK"
                    }
                    
                elif "status" in body:
                    # Handle status updates
                    status_update = body.get("status")
                    logger.info(f"Status update: {status_update}")
                    
                    response = {
                        "status": "ACK",
                        "message": "Status update received"
                    }
                    
                else:
                    # Unknown callback type
                    response = {
                        "status": "ACK",
                        "message": "Callback received"
                    }
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response_json = json.dumps(response)
                self.wfile.write(response_json.encode('utf-8'))
                
                logger.info(f"Sent response: {response_json}")
                
            except Exception as e:
                logger.error(f"Error processing callback: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                error_response = {
                    "error": "Internal server error",
                    "message": str(e)
                }
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET requests for testing"""
        if self.path == '/on_subscribe/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "OK",
                "message": "ONDC callback endpoint is working",
                "endpoint": "/on_subscribe"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")

def run_server(port=8001):
    """Run the simple ONDC callback server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ONDCCallbackHandler)
    logger.info(f"Starting ONDC callback server on port {port}")
    logger.info(f"Test endpoint: http://localhost:{port}/on_subscribe/test")
    logger.info(f"Callback endpoint: http://localhost:{port}/on_subscribe")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server() 