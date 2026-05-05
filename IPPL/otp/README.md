# OTP Verification Login System

A complete login and OTP verification system with both CLI and GUI interfaces.

## 📁 Files

- **otp_verification.py** - Core OTP logic (generate, send, verify)
- **gui_login.py** - Desktop GUI interface with tkinter

## 🚀 Features

✅ Generate random 6-digit OTP  
✅ Send OTP via email (Gmail SMTP)  
✅ Store OTP with 10-minute expiration  
✅ Beautiful GUI interface  
✅ 3 verification attempts limit  
✅ Email validation  
✅ Real-time feedback and error handling  

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- smtplib (built-in)

## 🔧 Setup

### 1. Set Up Email Credentials (Optional for Testing)

For the OTP email sending to work with Gmail:

1. Go to your Google Account: https://myaccount.google.com/
2. Enable 2-Step Verification
3. Generate an **App Password** (not your regular password)
4. Set environment variables:

**Windows (PowerShell):**
```powershell
$env:SENDER_EMAIL = "your_email@gmail.com"
$env:SENDER_PASSWORD = "your_16_char_app_password"
```

**Windows (Command Prompt):**
```cmd
set SENDER_EMAIL=your_email@gmail.com
set SENDER_PASSWORD=your_16_char_app_password
```

**Linux/Mac:**
```bash
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_16_char_app_password"
```

### 2. Without Email Setup

The system works fine for **testing purposes** - it will display the OTP in the console automatically if email credentials are not configured.

## 💻 Usage

### CLI Version (Command Line)

```bash
python otp_verification.py
```

Follow the prompts to enter your email and verify with OTP.

### GUI Version (Desktop Interface)

```bash
python gui_login.py
```

A login window will open with a nice interface:
1. Enter your email address
2. Click "Send OTP"
3. Check your email for the code
4. Enter the 6-digit code in the verification window
5. Access the application on success

## 🔐 Security Features

- **OTP Expiration**: Codes expire after 10 minutes
- **Attempt Limiting**: Maximum 3 verification attempts
- **Email Validation**: Basic email format validation
- **Secure Storage**: OTP stored with timestamps
- **HTTPS Support**: Uses SMTP with TLS encryption

## 🧪 Testing

To test without email:

1. Run the GUI application
2. Enter any valid email (e.g., test@example.com)
3. The OTP will be displayed in the console window
4. Enter that OTP in the GUI verification field

Example OTP from console:
```
📌 Using OTP: 123456 for testing purposes
```

## 📝 Integration

To integrate with your existing `Akun` class:

```python
from otp.otp_verification import login_with_otp

class Akun:
    def login(self):
        if login_with_otp():
            # User verified, proceed with login
            return True
        return False
```

## ⚙️ Customization

### Change OTP Length
Edit `otp_verification.py`:
```python
otp = generate_otp(length=8)  # For 8-digit OTP
```

### Change OTP Expiration
Edit `otp_verification.py`:
```python
expiration_time = datetime.now() + timedelta(minutes=30)  # 30 minutes
```

### Use Different Email Provider

Replace SMTP settings in `otp_verification.py`:
```python
SMTP_SERVER = "smtp.yahoo.com"  # Yahoo
SMTP_PORT = 587
```

## 🐛 Troubleshooting

**"Gmail authentication failed"**
- Use an App Password, not your regular password
- Ensure 2-Step Verification is enabled

**"Module not found: tkinter"**
- Install Python with tkinter included
- Or: `python -m pip install tk`

**"OTP not received"**
- Check spam folder
- Verify sender email is correct
- Check email provider settings

## 📄 License

Free to use and modify for your application.

---

**Created:** May 4, 2026  
**Version:** 1.0
