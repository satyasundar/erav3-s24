import re
from datetime import datetime, timedelta, timezone
from fpdf import FPDF
import smtplib
from email.message import EmailMessage


def extract_links(messages, time_frame_days):
    links = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=time_frame_days)
    for msg in messages:
        ts = datetime.fromisoformat(msg["timestamp"])
        # Ensure ts is also in UTC
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts >= cutoff:
            urls = re.findall(r"https?://\S+", msg["text"])
            for url in urls:
                links.append({"timestamp": msg["timestamp"], "url": url})
    return links


def generate_pdf(links):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Telegram Group Shared Links", ln=True)
    pdf.ln(10)
    for link in links:
        # pdf.multi_cell(0, 10, f"{link['timestamp']} - {link['url']}")
        pdf.multi_cell(0, 10, link)
    filename = "telegram_links.pdf"
    pdf.output(filename)
    return filename


def send_email_with_pdf(to_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "Telegram Group Links PDF"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = to_email

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(), maintype="application", subtype="pdf", filename=pdf_path
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("satyanayak2041@gmail.com", "tbid sior iewy lzur")
        smtp.send_message(msg)
    return "Email sent."
