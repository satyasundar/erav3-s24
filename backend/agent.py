import json
import datetime
from utils import extract_links, generate_pdf, send_email_with_pdf
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
# Load environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


def run_agentic_prompt(prompt, messages):
    system_prompt = """
You are a smart assistant helping a user document Telegram group links.

Respond with EXACTLY ONE of these formats:
1. FUNCTION_CALL: function_name|parameters
2. FINAL_ANSWER: <summary of what was done>

Available functions:
- extract_links: Extracts all links from messages within last N days. Format: {"messages": [...], "time_frame_days": int}
- generate_pdf: Generates a PDF from list of links. Format: {"links": [...]} 
- send_email_with_pdf: Sends the generated PDF to Gmail. Format: {"to_email": "satyanayak2040@gmail.com", "pdf_path": "telegram_links.pdf"}

Work plan:
1. Decide the time frame.
2. Call extract_links.
3. Call generate_pdf with the result.
4. Call send_email_with_pdf to complete.
Only use FUNCTION_CALL and FINAL_ANSWER.
"""

    conversation = [
        {
            "role": "user",
            "parts": [
                system_prompt
                + "\n\n"
                + prompt
                + "\nMessages:\n"
                + json.dumps(messages, indent=2)
            ],
        }
    ]

    iteration_count = 0
    extracted_links = []
    pdf_path = ""
    recipient_email = "satyasundar.nayak@gmail.com"

    while iteration_count < 5:
        response = model.generate_content(conversation)
        reply = response.text.strip()
        print(f"\n\n =====Iteration {iteration_count + 1}: ===== \n\n {reply}")

        if reply.startswith("FUNCTION_CALL:"):
            _, payload = reply.split(":", 1)
            func_name, param_str = payload.strip().split("|", 1)
            params = json.loads(param_str)

            if func_name == "extract_links":
                extracted_links = extract_links(**params)
                conversation.append({"role": "model", "parts": [reply]})
                conversation.append(
                    {
                        "role": "user",
                        "parts": ["Result:\n" + json.dumps(extracted_links, indent=2)],
                    }
                )

            elif func_name == "generate_pdf":
                pdf_path = generate_pdf(**params)
                conversation.append({"role": "model", "parts": [reply]})
                conversation.append(
                    {"role": "user", "parts": [f"Result: PDF generated at {pdf_path}"]}
                )

            elif func_name == "send_email_with_pdf":
                result = send_email_with_pdf(
                    to_email=params["to_email"], pdf_path=params["pdf_path"]
                )
                conversation.append({"role": "model", "parts": [reply]})
                conversation.append({"role": "user", "parts": [f"Result: {result}"]})

        elif reply.startswith("FINAL_ANSWER:"):
            return reply[len("FINAL_ANSWER:") :].strip()
        else:
            return "Unexpected LLM response format."

        iteration_count += 1

    return "Agent reached max iterations without final answer."
