import requests
from bs4 import BeautifulSoup
import urllib.robotparser
import time
import random
import csv

# URLs
robots_url = "https://rojgarresult.com/robots.txt"
target_url = "https://rojgarresult.com/recruitments/"

# Check robots.txt
rp = urllib.robotparser.RobotFileParser()
rp.set_url(robots_url)
rp.read()

if not rp.can_fetch("*", target_url):
    print("Crawling is disallowed by robots.txt for {target_url}")
else:
    print("Crawling is allowed by robots.txt for {target_url}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(target_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all recruitment links
        job_listings = []
        for link in soup.find_all('a', href=True):
            text = link.get_text(strip=True)
            href = link['href']
            if text and "recruitment" in href.lower():
                job_listings.append((text, href))
        
        # Save to CSV
        with open('job_listings.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Job Title', 'Link'])
            csv_writer.writerows(job_listings)

        print(f"Found {len(job_listings)} job listings. Saving to 'job_listings.csv'.")

        delay = random.uniform(2, 5)  # Random delay between 2 to 5 seconds
        print(f"Sleeping for {delay:.2f} seconds to avoid overloading the server...")
        time.sleep(delay)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


        