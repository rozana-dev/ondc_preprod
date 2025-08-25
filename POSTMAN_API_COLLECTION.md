# ONDC BAP API Routes - Postman Collection

## Base URL
```
https://neo-server.rozana.in
```

## 🏥 Health Check Endpoints

### 1. Health Check (K8s Style)
- **Method**: `GET`
- **URL**: `{{base_url}}/healthz`
- **Description**: Kubernetes-style health check
- **Expected Response**: 
```json
{
  "status": "ok"
}
```

### 2. Liveness Probe
- **Method**: `GET`
- **URL**: `{{base_url}}/livez`
- **Description**: Liveness probe endpoint
- **Expected Response**: 
```json
{
  "status": "ok"
}
```

### 3. Readiness Probe
- **Method**: `GET`
- **URL**: `{{base_url}}/readyz`
- **Description**: Readiness probe endpoint
- **Expected Response**: 
```json
{
  "status": "ok"
}
```

## 🔔 ONDC Subscription Endpoints

### 4. ONDC Subscription Callback
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/on_subscribe`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body (Challenge Test)**:
```json
{
  "challenge": "test_challenge_123",
  "subscriber_id": "neo-server.rozana.in"
}
```
- **Body (Status Update Test)**:
```json
{
  "status": "SUBSCRIBED",
  "subscriber_id": "neo-server.rozana.in",
  "timestamp": "2024-12-20T10:00:00Z"
}
```

### 5. Test Subscription Callback
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/on_subscribe/test`
- **Description**: Test endpoint to verify callback URL accessibility

### 6. Verification Page
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/verification`
- **Description**: HTML verification page for ONDC
- **Response**: HTML page

## 🛒 ONDC Core Action Endpoints

### 7. Search
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/search`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "search",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-123",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "test product"
        }
      }
    }
  }
}
```

### 8. Select
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/select`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "select",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-124",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order": {
      "items": [
        {
          "id": "item_1",
          "quantity": {
            "count": 1
          }
        }
      ]
    }
  }
}
```

### 9. Init
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/init`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "init",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-125",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order": {
      "billing": {
        "name": "John Doe",
        "phone": "9876543210"
      },
      "fulfillments": [
        {
          "end": {
            "location": {
              "address": {
                "name": "Test Address"
              }
            }
          }
        }
      ]
    }
  }
}
```

### 10. Confirm
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/confirm`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "confirm",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-126",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order": {
      "id": "order_123",
      "status": "Created"
    }
  }
}
```

### 11. Status
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/status`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "status",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-127",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order_id": "order_123"
  }
}
```

### 12. Track
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/track`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "track",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-128",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order_id": "order_123"
  }
}
```

### 13. Cancel
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/cancel`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "cancel",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-129",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "order_id": "order_123",
    "cancellation_reason_id": "001"
  }
}
```

### 14. Rating
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/rating`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "rating",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-130",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "rating_category": "Order",
    "id": "order_123",
    "value": "5"
  }
}
```

### 15. Support
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/support`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Body**:
```json
{
  "context": {
    "domain": "nic2004:52110",
    "action": "support",
    "version": "1.1.0",
    "bap_id": "neo-server.rozana.in",
    "bap_uri": "https://neo-server.rozana.in",
    "transaction_id": "test-txn-123",
    "message_id": "test-msg-131",
    "timestamp": "2024-12-20T10:00:00.000Z"
  },
  "message": {
    "support": {
      "order_id": "order_123",
      "issue": "Product not delivered"
    }
  }
}
```

## 🚀 ONDC Onboarding Endpoints

### 16. Get Onboarding Checklist
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/onboarding/checklist`
- **Description**: Get comprehensive onboarding requirements and status

### 17. Get Registration Payload
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/onboarding/registration-payload`
- **Description**: Generate registration payload for ONDC registry

### 18. Register with Registry
- **Method**: `POST`
- **URL**: `{{base_url}}/v1/bap/onboarding/register`
- **Description**: Automatically register with ONDC registry

### 19. Lookup Subscriber
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/onboarding/lookup/neo-server.rozana.in`
- **Description**: Lookup subscriber in ONDC registry

### 20. Update Subscriber Status
- **Method**: `PATCH`
- **URL**: `{{base_url}}/v1/bap/onboarding/status/SUBSCRIBED`
- **Description**: Update subscriber status in registry

### 21. Get Subscriber Info
- **Method**: `GET`
- **URL**: `{{base_url}}/v1/bap/onboarding/subscriber-info`
- **Description**: Get current subscriber information

## 📋 Postman Environment Variables

Create these variables in your Postman environment:

```
base_url: https://neo-server.rozana.in
subscriber_id: neo-server.rozana.in
domain: nic2004:52110
version: 1.1.0
```

## 🧪 Quick Test Sequence

For initial testing, try these endpoints in order:

1. **Health Check**: `GET /healthz`
2. **Subscriber Info**: `GET /v1/bap/onboarding/subscriber-info`
3. **Registration Payload**: `GET /v1/bap/onboarding/registration-payload`
4. **Onboarding Checklist**: `GET /v1/bap/onboarding/checklist`
5. **Test Callback**: `GET /v1/bap/on_subscribe/test`
6. **Challenge Test**: `POST /v1/bap/on_subscribe` (with challenge body)

## 📝 Notes

- All POST endpoints return `202 Accepted` for ONDC actions
- The subscription callback returns `200 OK`
- Health endpoints return `200 OK`
- Replace `{{base_url}}` with your actual domain
- Use proper ONDC message format for production testing
- Ensure HTTPS is enabled for production endpoints

## 🔐 Authentication

Currently, the endpoints don't require authentication for testing. For production:
- Implement ONDC authentication headers
- Add message signing
- Include proper encryption for sensitive data