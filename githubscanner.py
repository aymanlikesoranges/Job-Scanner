import os
import json
import smtplib
import time
from bs4 import BeautifulSoup
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
EMAIL_ADDRESS = "auddin6@binghamton.edu"  # Sender's email address
EMAIL_PASSWORD = "cqmu ious yesq dbtu"  # Sender's app-specific password
RECIPIENT_EMAIL = "auddin6@binghamton.edu"  # Recipient email address

# JSON Files to Track Links
SEEN_LINKS_FILE = "seen_links.json"
NEW_LINKS_FILE = "new_links.json"
GOOD_LINKS_SEEN_FILE = "good-links-seen.json"
GITHUB_LINKS_FILE = "github_links.json"

# GitHub job search URLs
GITHUB_URLS = [
    'https://github.com/SimplifyJobs/Summer2025-Internships',
    # Add more GitHub search URLs for job listings
]

def load_links(file_path):
    """Load links from a JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"Error loading {file_path}:", e)
            return set()
    return set()

def save_links(file_path, links):
    """Save links to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(list(links), f)
    except Exception as e:
        print(f"Error saving {file_path}:", e)

def send_email(new_links):
    """Send an email with new job listings."""
    if not new_links:
        print("No new job listings to send.")
        return
    
    listing_date = time.strftime('%Y-%m-%d %H:%M:%S')
    subject = f"New Job Listings Update - {listing_date}"
    body = f"New job listings as of {listing_date}:\n\n" + "\n".join(new_links)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

def is_internship_page(url):
    """Check if the job listing page contains the word 'intern' or 'internship'."""
    # Skip if the URL is not valid (doesn't start with 'http' or 'https')
    if not url.startswith(('http://', 'https://')):
        print(f"Skipping invalid URL: {url}")
        return False
    
    try:
        response = requests.get(url, verify=False)  # Skip SSL verification for now
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()
            if 'intern' in page_text or 'internship' in page_text:
                return True
        return False
    except requests.exceptions.SSLError as e:
        print(f"SSL Error with {url}: {e}")
        return False
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def github_job_search_task():
    """Main function to search GitHub job listings, filter results, and send an email."""
    print("Running GitHub job search task...")

    # Load existing link data
    seen_links = load_links(SEEN_LINKS_FILE)
    new_links = load_links(NEW_LINKS_FILE)
    good_seen_links = load_links(GOOD_LINKS_SEEN_FILE)

    all_new_links = set()

    for github_url in GITHUB_URLS:
        print(f"Searching GitHub for: {github_url}")
        search_results = requests.get(github_url)
        if search_results.status_code == 200:
            soup = BeautifulSoup(search_results.text, "html.parser")
            links = {a["href"] for a in soup.find_all("a", href=True) if "intern" in a["href"] or "internship" in a["href"]}
            all_new_links.update(links)

    new_links_found = all_new_links - seen_links
    valid_new_links = set()

    # Check each link to ensure it contains 'intern' or 'internship'
    for link in new_links_found:
        if is_internship_page(link):
            valid_new_links.add(link)

    print(f"Found {len(all_new_links)} links, {len(new_links_found)} are new.")
    print(f"{len(valid_new_links)} new valid job links after filtering.")

    if valid_new_links:
        send_email(valid_new_links)

        # Update JSON files with new valid links
        seen_links.update(valid_new_links)
        save_links(SEEN_LINKS_FILE, seen_links)
        save_links(NEW_LINKS_FILE, valid_new_links)
    else:
        print("No valid new job links to send.")

if __name__ == "__main__":
    github_job_search_task()
    print("GitHub job search completed for this run.")
