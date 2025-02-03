import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    url = "https://www.linkedin.com/jobs/search/?currentJobId=4119907052&geoId=106215326&keywords=Analyst&location=Bangladesh"

    webdriver_path = r"C:\Users\Sakibs pc\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"
    service = Service(webdriver_path)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    )
    chrome_options.add_argument("--start-maximized")  # Open browser in full-screen mode

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Initialize lists for job details
    companynames = []
    jobtitles = []
    locations = []
    descriptions = []

    # Wait for the page to load
    time.sleep(5)

    # Loop to scroll and load more job cards until we collect at least 196 rows
    while len(jobtitles) < 196:
        try:
            # Locate job cards
            job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")

            for index, job_card in enumerate(job_cards[len(jobtitles):]):  # Process only unvisited job cards
                try:
                    # Scroll to the job card to ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView();", job_card)
                    time.sleep(1)

                    # Extract job title and click on the card
                    title = job_card.find_element(By.CLASS_NAME, 'base-search-card__title').text
                    job_card.click()
                    time.sleep(3)  # Wait for the job details page to load

                    # Extract company name
                    try:
                        company = job_card.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text
                    except Exception:
                        company = "Not specified"

                    # Extract location
                    try:
                        location = job_card.find_element(By.CLASS_NAME, 'job-search-card__location').text
                    except Exception:
                        location = "Not specified"

                    # Extract description from job details section
                    try:
                        description_element = driver.find_element(
                            By.CSS_SELECTOR, "div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details"
                        )
                        description = description_element.text
                    except Exception:
                        description = "Description not available"

                    # Append details to respective lists
                    jobtitles.append(title)
                    companynames.append(company)
                    locations.append(location)
                    descriptions.append(description)

                    print(f"Job {len(jobtitles)}: {title} scraped successfully.")

                    # Navigate back to the main job listing page
                    driver.back()
                    time.sleep(3)

                    # Break the loop if we reach the desired number of rows
                    if len(jobtitles) >= 196:
                        break

                except Exception as e:
                    print(f"Error processing job {len(jobtitles) + 1}: {e}")
                    continue

            # Scroll down to load more jobs if needed
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        except Exception as e:
            print(f"Error loading job cards: {e}")
            break

    # Deduplicate results
    unique_jobs = pd.DataFrame({
        "Company": companynames,
        "Title": jobtitles,
        "Location": locations,
        "Description": descriptions
    }).drop_duplicates()

    # Save results to CSV
    unique_jobs.to_csv("linkedin_jobs.csv", index=False)

    print(f"Scraped {len(unique_jobs)} unique job postings.")
    print(unique_jobs)
    
    # Close the browser window after the job is done
    driver.quit()
    print("Driver closed successfully.")

if __name__ == "__main__":
    main()
