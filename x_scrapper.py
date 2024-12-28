# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# import time

# class TwitterScraper:
#     def __init__(self, email, password,username):
#         self.email = email
#         self.password = password
#         self.username =username
       
#     def setup_driver(self, proxy=None):
#         chrome_options = webdriver.ChromeOptions()
#         # if proxy:
#         #     chrome_options.add_argument(f'--proxy-server={proxy}')
#         #     chrome_options.add_argument('--ignore-certificate-errors')
#         #     chrome_options.add_argument('--allow-insecure-localhost')
#         #     chrome_options.add_argument('--disable-dev-shm-usage')
#         #     print(f"Setting up proxy: {proxy}")
#         # Updated initialization syntax
#         self.driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=chrome_options
#         )
#         self.driver.get("https://api.ipify.org?format=json")
#         print(f"Current IP: {self.driver.page_source}")
        
#     def login(self):
#         self.driver.get("https://x.com/login")
#         # print(f"Current URL: {self.driver.current_url}")  # Add this debug line
#         # print(f"Page source length: {len(self.driver.page_source)}") 
#         try:
#             # Wait for email field and enter email
#             email_field = WebDriverWait(self.driver, 20).until(
#                 EC.presence_of_element_located((By.NAME, "text"))
#             )
#             email_field.send_keys(self.email)
            
#             # Click next
#             next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
#             next_button.click()
            
#             try:
#                 username_field = WebDriverWait(self.driver, 5).until(
#                     EC.presence_of_element_located((By.NAME, "text"))
#                 )
#                 username_field.send_keys(self.username)
                
#                 next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
#                 next_button.click()
#             except:
#                 # If username field doesn't appear, continue to password
#                 pass
            
#             password_field = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.NAME, "password"))
#             )
#             password_field.send_keys(self.password)
#             # Wait for password field and enter password
#             # password_field = WebDriverWait(self.driver, 10).until(
#             #     EC.presence_of_element_located((By.NAME, "password"))
#             # )
#             # password_field.send_keys(self.password)
            
#             # Click login
#             login_button = self.driver.find_element(By.XPATH, "//span[text()='Log in']")
#             login_button.click()
            
#             time.sleep(5)  # Wait for login to complete
#             return True
            
#         except Exception as e:
#             print(f"Login failed: {str(e)}")
#             return False
            
#     def get_trending_topics(self):
#       try:
#         # Wait for trending section
#         trending_section = WebDriverWait(self.driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'happening')]"))
#         )
            
#         # Get trending topics with their actual content
#         trending_topics = WebDriverWait(self.driver, 10).until(
#             EC.presence_of_all_elements_located((
#                 By.CSS_SELECTOR, 
#                 '[data-testid="trend"]'
#             ))
#         )[:5]  # Limiting to top 5 trends
        
#         # Extract both the topic and tweet count
#         trends = []
#         for topic in trending_topics:
#             try:
#                 # Get all text elements within the trend
#                 trend_texts = topic.text.split('\n')
#                 # The actual topic/hashtag is usually the first or second element
#                 # Filter out category headers
#                 for text in trend_texts:
#                     if not any(header in text for header in ['Trending in', 'Sports', '· Trending']):
#                         if text.strip():  # Make sure it's not empty
#                             trends.append(text.strip())
#                             break
#             except:
#                 continue
                
#         return trends
            
#       except Exception as e:
#         print(f"Error getting trending topics: {str(e)}")
#         return []

            
#     def close(self):
#         self.driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import random
import time

class TwitterScraper:
    def __init__(self, email, password, username, proxy_list=None):
        self.email = email
        self.password = password
        self.username = username
        # List of ProxyMesh proxies
        self.proxy_list = proxy_list or [
            "http://Daddymax:%403P7eX4m%40JzABzq@in.proxymesh.com:31280",
            "http://Daddymax:%403P7eX4m%40JzABzq@us.proxymesh.com:31280",
            "http://Daddymax:%403P7eX4m%40JzABzq@uk.proxymesh.com:31280",
            "http://Daddymax:%403P7eX4m%40JzABzq@au.proxymesh.com:31280"
        ]
        
    def get_random_proxy(self):
        """Get a random proxy from the proxy list"""
        return random.choice(self.proxy_list)
    
    # def setup_driver(self, use_proxy=True):
    #     """Initialize Chrome driver with optional proxy support"""
    #     chrome_options = webdriver.ChromeOptions()
        
    #     if use_proxy:
    #         proxy = self.get_random_proxy()
    #         chrome_options.add_argument(f'--proxy-server={proxy}')
    #         chrome_options.add_argument('--ignore-certificate-errors')
    #         chrome_options.add_argument('--allow-insecure-localhost')
    #         chrome_options.add_argument('--disable-dev-shm-usage')
    #         chrome_options.add_argument('--no-sandbox')
    #         chrome_options.add_argument('--disable-gpu')
    #         print(f"Setting up proxy: {proxy}")
            
    #     self.driver = webdriver.Chrome(
    #         service=Service(ChromeDriverManager().install()),
    #         options=chrome_options
    #     )
        
    #     # Verify IP
    #     self.driver.get("https://api.ipify.org?format=json")
    #     print(f"Current IP: {self.driver.page_source}")
    def setup_driver(self, use_proxy=True):
      chrome_options = webdriver.ChromeOptions()
    # Force HTTP
      chrome_options.add_argument('--explicitly-allowed-ports=80,5000')
      chrome_options.add_argument('--disable-web-security')
    
    #   if use_proxy:
    #     proxy = self.get_random_proxy()
    #     chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # # Other options
    #   chrome_options.add_argument('--ignore-certificate-errors')
    #   chrome_options.add_argument('--no-sandbox')
    #   chrome_options.add_argument('--disable-dev-shm-usage')
    
      self.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Test connection with HTTP
      try:
        self.driver.get("http://api.ipify.org?format=json")
        print(f"Current IP: {self.driver.page_source}")
        return True
      except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False
   
    def login(self):
        self.driver.get("https://x.com/login")
        try:
            # Wait for email field and enter email
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_field.send_keys(self.email)
            
            # Click next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            
            try:
                username_field = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                username_field.send_keys(self.username)
                
                next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
                next_button.click()
            except:
                # If username field doesn't appear, continue to password
                pass
            
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.send_keys(self.password)
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//span[text()='Log in']")
            login_button.click()
            
            time.sleep(5)  # Wait for login to complete
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def get_trending_topics(self):
        try:
            # Wait for trending section
            trending_section = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'happening')]"))
            )
                
            # Get trending topics with their actual content
            trending_topics = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, 
                    '[data-testid="trend"]'
                ))
            )[:5]  # Limiting to top 5 trends
            
            # Extract both the topic and tweet count
            trends = []
            for topic in trending_topics:
                try:
                    trend_texts = topic.text.split('\n')
                    for text in trend_texts:
                        if not any(header in text for header in ['Trending in', 'Sports', '· Trending']):
                            if text.strip():
                                trends.append(text.strip())
                                break
                except:
                    continue
                    
            return trends
                
        except Exception as e:
            print(f"Error getting trending topics: {str(e)}")
            return []
            
    def close(self):
        """Close the browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()

