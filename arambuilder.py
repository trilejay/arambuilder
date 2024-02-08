from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['GET'])
def scrape():
    # Get the URL from the query parameters
    url = request.args.get('url')

    # Check if the URL parameter is provided
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        # Initialize the webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = '/usr/bin/chromium-browser'  # Specify the binary location
        driver = webdriver.Chrome(options=options)

        # Open the website
        driver.get(url)

        # Wait for the page to load
        driver.implicitly_wait(10)

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the specific div element with the desired class
        specific_div = soup.find('div', class_='css-11qoik6 ep5npri1')

        # Check if the specific div is found
        if specific_div:
            scraped_data = []

            # Find all tr elements within the specific div
            tr_elements = specific_div.find_all('tr')

            # Iterate over each tr element and find all td elements within it
            for tr in tr_elements:
                row_data = []

                # Find all td elements within the tr
                td_elements = tr.find_all('td')

                # Extract and append the text from each td element
                for td in td_elements:
                    row_data.append(td.text)

                    # If there's an img element with alt attribute, append the alt text (item name)
                    img_elements = td.find_all('img', alt=True)
                    for img in img_elements:
                        row_data.append(img['alt'])

                # Append the row data to the scraped data list
                scraped_data.append(row_data)

            return jsonify({'scraped_data': scraped_data})

        else:
            return jsonify({'error': 'No div with the specified class found on the page'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Close the driver
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
