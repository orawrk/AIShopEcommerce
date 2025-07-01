"""
Screenshot Capture System for Visual Documentation

This script captures screenshots of all key platform features for documentation purposes.
It automatically navigates through the application and saves high-quality screenshots.

Author: AI E-Commerce Platform Team
Version: 1.0.0
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests

class ScreenshotCapture:
    """Automated screenshot capture system for documentation"""
    
    def __init__(self, base_url="http://localhost:5000", output_dir="docs/images"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.driver = None
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Chrome WebDriver setup failed: {e}")
            print("Screenshots will need to be captured manually")
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to fully load"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Additional wait for dynamic content
        except Exception as e:
            print(f"Page load timeout: {e}")
    
    def capture_screenshot(self, filename, element_selector=None):
        """Capture screenshot of full page or specific element"""
        try:
            if element_selector:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
                )
                element.screenshot(os.path.join(self.output_dir, filename))
            else:
                self.driver.save_screenshot(os.path.join(self.output_dir, filename))
            
            print(f"✓ Screenshot saved: {filename}")
            return True
        except Exception as e:
            print(f"✗ Failed to capture {filename}: {e}")
            return False
    
    def capture_product_catalog(self):
        """Capture product catalog screenshots"""
        print("Capturing Product Catalog...")
        
        try:
            self.driver.get(self.base_url)
            self.wait_for_page_load()
            
            # Main product catalog view
            self.capture_screenshot("01_product_catalog.png")
            
            # Try to interact with search/filter if available
            try:
                # Look for search input
                search_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if search_inputs:
                    search_inputs[0].send_keys("iPhone")
                    time.sleep(2)
                    self.capture_screenshot("02_product_search.png")
            except Exception as e:
                print(f"Search interaction failed: {e}")
            
        except Exception as e:
            print(f"Product catalog capture failed: {e}")
    
    def capture_cart_functionality(self):
        """Capture shopping cart screenshots"""
        print("Capturing Shopping Cart...")
        
        try:
            # Navigate to cart page
            # This assumes there's a navigation to cart
            try:
                cart_links = self.driver.find_elements(By.LINK_TEXT, "Cart")
                if cart_links:
                    cart_links[0].click()
                    self.wait_for_page_load()
                    self.capture_screenshot("03_shopping_cart.png")
            except Exception as e:
                print(f"Cart navigation failed: {e}")
                
        except Exception as e:
            print(f"Cart capture failed: {e}")
    
    def capture_ai_chat(self):
        """Capture AI chat interface"""
        print("Capturing AI Chat Interface...")
        
        try:
            # Navigate to AI Chat
            try:
                ai_links = self.driver.find_elements(By.LINK_TEXT, "AI Chat")
                if ai_links:
                    ai_links[0].click()
                    self.wait_for_page_load()
                    self.capture_screenshot("04_ai_chat.png")
                    
                    # Try to send a message
                    try:
                        text_areas = self.driver.find_elements(By.CSS_SELECTOR, "textarea")
                        if text_areas:
                            text_areas[0].send_keys("Hello, can you help me find a good laptop?")
                            time.sleep(1)
                            
                            # Look for send button
                            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                            for button in buttons:
                                if "send" in button.text.lower() or "submit" in button.text.lower():
                                    button.click()
                                    time.sleep(3)  # Wait for response
                                    self.capture_screenshot("05_ai_chat_conversation.png")
                                    break
                    except Exception as e:
                        print(f"Chat interaction failed: {e}")
                        
            except Exception as e:
                print(f"AI Chat navigation failed: {e}")
                
        except Exception as e:
            print(f"AI Chat capture failed: {e}")
    
    def capture_analytics_dashboard(self):
        """Capture analytics and ML dashboard"""
        print("Capturing Analytics Dashboard...")
        
        try:
            # Navigate to Analytics
            try:
                analytics_links = self.driver.find_elements(By.LINK_TEXT, "Analytics")
                if analytics_links:
                    analytics_links[0].click()
                    self.wait_for_page_load()
                    self.capture_screenshot("06_analytics_dashboard.png")
                    
                    # Try to trigger ML prediction
                    try:
                        predict_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                        for button in predict_buttons:
                            if "predict" in button.text.lower():
                                button.click()
                                time.sleep(3)
                                self.capture_screenshot("07_ml_predictions.png")
                                break
                    except Exception as e:
                        print(f"ML prediction interaction failed: {e}")
                        
            except Exception as e:
                print(f"Analytics navigation failed: {e}")
                
        except Exception as e:
            print(f"Analytics capture failed: {e}")
    
    def capture_retraining_dashboard(self):
        """Capture real-time retraining dashboard"""
        print("Capturing Real-time Retraining Dashboard...")
        
        try:
            # The retraining dashboard should be part of analytics
            # Look for retraining section
            try:
                retraining_sections = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Retraining')]")
                if retraining_sections:
                    # Scroll to retraining section
                    self.driver.execute_script("arguments[0].scrollIntoView();", retraining_sections[0])
                    time.sleep(2)
                    self.capture_screenshot("08_retraining_dashboard.png")
                    
                    # Try to interact with retraining controls
                    try:
                        status_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
                        for button in status_buttons:
                            if "status" in button.text.lower() or "retraining" in button.text.lower():
                                button.click()
                                time.sleep(2)
                                self.capture_screenshot("09_retraining_status.png")
                                break
                    except Exception as e:
                        print(f"Retraining interaction failed: {e}")
                        
            except Exception as e:
                print(f"Retraining section not found: {e}")
                
        except Exception as e:
            print(f"Retraining dashboard capture failed: {e}")
    
    def capture_admin_dashboard(self):
        """Capture admin dashboard"""
        print("Capturing Admin Dashboard...")
        
        try:
            # Navigate to Admin
            try:
                admin_links = self.driver.find_elements(By.LINK_TEXT, "Admin")
                if admin_links:
                    admin_links[0].click()
                    self.wait_for_page_load()
                    self.capture_screenshot("10_admin_dashboard.png")
                    
            except Exception as e:
                print(f"Admin navigation failed: {e}")
                
        except Exception as e:
            print(f"Admin dashboard capture failed: {e}")
    
    def check_services_health(self):
        """Check if all services are running before capturing"""
        services = {
            "Streamlit App": "http://localhost:5000",
            "FastAPI Backend": "http://localhost:8001/docs",
            "ML API": "http://localhost:8000/health"
        }
        
        all_healthy = True
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ {service} is running")
                else:
                    print(f"✗ {service} returned status {response.status_code}")
                    all_healthy = False
            except Exception as e:
                print(f"✗ {service} is not accessible: {e}")
                all_healthy = False
        
        return all_healthy
    
    def capture_all_screenshots(self):
        """Capture all screenshots for documentation"""
        print("=== AI E-Commerce Platform Screenshot Capture ===")
        print("Capturing screenshots for visual documentation...")
        
        if not self.driver:
            print("WebDriver not available. Please capture screenshots manually.")
            return False
        
        # Check if services are running
        if not self.check_services_health():
            print("⚠️  Some services are not running. Screenshots may be incomplete.")
            print("Please ensure all services are started before running screenshot capture.")
        
        try:
            # Capture all main features
            self.capture_product_catalog()
            self.capture_cart_functionality()
            self.capture_ai_chat()
            self.capture_analytics_dashboard()
            self.capture_retraining_dashboard()
            self.capture_admin_dashboard()
            
            print("\n=== Screenshot Capture Complete ===")
            print(f"Screenshots saved to: {self.output_dir}")
            print("You can now use these images in your documentation.")
            
            return True
            
        except Exception as e:
            print(f"Screenshot capture failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def generate_screenshot_index(self):
        """Generate an index of all captured screenshots"""
        screenshots = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.png'):
                screenshots.append(filename)
        
        screenshots.sort()
        
        # Create index file
        index_content = "# Screenshot Index\n\n"
        index_content += "This directory contains screenshots of the AI E-commerce Platform features:\n\n"
        
        for screenshot in screenshots:
            name = screenshot.replace('.png', '').replace('_', ' ').title()
            index_content += f"- **{name}**: `{screenshot}`\n"
        
        with open(os.path.join(self.output_dir, "README.md"), 'w') as f:
            f.write(index_content)
        
        print(f"Screenshot index created: {self.output_dir}/README.md")

def main():
    """Main function to run screenshot capture"""
    capturer = ScreenshotCapture()
    
    print("Starting screenshot capture process...")
    print("Make sure the application is running on http://localhost:5000")
    print("Press Ctrl+C to cancel if needed.")
    
    try:
        time.sleep(3)  # Give user time to read
        success = capturer.capture_all_screenshots()
        
        if success:
            capturer.generate_screenshot_index()
            print("\n✅ Screenshot capture completed successfully!")
        else:
            print("\n❌ Screenshot capture completed with errors.")
            
    except KeyboardInterrupt:
        print("\n🛑 Screenshot capture cancelled by user.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()