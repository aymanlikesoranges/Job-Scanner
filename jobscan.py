import os
import json
import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googlesearch import search

EMAIL_ADDRESS = "auddin6@binghamton.edu"  # Sender's email address
EMAIL_PASSWORD = "cqmu ious yesq dbtu"  # Sender's app-specific password
RECIPIENT_EMAIL = "auddin6@binghamton.edu"  # Recipient email address

SEEN_LINKS_FILE = "seen_links.json"
NEW_LINKS_FILE = "new_links.json"
GOOD_LINKS_SEEN_FILE = "good-links-seen.json"

QUERIES = [
    'site:boards.greenhouse.io united states intext:"apply" (intext:"Software Developer intern" OR intext:"Software Developer internship")',
    'site:boards.greenhouse.io united states intext:"apply" (intext:"Software Engineer intern" OR intext:"Software Engineer internship")',
    'site:myworkdayjobs.com Summer 2025 Software NY"'
]

NUM_RESULTS = 200

def load_seen_links():
    if os.path.exists(SEEN_LINKS_FILE):
        try:
            with open(SEEN_LINKS_FILE, "r") as f:
                seen_links = json.load(f)
                return set(seen_links)
        except Exception as e:
            print("Error loading seen links:", e)
            return set()
    return set()

def save_seen_links(seen_links):
    try:
        with open(SEEN_LINKS_FILE, "w") as f:
            json.dump(list(seen_links), f)
    except Exception as e:
        print("Error saving seen links:", e)

def load_new_links():
    if os.path.exists(NEW_LINKS_FILE):
        try:
            with open(NEW_LINKS_FILE, "r") as f:
                new_links = json.load(f)
                return set(new_links)
        except json.JSONDecodeError:
            print(f"Error decoding {NEW_LINKS_FILE}, returning empty set.")
            return set()
        except Exception as e:
            print("Error loading new links:", e)
            return set()
    return set()

def save_new_links(new_links):
    try:
        with open(NEW_LINKS_FILE, "w") as f:
            json.dump(list(new_links), f)
    except Exception as e:
        print("Error saving new links:", e)

def load_good_seen_links():
    if os.path.exists(GOOD_LINKS_SEEN_FILE):
        try:
            with open(GOOD_LINKS_SEEN_FILE, "r") as f:
                good_seen_links = json.load(f)
                return set(good_seen_links)
        except Exception as e:
            print("Error loading good seen links:", e)
            return set()
    return set()

def send_email(new_links):
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

def search_job_links():
    results = set()
    for query in QUERIES:
        try:
            print(f"Searching for: {query}")
            for url in search(query, num=150, start=0, pause=1):
                results.add(url)
        except Exception as e:
            print(f"Error during Google search for query: {query} - {e}")
    return results

def job_search_task():
    print("Running job search task...")

    # Load previously seen links
    seen_links = load_seen_links()

    # Load new links already found in the previous run
    new_links = load_new_links()

    # Search for new job links (this time, batching them in a loop)
    current_links = search_job_links()

    # Identify new links by subtracting the seen ones from the current links
    new_links_found = current_links - seen_links

    print(f"Found {len(current_links)} links, {len(new_links_found)} are new.")

    # Load the good-seen links file
    good_seen_links = load_good_seen_links()

    # Filter out any links already present in good-links-seen.json from new_links_found
    valid_new_links = new_links_found - good_seen_links

    print(f"{len(valid_new_links)} new valid job links found after checking good-links-seen.json.")

    if valid_new_links:
        send_email(valid_new_links)
        
        # Update the seen links with new links
        seen_links.update(valid_new_links)
        save_seen_links(seen_links)

        # Save valid new links to new_links.json
        save_new_links(valid_new_links)

        # Update new links list by adding the valid new links
        new_links.update(valid_new_links)
        save_new_links(new_links)
    else:
        print("No valid new job links to send.")
    
    return valid_new_links  # Return valid new links

if __name__ == "__main__":
    job_search_task()
    print("Job search completed for this run.")
