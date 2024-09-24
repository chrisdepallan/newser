import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

class DetailPageTest(unittest.TestCase):
    def setUp(self):
        # Set up Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://newser.chrisdepallan.com/article-detail?article=https://www.wired.com/story/brazil-x-ban-isp-blocking/")  # Replace with your actual detail page URL

    def tearDown(self):
        self.driver.quit()

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def test_page_title(self):
        self.assertIn("Newsers", self.driver.title)

    def test_article_title(self):
        article_title = self.driver.find_element(By.CLASS_NAME, "h1.display-5")
        self.assertTrue(article_title.is_displayed())

    def test_article_image(self):
        article_image = self.driver.find_element(By.CSS_SELECTOR, ".img-zoomin.img-fluid.rounded.w-100")
        self.assertTrue(article_image.is_displayed())

    def test_article_content(self):
        article_content = self.driver.find_element(By.ID, "premium-content")
        self.assertTrue(article_content.is_displayed())

    def test_summarize_button(self):
        summarize_btn = self.driver.find_element(By.ID, "summarize-btn")
        self.assertTrue(summarize_btn.is_displayed())
        self.driver.execute_script("arguments[0].click();", summarize_btn)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "summary-result"), "")
        )

    def test_sentiment_analysis_button(self):
        sentiment_btn = self.driver.find_element(By.ID, "sentiment-btn")
        self.assertTrue(sentiment_btn.is_displayed())
        self.scroll_to_element(sentiment_btn)
        self.driver.execute_script("arguments[0].click();", sentiment_btn)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.text_to_be_present_in_element((By.ID, "sentiment-result"), "Sentiment:")
            )
        except selenium.common.exceptions.TimeoutException:
            # Print the current content of the sentiment-result element
            result_element = self.driver.find_element(By.ID, "sentiment-result")
            print(f"Sentiment result content: {result_element.text}")
            raise  # Re-raise the exception after printing the debug information

        # If we get here, the wait was successful
        result_element = self.driver.find_element(By.ID, "sentiment-result")
        self.assertIn("Sentiment:", result_element.text)

    def test_question_answering(self):
        question_input = self.driver.find_element(By.ID, "question-input")
        ask_btn = self.driver.find_element(By.ID, "ask-btn")
        self.assertTrue(question_input.is_displayed())
        self.assertTrue(ask_btn.is_displayed())
        
        question_input.send_keys("What is the main topic of this article?")
        self.driver.execute_script("arguments[0].click();", ask_btn)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "answer-result"), "Answer:")
        )

    def test_named_entity_recognition_button(self):
        ner_btn = self.driver.find_element(By.ID, "ner-btn")
        self.assertTrue(ner_btn.is_displayed())
        self.scroll_to_element(ner_btn)
        self.driver.execute_script("arguments[0].click();", ner_btn)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.text_to_be_present_in_element((By.ID, "ner-result"), "Entities:")
            )
        except selenium.common.exceptions.TimeoutException:
            # Print the current content of the ner-result element
            result_element = self.driver.find_element(By.ID, "ner-result")
            print(f"NER result content: {result_element.text}")
            raise  # Re-raise the exception after printing the debug information

        # If we get here, the wait was successful
        result_element = self.driver.find_element(By.ID, "ner-result")
        self.assertIn("Entities:", result_element.text)

    def test_popular_categories(self):
        categories = self.driver.find_elements(By.CSS_SELECTOR, ".btn.btn-light.w-100.rounded.text-uppercase.text-dark.py-3")
        self.assertGreater(len(categories), 0)
        for category in categories:
            self.assertTrue(category.is_displayed())

    def test_popular_news(self):
        popular_news = self.driver.find_elements(By.CSS_SELECTOR, ".features-item")
        self.assertGreater(len(popular_news), 0)
        for news in popular_news:
            self.assertTrue(news.is_displayed())

    def test_social_share_buttons(self):
        share_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn.btn-square.rounded-circle.border-primary.text-dark")
        self.assertEqual(len(share_buttons), 4)  # Facebook, Twitter, Instagram, LinkedIn
        for button in share_buttons:
            self.assertTrue(button.is_displayed())

if __name__ == "__main__":
    unittest.main()