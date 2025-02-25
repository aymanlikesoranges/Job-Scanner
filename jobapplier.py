import webbrowser
import time
import json

# Function to load job links from good_links.json
def load_job_links(filename="new_links.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if isinstance(data, list):  # Ensure it's a list of URLs
                return data
            else:
                print(f"Invalid data format in {filename}. Expected a list of links.")
                return []
    except FileNotFoundError:
        print(f"{filename} not found. Please ensure the file exists.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}. Please check the file format.")
        return []

# Function to save the updated job links to the JSON file
def save_job_links(job_links, filename="new_links.json"):
    try:
        with open(filename, "w") as file:
            json.dump(job_links, file, indent=4)
            print(f"Updated {filename} with remaining job links.")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Function to load links from good-links-seen.json (to track opened links)
def load_seen_links(filename="seen-links.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if isinstance(data, list):  # Ensure it's a list of URLs
                return data
            else:
                print(f"Invalid data format in {filename}. Expected a list of links.")
                return []
    except FileNotFoundError:
        print(f"{filename} not found. Creating a new one.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}. Please check the file format.")
        return []

# Function to save the seen links to good-links-seen.json
def save_seen_links(seen_links, filename="good-links-seen.json"):
    try:
        with open(filename, "w") as file:
            json.dump(seen_links, file, indent=4)
            print(f"Updated {filename} with seen links.")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Load job links from good_links.json
job_links = load_job_links()

# Load seen links from good-links-seen.json
seen_links = load_seen_links()

# Check if job_links is empty
if not job_links:
    print("No valid links found. Please check the good_links.json file.")
else:
    # Open job application links in Chrome and process them
    for link in job_links[:]:  # Iterate over a copy of the list to modify the original list
        # Skip link if it has already been opened (exists in seen_links)
        if link in seen_links:
            print(f"Skipping already processed link: {link}")
            continue

        # Open the link in the default web browser
        webbrowser.open(link)
        time.sleep(2)  # Delay to allow the page to load (you can adjust the wait time)

        # After the link is opened, add it to seen_links and save
        seen_links.append(link)
        save_seen_links(seen_links)

        # Optionally remove the link from the job_links list if it's processed
        job_links.remove(link)
        save_job_links(job_links)

    print("All links processed.")
