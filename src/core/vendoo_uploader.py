import os
import time
import glob
from dotenv import load_dotenv
from src.utils.base_page import BasePage
from src.core.locators import VendooLocators as vl


load_dotenv()

class VendooUploader(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.vendoo.co/"

    def login_to_vendoo_account(self):
        self.open_new_tab(self.url)
        login_btn = self.check_element_exists(vl.login_button, timeout=3)
        if login_btn:
            self.click_element_by_js(vl.login_button)
            email_input = self.check_element_exists(vl.email_input, timeout=3)
            if email_input:
                self.input_element(vl.email_input, os.getenv("VENDOO_USERNAME"))
                self.input_element(vl.password_input, os.getenv("VENDOO_PASSWORD"))
                self.click_element_by_js(vl.submit_login)
        time.sleep(10)  # Wait for login to complete

    def upload_images(self, image_folder: str):
        image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp')
        all_images = []
        for ext in image_extensions:
            search_pattern = os.path.join(image_folder, ext)
            all_images.extend(glob.glob(search_pattern))
        all_paths_string = '\n'.join(all_images)
        try:
            ele = self.find_element_using_WebDriverWait(vl.images_input)
            if ele:
                ele.send_keys(all_paths_string)
        except Exception as e:
            print(f"Error locating or sending files: {e}")

    def upload_product(self, asin: str, upc_code: str, title: str, price: str, image_folder: str):
        self.shift_to_next_tab()
        self.click_element(vl.new_item_button)
        self.wait_for_page_load()
        self.click_element(vl.templete_dropdown)
        time.sleep(0.5)
        self.click_element(vl.drop_down_option)
        self.upload_images(image_folder)
        time.sleep(1)
        self.input_element(vl.title_input, title)
        self.input_element(vl.price_input, price)
        self.input_element(vl.notes_input, f"ASIN: {asin}\nUPC: {upc_code}")
        self.click_element(vl.save_button)
        time.sleep(1)  # Wait for save to complete
        self.switch_to_tab_by_index(0)
        time.sleep(1)
