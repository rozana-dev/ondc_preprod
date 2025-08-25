# 📤 Send ONDC BAP to DevOps Team

## 🎯 **What to Send to DevOps Team**

### **1. Application Files**
Send the complete `one_ondc` folder to your DevOps team member.

### **2. Deployment Instructions**
Send the `DEVOPS_DEPLOYMENT_STEPS.md` file with detailed deployment steps.

### **3. Quick Deployment Script**
Send the `deployment/quick_deploy.sh` script for automated deployment.

## 📦 **Step 1: Prepare Files for Transfer**

### **Option A: Create Archive (Recommended)**
```bash
# On your local machine
cd /Users/anshumankumar/Desktop/one_ondc

# Create deployment package
tar -czf ondc-bap-deployment.tar.gz \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='*.log' \
  .
```

### **Option B: Send Entire Folder**
```bash
# Copy the entire folder to a shared location
cp -r /Users/anshumankumar/Desktop/one_ondc /path/to/shared/folder/
```

## 📤 **Step 2: Transfer Methods**

### **Method 1: File Sharing (Recommended)**
- Upload `ondc-bap-deployment.tar.gz` to Google Drive, Dropbox, or your company's file sharing system
- Share the link with your DevOps team member

### **Method 2: Direct Transfer**
```bash
# If DevOps team has server access, transfer directly
scp ondc-bap-deployment.tar.gz devops-team@server:/tmp/
```

### **Method 3: Git Repository**
```bash
# Push to a private repository
git remote add deployment git@your-company.com:ondc-bap.git
git push deployment main
```

## 📋 **Step 3: Instructions for DevOps Team**

### **What to Tell Your DevOps Team Member:**

**Subject: ONDC BAP Application Deployment**

**Message:**
```
Hi [DevOps Team Member],

I need to deploy the ONDC BAP application to neo-server.rozana.in.

Files included:
1. ondc-bap-deployment.tar.gz - Complete application
2. DEVOPS_DEPLOYMENT_STEPS.md - Detailed deployment guide
3. deployment/quick_deploy.sh - Automated deployment script

Key Information:
- Server: neo-server.rozana.in
- Application: ONDC BAP (Buyer App Platform)
- Technology: FastAPI + Python 3.8+
- Web Server: Apache2 with reverse proxy
- Port: 8000 (internal), 443 (external)

Please follow the deployment steps in DEVOPS_DEPLOYMENT_STEPS.md
or run the quick_deploy.sh script for automated deployment.

Required endpoints after deployment:
- https://neo-server.rozana.in/healthz
- https://neo-server.rozana.in/lookup
- https://neo-server.rozana.in/vlookup
- https://neo-server.rozana.in/on_subscribe
- https://neo-server.rozana.in/ondc-site-verification.html

Let me know if you need any clarification!

Thanks,
[Your Name]
```

## 🚀 **Step 4: DevOps Team Actions**

### **What Your DevOps Team Should Do:**

1. **Download/Extract Files**
   ```bash
   # Extract the deployment package
   tar -xzf ondc-bap-deployment.tar.gz -C /opt/ondc-bap/
   ```

2. **Follow Deployment Guide**
   - Read `DEVOPS_DEPLOYMENT_STEPS.md`
   - Follow the 10-step deployment process

3. **Or Use Quick Script**
   ```bash
   # Run the automated deployment script
   chmod +x deployment/quick_deploy.sh
   sudo ./deployment/quick_deploy.sh
   ```

4. **Verify Deployment**
   - Test all endpoints
   - Check service status
   - Verify logs

## ✅ **Step 5: Verification Checklist**

After deployment, verify these endpoints work:

- [ ] `https://neo-server.rozana.in/healthz` - Returns `{"status":"ok"}`
- [ ] `https://neo-server.rozana.in/lookup` - Returns subscriber information
- [ ] `https://neo-server.rozana.in/vlookup` - Accepts POST requests
- [ ] `https://neo-server.rozana.in/on_subscribe` - Accepts ONDC callbacks
- [ ] `https://neo-server.rozana.in/ondc-site-verification.html` - Shows verification page

## 📞 **Support Information**

**If DevOps team needs help:**
- **Application Logs**: `journalctl -u ondc-bap.service -f`
- **Apache Logs**: `/var/log/apache2/ondc-bap-error.log`
- **Service Status**: `systemctl status ondc-bap.service`
- **Configuration**: `/etc/apache2/sites-available/ondc-bap.conf`

**Files to include in transfer:**
- ✅ Complete application code
- ✅ Python requirements
- ✅ ONDC cryptographic keys
- ✅ Deployment scripts
- ✅ Configuration files
- ✅ Documentation

**Ready to send to DevOps team!** 🚀 