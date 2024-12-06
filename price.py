from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time
import traceback

def test_currency_change_for_cards(driver, url):
    try:
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

        # Comprehensive debugging of page structure
        print("\n--- Page Structure Investigation ---")
        
        # Find all elements that might be related to currency selection
        currency_related_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'CURRENCY', 'currency'), 'currency') or contains(@id, 'currency') or contains(@class, 'currency')]")
        print(f"Found {len(currency_related_elements)} currency-related elements:")
        for i, elem in enumerate(currency_related_elements):
            print(f"{i+1}. Tag: {elem.tag_name}, ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}, Text: {elem.text}, Visible: {elem.is_displayed()}")

        # Try multiple locator strategies for dropdown
        dropdown_locators = [
            (By.ID, 'js-currency-sort-footer'),
            (By.XPATH, "//select[contains(@id, 'currency') or contains(@class, 'currency')]"),
            (By.XPATH, "//div[contains(@class, 'currency-selector')]"),
            (By.XPATH, "//*[contains(translate(text(), 'CURRENCY', 'currency'), 'currency')]")
        ]

        dropdown_element = None
        for locator in dropdown_locators:
            try:
                dropdown_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                print(f"\nFound clickable dropdown using locator: {locator}")
                print(f"Dropdown details - Tag: {dropdown_element.tag_name}, Text: {dropdown_element.text}")
                break
            except TimeoutException:
                print(f"Could not find dropdown with locator: {locator}")

        if dropdown_element is None:
            print("\nCould not find any currency dropdown. Saving page source for investigation.")
            with open('page_source.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            return

        # Advanced interaction techniques
        interaction_methods = [
            lambda: dropdown_element.click(),
            lambda: ActionChains(driver).move_to_element(dropdown_element).click().perform(),
            lambda: driver.execute_script("arguments[0].click();", dropdown_element)
        ]

        # Find USD option strategies
        usd_locators = [
            (By.XPATH, "//*[contains(translate(text(), 'USD', 'usd'), 'usd')]"),
            (By.XPATH, "//option[contains(translate(text(), 'USD', 'usd'), 'usd')]"),
            (By.XPATH, "//li[contains(translate(text(), 'USD', 'usd'), 'usd')]")
        ]

        success = False
        for interaction_method in interaction_methods:
            try:
                # Scroll to element
                driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)
                time.sleep(1)

                # Attempt interaction
                interaction_method()
                print("\nSuccessfully interacted with dropdown.")

                # Try to find USD option
                usd_option = None
                for locator in usd_locators:
                    try:
                        usd_option = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(locator)
                        )
                        print(f"Found USD option using locator: {locator}")
                        print(f"USD Option details - Tag: {usd_option.tag_name}, Text: {usd_option.text}")
                        break
                    except TimeoutException:
                        print(f"Could not find USD option with locator: {locator}")

                if usd_option:
                    # Try multiple ways to select USD
                    select_methods = [
                        lambda: usd_option.click(),
                        lambda: ActionChains(driver).move_to_element(usd_option).click().perform(),
                        lambda: driver.execute_script("arguments[0].click();", usd_option)
                    ]

                    for select_method in select_methods:
                        try:
                            select_method()
                            print("Successfully selected USD option.")
                            success = True
                            break
                        except Exception as select_error:
                            print(f"USD selection method failed: {select_error}")

                if success:
                    break
            except Exception as interaction_error:
                print(f"Dropdown interaction method failed: {interaction_error}")

        if not success:
            print("\nFailed to change currency. Saving page source and screenshot.")
            with open('currency_change_failure.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            driver.save_screenshot('currency_change_failure.png')
            return

        # Wait for prices to update
        try:
            WebDriverWait(driver, 30).until(
                lambda d: any('$' in elem.text for elem in d.find_elements(By.CLASS_NAME, 'js-price-value'))
            )
        except TimeoutException:
            print("\nPrices did not update to USD. Investigating...")
            updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
            print("Current price texts:")
            for elem in updated_price_elements:
                print(elem.text)
            return

        # Capture and print updated prices
        updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        updated_prices = [elem.text for elem in updated_price_elements]

        print("\nUpdated Prices (After Currency Change):")
        for i, price in enumerate(updated_prices):
            print(f"Card {i + 1}: {price}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        
        # Save page source for debugging
        with open('unexpected_error_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        # Take screenshot
        driver.save_screenshot("unexpected_error_screenshot.png")

# Main execution
if __name__ == "__main__":
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        test_currency_change_for_cards(driver, "https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483")
    finally:
        driver.quit()