from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
import time


def test_currency_change_for_cards(driver, url):
    # Open the webpage
    driver.get(url)

    # Wait for the price elements to load
    print("Waiting for price elements...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
    )
    price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
    initial_prices = [elem.text for elem in price_elements]
    print(f"Found {len(initial_prices)} price elements.")

    # Print initial prices
    print("Initial Prices:")
    for i, price in enumerate(initial_prices):
        print(f"Card {i + 1}: {price}")

    # Scroll to the footer section to locate the currency dropdown
    print("Waiting for currency dropdown to become present...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
    )
    footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
    driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
    
    time.sleep(1)  # Wait for the scroll to complete

    # Click on the currency dropdown
    try:
        # Wait for the currency dropdown to become clickable
        print("Waiting for currency dropdown to become clickable...")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
        ).click()
        print("Currency dropdown clicked.")

        # Wait for the dropdown to become visible
        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//ul[@class='select-ul']//li[.//div[@class='option']//p[contains(text(), 'USD')]]")
                )
            )
            print("Dropdown menu is visible.")
        except Exception as e:
            print(f"Error waiting for the dropdown menu: {e}")

          
       
        # Find the USD option using the text content
        usd_option = driver.find_element(By.XPATH, "//ul[@class='select-ul']//li[.//div[@class='option']//p[contains(text(), 'USD')]]")

        #Use JavaScript to click the dropdown and option
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, 'js-currency-sort-footer'))
        driver.execute_script("arguments[0].click();", usd_option)

        time.sleep(1)  # Optional: Wait a bit for smooth scrolling

        print("USD option found and scrolled into view.")
        
        # Click the USD option
        usd_option.click()
        print("USD option clicked.")

        # Wait for the prices to update
        WebDriverWait(driver, 50).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'js-price-value'), '$')
        )
        print("Prices updated with USD.")
    except Exception as e:
        print(f"Error interacting with currency dropdown: {e}")
        return

    # Capture updated prices after currency change
    updated_prices = [elem.text for elem in driver.find_elements(By.CLASS_NAME, 'js-price-value')]

    # Print updated prices
    print("Updated Prices (After Currency Change to USD):")
    for i, price in enumerate(updated_prices):
        print(f"Card {i + 1}: {price}")

    # Compare initial and updated prices
    test_results = []
    for i in range(len(initial_prices)):
        if initial_prices[i] != updated_prices[i]:
            test_results.append(f"PASS (Currency changed successfully)")
        else:
            test_results.append(f"FAIL (Currency did not change)")

    # Print test results
    print("\nTest Results:")
    for i, result in enumerate(test_results):
        print(f"Card {i + 1}: {result}")

    # Save results to Excel
    save_results_to_excel(initial_prices, updated_prices, test_results)

def save_results_to_excel(initial_prices, updated_prices, test_results):
    # Create a new workbook
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Currency Change Test"

    # Write header row
    sheet.append(["Card Number", "Initial Price", "Updated Price", "Test Result"])

    # Write test results
    for i in range(len(initial_prices)):
        sheet.append([f"Card {i + 1}", initial_prices[i], updated_prices[i], test_results[i]])

    # Save workbook to file
    workbook.save("currency_change_test_report.xlsx")
    print("\nTest results saved to 'currency_change_test_report.xlsx'.")


# Main execution
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run in headless mode (optional)
    driver = webdriver.Chrome(options=options)

    try:
        test_currency_change_for_cards(driver, "https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483")
    finally:
        driver.quit()
