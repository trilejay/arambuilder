from flask import Flask, request, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['GET'])

def scrape():

    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = '/usr/bin/chromium-browser'  # Specify the binary location
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        driver.implicitly_wait(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the specific div tag with class that contains build information
        specific_div = soup.find('div', class_='css-11qoik6 ep5npri1')

        if specific_div:
            scraped_data = []

            tr_elements = specific_div.find_all('tr')

            for tr in tr_elements:
                row_data = []

                td_elements = tr.find_all('td')

                for td in td_elements:
                    row_data.append(td.text)

                    img_elements = td.find_all('img', alt=True)
                    for img in img_elements:
                        row_data.append(img['alt'])

                scraped_data.append(row_data)

            return jsonify({'scraped_data': scraped_data})

        else:
            return jsonify({'error': 'No div with the specified class found on the page'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
