from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from utils.threat_intelligence import check_threat_intelligence
from utils.firewall import block_ip
from utils.autoencoder import detect_anomaly_autoencoder
from utils.user_behavior import detect_behavior_anomaly
from utils.alerting import send_slack_alert, send_sms_alert
from utils.compliance import generate_compliance_report
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
socketio = SocketIO(app)

# Logging configuration
logging.basicConfig(filename='logs/anomaly_detection.log', level=logging.INFO)

# Email configuration
SENDER_EMAIL = "urmishikhadash2004@gmail.com"  # Replace with your email
SENDER_PASSWORD = "wmcgtzwnpkmeermd"  # Replace with your email app password
RECEIVER_EMAIL = "integrasbiotek@gmail.com"  # Replace with recipient email

def send_email_alert(subject, message):
    """
    Send an email alert to the administrator.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        # Add the message body
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Log in to the email account
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())  # Send the email

        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {str(e)}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_anomaly():
    data = request.json
    ip_address = request.remote_addr
    features = data['features']
    
    # Multi-layer detection
    is_anomaly, detection_method, details = multi_layer_detection(features, ip_address)
    
    if is_anomaly:
        # Log anomaly
        logging.info(f"Anomaly detected from IP {ip_address}: {detection_method}")
        
        # Send alerts
        send_slack_alert(f"Anomaly detected from IP {ip_address}")
        send_sms_alert(f"Anomaly detected from IP {ip_address}")
        
        # Send email alert
        email_subject = "⚠️ Anomaly Detected ⚠️"
        email_message = f"""
        Anomaly detected from IP: {ip_address}
        Detection Method: {detection_method}
        Details: {details}
        """
        send_email_alert(email_subject, email_message)
        
        # Block IP
        block_ip(ip_address)
        
        # Send socket notification
        socketio.emit('anomaly_alert', {
            'ip_address': ip_address,
            'detection_method': detection_method,
            'details': details
        })
    
    return jsonify({
        'anomaly_detected': is_anomaly,
        'detection_method': detection_method,
        'details': details
    })

def multi_layer_detection(features, ip_address):
    # Layer 1: Threat intelligence
    is_malicious, ti_details = check_threat_intelligence(ip_address)
    if is_malicious:
        return True, "Threat intelligence detection", ti_details
    
    # Layer 2: Autoencoder
    if detect_anomaly_autoencoder(features):
        return True, "Autoencoder detection", {}
    
    # Layer 3: User Behavior Analytics
    if detect_behavior_anomaly(features):
        return True, "Behavior-based detection", {}
    
    return False, "No threat detected", {}

if __name__ == '__main__':
    socketio.run(app, debug=True)