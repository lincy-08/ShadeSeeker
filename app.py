from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch lipsticks based on shade
def get_lipsticks(shade):
    api_url = "https://makeup-api.herokuapp.com/api/v1/products.json?product_type=lipstick"
    response = requests.get(api_url)

    if response.status_code == 200:
        products = response.json()
        # Filter products based on the user input shade
        filtered_lipsticks = [p for p in products if shade.lower() in p.get("name", "").lower()]
        return filtered_lipsticks

    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    lipsticks = []
    shade = ""
    if request.method == 'POST':
        shade = request.form.get('shade')
        lipsticks = get_lipsticks(shade)
    return render_template('index.html', lipsticks=lipsticks, shade=shade)

if __name__ == '__main__':
    app.run(debug=True)
