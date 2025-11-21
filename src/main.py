import time
from utils import base_page
from utils.base_page import BasePage
from core.amazon_scraper import AmazonScraper
from core.vendoo_uploader import VendooUploader
from utils.static import (
    read_csv_data, asin_already_processed,
    save_asin_to_done_list, delete_directory,
    save_images_to_directory
)


class MainApp:
    def __init__(self, driver=None):
        self.driver = driver or BasePage.get_undetected_driver()
        self.scraper = AmazonScraper(self.driver)
        self.uploader = VendooUploader(self.driver)

    def processor(self):
        if not self.driver:
            base_page.logger.error("Driver initialization failed.")
            return
        try:
            self.scraper.login_to_amazon_seller_account()
            self.scraper.go_to_amazon_seller_central()
            asins = read_csv_data()
            loop_count = 0
            for asin in asins:
                if asin_already_processed(asin):
                    continue
                base_page.logger.info(f"Processing ASIN: {asin}")
                if loop_count == 0:
                    self.scraper.search_product(asin, page='main')
                else:
                    self.scraper.search_product(asin, page='side')
                title, upc_code = self.scraper.click_result_link()
                product_title = f"{asin} {upc_code} {title}".strip()
                image_urls = self.scraper.get_all_image_urls()
                price = self.scraper.get_price()
                images_directory = save_images_to_directory(image_urls, asin)
                if loop_count == 0:
                    self.uploader.login_to_vendoo_account()
                self.uploader.upload_product(asin, upc_code, product_title, price, images_directory)
                save_asin_to_done_list(asin)
                delete_directory(asin)
                loop_count += 1
            time.sleep(1)
        except Exception as e:
            base_page.logger.error(f"An error occurred: {e}")
        finally:
            self.driver.quit()


if __name__ == "__main__":
    app = MainApp()
    app.processor()