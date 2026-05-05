import smtplib
import random
import string
import os
from datetime import datetime, timedelta

# Email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# OTP Storage (In production, use a database)
otp_storage = {}

def generate_otp(length=6):
    """Generates a random numerical OTP of the specified length."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(receiver_email, otp):
    """Sends the generated OTP to the designated email address."""
    subject = "Your OTP for Login"
    body = f"Your OTP for verification is: {otp}\n\nPlease do not share this code with anyone.\nThis code is valid for 10 minutes."
    
    message = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)
        server.quit()
        print(f"✅ OTP successfully sent to {receiver_email}")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not send OTP email: {e}")
        print(f"📌 Using OTP: {otp} for testing purposes")
        return True  # Allow to continue for testing

def store_otp(email, otp):
    """Store OTP with expiration time."""
    expiration_time = datetime.now() + timedelta(minutes=10)
    otp_storage[email] = {"otp": otp, "expires": expiration_time}

def verify_otp(email, user_otp):
    """Verify if the provided OTP is correct and not expired."""
    if email not in otp_storage:
        return False, "No OTP found for this email."
    
    stored_data = otp_storage[email]
    
    # Check expiration
    if datetime.now() > stored_data["expires"]:
        del otp_storage[email]
        return False, "OTP has expired. Please request a new one."
    
    # Check OTP
    if user_otp == stored_data["otp"]:
        del otp_storage[email]
        return True, "Verification successful!"
    
    return False, "Invalid OTP. Please try again."

def login_with_otp():
    """Main flow for OTP Login."""
    print("\n" + "="*40)
    print("   🔐 App Login Verification")
    print("="*40)
    user_email = input("\n📧 Enter your email address: ").strip()
    
    if not user_email or "@" not in user_email:
        print("❌ Invalid email format!")
        return False
    
    # Generate and send OTP
    otp = generate_otp()
    store_otp(user_email, otp)
    
    print(f"\n⏳ Sending OTP to {user_email}...")
    send_otp_email(user_email, otp)
    
    attempts = 3
    
    # Verify OTP
    while attempts > 0:
        user_input = input("\n🔑 Enter the 6-digit OTP: ").strip()
        
        success, message = verify_otp(user_email, user_input)
        
        if success:
            print(f"\n✅ {message}")
            print("🎉 Welcome to the application!\n")
            return True
        else:
            attempts -= 1
            print(f"❌ {message} ({attempts} attempts remaining)")
                
    print("\n🚫 Login failed. Too many invalid attempts.")
    return False

if __name__ == "__main__":
    login_with_otp()