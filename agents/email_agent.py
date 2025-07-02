import smtplib
from email.mime.text import MIMEText
import os
from config_loader import config

def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email using Gmail's SMTP server.

    Args:
        to_email (str): Recipient's email address.
        subject (str): Subject of the email.
        body (str): Plain text body of the email.

    Returns:
        str: Status message indicating success or failure.
    """
    try:
        sender =  config["email_sender"]
        password = config["email_password"]

        if not sender or not password:
            return "❌ EMAIL_SENDER or EMAIL_PASSWORD not set in environment variables."

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())

        return f"✅ Email sent to {to_email} successfully."

    except smtplib.SMTPAuthenticationError:
        return "❌ Authentication failed. Check your email and app password."
    except smtplib.SMTPRecipientsRefused:
        return f"❌ Recipient address refused: {to_email}"
    except smtplib.SMTPException as e:
        return f"❌ SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"



