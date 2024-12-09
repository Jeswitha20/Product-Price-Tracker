import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# In-memory storage for tracking product prices
price_tracking_data = {}

def scrape_price(url):
    """Scrape the product price from the provided URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update with the correct selector for your target site
        price_element = soup.select_one('.a-price-whole')  # For Amazon, for example

        if price_element:
            price_text = price_element.text.strip()
            price = float(price_text.replace(',', '').replace('₹', ''))  # Clean and convert price
            return price
        else:
            print("Price element not found.")
            return None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def send_email(subject, body, to_email):
    """Send an email notification."""
    from_email = "your-email"
    from_password = "your-email-password"  # Replace with your email password

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_price():
    """Check the price of all tracked products every 10 minutes."""
    for product_id, data in price_tracking_data.items():
        url = data["url"]
        target_price = data["targetPrice"]
        email = data["email"]
        last_price = data["lastPrice"]

        # Get the current price from the URL (scraping logic)
        current_price = scrape_price(url)

        if current_price is None:
            # Skip if price couldn't be fetched
            continue

        # Determine the status of the price
        if current_price < last_price:
            status = "decreased"
            subject = "Price Alert: Price decreased!"
            body = f"The price of your product has decreased to ₹{current_price}.\nThis is below your last tracked price of ₹{last_price}.\nTarget price: ₹{target_price}.\nCheck the product here: {url}"
        elif current_price > last_price:
            status = "increased"
            subject = "Price Update: Price increased!"
            body = f"The price of your product has increased to ₹{current_price}.\nLast tracked price was ₹{last_price}.\nTarget price: ₹{target_price}.\nCheck the product here: {url}"
        else:
            status = "no change"
            subject = "Price Update: No change in price"
            body = f"The price of your product remains the same at ₹{current_price}.\nLast tracked price: ₹{last_price}.\nTarget price: ₹{target_price}.\nCheck the product here: {url}"

        # Send email with the price update
        send_email(subject, body, email)

        # Update the last price to the new price
        price_tracking_data[product_id]["lastPrice"] = current_price

    """Check the price of all tracked products every hour."""
    for product_id, data in price_tracking_data.items():
        url = data["url"]
        target_price = data["targetPrice"]
        email = data["email"]
        last_price = data["lastPrice"]

        # Get the current price from the URL (scraping logic)
        current_price = scrape_price(url)

        if current_price is None:
            continue

        # If the price has decreased, send an email
        if current_price < last_price:
            subject = "Price Alert: Price dropped!"
            body = f"The price dropped to ₹{current_price}!\nThis is below your target price of ₹{target_price}.\nCheck the product here: {url}"
            send_email(subject, body, email)

            # Update the last price to the new price
            price_tracking_data[product_id]["lastPrice"] = current_price

@app.route('/track-price', methods=['POST'])
def track_price():
    try:
        # Parse the JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input provided"}), 400

        # Extract the required fields
        url = data.get('url')
        target_price = data.get('targetPrice')
        email = data.get('email')

        # Validate the inputs
        if not url or not target_price or not email:
            return jsonify({"error": "Invalid input"}), 400

        # Get the current price from the URL (scraping logic)
        current_price = scrape_price(url)

        if current_price is None:
            return jsonify({"error": "Could not fetch the price. Please check the URL."}), 400

        # Store the product tracking data
        product_id = len(price_tracking_data) + 1  # Unique product ID for tracking
        price_tracking_data[product_id] = {
            "url": url,
            "targetPrice": target_price,
            "email": email,
            "lastPrice": current_price
        }

        # Notify the user that tracking has started
        # Notify the user that tracking has started
        subject = "Price Tracking Started"
        body = f"Price tracking has started for your product.\nYou will receive an email every 10 minutes with the current price status (decreased, increased, or unchanged).\nCurrent price is ₹{current_price}.\nTarget price: ₹{target_price}."
        send_email(subject, body, email)

        return jsonify({"message": f"Price tracking started for your product. You will be notified 10 minutes with current price status."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Start the price check every 10 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_price, trigger="interval", minutes=10)
    scheduler.start()

    app.run(debug=True)
