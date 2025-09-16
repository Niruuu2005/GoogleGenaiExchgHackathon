import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

def scrape_website_content(url, max_retries=3, delay=5):
    """
    Fetches the content from a given URL and extracts the main text content,
    with a retry mechanism and a user-agent header.
    
    Args:
        url (str): The URL of the website to scrape.
        max_retries (int): The maximum number of retries to attempt.
        delay (int): The delay in seconds between retries.

    Returns:
        str: The extracted text content or an error message.
    """
    # Define a user-agent header to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Check if the URL has a scheme (like http or https)
    if not urlparse(url).scheme:
        url = "https://" + url

    response = None
    for attempt in range(max_retries):
        try:
            # Send a GET request to the URL with headers
            print(f"Attempt {attempt + 1} of {max_retries} to fetch URL...")
            response = requests.get(url, headers=headers, timeout=10)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            # If the request is successful, break the retry loop
            break
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return f"All {max_retries} attempts failed. An error occurred while fetching the URL: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    if response and response.status_code == 200:
        try:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style tags to clean up the content
            for script_or_style in soup(['script', 'style']):
                script_or_style.extract()

            # Get all the visible text from the page
            text_content = soup.get_text()

            # Clean up the text by stripping leading/trailing whitespace and multiple newlines
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)

            return text_content
        except Exception as e:
            return f"An unexpected error occurred during parsing: {e}"

    return "Failed to retrieve a successful response after all attempts."


if __name__ == "__main__":
    # Get the URL from the user
    url_to_scrape = input("Please enter the URL of the website to scrape: ")
    
    print("\nScraping content. This may take a moment...\n")

    # Call the scraping function
    content = scrape_website_content(url_to_scrape)

    # Print the result
    print("-" * 50)
    print(content)
    print("-" * 50)
