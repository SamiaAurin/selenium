import openpyxl
from openpyxl.styles import Font
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests


# Initialize the Excel report
def initialize_excel_report():
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Test Report"
    sheet.append(["Page URL", "Test Name", "Status", "Comments"])  # Header row
    for cell in sheet[1]:
        cell.font = Font(bold=True)  # Make headers bold
    return workbook, sheet

# H1 Tag Existence Test
def test_h1_tag(driver, url):
    driver.get(url)
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        return ("H1 Tag Existence", "Pass", "H1 tag found")
    except:
        return ("H1 Tag Existence", "Fail", "H1 tag missing")

# HTML Tag Sequence Test
def test_html_tag_sequence(driver, url):
    driver.get(url)
    headings = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
    heading_levels = [int(h.tag_name[1]) for h in headings]  # Extract the number from h1, h2, etc.

    # Check if the sequence is correct
    for i in range(1, len(heading_levels)):
        if heading_levels[i] > heading_levels[i - 1] + 1:  # If a level is skipped
            return ("HTML Tag Sequence", "Fail", f"Sequence broken: {heading_levels}")
    
    if not heading_levels:
        return ("HTML Tag Sequence", "Fail", "No headings found on the page")
    
    return ("HTML Tag Sequence", "Pass", f"Sequence correct: {heading_levels}")


# Image Alt Attribute Test
def test_image_alt_attribute(driver, url):
    driver.get(url)
    images = driver.find_elements(By.TAG_NAME, "img")  # Find all <img> tags on the page
    missing_alt = []  # List to store images missing the alt attribute

    for img in images:
        alt_text = img.get_attribute("alt")
        if not alt_text:  # Check if alt is missing or empty
            missing_alt.append(img.get_attribute("src"))  # Store the image source for reference

    if missing_alt:
        return ("Image Alt Attribute", "Fail", f"Missing alt attribute for {len(missing_alt)} images")
    else:
        return ("Image Alt Attribute", "Pass", "All images have alt attributes")


# URL Status Code Test
def test_url_status_code(driver, url, sheet_urls):
    driver.get(url)
    # Find only <a> tags within the body of the page
    body = driver.find_element(By.TAG_NAME, 'body')
    links = body.find_elements(By.TAG_NAME, "a")  
    broken_links = []  

    for link in links:
        href = link.get_attribute("href")  
        if href:  # Ensure the link is not empty
            try:
                response = requests.head(href, allow_redirects=True)  # Check the URL status
                if response.status_code == 404:  # Log only broken links
                    broken_links.append(href)
                    sheet_urls.append([href, "Fail", "404 Not Found"])
            except requests.RequestException as e:  # Log request errors
                broken_links.append(href)
                sheet_urls.append([href, "Fail", f"Request error: {str(e)}"])
        else:
            sheet_urls.append(["Empty Link", "Fail", "No href attribute found"])  # Log missing href attributes

    # Return the test result
    if broken_links:
        return ("URL Status Code", "Fail", f"{len(broken_links)} broken links found")
    else:
        return ("URL Status Code", "Pass", "No broken links found")

    

# Main function to run the tests and generate the Excel report
def main():
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')  

    # Use Service to pass the executable path
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Test site URL
    url = "https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483"
    
    # Initialize the Excel report
    workbook, sheet = initialize_excel_report()
    
    # Create a new sheet for URL status results
    sheet_urls = workbook.create_sheet(title="URL Status")
    sheet_urls.append(["URL", "Status", "Comments"])  # Header row
    for cell in sheet_urls[1]:
        cell.font = Font(bold=True)  # Make headers bold
    
    # Run the H1 tag test
    test_name, status, comments = test_h1_tag(driver, url)
    sheet.append([url, test_name, status, comments])
    
    # Run the HTML tag sequence test
    test_name, status, comments = test_html_tag_sequence(driver, url)
    sheet.append([url, test_name, status, comments])
    
    # Run the image alt attribute test
    test_name, status, comments = test_image_alt_attribute(driver, url)
    sheet.append([url, test_name, status, comments])
    
    # Run the URL status code test
    test_name, status, comments = test_url_status_code(driver, url, sheet_urls)
    sheet.append([url, test_name, status, comments])
    
    # Save the report
    workbook.save("test_report.xlsx")
    print("Test completed. Report saved as 'test_report.xlsx'.")
    
    # Quit the WebDriver
    driver.quit()

# Execute the script
if __name__ == "__main__":
    main()