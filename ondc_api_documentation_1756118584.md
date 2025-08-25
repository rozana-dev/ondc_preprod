# ONDC BAP API Documentation

## Overview
Complete API documentation for ONDC BAP (Buyer App Platform) with request/response examples.

- **Base URL**: `https://neo-server.rozana.in`
- **Generated**: 2025-08-25T10:43:04.856480+00:00
- **Transaction ID**: `de1f7462-3c04-45a1-93a1-fc81f6106802`

## API Categories


## Health APIs

### ✅ GET /health

**Description**: Main application health check

**URL**: `https://neo-server.rozana.in/health`

**Method**: GET

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "status": "ok"
  }
}
```

---

### ✅ GET /ekyc/health

**Description**: eKYC service health check

**URL**: `https://neo-server.rozana.in/ekyc/health`

**Method**: GET

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "status": "ok",
    "service": "eKYC",
    "version": "1.0.0",
    "timestamp": "2025-08-25T10:43:02.595885+00:00",
    "endpoints": [
      "/ekyc/health",
      "/ekyc/search",
      "/ekyc/select",
      "/ekyc/initiate",
      "/ekyc/verify",
      "/ekyc/status"
    ]
  }
}
```

---


## ONDC Core APIs

### ✅ POST /search

**Description**: Search for products/services

**URL**: `https://neo-server.rozana.in/search`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "search",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "0461d231-711f-4291-81c6-2c2dce2fb006",
    "timestamp": "2025-08-25T10:43:02.582114+00:00"
  },
  "message": {
    "intent": {
      "item": {
        "descriptor": {
          "name": "Test Product from Pramaan Store"
        }
      },
      "fulfillment": {
        "type": "Delivery",
        "end": {
          "location": {
            "gps": "28.6139,77.2090",
            "address": {
              "area_code": "110037"
            }
          }
        }
      },
      "payment": {
        "type": "PRE-PAID"
      }
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /select

**Description**: Select items from catalog

**URL**: `https://neo-server.rozana.in/select`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "select",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "e7544e4f-8056-4e18-89dd-dceba8dacde9",
    "timestamp": "2025-08-25T10:43:02.698794+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order": {
      "provider": {
        "id": "pramaan_provider_1"
      },
      "items": [
        {
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }
      ],
      "billing": {
        "address": {
          "name": "Test User",
          "building": "123 Test Building",
          "city": "New Delhi",
          "state": "Delhi",
          "country": "IND",
          "area_code": "110037"
        },
        "phone": "9876543210"
      }
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /init

**Description**: Initialize order

**URL**: `https://neo-server.rozana.in/init`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "init",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "e1c2ad88-09ff-4bd2-8b0f-4f65add774b5",
    "timestamp": "2025-08-25T10:43:02.823268+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order": {
      "provider": {
        "id": "provider_1"
      },
      "items": [
        {
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }
      ],
      "billing": {
        "address": {
          "name": "Test User",
          "city": "New Delhi",
          "state": "Delhi"
        },
        "phone": "9876543210"
      },
      "payment": {
        "type": "PRE-PAID"
      }
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /confirm

**Description**: Confirm order

**URL**: `https://neo-server.rozana.in/confirm`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "confirm",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "f6e8c4d7-8500-48ff-90b7-5b0fc3317c92",
    "timestamp": "2025-08-25T10:43:02.939727+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order": {
      "id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802",
      "provider": {
        "id": "provider_1"
      },
      "items": [
        {
          "id": "item_001",
          "quantity": {
            "count": 2
          }
        }
      ],
      "payment": {
        "type": "PRE-PAID",
        "status": "PAID"
      }
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /status

**Description**: Get order status

**URL**: `https://neo-server.rozana.in/status`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "status",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "da6c8d2a-8e71-4c75-b632-488183c3b010",
    "timestamp": "2025-08-25T10:43:03.057084+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order_id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802"
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /track

**Description**: Track order

**URL**: `https://neo-server.rozana.in/track`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "track",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "46a8d570-2092-4b57-b363-7b1633d0cac9",
    "timestamp": "2025-08-25T10:43:03.199475+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order_id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802"
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /cancel

**Description**: Cancel order

**URL**: `https://neo-server.rozana.in/cancel`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "cancel",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "86a3a440-722d-4e54-b5b2-08b1662f0b33",
    "timestamp": "2025-08-25T10:43:03.326677+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "order_id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802",
    "cancellation_reason_id": "001",
    "descriptor": {
      "short_desc": "Test cancellation"
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ❌ POST /update

**Description**: Update order

**URL**: `https://neo-server.rozana.in/update`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "update",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "61e2df10-069a-48e8-830a-dae74400a70f",
    "timestamp": "2025-08-25T10:43:03.432992+00:00",
    "bpp_id": "pramaan.ondc.org/beta/preprod/mock/seller",
    "bpp_uri": "https://pramaan.ondc.org/beta/preprod/mock/seller"
  },
  "message": {
    "update_target": "order",
    "order": {
      "id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802",
      "status": "UPDATED"
    }
  }
}
```

**Response**:
```json
{
  "status_code": 404,
  "body": {
    "error": "HTTP 404: Not Found"
  }
}
```

---


## eKYC APIs

### ✅ POST /ekyc/search

**Description**: Search for eKYC providers

**URL**: `https://neo-server.rozana.in/ekyc/search`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "search",
    "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
    "message_id": "e766948a-debc-4b0c-8f5b-d9db6e02731a",
    "timestamp": "2025-08-25T10:43:03.547919+00:00"
  },
  "message": {
    "intent": {
      "provider": {
        "category_id": "ekyc"
      }
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "search",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
      "message_id": "1d332a57-1f3b-4de8-8d39-c1a8b647879c",
      "timestamp": "2025-08-25T10:43:03.685661+00:00",
      "ttl": "PT30S"
    },
    "message": {
      "ack": {
        "status": "ACK"
      },
      "catalog": {
        "providers": [
          {
            "id": "pramaan.ondc.org",
            "name": "Pramaan eKYC",
            "description": "Official ONDC eKYC service",
            "category": "GOVERNMENT",
            "rating": 4.8,
            "supported_documents": [
              "AADHAAR",
              "PAN",
              "DRIVING_LICENSE",
              "PASSPORT"
            ]
          },
          {
            "id": "uidai.ondc.org",
            "name": "UIDAI eKYC",
            "description": "Aadhaar-based eKYC service",
            "category": "GOVERNMENT",
            "rating": 4.9,
            "supported_documents": [
              "AADHAAR"
            ]
          },
          {
            "id": "nsdl.ondc.org",
            "name": "NSDL eKYC",
            "description": "PAN-based eKYC service",
            "category": "GOVERNMENT",
            "rating": 4.7,
            "supported_documents": [
              "PAN",
              "AADHAAR"
            ]
          }
        ],
        "total_count": 3
      }
    }
  }
}
```

---

### ✅ POST /ekyc/select

**Description**: Select eKYC service

**URL**: `https://neo-server.rozana.in/ekyc/select`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "select",
    "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
    "message_id": "7c756b76-c08f-497b-b4e8-b4bf2b65df0f",
    "timestamp": "2025-08-25T10:43:03.683309+00:00"
  },
  "message": {
    "order": {
      "provider": {
        "id": "pramaan.ondc.org"
      },
      "items": [
        {
          "id": "aadhaar_verification"
        }
      ]
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "select",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
      "message_id": "c7292f5e-e517-4a90-b112-5a9445869270",
      "timestamp": "2025-08-25T10:43:03.830325+00:00",
      "ttl": "PT30S"
    },
    "message": {
      "ack": {
        "status": "ACK"
      },
      "order": {
        "provider": {
          "id": "pramaan.ondc.org",
          "name": "pramaan.ondc.org eKYC Service",
          "description": "eKYC service provided by pramaan.ondc.org",
          "supported_documents": [
            "AADHAAR",
            "PAN",
            "DRIVING_LICENSE"
          ],
          "supported_auth_methods": [
            "OTP",
            "BIO",
            "IRIS"
          ],
          "estimated_time": "2-5 minutes",
          "success_rate": "99.5%"
        },
        "items": [
          {
            "id": "ekyc_verification",
            "name": "eKYC Verification",
            "price": {
              "currency": "INR",
              "value": "0.00"
            }
          }
        ]
      }
    }
  }
}
```

---

### ✅ POST /ekyc/initiate

**Description**: Initiate eKYC process

**URL**: `https://neo-server.rozana.in/ekyc/initiate`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "initiate",
    "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
    "message_id": "1c80370d-303b-4178-9518-da6d85925dfe",
    "timestamp": "2025-08-25T10:43:03.807464+00:00"
  },
  "message": {
    "order": {
      "provider": {
        "id": "pramaan.ondc.org"
      },
      "items": [
        {
          "id": "aadhaar_verification"
        }
      ]
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "initiate",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
      "message_id": "8e25c590-7cb7-44ff-abc5-9663e29b28b1",
      "timestamp": "2025-08-25T10:43:03.947861+00:00",
      "ttl": "PT30S"
    },
    "message": {
      "ack": {
        "status": "ACK"
      },
      "order": {
        "id": "ekyc_order_1756118583",
        "status": "INITIATED",
        "provider": {
          "id": "pramaan.ondc.org"
        },
        "items": [
          {
            "id": "ekyc_verification",
            "name": "eKYC Verification",
            "status": "INITIATED"
          }
        ],
        "fulfillment": {
          "type": "ONDC:ekyc",
          "status": "PENDING",
          "tracking": true
        }
      }
    }
  }
}
```

---

### ✅ POST /ekyc/verify

**Description**: Verify documents

**URL**: `https://neo-server.rozana.in/ekyc/verify`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "verify",
    "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
    "message_id": "c15d0e7d-8db9-4bb8-94e1-14489399f1f9",
    "timestamp": "2025-08-25T10:43:03.932907+00:00"
  },
  "message": {
    "documents": [
      {
        "document_type": "AADHAAR",
        "document_number": "1234-5678-9012",
        "name": "Test User"
      }
    ]
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "verify",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
      "message_id": "7c1513a8-da01-4090-b987-1b8f8b7b2347",
      "timestamp": "2025-08-25T10:43:04.079170+00:00",
      "ttl": "PT30S"
    },
    "message": {
      "ack": {
        "status": "ACK"
      },
      "verification": {
        "status": "SUCCESS",
        "verified": true,
        "confidence_score": 0.95,
        "document_type": "AADHAAR",
        "verification_id": "verify_1756118584",
        "verified_at": "2025-08-25T10:43:04.079144+00:00"
      }
    }
  }
}
```

---

### ✅ POST /ekyc/status

**Description**: Check verification status

**URL**: `https://neo-server.rozana.in/ekyc/status`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "status",
    "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
    "message_id": "77b19901-2294-4434-91c8-d9619e82924f",
    "timestamp": "2025-08-25T10:43:04.065410+00:00"
  },
  "message": {
    "verification_id": "verify_1756118584"
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "context": {
      "domain": "ONDC:RET10",
      "country": "IND",
      "city": "std:011",
      "action": "status",
      "core_version": "1.2.0",
      "bap_id": "neo-server.rozana.in",
      "bap_uri": "https://neo-server.rozana.in",
      "transaction_id": "62c92b27-c4b4-4c8b-893d-56a5960bf219",
      "message_id": "4c35a7cb-4411-40ab-9330-4018d91a4e0c",
      "timestamp": "2025-08-25T10:43:04.213879+00:00",
      "ttl": "PT30S"
    },
    "message": {
      "ack": {
        "status": "ACK"
      },
      "order": {
        "id": "ekyc_order_1756118583",
        "status": "VERIFIED",
        "updated_at": "2025-08-25T10:43:04.079158+00:00",
        "verification_result": {
          "status": "SUCCESS",
          "verified": true,
          "confidence_score": 0.95,
          "document_type": "AADHAAR",
          "verification_id": "verify_1756118584",
          "verified_at": "2025-08-25T10:43:04.079144+00:00"
        }
      }
    }
  }
}
```

---


## Registry APIs

### ✅ POST /on_subscribe

**Description**: Registry subscription callback

**URL**: `https://neo-server.rozana.in/on_subscribe`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "on_subscribe",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "424ff5b2-3244-4fdb-9dda-0d0bfb2d702a",
    "timestamp": "2025-08-25T10:43:04.239561+00:00"
  },
  "message": {
    "ack": {
      "status": "ACK"
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "status": "ACK",
    "message": "Callback received",
    "timestamp": "2025-08-25T10:43:04.389788"
  }
}
```

---

### ❌ GET /vlookup

**Description**: Participant lookup

**URL**: `https://neo-server.rozana.in/vlookup`

