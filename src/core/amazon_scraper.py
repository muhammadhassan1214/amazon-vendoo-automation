import time
from typing import Any
from lxml.html import fromstring
from src.core.locators import AmazonLocators as al
from src.utils.base_page import BasePage


class AmazonScraper(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://sellercentral.amazon.com/"

    def login_to_amazon_seller_account(self):
        self.safe_navigate_to_url(self.url)
        login_btn = self.check_element_exists(al.login_button, timeout=3)
        if login_btn:
            self.click_element_by_js(al.login_button)
            input("Log In and Press Enter key to continue...")

    def go_to_amazon_seller_central(self):
        self.click_element_by_js(al.nav_button)
        self.move_to_element(al.catalog_menu)
        self.click_element_by_js(al.add_product_button)
        self.click_element_by_js(al.search_nav)

    def search_product(self, product_asin: str, page: str):
        button_1, button_2 = al.side_panel_search_input, al.side_panel_search_button
        if page == 'main':
            button_1, button_2 = al.search_input, al.search_button
        self.click_using_action_chain(button_1)
        element = self.find_element_using_WebDriverWait(button_1, timeout=3)
        time.sleep(1)
        if element:
            self.input_element(button_1, product_asin)
        self.click_element_by_js(button_2)

    def click_result_link(self) -> str | tuple[Any, str]:
        self.click_element(al.result_item)
        element = self.find_element_using_WebDriverWait(al.result_link, timeout=5)
        if not element:
            return ""
        title, link = element.get_attribute("label").strip(), element.get_attribute("href")
        upc = self.get_element_text(al.upc)
        upc_code = upc.split("UPC:")[-1].strip() if "UPC:" in upc else ""
        self.open_new_tab(link)
        return title, upc_code

    def get_all_image_urls(self) -> list:
        self.shift_to_next_tab()
        self.wait_for_page_load()
        all_images = []
        image_elements = len(self.driver.find_elements(*al.all_images))
        for i in range(1, image_elements + 1):
            img_locator = (al.all_images[0], f"({al.all_images[1]})[{i}]//img")
            self.move_to_element(img_locator)
            img_url = self.get_element_attribute(al.active_image, "src")
            all_images.append(img_url)
        return all_images

    def get_price(self) -> str:
        page_source_data = self.driver.page_source
        data = fromstring(page_source_data)
        listed_price = data.xpath(f"{al.list_price}/text()")
        dwp = data.xpath(f"{al.discounted_price_whole}/text()")
        dfp = data.xpath(f"{al.discounted_price_fraction}/text()")
        discounted_price = f"{dwp[0]}.{dfp[0]}" if dwp and dfp else ""
        if not listed_price:
            listed_price = data.xpath(f"{al.list_price_2}/text()")
        if discounted_price == "":
            discounted_price = data.xpath(f"{al.discounted_price}/text()")
            discounted_price = discounted_price[0].strip().split('$')[-1] if discounted_price else ""
        list_price = listed_price[0].strip().split('$')[-1] if listed_price else ""
        self.close_current_tab_and_switch_back()
        if list_price == "" and discounted_price == "":
            return "0.00"
        return list_price if list_price != "" else discounted_price
