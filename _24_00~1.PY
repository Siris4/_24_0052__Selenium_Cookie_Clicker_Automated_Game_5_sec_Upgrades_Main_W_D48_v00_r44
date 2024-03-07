
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
import time

upgrade_IDs = {
    'YOU_UPGRADE': 'productName19',
    'CORTEX_BAKER': 'productName18',
    'IDLEVERSE': 'productName17',
    'JAVASCRIPT_CONSOLE': 'productName16',
    'FRACTAL_ENGINE': 'productName15',
    'CHANCEMAKER': 'productName14',
    'PRISM': 'productName13',
    'ANTIMATTER_CONDENSER': 'productName12',
    'TIME_MACHINE': 'productName11',
    'PORTAL': 'productName10',
    'ALCHEMY_LAB': 'productName9',
    'SHIPMENT': 'productName8',
    'WIZARD_TOWER': 'productName7',
    'TEMPLE': 'productName6',
    'BANK': 'productName5',
    'FACTORY': 'productName4',
    'MINE': 'productName3',
    'FARM': 'productName2',
    'GRANDMA': 'productName1',
    'CURSOR': 'productName0',
}

def setup_chrome_driver_for_selenium():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    return driver

def select_language(driver):
    time.sleep(5)  # allows the game to load
    language_selection = driver.find_element(By.ID, "langSelect-EN")
    language_selection.click()
    time.sleep(1)  # waits for language selection to apply

def continuously_click_cookie(driver):
    while True:
        cookie = driver.find_element(By.ID, "bigCookie")
        cookie.click()

def try_clicking_upgrades_periodically(driver):
    while True:
        # iterates through the product ids, starting from the highest productName number, and shifts to the tier below the current one, after that
        for i in range(19, -1, -1):
            product_id = f"product{i}"
            try:
                product_element = driver.find_element(By.ID, product_id)
                # checks if the product is unlocked and enabled
                if "unlocked enabled" in product_element.get_attribute("class"):
                    for _ in range(5):  # attempts up to 5 clicks per upgrade
                        product_element.click()
                        print(f"Clicked on the upgrade: {product_id}.")
                        time.sleep(0.1)  # a brief pause between clicks
                        # this assumes that further validation of availability is not required between clicks.
                    print(f"Finished multiple clicks on: {product_id}. Moving to next available upgrade.")
                else:
                    print(f"Upgrade: {product_id} is not available.")
            except Exception as e:
                print(f"Error accessing {product_id}: {str(e)}")
        time.sleep(5)  # waits for 5 seconds before attempting upgrades again

driver = setup_chrome_driver_for_selenium()
select_language(driver)

# starts continuously clicking the cookie in a separate thread
cookie_clicking_thread = Thread(target=continuously_click_cookie, args=(driver,))
cookie_clicking_thread.start()

# starts trying to click upgrades every 2 seconds in a separate thread
upgrade_clicking_thread = Thread(target=try_clicking_upgrades_periodically, args=(driver,))
upgrade_clicking_thread.start()

# these threads will run indefinitely. to stop them, implement a stopping condition or manually terminate the program.
