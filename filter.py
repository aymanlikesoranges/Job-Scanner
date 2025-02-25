import requests
from bs4 import BeautifulSoup
import re
import json

# Load job links from the seen_links.json file
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

# List of field names to check for
required_fields = ['first', 'last', 'email', 'phone', 'cover']

def check_required_fields(soup):
    """Check if the page contains required fields for autofill."""
    # Look for input fields with specific keywords in id or name attributes
    inputs = soup.find_all('input')

    # Field match patterns (slightly more flexible for matching fields)
    patterns = {
        'first': r'(first|given|name)',
        'last': r'(last|family|surname)',
        'email': r'(email)',
        'phone': r'(phone)',
        'cover': r'(cover|letter)'
    }

    found_fields = {field: False for field in required_fields}
    matched_inputs = []

    # Check if any field matches the patterns
    for input_tag in inputs:
        input_id = input_tag.get('id', '').lower()
        input_name = input_tag.get('name', '').lower()
        matched_field = None

        for field, pattern in patterns.items():
            if re.search(pattern, input_id) or re.search(pattern, input_name):
                found_fields[field] = True
                matched_field = field

        if matched_field:
            matched_inputs.append(f"{matched_field} field found (ID: {input_id}, Name: {input_name})")

    # Log found fields for debugging
    if matched_inputs:
        print("\n".join(matched_inputs))
    else:
        print("No matching fields found on this page.")

    # Return True if at least one required field is found (to be more lenient)
    return any(found_fields.values())

def scrape_and_check(job_links):
    valid_links = []
    
    for link in job_links:
        try:
            # Fetch the page content with a timeout of 10 seconds to prevent hanging
            response = requests.get(link, timeout=2)
            response.raise_for_status()  # Raise an error for bad status codes (e.g., 404)

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for required fields
            if check_required_fields(soup):
                valid_links.append(link)
            else:
                print(f"Skipped (No matching fields): {link}")

        except requests.exceptions.RequestException as e:
            # Handle any request exceptions (e.g., 404, timeout, etc.)
            print(f"Error fetching {link}: {e}")
            continue  # Skip this link and move to the next one

    return valid_links

def save_good_links(valid_links, filename="good_links.json"):
    """Save valid job links to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(valid_links, file, indent=4)
        print(f"Valid links saved to {filename}")
    except IOError as e:
        print(f"Error writing to {filename}: {e}")

# Load job links from the seen_links.json file
job_links = load_job_links()

# Proceed if job links are found
if job_links:
    # Get valid links that can be autofilled
    valid_job_links = scrape_and_check(job_links)

    # Save the valid links to the good_links.json file
    save_good_links(valid_job_links)

    # Completion message
    if valid_job_links:
        print("\nProcess completed. Valid links saved to good_links.json.")
    else:
        print("\nProcess completed. No valid links found.")
else:
    print("\nNo job links to process. Please check the seen_links.json file.")
