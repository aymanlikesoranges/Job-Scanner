import os
import json
import smtplib
import time
from bs4 import BeautifulSoup
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google API Credentials
API_KEY = "AIzaSyArfjw_1cjheC0argTxZKUESDb5_XXTUj8"

#"AIzaSyDeVm-Ml7E3Whyf-e29rWX0ugNxJdqY6kI"  # Replace with a new API key
CX_ID = "5634a00ef882e4378"  # Your custom search engine ID

# Email Configuration
EMAIL_ADDRESS = "auddin6@binghamton.edu"  # Sender's email address
EMAIL_PASSWORD = "cqmu ious yesq dbtu"  # Sender's app-specific password
RECIPIENT_EMAIL = "auddin6@binghamton.edu"  # Recipient email address

# JSON Files to Track Links
SEEN_LINKS_FILE = "seen_links.json"
NEW_LINKS_FILE = "new_links.json"
GOOD_LINKS_SEEN_FILE = "good-links-seen.json"
QUERIES = [
    # Greenhouse.io variations (United States)
    'site:boards.greenhouse.io United States apply Software Developer intern',
    'site:boards.greenhouse.io United States apply Software Developer internship',
    'site:boards.greenhouse.io United States apply Software Engineer intern',
    'site:boards.greenhouse.io United States apply Software Engineer internship',
    'site:boards.greenhouse.io United States apply Software Development intern',
    'site:boards.greenhouse.io United States apply Software Development internship',
    'site:boards.greenhouse.io United States apply Software Engineering intern',
    'site:boards.greenhouse.io United States apply Software Engineering internship',

    # MyWorkdayJobs variations (United States)
    'site:myworkdayjobs.com United States Summer 2025 Software NY',
    'site:myworkdayjobs.com United States Summer 2025 Software Developer NY',
    'site:myworkdayjobs.com United States Summer 2025 Software Development NY',
    'site:myworkdayjobs.com United States Summer 2025 Software Engineer NY',
    'site:myworkdayjobs.com United States Summer 2025 Software Engineering NY',
    'site:myworkdayjobs.com United States Software Developer intern NY',
    'site:myworkdayjobs.com United States Software Developer internship NY',
    'site:myworkdayjobs.com United States Software Engineer intern NY',
    'site:myworkdayjobs.com United States Software Engineer internship NY',
    'site:myworkdayjobs.com United States Software Development intern NY',
    'site:myworkdayjobs.com United States Software Development internship NY',
    'site:myworkdayjobs.com United States Software Engineering intern NY',
    'site:myworkdayjobs.com United States Software Engineering internship NY',

    # NYC-specific searches (Greenhouse.io & MyWorkdayJobs)
    'site:boards.greenhouse.io New York City apply Software Developer intern',
    'site:boards.greenhouse.io New York City apply Software Developer internship',
    'site:boards.greenhouse.io New York City apply Software Engineer intern',
    'site:boards.greenhouse.io New York City apply Software Engineer internship',
    'site:boards.greenhouse.io New York City apply Software Development intern',
    'site:boards.greenhouse.io New York City apply Software Development internship',
    'site:boards.greenhouse.io New York City apply Software Engineering intern',
    'site:boards.greenhouse.io New York City apply Software Engineering internship',
    'site:myworkdayjobs.com New York City Summer 2025 Software',
    'site:myworkdayjobs.com New York City Summer 2025 Software Developer',
    'site:myworkdayjobs.com New York City Summer 2025 Software Development',
    'site:myworkdayjobs.com New York City Summer 2025 Software Engineer',
    'site:myworkdayjobs.com New York City Summer 2025 Software Engineering',
    'site:myworkdayjobs.com New York City Software Developer intern',
    'site:myworkdayjobs.com New York City Software Developer internship',
    'site:myworkdayjobs.com New York City Software Engineer intern',
    'site:myworkdayjobs.com New York City Software Engineer internship',
    'site:myworkdayjobs.com New York City Software Development intern',
    'site:myworkdayjobs.com New York City Software Development internship',
    'site:myworkdayjobs.com New York City Software Engineering intern',
    'site:myworkdayjobs.com New York City Software Engineering internship',

    # Lever.co variations (United States)
    'site:jobs.lever.co United States apply Software Developer intern',
    'site:jobs.lever.co United States apply Software Developer internship',
    'site:jobs.lever.co United States apply Software Engineer intern',
    'site:jobs.lever.co United States apply Software Engineer internship',
    'site:jobs.lever.co United States apply Software Development intern',
    'site:jobs.lever.co United States apply Software Development internship',
    'site:jobs.lever.co United States apply Software Engineering intern',
    'site:jobs.lever.co United States apply Software Engineering internship',

    # Lever.co variations (NYC)
    'site:jobs.lever.co New York City apply Software Developer intern',
    'site:jobs.lever.co New York City apply Software Developer internship',
    'site:jobs.lever.co New York City apply Software Engineer intern',
    'site:jobs.lever.co New York City apply Software Engineer internship',
    'site:jobs.lever.co New York City apply Software Development intern',
    'site:jobs.lever.co New York City apply Software Development internship',
    'site:jobs.lever.co New York City apply Software Engineering intern',
    'site:jobs.lever.co New York City apply Software Engineering internship',

    # Lever.co variations (Summer 2025 - United States)
    'site:jobs.lever.co United States Summer 2025 Software Developer NY',
    'site:jobs.lever.co United States Summer 2025 Software Engineering NY',
    'site:jobs.lever.co United States Software Developer intern NY',
    'site:jobs.lever.co United States Software Developer internship NY',
    'site:jobs.lever.co United States Software Engineer intern NY',
    'site:jobs.lever.co United States Software Engineer internship NY',
    'site:jobs.lever.co United States Software Development intern NY',
    'site:jobs.lever.co United States Software Development internship NY',
    'site:jobs.lever.co United States Software Engineering intern NY',
    'site:jobs.lever.co United States Software Engineering internship NY',

    # Lever.co variations (NYC-Specific)
    'site:jobs.lever.co New York City Software Developer intern',
    'site:jobs.lever.co New York City Software Developer internship',
    'site:jobs.lever.co New York City Software Engineer intern',
    'site:jobs.lever.co New York City Software Engineer internship',
    'site:jobs.lever.co New York City Software Development intern',
    'site:jobs.lever.co New York City Software Development internship',
    'site:jobs.lever.co New York City Software Engineering intern',
    'site:jobs.lever.co New York City Software Engineering internship'
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

def google_search(query):
    """Perform a Google search using Custom Search API."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX_ID,
        "num": 10  # Maximum results per API request
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("items", [])
            return {result["link"] for result in results}
        else:
            print(f"Google API Error {response.status_code}: {response.text}")
            return set()
    except Exception as e:
        print("Error during Google search:", e)
        return set()

def is_internship_page(url):
    """Check if the job listing page contains the word 'intern' or 'internship'."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()
            if 'intern' in page_text or 'internship' in page_text:
                return True
        return False
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def job_search_task():
    """Main function to search jobs, filter results, and send an email."""
    print("Running job search task...")

    # Load existing link data
    seen_links = load_links(SEEN_LINKS_FILE)
    new_links = load_links(NEW_LINKS_FILE)
    good_seen_links = load_links(GOOD_LINKS_SEEN_FILE)

    all_new_links = set()
    
    for query in QUERIES:
        print(f"Searching for: {query}")
        search_results = google_search(query)
        all_new_links.update(search_results)

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
    job_search_task()
    print("Job search completed for this run.")