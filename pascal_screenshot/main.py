import asyncio
import hashlib
import json
from pyppeteer import launch

class ScrapPascal:
    """
    ScrapPascal class for scraping Pascal Coste Shopping website.
    """

    def __init__(self, url):
        self.url = url
        self.browser = None
        self.page = None

    async def initialize(self):
        self.browser = await launch(headless=False)  # Launches a new browser
        self.page = await self.browser.newPage()  # Opens a new page in the browser
        await self.page.setViewport({'width': 1200, 'height': 1200})  # Sets the viewport size

    async def take_screenshot(self):
        try:
            await self.page.goto(self.url, {'waitUntil': 'domcontentloaded'})  # Navigates to the URL
            await self.page.waitForSelector('img.uk-cover', visible=True)  # Waits for the image to be visible

            img_element = await self.page.querySelector('img.uk-cover')  # Finds the image element
            screenshot_path = 'screenshot.png'
            await img_element.screenshot({'path': screenshot_path})  # Takes a screenshot of the image

            return screenshot_path
        except Exception as e:
            print('Error taking screenshot:', e)
            return None

    async def get_other_details(self):
        try:
            img_element = await self.page.querySelector('img.uk-cover')  # Finds the image element
            src_value = await self.page.evaluate('(element) => element.src', img_element)  # Gets the 'src' attribute of the image

            md5_hash = hashlib.md5(src_value.encode()).hexdigest()  # Calculates MD5 hash of the image URL

            href = await self.page.evaluate('(element) => { const nextATag = element.nextElementSibling; return nextATag ? nextATag.getAttribute("href") : null; }', img_element)  # Retrieves the 'href' attribute of the next sibling (if exists)

            return {'srcValue': src_value, 'md5Hash': md5_hash, 'href': href}
        except Exception as e:
            print('Error getting other details:', e)
            return None

    async def close_browser(self):
        if self.browser:
            await self.browser.close()  # Closes the browser

# Usage
url = 'https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html'
screenshot_taker = ScrapPascal(url)  # Instantiates the ScrapPascal class with the URL

async def main():
    try:
        await screenshot_taker.initialize()  # Initializes Pyppeteer
        screenshot_path = await screenshot_taker.take_screenshot()  # Takes a screenshot
        other_details = await screenshot_taker.get_other_details()  # Retrieves additional details

        if screenshot_path and other_details:
            data = {
                'id': other_details['md5Hash'],
                'redirection_url': other_details['href'],
                'img_link': other_details['srcValue'],
                'img_url': screenshot_path,
                'format': 'Left Side Banner'
            }

            with open('data.json', 'w') as json_file:
                json.dump(data, json_file, indent=2)  # Writes data to JSON file
                print('JSON data saved to file.')
    except Exception as e:
        print('Error:', e)
    finally:
        await screenshot_taker.close_browser()  # Closes the browser

asyncio.get_event_loop().run_until_complete(main())
