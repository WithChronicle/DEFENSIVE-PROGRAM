import tkinter as tk
from tkinter import messagebox, ttk
import threading
from otp_verification import generate_otp, store_otp, send_otp_email, verify_otp

class OTPLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Login - OTP Verification")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.current_email = None
        self.otp_sent = False
        self.remaining_attempts = 3
        
        self.show_login_page()
    
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_page(self):
        """Display the login/email entry page."""
        self.clear_window()
        self.otp_sent = False
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="🔐 Secure Login", font=("Arial", 24, "bold"), 
                        fg="white", bg="#2c3e50")
        title.pack(pady=20)
        
        subtitle = tk.Label(header_frame, text="Enter your email to get started", 
                           font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50")
        subtitle.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Email label and entry
        email_label = tk.Label(content_frame, text="📧 Email Address", font=("Arial", 11, "bold"), 
                              bg="#f0f0f0")
        email_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.email_entry = tk.Entry(content_frame, font=("Arial", 12), width=35, 
                                   relief=tk.FLAT, bd=2)
        self.email_entry.pack(pady=(0, 20), ipady=8)
        self.email_entry.configure(bg="white", fg="black")
        
        # Send OTP Button
        send_btn = tk.Button(content_frame, text="Send OTP", font=("Arial", 12, "bold"),
                            bg="#3498db", fg="white", relief=tk.FLAT, padx=20, pady=10,
                            command=self.send_otp_handler, cursor="hand2")
        send_btn.pack(fill=tk.X, pady=10)
        
        # Info message
        info_label = tk.Label(content_frame, 
                             text="We'll send a 6-digit code to your email for verification.",
                             font=("Arial", 9), fg="#7f8c8d", bg="#f0f0f0", wraplength=350)
        info_label.pack(pady=20)
        
        # Footer
        footer = tk.Label(self.root, text="Secure Login System © 2026", 
                         font=("Arial", 9), fg="#95a5a6", bg="#f0f0f0")
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def send_otp_handler(self):
        """Handle sending OTP."""
        email = self.email_entry.get().strip()
        
        # Validation
        if not email:
            messagebox.showerror("Error", "Please enter your email address.")
            return
        
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        
        self.current_email = email
        
        # Show sending status
        self.email_entry.config(state=tk.DISABLED)
        messagebox.showinfo("Info", f"Sending OTP to {email}...\n\nFor testing, the OTP will be displayed in the console.")
        
        # Generate OTP
        otp = generate_otp()
        store_otp(email, otp)
        
        # Send in background thread
        thread = threading.Thread(target=send_otp_email, args=(email, otp))
        thread.daemon = True
        thread.start()
        
        self.otp_sent = True
        self.remaining_attempts = 3
        
        # Show OTP entry page
        self.root.after(1000, self.show_otp_page)
    
    def show_otp_page(self):
        """Display the OTP verification page."""
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#27ae60", height=80)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="✓ Code Sent", font=("Arial", 24, "bold"), 
                        fg="white", bg="#27ae60")
        title.pack(pady=20)
        
        subtitle = tk.Label(header_frame, text=f"Check your email: {self.current_email}", 
                           font=("Arial", 10), fg="#ecf0f1", bg="#27ae60")
        subtitle.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # OTP label and entry
        otp_label = tk.Label(content_frame, text="🔑 Enter 6-Digit Code", 
                            font=("Arial", 11, "bold"), bg="#f0f0f0")
        otp_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.otp_entry = tk.Entry(content_frame, font=("Arial", 16, "bold"), width=15, 
                                 relief=tk.FLAT, bd=2, justify=tk.CENTER)
        self.otp_entry.pack(pady=(0, 20), ipady=10)
        self.otp_entry.configure(bg="white", fg="black")
        self.otp_entry.focus()
        
        # Bind Enter key
        self.otp_entry.bind("<Return>", lambda e: self.verify_otp_handler())
        
        # Verify Button
        verify_btn = tk.Button(content_frame, text="Verify", font=("Arial", 12, "bold"),
                              bg="#27ae60", fg="white", relief=tk.FLAT, padx=20, pady=10,
                              command=self.verify_otp_handler, cursor="hand2")
        verify_btn.pack(fill=tk.X, pady=10)
        
        # Attempts label
        self.attempts_label = tk.Label(content_frame, 
                                      text=f"Attempts remaining: {self.remaining_attempts}",
                                      font=("Arial", 9), fg="#e74c3c", bg="#f0f0f0")
        self.attempts_label.pack(pady=10)
        
        # Resend button
        resend_btn = tk.Button(content_frame, text="Resend Code", font=("Arial", 10),
                              bg="#ecf0f1", fg="#2c3e50", relief=tk.FLAT, padx=15, pady=8,
                              command=self.show_login_page, cursor="hand2")
        resend_btn.pack(pady=10)
    
    def verify_otp_handler(self):
        """Handle OTP verification."""
        otp_input = self.otp_entry.get().strip()
        
        if not otp_input or len(otp_input) != 6 or not otp_input.isdigit():
            messagebox.showerror("Error", "Please enter a valid 6-digit code.")
            return
        
        success, message = verify_otp(self.current_email, otp_input)
        
        if success:
            self.show_success_page()
        else:
            self.remaining_attempts -= 1
            self.attempts_label.config(text=f"Attempts remaining: {self.remaining_attempts}")
            
            if self.remaining_attempts <= 0:
                messagebox.showerror("Error", "Too many failed attempts. Please try again.")
                self.show_login_page()
            else:
                messagebox.showerror("Error", f"Invalid code. {message}")
                self.otp_entry.delete(0, tk.END)
                self.otp_entry.focus()
    
    def show_success_page(self):
        """Display the success page."""
        self.clear_window()
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2ecc71", height=100)
        header_frame.pack(fill=tk.X)
        
        title = tk.Label(header_frame, text="✓ Login Successful!", font=("Arial", 26, "bold"), 
                        fg="white", bg="#2ecc71")
        title.pack(pady=15)
        
        subtitle = tk.Label(header_frame, text="Welcome to the application", 
                           font=("Arial", 12), fg="white", bg="#2ecc71")
        subtitle.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Success message
        success_msg = tk.Label(content_frame, 
                              text=f"You have successfully logged in as:\n{self.current_email}",
                              font=("Arial", 12), fg="#27ae60", bg="#f0f0f0", 
                              justify=tk.CENTER, wraplength=350)
        success_msg.pack(pady=40)
        
        # Continue button
        continue_btn = tk.Button(content_frame, text="Continue to Dashboard", 
                                font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", 
                                relief=tk.FLAT, padx=20, pady=12,
                                command=self.close_app, cursor="hand2")
        continue_btn.pack(pady=20)
        
        # Login again button
        again_btn = tk.Button(content_frame, text="Login with Another Account", 
                             font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50", 
                             relief=tk.FLAT, padx=15, pady=8,
                             command=self.show_login_page, cursor="hand2")
        again_btn.pack(pady=10)
    
    def close_app(self):
        """Close the application."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = OTPLoginApp(root)
    root.mainloop()
