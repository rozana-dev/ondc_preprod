# 🚀 ONDC BAP Deployment Guide

## 📋 Prerequisites

- **Server Access**: SSH access to `neo-server.rozana.in`
- **Root/Sudo Access**: Required for system configuration
- **Domain**: `neo-server.rozana.in` (already configured)
- **SSL Certificate**: Let's Encrypt (already installed)

## 🎯 Quick Deployment

### **Step 1: Upload Files to Server**
```bash
# From your local machine
./deployment/upload_files.sh
```

### **Step 2: Deploy on Server**
```bash
# SSH to your server
ssh root@neo-server.rozana.in

# Navigate to application directory
cd /opt/ondc-bap

# Run deployment script
sudo ./deployment/deploy.sh
```

## 🔧 Manual Deployment Steps

### **1. Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv apache2 libapache2-mod-proxy-html
```

### **2. Apache Configuration**
```bash
# Enable required modules
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite

# Copy configuration
sudo cp deployment/apache_config.conf /etc/apache2/sites-available/ondc-bap.conf
sudo a2ensite ondc-bap.conf
```

### **3. Application Setup**
```bash
# Create application directory
sudo mkdir -p /opt/ondc-bap
sudo chown www-data:www-data /opt/ondc-bap

# Setup Python environment
cd /opt/ondc-bap
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt
```

### **4. Systemd Service**
```bash
# Copy service file
sudo cp deployment/systemd_service.service /etc/systemd/system/ondc-bap.service

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap.service
sudo systemctl start ondc-bap.service
```

### **5. Restart Apache**
```bash
sudo systemctl restart apache2
```

## 🧪 Testing Deployment

### **Local Testing**
```bash
# Check service status
sudo systemctl status ondc-bap.service

# Check logs
sudo journalctl -u ondc-bap.service -f
```

### **Public Testing**
```bash
# Test health endpoint
curl https://neo-server.rozana.in/healthz

# Test ONDC callback
curl -X POST https://neo-server.rozana.in/v1/bap/on_subscribe \
  -H "Content-Type: application/json" \
  -d '{"test": "deployment_test"}'
```

## 📁 File Structure

```
/opt/ondc-bap/
├── app/                    # FastAPI application
├── deployment/             # Deployment files
│   ├── apache_config.conf  # Apache configuration
│   ├── systemd_service.service # Systemd service
│   ├── deploy.sh          # Deployment script
│   └── upload_files.sh    # Upload script
├── requirements.txt        # Python dependencies
├── .venv/                 # Virtual environment
└── secrets/               # ONDC credentials
```

## 🔍 Troubleshooting

### **Service Not Starting**
```bash
# Check logs
sudo journalctl -u ondc-bap.service -f

# Check permissions
sudo chown -R www-data:www-data /opt/ondc-bap
```

### **Apache Issues**
```bash
# Check Apache configuration
sudo apache2ctl configtest

# Check Apache logs
sudo tail -f /var/log/apache2/ondc-bap-error.log
```

### **SSL Issues**
```bash
# Check SSL certificate
sudo certbot certificates

# Renew if needed
sudo certbot renew
```

## 🌐 Final URLs

After deployment, your ONDC BAP will be accessible at:

- **Health Check**: `https://neo-server.rozana.in/healthz`
- **ONDC Callback**: `https://neo-server.rozana.in/v1/bap/on_subscribe`
- **API Base**: `https://neo-server.rozana.in/v1/bap/`
- **Site Verification**: `https://neo-server.rozana.in/ondc-site-verification.html`

## ✅ Next Steps

1. **Deploy Application**: Run the deployment scripts
2. **Test Endpoints**: Verify all endpoints are working
3. **Submit ONDC Registration**: Use the working callback URL
4. **Monitor Logs**: Keep an eye on service logs

## 📞 Support

If you encounter issues:
- Check service logs: `sudo journalctl -u ondc-bap.service`
- Check Apache logs: `/var/log/apache2/ondc-bap-error.log`
- Verify SSL: `sudo certbot certificates` 