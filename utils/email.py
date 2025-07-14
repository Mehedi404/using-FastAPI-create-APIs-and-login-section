
import aiosmtplib
from email.message import EmailMessage
from config import EMAIL_FROM, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

async def send_email_async(subject: str, recipient: str, body: str):
    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        print(f"Email sent successfully to {recipient}") # For debugging
    except aiosmtplib.SMTPException as e:
        print(f"Failed to send email: {e}") # This will print the exact SMTP error
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
