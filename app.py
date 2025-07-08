from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://makeup-api.herokuapp.com/api/v1/products.json?product_type=lipstick"

def get_lipsticks(shade=None, brand=None):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        products = response.json()

        # Filter by shade and brand if provided
        filtered = products
        if shade:
            filtered = [p for p in filtered if shade.lower() in p.get("name", "").lower()]
        if brand:
            filtered = [p for p in filtered if brand.lower() in p.get("brand", "").lower()]

        return filtered
    except Exception as e:
        print(f"API Error: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    lipsticks = []
    shade = ""
    brand = ""
    if request.method == 'POST':
        shade = request.form.get('shade')
        brand = request.form.get('brand')
        lipsticks = get_lipsticks(shade, brand)

    return render_template('index.html', lipsticks=lipsticks, shade=shade, brand=brand)

if __name__ == '__main__':
    app.run(debug=True)
