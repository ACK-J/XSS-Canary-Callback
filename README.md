<p align="center">
  <img src="https://github.com/user-attachments/assets/735c457f-0fcf-4d27-abfb-14bcbc03c955" alt="canary" width="250" />
</p>

# XSS Canary Callback WebServer

A lightweight Flask application designed to log and display XSS Canary alerts in a real‑time dashboard. This repo is compatible with the canary code found at https://xsscanary.com.

Please reference the [Black Hills Information Security blog post](https://www.blackhillsinfosec.com/alerting-on-xss-exploits/) to learn more.

## Overview

This project provides a simple backend to collect potential cross‑site scripting (XSS) alerts. Alerts are received as JSON payloads via a dedicated POST endpoint and logged to a file for later review. A password‑protected dashboard lets you review alerts along with details like the alert message, stack trace, URL, DOM snapshot, and timestamp.

## Features

- **Alert Reception:**  
  - **Endpoint:** `POST /xss`  
  - Expects a JSON payload with required keys:  
    - `alert_msg`: A short description of the alert.  
    - `stack`: The associated stack trace.  
    - `url`: The URL where the alert was triggered.  
    - `ref`: The referrer URL (if applicable).  
    - `timestamp`: (Optional) If not provided, the current timestamp is added.
  - **Logging:** Alerts are appended as individual JSON lines to `xss_canary.json`.

- **Basic Health Check:**  
  - **Endpoint:** `GET /` and `GET /xss`  
  - Simply returns "It's working!" to indicate the service is online.

- **Secure Dashboard:**  
  - **Endpoint:** `GET /dashboard`  
  - Protected via HTTP Basic Authentication (username: `admin`).  
  - Displays a styled view of all logged alerts, with support for expandable DOM sections.
- **Hosted Canary Scripts**
    - **Endpoint:** `GET /canary.js?domain=example.com`
    - **Endpoint:** `GET /canary_no_dom.js?domain=example.com`
    - Static canary scripts used to identify XSS within your webserver and report exploits to the XSS Canary webserver.
    - To prevent the user's DOM from getting sent use the `/canary_no_dom.js` file

## Requirements

- [Python 3.x](https://www.python.org/)
- Dependencies listed in [requirements.txt](./requirements.txt):
  - Flask
  - Flask-Cors
  - gunicorn (for production deployment)

## Installation
To easily install the XSS canary callback software on your server I've created an installation script . This script first installs dependencies and then creates a system daemon to run the web server as a low privileged user. The email in the command is used by Let's Encrypt to notify you when your SSL certificate is nearing expiration, although auto-renewal is enabled by default. Piping curl to bash as root is commonly ill-advised so, please read the code before executing the following command. The install script is a Gist you can find [HERE](https://gist.github.com/ACK-J/9acef3f7d188de49d6ff7304328e168a).
   ```bash
   bash <(curl -s https://gist.githubusercontent.com/ACK-J/9acef3f7d188de49d6ff7304328e168a/raw/284f0f41127c40ecb162904c7a31881b49521680/install_xss_canary_callback_server.sh) example.com your@email.com
   ```

### Development Mode

Start the Flask application by running:

```bash
python app.py
```

The application will run on [http://localhost:9000](http://localhost:9000).  
You should see a message in the terminal:

```
==================================================
Access the dashboard at http://localhost:9000/dashboard
Username: admin
Password: [Set in DASHBOARD_PASSWORD environment variable]
==================================================
```

### Production Deployment

You can use [gunicorn](https://gunicorn.org/) to run the application in production:

```bash
gunicorn --bind 0.0.0.0:443 \\
  --certfile=/etc/letsencrypt/live/${CALLBACK_DOMAIN}/fullchain.pem \\
  --keyfile=/etc/letsencrypt/live/${CALLBACK_DOMAIN}/privkey.pem \\
  --workers 4 --daemon\\
  app:app
```

## Logging

Each valid XSS alert POSTed to `/xss` is logged in `xss_canary.json` as a JSON object on a new line.

## Brought to you by:

![Black Hills Information Security](https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png "Black Hills Information Security")

## Terms of Service
By using XSS Canary Callback, you agree to use it solely for lawful and ethical purposes, specifically for authorized penetration testing and security research with the explicit, written consent of the system owner. Unauthorized use of this tool against third-party systems without permission is strictly prohibited and may constitute a violation of local, national, or international laws. You are solely responsible for ensuring your use complies with all applicable regulations. The developers and distributors of XSS Canary Callback disclaim all liability for any misuse or damage resulting from its use and provide the tool “as-is” without warranties of any kind. By using the tool, you agree to indemnify and hold harmless its creators from any claims, damages, or legal consequences arising from your actions. Continued use of the tool following any updates to these terms constitutes your acceptance of the revised Terms of Service.
