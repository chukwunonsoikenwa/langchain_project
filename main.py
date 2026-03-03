from dotenv import load_dotenv
import json
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()


SUMMARY_TEMPLATE = """
You are a helpful assistant.
Given the subject text below, produce:
1) A short summary (2-4 sentences)
2) Three interesting facts

Subject text:
{information}

Return exactly this format:
SUMMARY:
<summary>
FACTS:
- <fact 1>
- <fact 2>
- <fact 3>
"""


def build_chain():
    summary_prompt = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["information"])
    llm = ChatOllama(model="gemma3:270m", temperature=0)
    return summary_prompt | llm


def parse_response(content: str):
    summary = ""
    facts = []
    mode = None

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        upper = line.upper()
        if upper.startswith("SUMMARY:"):
            mode = "summary"
            summary_line = line.split(":", 1)[1].strip()
            if summary_line:
                summary = summary_line
            continue
        if upper.startswith("FACTS:"):
            mode = "facts"
            continue
        if mode == "summary":
            summary = f"{summary} {line}".strip()
        elif mode == "facts":
            if line.startswith("- "):
                facts.append(line[2:].strip())
            elif re.match(r"^\d+\.\s+", line):
                facts.append(re.sub(r"^\d+\.\s+", "", line))
            else:
                facts.append(line)

    if not summary:
        summary = content.strip()
    return {"summary": summary, "facts": facts, "raw": content}


def analyze_subject(text: str):
    chain = build_chain()
    response = chain.invoke({"information": text})
    return parse_response(response.content)


class ProjectHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        if self.path != "/analyze":
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            payload = json.loads(body) if body else {}
            text = payload.get("text", "").strip()
            if not text:
                self.send_json({"error": "Please provide input text."}, status=400)
                return

            result = analyze_subject(text)
            self.send_json(result, status=200)
        except Exception as exc:
            self.send_json({"error": f"Analysis failed: {exc}"}, status=500)

    def send_json(self, data, status=200):
        output = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(output)))
        self.end_headers()
        self.wfile.write(output)


def main():
    server = HTTPServer(("127.0.0.1", 8000), ProjectHandler)
    print("Server running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
