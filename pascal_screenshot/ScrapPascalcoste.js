const puppeteer = require('puppeteer');
const crypto = require("crypto");
const fs = require('fs');

class ScrapPascal {
  /**
   * ScrapPascal class for scraping Pascal Coste Shopping website.
   * @param {string} url - The URL of the webpage to scrape.
   */
  constructor(url) {
    this.url = url;
    this.browser = null;
    this.page = null;
  }

  /**
   * Initializes Puppeteer and sets up a new page.
   */
  async initialize() {
    this.browser = await puppeteer.launch({ headless: false }); // Launches a new browser
    this.page = await this.browser.newPage(); // Opens a new page in the browser
    await this.page.setViewport({ width: 1200, height: 1200 }); // Sets the viewport size
  }

  /**
   * Takes a screenshot of the specified element on the page.
   * @returns {string|null} - Path to the saved screenshot or null if an error occurs.
   */
  async takeScreenshot() {
    try {
      await this.page.goto(this.url, { waitUntil: 'domcontentloaded' }); // Navigates to the URL
      await this.page.waitForSelector('img.uk-cover', { visible: true }); // Waits for the image to be visible

      const imgElement = await this.page.$('img.uk-cover'); // Finds the image element
      const screenshotPath = 'screenshot.png';
      await imgElement.screenshot({ path: screenshotPath }); // Takes a screenshot of the image

      return screenshotPath;
    } catch (error) {
      console.error('Error taking screenshot:', error);
      return null;
    }
  }

  /**
   * Retrieves additional details from the page.
   * @returns {Object|null} - Object containing the retrieved details or null if an error occurs.
   */
  async getOtherDetails() {
    try {
      const imgElement = await this.page.$('img.uk-cover'); // Finds the image element
      const src = await imgElement.getProperty("src"); // Gets the 'src' property of the image
      const srcValue = await src.jsonValue(); // Retrieves the value of the 'src' property

      const md5Hash = crypto.createHash('md5').update(srcValue).digest('hex'); // Calculates MD5 hash of the image URL

      const href = await this.page.evaluate(() => {
        const img = document.querySelector('img.uk-cover'); // Finds the image element
        const nextATag = img.nextElementSibling; // Gets the next sibling element
        return nextATag ? nextATag.getAttribute('href') : null; // Retrieves the 'href' attribute of the next sibling (if exists)
      });

      return { srcValue, md5Hash, href };
    } catch (error) {
      console.error('Error getting other details:', error);
      return null;
    }
  }

  /**
   * Closes the browser instance.
   */
  async closeBrowser() {
    if (this.browser) {
      await this.browser.close(); // Closes the browser
    }
  }
}

// Usage
const url = 'https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html';
const screenshotTaker = new ScrapPascal(url); // Instantiates the ScrapPascal class with the URL

(async () => {
  try {
    await screenshotTaker.initialize(); // Initializes Puppeteer
    const screenshotPath = await screenshotTaker.takeScreenshot(); // Takes a screenshot
    const otherDetails = await screenshotTaker.getOtherDetails(); // Retrieves additional details

    if (screenshotPath && otherDetails) {
      const data = {
        id: otherDetails.md5Hash,
        redirection_url: otherDetails.href,
        img_link: otherDetails.srcValue,
        img_url: screenshotPath,
        format: "Left Side Banner"
      };

      fs.writeFileSync('data.json', JSON.stringify(data, null, 2)); // Writes data to JSON file
      console.log('JSON data saved to file.');
    }
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await screenshotTaker.closeBrowser(); // Closes the browser
  }
})();
