# README: Pascal Coste Website Scraper

This script utilizes Puppeteer to scrape data from the Pascal Coste Shopping website.

## Features

- Captures a screenshot of the main banner image.
- Extracts details like image source URL, MD5 hash of the URL, and potential redirection URL from the next sibling element of the banner image.

## Requirements

- Node.js and npm installed ([Node.js website](https://nodejs.org/en))

## Installation

1. Navigate to the project directory in your terminal.
2. Run `npm install` to install the required dependencies (`puppeteer` and `crypto`).

## Usage

1. Navigate to the directory i.e 'pascal_screenshot' in terminal.
2. Run the script using `node ScrapPascalcoste.js` .

## Output

The script generates a JSON file named `data.json` containing:
- `id`: MD5 hash of the image source URL (unique identifier).
- `redirection_url`: URL from the next sibling element of the banner image (if available).
- `img_link`: Source URL of the banner image.
- `img_url`: Path to the saved screenshot of the banner image.
- `format`: "Left Side Banner" (assuming the banner is on the left side).

## Error Handling

The script logs any errors encountered during execution to the console.