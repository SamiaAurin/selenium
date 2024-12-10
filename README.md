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

Customize the URL

Update the `url` variable in `test.py` to test a different webpage:

url = "[https://www.alojamiento.io/property/luxury-apartment-heart-madrid/HA-6156815498](https://www.alojamiento.io/property/luxury-apartment-heart-madrid/HA-6156815498)"


### **Tests Performed**

| **Test Name**            | **Description**                                          |
|--------------------------|----------------------------------------------------------|
| H1 Tag Validation        | Checks if an H1 tag exists on the page.                  |
| HTML Heading Sequence    | Ensures heading tags are in proper order.                |
| Image Alt Attributes     | Verifies that all images have alt attributes.            |
| URL Status Code Check    | Identifies broken or invalid links.                      |
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

