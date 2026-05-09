import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://benjamincowen.com/reports"
STATE_FILE = "last_report.json"

def get_latest_report():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    reports = soup.find_all("a")

    for link in reports:
        text = link.get_text(strip=True)

        if "Crypto Macro Risk Memo" in text:
            return {
                "title": text,
                "link": link["href"]
            }

    return None

def load_last():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None

def save_current(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def extract_pdf(report_url):
    r = requests.get(report_url)
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href", "")
        if ".pdf" in href:
            return href

    return None

def download_pdf(pdf_url):
    r = requests.get(pdf_url)
    filename = pdf_url.split("/")[-1]

    with open(filename, "wb") as f:
        f.write(r.content)

    print(f"Downloaded: {filename}")

def main():
    latest = get_latest_report()
    last = load_last()

    if not latest:
        print("Kein Report gefunden")
        return

    if latest != last:
        print("Neuer Report gefunden:", latest["title"])

        pdf = extract_pdf(latest["link"])

        if pdf:
            download_pdf(pdf)
        else:
            print("Kein PDF-Link gefunden")

        save_current(latest)
    else:
        print("Kein neuer Report")

if __name__ == "__main__":
    main()