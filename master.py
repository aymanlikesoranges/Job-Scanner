import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
    else:
        print(f"{script_name} output:\n{result.stdout}")

def main():
    # Run jobscan.py to scan for new jobs and send an email
    run_script("jobscan.py")
    
    # Run filter.py to filter through the new jobs and store good ones in good_links.json
    run_script("filter.py")
    
    # Run jobapplier.py to open the good job links in your browser and log them in good-links-seen.json
    run_script("jobapplier.py")
    
    print("All tasks completed.")

if __name__ == "__main__":
    main()
