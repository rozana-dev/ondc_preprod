#!/usr/bin/env python3

"""
🔍 ONDC API Schema v2.0 Compliance Validator
Validates responses against ONDC API Schema v2.0 for Pramaan testing
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys

class ONDCSchemaValidator:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.results = []
        
    def validate_context(self, context: Dict[str, Any], action: str) -> List[str]:
        """Validate ONDC context object"""
        errors = []
        
        required_fields = [
            'domain', 'country', 'city', 'action', 'core_version',
            'bap_id', 'bap_uri', 'transaction_id', 'message_id', 'timestamp'
        ]
        
        for field in required_fields:
            if field not in context:
                errors.append(f"Missing required context field: {field}")
        
        # Validate specific field formats
        if 'domain' in context and not context['domain'].startswith('ONDC:'):
            errors.append(f"Invalid domain format: {context['domain']}")
            
        if 'country' in context and context['country'] != 'IND':
            errors.append(f"Invalid country: {context['country']}")
            
        if 'action' in context and context['action'] != action:
            errors.append(f"Action mismatch: expected {action}, got {context['action']}")
            
        if 'core_version' in context and not context['core_version'].startswith('1.'):
            errors.append(f"Invalid core_version: {context['core_version']}")
            
        # Validate timestamp format
        if 'timestamp' in context:
            try:
                datetime.fromisoformat(context['timestamp'].replace('Z', '+00:00'))
            except ValueError:
                errors.append(f"Invalid timestamp format: {context['timestamp']}")
        
        return errors
    
    def validate_message(self, message: Dict[str, Any], action: str) -> List[str]:
        """Validate ONDC message object"""
        errors = []
        
        # Most responses should have an ack field
        if 'ack' not in message:
            errors.append("Missing 'ack' field in message")
        elif 'status' not in message['ack']:
            errors.append("Missing 'status' field in ack")
        elif message['ack']['status'] not in ['ACK', 'NACK']:
            errors.append(f"Invalid ack status: {message['ack']['status']}")
        
        return errors
    
    def test_endpoint(self, endpoint: str, method: str = 'POST', payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Test a single endpoint for schema compliance"""
        url = f"{self.base_url}{endpoint}"
        
        if payload is None:
            payload = {
                "context": {
                    "domain": "ONDC:RET10",
                    "country": "IND",
                    "city": "std:011",
                    "action": endpoint.lstrip('/'),
                    "core_version": "1.2.0",
                    "bap_id": "neo-server.rozana.in",
                    "bap_uri": self.base_url,
                    "transaction_id": f"test_{int(datetime.now().timestamp())}",
                    "message_id": f"msg_{int(datetime.now().timestamp())}",
                    "timestamp": datetime.now().isoformat() + "Z"
                },
                "message": {}
            }
        
        result = {
            'endpoint': endpoint,
            'method': method,
            'url': url,
            'status': 'UNKNOWN',
            'http_code': 0,
            'response_time': 0,
            'schema_errors': [],
            'response_data': None
        }
        
        try:
            start_time = datetime.now()
            
            if method == 'GET':
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(
                    url, 
                    json=payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
            
            end_time = datetime.now()
            result['response_time'] = (end_time - start_time).total_seconds() * 1000
            result['http_code'] = response.status_code
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    result['response_data'] = response_data
                    
                    # Validate schema if it's a proper JSON response
                    if isinstance(response_data, dict):
                        if 'context' in response_data:
                            context_errors = self.validate_context(
                                response_data['context'], 
                                f"on_{endpoint.lstrip('/')}"
                            )
                            result['schema_errors'].extend(context_errors)
                        else:
                            result['schema_errors'].append("Missing 'context' object")
                        
                        if 'message' in response_data:
                            message_errors = self.validate_message(
                                response_data['message'],
                                endpoint.lstrip('/')
                            )
                            result['schema_errors'].extend(message_errors)
                        else:
                            result['schema_errors'].append("Missing 'message' object")
                    
                    result['status'] = 'PASS' if not result['schema_errors'] else 'SCHEMA_ERROR'
                    
                except json.JSONDecodeError:
                    # Handle non-JSON responses (like "OK")
                    result['response_data'] = response.text
                    if response.text == "OK":
                        result['status'] = 'SIMPLE_OK'
                    else:
                        result['schema_errors'].append("Response is not valid JSON")
                        result['status'] = 'JSON_ERROR'
            else:
                result['status'] = 'HTTP_ERROR'
                result['response_data'] = response.text
                
        except requests.exceptions.RequestException as e:
            result['status'] = 'CONNECTION_ERROR'
            result['schema_errors'].append(f"Connection error: {str(e)}")
        
        return result
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete ONDC schema validation"""
        
        print("🔍 ONDC API Schema v2.0 Compliance Validator")
        print("=" * 50)
        print(f"Testing: {self.base_url}")
        print()
        
        # Core ONDC endpoints
        endpoints_to_test = [
            ('/search', 'POST'),
            ('/select', 'POST'),
            ('/init', 'POST'),
            ('/confirm', 'POST'),
            ('/status', 'POST'),
            ('/track', 'POST'),
            ('/cancel', 'POST'),
            ('/update', 'POST'),
            ('/rating', 'POST'),
            ('/support', 'POST'),
            ('/on_subscribe', 'GET'),
            ('/health', 'GET'),
            ('/ekyc/health', 'GET'),
            ('/ekyc/search', 'POST'),
            ('/ekyc/verify', 'POST'),
        ]
        
        total_tests = len(endpoints_to_test)
        passed = 0
        schema_compliant = 0
        
        for endpoint, method in endpoints_to_test:
            print(f"Testing: {endpoint} ({method})")
            result = self.test_endpoint(endpoint, method)
            self.results.append(result)
            
            if result['status'] in ['PASS', 'SIMPLE_OK']:
                passed += 1
                if result['status'] == 'PASS':
                    schema_compliant += 1
                print(f"  ✅ {result['status']} ({result['response_time']:.0f}ms)")
            else:
                print(f"  ❌ {result['status']}")
                for error in result['schema_errors']:
                    print(f"     • {error}")
            print()
        
        # Summary
        print("📊 Validation Summary")
        print("=" * 30)
        print(f"Total Endpoints: {total_tests}")
        print(f"Working: {passed}")
        print(f"Schema Compliant: {schema_compliant}")
        print(f"Success Rate: {(passed/total_tests)*100:.1f}%")
        print(f"Schema Compliance: {(schema_compliant/total_tests)*100:.1f}%")
        
        if passed == total_tests:
            print("\n🎉 All endpoints are working!")
        
        if schema_compliant == total_tests:
            print("✅ Full ONDC Schema v2.0 compliance!")
        elif schema_compliant > 0:
            print(f"⚠️  {total_tests - schema_compliant} endpoints need schema fixes")
        else:
            print("❌ Schema compliance needs improvement")
        
        return {
            'total': total_tests,
            'passed': passed,
            'schema_compliant': schema_compliant,
            'results': self.results
        }

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://neo-server.rozana.in"
    
    validator = ONDCSchemaValidator(base_url)
    summary = validator.run_full_validation()
    
    # Return appropriate exit code
    if summary['passed'] == summary['total']:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()