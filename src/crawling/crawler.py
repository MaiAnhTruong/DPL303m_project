import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class Crawler:
    def __init__(self, web_url, driver_path, scroll_pause_time=1.0):
        """
        Initialize the Crawler class with the given web URL and driver path to Chrome driver.
        """
        self.web_url = web_url
        self.driver_path = driver_path
        self.links = [] # save product links
        # self.count = 0
        self.scroll_pause_time = scroll_pause_time

    def crawl_product_links(self, num_product_pages, product_style, button_style):
        """
        Crawl the product listing page to collect product links.
        - Scrolls down the page incrementally and clicks 'Load more' to paginate.
        - Collects the hrefs of product links.
        
        Args:
        num_product_pages (int): Number of pages to scroll through and load.
        product_style (str): CSS selector for the product links.
        button_style (str): CSS selector for the 'Load more' button.
        """
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.driver = Chrome(service=Service(self.driver_path), options=options)
        self.driver.get(self.web_url)
        print("Start collecting product links!")

        # Scroll the page in increments to load more products
        time.sleep(random.uniform(4, 5))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
        time.sleep(self.scroll_pause_time)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(self.scroll_pause_time)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4 * 3);")
        time.sleep(self.scroll_pause_time)

        # Click 'Load more' button multiple times for pagination
        for i in range(num_product_pages):
            time.sleep(self.scroll_pause_time)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, button_style)))
                button = self.driver.find_element(By.CSS_SELECTOR, button_style)
                self.driver.execute_script("arguments[0].click();", button)
            except Exception as e:
                print(e)
                break

        # Collect product links from the page
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, product_style)))
            links = self.driver.find_elements(By.CSS_SELECTOR, product_style)
            self.links = [link.get_attribute('href') for link in links]
        except Exception as e:
            print(e)
        self.driver.quit()
        return self.links

    # def crawl_product_data(self, num_comment_pages):
    #     """
    #     Visit each product link to collect product information and comments.
    #     - Extracts details like title, price, sold quantity, rating, and comments.
    #     - Handles multiple pages of comments for each product.

    #     Args:
    #     num_comment_pages (int): Number of comment pages to crawl per product.
    #     """
    #     previous_html = None
    #     with open('raw_data.csv', mode='w', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['Url', 'Title', 'Price', 'Selled Quantity', 'Overall Rating', 'Comment'])  # CSV header

    #         # Iterate over each product link
    #         for index, href in enumerate(self.hrefs, 1):
    #             print(f"Processing link {index}")
    #             options = ChromeOptions()
    #             options.add_argument("--disable-blink-features=AutomationControlled")
    #             options.add_argument("--disable-dev-shm-usage")
    #             options.add_argument("--no-sandbox")
    #             options.add_argument("--ignore-certificate-errors")
    #             options.add_argument("--disable-web-security")
    #             options.add_argument("--incognito")
    #             options.add_argument("--headless")
    #             options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    #             self.driver = Chrome(service=Service(self.driver_path), options=options)
    #             self.driver.get(href)
    #             time.sleep(random.uniform(4, 5))

    #             # Scroll product page to load data
    #             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
    #             time.sleep(self.scroll_pause_time)
    #             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    #             time.sleep(self.scroll_pause_time)
    #             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4 * 3);")
    #             time.sleep(self.scroll_pause_time)

    #             try:
    #                 WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Title__TitledStyled-sc-c64ni5-0.iXccQY')))
    #             except Exception as e:
    #                 print(e)

    #             # Extract product details and comments
    #             self.get_info_data(href, writer)

    #             # Crawl through multiple comment pages
    #             for i in range(1, num_comment_pages):
    #                 try:
    #                     current_html = self.driver.page_source

    #                     # Stop if no new content is loaded
    #                     if previous_html and current_html == previous_html:
    #                         print("No more new content to load! Stop crawling.")
    #                         break

    #                     previous_html = current_html

    #                     # Click 'Next' button to load next comment page
    #                     next_button = self.driver.find_element(By.CSS_SELECTOR, '.btn.next')
    #                     self.driver.execute_script("arguments[0].click();", next_button)
    #                     time.sleep(self.scroll_pause_time)

    #                     # Extract new page's data
    #                     self.get_info_data(href, writer)

    #                 except Exception as e:
    #                     print(f"No more pages to crawl!")
    #                     break

    #             self.driver.quit()

    # def get_info_data(self, href, writer):
    #     """
    #     Helper function to extract product details and comments.
    #     - Extracts title, price, quantity sold, rating, and user comments.

    #     Args:
    #     href (str): The URL of the current product page.
    #     writer (csv.writer): CSV writer object to save the data.
    #     """
    #     try:
    #         url = self.driver.current_url  # Get the current product URL
    #     except:
    #         url = np.nan

    #     try:
    #         title = self.driver.find_element(By.CSS_SELECTOR, '.Title__TitledStyled-sc-c64ni5-0.iXccQY').text  # Get product title
    #     except:
    #         title = np.nan

    #     try:
    #         price = self.driver.find_element(By.CSS_SELECTOR, '.product-price__current-price').text  # Get product price
    #     except:
    #         price = np.nan

    #     try:
    #         selled_quantity = self.driver.find_element(By.CSS_SELECTOR, '.styles__StyledQuantitySold-sc-1onuk2l-3.eWJdKv').text  # Get sold quantity
    #     except:
    #         selled_quantity = np.nan

    #     try:
    #         overall_rating = self.driver.find_element(By.CSS_SELECTOR, 'div.styles__StyledReview-sc-1onuk2l-1.dRFsZg > div:first-child').text  # Get overall rating
    #     except:
    #         overall_rating = np.nan

    #     try:
    #         product_comments_element = self.driver.find_elements(By.CSS_SELECTOR, '.review-comment__content')  # Get all comments
    #         product_comments = [comment.text for comment in product_comments_element]
    #     except:
    #         print(f"No comment in link: {href}")
    #         return
        
    #     # Write product data and comments to CSV
    #     for comment in product_comments:
    #         if comment != "":
    #             self.count += 1
    #             writer.writerow([url, title, price, selled_quantity, overall_rating, comment])
    #             print(f"Successfully crawled {self.count}")

# # Instantiate the Crawler and start crawling
# crawler = Crawler("https://tiki.vn/trang-phuc-the-thao/c67647", "C:/Users/Asus/chromedriver_win64/chromedriver.exe")
# crawler.crawl_product_href(num_product_pages=20)
# crawler.crawl_product_data(num_comment_pages=50)