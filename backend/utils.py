import re
from datetime import datetime, timedelta, timezone
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
from typing import List, Dict


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


def summarize_links(links: List[Dict[str, str]], llm_model) -> List[Dict[str, str]]:
    summarized_links = []

    for item in links:
        url = item["url"]
        timestamp = item["timestamp"]

        # Build prompt
        prompt = f"""Summarize the article or content at the following link in 7 words or less. 
                     Return only the summary, no explanation or formatting:

                    {url}
                    """

        # LLM call
        response = llm_model.generate_content(prompt)
        summary = response.text.strip()

        summarized_links.append(
            {"timestamp": timestamp, "summary": summary, "url": url}
        )

    return summarized_links


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Telegram Link Summary Report", ln=True, align="C")
        self.ln(5)

    def table_header(self):
        self.set_font("Arial", "B", 12)
        self.cell(40, 10, "Date", 1)
        self.cell(100, 10, "Summary", 1)
        self.cell(50, 10, "Link", 1)
        self.ln()

    def table_row(self, date, summary, url):
        self.set_font("Arial", "", 11)
        self.cell(40, 10, date, 1)
        self.cell(100, 10, summary, 1)
        # Add hyperlink as text
        self.set_text_color(0, 0, 255)
        self.cell(50, 10, "Click Here", 1, link=url)
        self.set_text_color(0, 0, 0)
        self.ln()


def generate_pdf(links):
    pdf = PDF()
    pdf.add_page()
    pdf.table_header()

    for link in links:
        timestamp = link.get("timestamp", "No Timestamp")
        date_str = (
            datetime.fromisoformat(timestamp).strftime("%Y-%m-%d")
            if timestamp != "No Timestamp"
            else "Unknown"
        )
        summary = link.get("summary", "No Summary")
        url = link.get("url", "No URL")

        pdf.table_row(date_str, summary, url)

    filename = "telegram_links_summary.pdf"
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