**Method**: GET

**Response**:
```json
{
  "status_code": 405,
  "body": {
    "error": "HTTP 405: Method Not Allowed"
  }
}
```

---


## Additional APIs

### ✅ POST /rating

**Description**: Rate order/service

**URL**: `https://neo-server.rozana.in/rating`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "rating",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "c091a4f9-7106-413b-bbbe-eaa67ed7e29a",
    "timestamp": "2025-08-25T10:43:04.558258+00:00"
  },
  "message": {
    "rating_category": "Order",
    "id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802",
    "value": "4"
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

### ✅ POST /support

**Description**: Customer support

**URL**: `https://neo-server.rozana.in/support`

**Method**: POST

**Request Headers**:
```json
{
  "Content-Type": "application/json"
}
```

**Request Body**:
```json
{
  "context": {
    "domain": "ONDC:RET10",
    "action": "support",
    "transaction_id": "de1f7462-3c04-45a1-93a1-fc81f6106802",
    "message_id": "c08a4a73-2f7d-4f2e-bd49-d736d46427db",
    "timestamp": "2025-08-25T10:43:04.684236+00:00"
  },
  "message": {
    "support": {
      "order_id": "order_de1f7462_3c04_45a1_93a1_fc81f6106802",
      "phone": "1800-XXX-XXXX",
      "email": "support@neo-server.rozana.in"
    }
  }
}
```

**Response**:
```json
{
  "status_code": 200,
  "body": {
    "raw_response": "OK\n"
  }
}
```

---

## Summary

- **Total APIs**: 19
- **Successful**: 17
- **Failed**: 2
- **Success Rate**: 89.5%

### API Status by Category

- **Health**: 2/2 (100.0%)
- **ONDC Core**: 7/8 (87.5%)
- **eKYC**: 5/5 (100.0%)
- **Registry**: 1/2 (50.0%)
- **Additional**: 2/2 (100.0%)
