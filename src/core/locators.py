from selenium.webdriver.common.by import By

wrap_xpath = lambda t: f"//div[@id= 'corePriceDisplay_desktop_feature_div']/div//span[@class= 'a-price-{t}']"

class AmazonLocators:
    login_button = (By.XPATH, "(//strong[text()= 'Log in']/parent::a)[1]")
    nav_button = (By.CSS_SELECTOR, ".nav-button")
    catalog_menu = (By.XPATH, "//span[text()= 'Catalog']")
    add_product_button = (By.XPATH, "//span[text()= 'Add Products']/ancestor::a")
    search_nav = (By.XPATH, "//kat-box[@data-testid= 'keywords-selector']")
    search_input = (By.XPATH , "(//kat-predictive-input[contains(@unique-id, 'katal-id')])[1]")
    search_button = (By.XPATH, "//kat-button[@label= 'Search']")
    result_item = (By.XPATH, "//div[@data-testid= 'search-results-rows']/div")
    result_link = (By.XPATH, "(//kat-link[contains(@href, 'https://amazon.com/dp/')])[1]")
    upc = (By.XPATH, "//b[text()='UPC:']/parent::span")
    active_image = (By.XPATH, "//li[contains(@class, 'image') and contains(@class, 'selected')]//img")
    all_images = (By.XPATH, "//li[contains(@class, 'item') and contains(@class, 'imageThumbnail')]")
    list_price = "//span[contains(text(), 'List Price: $')]"
    list_price_2 = "//td[text()= 'List Price:']/following-sibling::td/span[1]/span[1]"
    discounted_price = "//span[text()= 'Price:']/parent::td/following-sibling::td/span[1]/span[1]"
    discounted_price_whole = wrap_xpath("whole")
    discounted_price_fraction = wrap_xpath("fraction")
    side_panel_search_input = (By.XPATH , "(//kat-predictive-input[contains(@unique-id, 'katal-id')])[2]")
    side_panel_search_button = (By.CSS_SELECTOR, "kat-button[data-testid=search-results-search-submit-button]")


class VendooLocators:
    login_button = (By.XPATH, "(//a[@id= 'Main-Menu-Log-in'])[1]")
    email_input = (By.CSS_SELECTOR, "#email")
    password_input = (By.CSS_SELECTOR, "#password")
    submit_login = (By.CSS_SELECTOR, "#login-btn")
    new_item_button = (By.XPATH, "//a[text()= 'New Item']")
    title_input = (By.CSS_SELECTOR, "input[id='generalDetails.title']")
    price_input = (By.CSS_SELECTOR, "input[id='generalDetails.price']")
    notes_input = (By.CSS_SELECTOR, "textarea[id='generalDetails.notes']")
    images_input = (By.CSS_SELECTOR, "input[id=imageInput]")
    templete_dropdown = (By.CSS_SELECTOR, "#template")
    drop_down_option = (By.XPATH, f"//span[text()= 'Amazon Lot SAMPLE']/ancestor::div[@role= 'option']")
    save_button = (By.XPATH, "//button[text()= 'Save']")
