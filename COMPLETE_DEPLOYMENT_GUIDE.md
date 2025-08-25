# 🚀 Complete ONDC BAP Server Deployment Guide

## 📦 **Deployment Package Ready**
- **File**: `ondc-bap-complete-deployment.tar.gz` (130KB)
- **Contains**: Complete application, scripts, and configuration files

## 🔧 **Server Requirements**
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+
- Apache2
- SSL certificates (Let's Encrypt recommended)
- 1GB+ RAM, 10GB+ disk space

## 📋 **Pre-Deployment Checklist**
- [ ] Server IP/hostname: `_________________`
- [ ] SSH username: `_________________`
- [ ] SSH method: Password / SSH Key
- [ ] Domain: `neo-server.rozana.in`
- [ ] SSL certificates installed: Yes / No

## 🚀 **Deployment Methods**

### **Method 1: Automated Deployment (Recommended)**
```bash
# On your local machine, upload the package
scp ondc-bap-complete-deployment.tar.gz username@server-ip:/tmp/

# SSH to server and run deployment
ssh username@server-ip
cd /tmp
tar -xzf ondc-bap-complete-deployment.tar.gz
cd one_ondc
chmod +x deployment/quick_deploy.sh
./deployment/quick_deploy.sh
```

### **Method 2: Manual Step-by-Step**
```bash
# 1. Upload files
scp -r . username@server-ip:/opt/ondc-bap/

# 2. SSH to server
ssh username@server-ip

# 3. Run these commands on server:
cd /opt/ondc-bap
sudo apt update
sudo apt install -y python3 python3-pip python3-venv apache2 libapache2-mod-proxy-html
sudo a2enmod proxy proxy_http ssl
sudo systemctl restart apache2

# 4. Setup Python environment
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt

# 5. Generate ONDC keys
sudo -u www-data python3 scripts/generate_ondc_keys.py

# 6. Setup systemd service
sudo cp deployment/systemd_service.service /etc/systemd/system/ondc-bap.service
sudo systemctl daemon-reload
sudo systemctl enable ondc-bap
sudo systemctl start ondc-bap

# 7. Configure Apache
sudo cp deployment/apache_config.conf /etc/apache2/sites-available/neo-server.rozana.in.conf
sudo a2ensite neo-server.rozana.in
sudo systemctl reload apache2
```

### **Method 3: Quick Fix (If Apache is already configured)**
```bash
# Just update Apache configuration
sudo cp /etc/apache2/sites-available/neo-server.rozana.in.conf /etc/apache2/sites-available/neo-server.rozana.in.conf.backup
sudo tee /etc/apache2/sites-available/neo-server.rozana.in.conf > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName neo-server.rozana.in
    Redirect permanent / https://neo-server.rozana.in/
</VirtualHost>

<VirtualHost *:443>
    ServerName neo-server.rozana.in
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/neo-server.rozana.in/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/neo-server.rozana.in/privkey.pem
    ProxyPreserveHost On
    ProxyPass /healthz http://localhost:8000/healthz
    ProxyPassReverse /healthz http://localhost:8000/healthz
    ProxyPass /livez http://localhost:8000/livez
    ProxyPassReverse /livez http://localhost:8000/livez
    ProxyPass /readyz http://localhost:8000/readyz
    ProxyPassReverse /readyz http://localhost:8000/readyz
    ProxyPass /lookup http://localhost:8000/lookup
    ProxyPassReverse /lookup http://localhost:8000/lookup
    ProxyPass /vlookup http://localhost:8000/vlookup
    ProxyPassReverse /vlookup http://localhost:8000/vlookup
    ProxyPass /on_subscribe http://localhost:8000/on_subscribe
    ProxyPassReverse /on_subscribe http://localhost:8000/on_subscribe
    ProxyPass /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    ProxyPassReverse /ondc-site-verification.html http://localhost:8000/ondc-site-verification.html
    ProxyPass /onboarding http://localhost:8000/onboarding
    ProxyPassReverse /onboarding http://localhost:8000/onboarding
    ProxyPass /search http://localhost:8000/search
    ProxyPassReverse /search http://localhost:8000/search
    ProxyPass /select http://localhost:8000/select
    ProxyPassReverse /select http://localhost:8000/select
    ProxyPass /init http://localhost:8000/init
    ProxyPassReverse /init http://localhost:8000/init
    ProxyPass /confirm http://localhost:8000/confirm
    ProxyPassReverse /confirm http://localhost:8000/confirm
    ProxyPass /status http://localhost:8000/status
    ProxyPassReverse /status http://localhost:8000/status
    ProxyPass /track http://localhost:8000/track
    ProxyPassReverse /track http://localhost:8000/track
    ProxyPass /cancel http://localhost:8000/cancel
    ProxyPassReverse /cancel http://localhost:8000/cancel
    ProxyPass /rating http://localhost:8000/rating
    ProxyPassReverse /rating http://localhost:8000/rating
    ProxyPass /support http://localhost:8000/support
    ProxyPassReverse /support http://localhost:8000/support
    ErrorLog ${APACHE_LOG_DIR}/ondc-bap-error.log
    CustomLog ${APACHE_LOG_DIR}/ondc-bap-access.log combined
</VirtualHost>
EOF
sudo apache2ctl configtest && sudo systemctl reload apache2 && sudo systemctl restart ondc-bap
```

## ✅ **Verification Commands**
```bash
# Check services
sudo systemctl status apache2
sudo systemctl status ondc-bap

# Test endpoints
curl -s "https://neo-server.rozana.in/healthz"
curl -s "https://neo-server.rozana.in/livez"
curl -s "https://neo-server.rozana.in/lookup"
curl -s "https://neo-server.rozana.in/onboarding/checklist"

# Check logs
sudo journalctl -u ondc-bap -f
sudo tail -f /var/log/apache2/ondc-bap-error.log
```

## 🔍 **Troubleshooting**
- **Service not starting**: Check logs with `sudo journalctl -u ondc-bap -f`
- **Apache errors**: Check with `sudo apache2ctl configtest`
- **Permission issues**: Ensure files owned by `www-data`
- **Port conflicts**: Check if port 8000 is free with `sudo netstat -tlnp | grep 8000`

## 📞 **Support**
If you encounter issues:
1. Check service status: `sudo systemctl status ondc-bap`
2. View logs: `sudo journalctl -u ondc-bap -f`
3. Test configuration: `sudo apache2ctl configtest`

## 🎯 **Expected Results**
After deployment, all these endpoints should work:
- ✅ `https://neo-server.rozana.in/healthz`
- ✅ `https://neo-server.rozana.in/livez`
- ✅ `https://neo-server.rozana.in/readyz`
- ✅ `https://neo-server.rozana.in/lookup`
- ✅ `https://neo-server.rozana.in/vlookup`
- ✅ `https://neo-server.rozana.in/on_subscribe`
- ✅ `https://neo-server.rozana.in/ondc-site-verification.html`
- ✅ `https://neo-server.rozana.in/onboarding/*`
- ✅ `https://neo-server.rozana.in/search`
- ✅ `https://neo-server.rozana.in/select`
- ✅ `https://neo-server.rozana.in/init`
- ✅ And all other ONDC endpoints

**Ready to deploy! Just let me know your server details and preferred method.** 🚀 