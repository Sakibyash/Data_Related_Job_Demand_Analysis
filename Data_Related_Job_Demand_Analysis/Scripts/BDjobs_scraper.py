import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    url = "https://jobs.bdjobs.com/jobsearch.asp?txtsearch=AI%20Engineer&fcat=-1&qOT=0&iCat=0&Country=0&qPosted=0&qDeadline=0&Newspaper=0&qJobNature=0&qJobLevel=0&qExp"

    webdriver_path = r"C:\Users\Sakibs pc\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"
    service = Service(webdriver_path)

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # Initialize lists for job details
    job_titles = []
    company_names = []
    locations = []
    education_requirements = []
    experience_requirements = []

    # Extract job details
    job_title_elements = driver.find_elements(By.CLASS_NAME, 'job-title-text')
    company_name_elements = driver.find_elements(By.CLASS_NAME, 'comp-name-text')
    location_elements = driver.find_elements(By.CLASS_NAME, 'locon-text')
    education_elements = driver.find_elements(By.CLASS_NAME, 'edu-text')
    experience_elements = driver.find_elements(By.CLASS_NAME, 'exp-text')

    for title, company, location, education, experience in zip(job_title_elements, company_name_elements, location_elements, education_elements, experience_elements):
        job_titles.append(title.text)
        company_names.append(company.text)
        locations.append(location.text)
        education_requirements.append(education.text)
        experience_requirements.append(experience.text)

    # Create a DataFrame
    jobs_df = pd.DataFrame({
        "Job Title": job_titles,
        "Company Name": company_names,
        "Location": locations,
        "Education Requirements": education_requirements,
        "Experience Requirements": experience_requirements
    })

    # Save results to CSV
    jobs_df.to_csv("bdjobs_AI_Engineer.csv", index=False)

    print(f"Scraped {len(jobs_df)} job postings.")
    print(jobs_df)
    driver.quit()

if __name__ == "__main__":
    main()