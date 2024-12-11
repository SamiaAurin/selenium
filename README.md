# **Selenium Automation Testing Project**

This project automates testing of a vacation rental details page using Selenium. It validates essential SEO elements, tests currency filtering, checks URL status codes, and scrapes required data from the webpage. The results are saved in an Excel file.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Usage](#usage)
6. [Report Model](#report-model)
7. [Known Issues and Troubleshooting](#known-issues-and-troubleshooting)
---

## **Features**
- **H1 Tag Validation:** Ensures the presence of an H1 tag on the webpage.
- **HTML Heading Sequence Validation:** Checks that headings (h1, h2, etc.) follow the correct order.
- **Image Alt Attribute Test:** Confirms that all images have alt attributes for accessibility.
- **URL Status Code Validation:** Identifies and reports broken links on the page.
- **Currency Change Test:** Tests if changing the currency updates the prices on the page.
- **Data Scraping:** Extracts campaign and site-specific data from the webpage.
- **Excel Report Generation:** Logs all test results in an Excel file for review.


## **Requirements**
- Python 3.9 or higher
- Google Chrome browser
- Selenium WebDriver
- See `requirements.txt` for all dependencies.

## **Installation**

1. **Clone this repository**

   ```bash
   git clone https://github.com/SamiaAurin/selenium.git
   cd selenium
   ```
2. **Create a virtual environment** 

   2.1 Navigate to your project directory and run:

   ```bash
   python3 -m venv venv  #or python -m venv venv 
   ```
   2.2 Activate the virtual environment:
   
   For Linux/macOS:
   ```bash
   source venv/bin/activate   
   ```

   For Windows:
   ```bash
   .\venv\Scripts\activate
   ```

3. **Install Requirements** 
   Once the virtual environment is activated, you can install the required dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

   ```bash
   selenium/
      │
      ├── test.py                   # Main script to execute all tests
      ├── requirements.txt          # Python dependencies
      ├── TestReports_All.xlsx      # Auto-generated test report (output)
      ├── .gitignore                # Ignored files (e.g., ChromeDriver logs, temporary files)
      └── README.md                 # Project documentation
   ```


## Usage

Run the Script

```bash
python3 test.py #or python test.py
```
The test report will be generated as `TestReports_All.xlsx.`

**Note:**
The testing is being conducted on the following website: https://www.alojamiento.io/. This is the homepage URL, but you are welcome to use any other URL from the same website for testing. Please ensure that you verify and use the correct attribute identifiers (e.g., class names, IDs, XPaths) for accurate results. If you want to ustomize the URL, update the `url` variable in `test.py` to test a different webpage of the same website.

url = "[https://www.alojamiento.io/property/luxury-apartment-heart-madrid/HA-6156815498](https://www.alojamiento.io/property/luxury-apartment-heart-madrid/HA-6156815498)"


### **Tests Performed**

| **Test Name**            | **Description**                                          |
|--------------------------|----------------------------------------------------------|
| H1 Tag Existence Test    | If H1 tag is missing it should be reported as fail.                  |
| HTML Tag Sequence Test   | [H1-H6] tag available if any of the sequence broken or missing it should be reported as fail.|
| Image Alt Attributes     | If image alter attribute is missing it should be reported as fail.            |
| URL Status Code Check    | If any URL status is 404 it should be reported as fail                      |
| Currency Filtering       | Tests if prices update when the currency changes.        |
| Data Scraping            | Extracts campaign and browser-specific metadata. 


## Report Model
The Excel report (TestReports_All.xlsx) includes multiple sheets for detailed results.

Excel Report Example:
1. **Test Report:** Summarizes all tests with status (Pass/Fail) and comments.

2. **URL Status:** Logs URLs and their status (e.g., 404 errors).

3. **Currency Change Results:** This section records all the available currency options from the footer section of the page. For each currency, the test checks if the prices for all cards on the page update accordingly. The results for each currency change will be displayed, showing whether the price changes were applied correctly across all cards.

4. **Scraped Data:** This script extracts the following data from the `<script>` tags in the webpage and records it in the Excel file:

   - **SiteURL**: The URL of the website.
   - **CampaignID**: The ID associated with the campaign.
   - **SiteName**: The name of the website.
   - **Browser**: The browser being used for the test.
   - **CountryCode**: The country code based on the user's location.
   - **IP**: The IP address used for accessing the page. 

###  **Generated Test Report**

The `Test Report` sheet of the `TestReport_All.xlsx` will be structured as follows:

| **Page URL**                                                                                   | **Test Name**              | **Status** | **Comments**                                                                                                                                              |
|------------------------------------------------------------------------------------------------|----------------------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | H1 Tag Existence           | Pass       | H1 tag found                                                                                                                                              |
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | HTML Tag Sequence          | Fail       | Sequence broken: [1, 3, 2] |
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | Image Alt Attribute        | Pass       | All images have alt attributes                                                                                                                             |
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | URL Status Code            | Pass       | No broken links found                                                                                                                                     |
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | Currency Change Test       | Pass       | Currency test results saved in Excel                                                                                                                       |
| https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483                       | Scraped Data               | Pass       | Data written to sheet                                                                                                                                     |

---

## Known Issues and Troubleshooting

While running this project, the following issues might be encountered:


1. **Driver Compatibility**: Ensure the correct version of the WebDriver is installed for your browser. Use tools like `webdriver-manager` for automatic version management.

2. **Dependency Installation**: If installing dependencies from `requirements.txt` fails, try clearing the pip cache using:

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```
3. **Attribute Identification:** Verify that attribute names (e.g., class names, IDs, or XPaths) used in the code match the current structure of the website being tested.

4. **Resource Limitations:** Running the project in a headless browser mode (--headless) can reduce resource usage and may resolve performance issues on low-end devices. In the test.py file, the following line of code is already commented:

   ```bash 
   options.add_argument('--headless') 
   ``` 
   If you require visualization during testing, you can uncomment this line to disable headless mode.


5. **Timeout Errors:** Increase the wait time for elements using WebDriver's explicit waits (WebDriverWait) if elements take longer to load on your network. For Example, In the following code snippet:

    ```bash
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
    )
    ```
   The value `60` specifies a wait time of 60 seconds. You can adjust this value as needed to increase the maximum wait time. Similarly, the wait time can be modified for other WebDriverWait functions in the `test.py` file as well.
    
