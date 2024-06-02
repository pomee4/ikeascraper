import requests
import sqlite3
import json

# Define the URL and parameters for the API request
url = "https://web-api.ikea.com/circular/circular-asis/offers/public/hu/hu"
headers = {
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('ikea_offers.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS offers (
        id INTEGER PRIMARY KEY,
        sekundId TEXT,
        title TEXT,
        description TEXT,
        price REAL,
        heroImage TEXT,
        images TEXT,
        productCondition TEXT,
        isInBox BOOLEAN,
        currency TEXT,
        priority INTEGER,
        reasonDiscount TEXT,
        additionalInfo TEXT,
        articlesPrice REAL,
        unitId TEXT
    )
''')

# Function to notify bot about new entry
def notify_bot(item):
    bot_url = 'http://localhost:4321/notify'  # Assuming the bot listens on this endpoint
    try:
        response = requests.post(bot_url, json=item)
        if response.status_code == 200:
            print("Notification sent to bot successfully.")
        else:
            print("Failed to notify bot:", response.status_code)
    except Exception as e:
        print("Exception occurred while notifying bot:", str(e))

# Iterate from page 0 to page 10
for page in range(11):
    # Define the parameters for the API request
    params = {
        "size": 64,
        "stores": 180,
        "page": page
    }

    # Send the API request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Insert data into the table
        for item in data['content']:
            cursor.execute('''
            INSERT OR IGNORE INTO offers (
                id, sekundId, title, description, price, heroImage, images, 
                productCondition, isInBox, currency, priority, reasonDiscount, 
                additionalInfo, articlesPrice, unitId
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            item['id'],
            item['sekundId'],
            item['title'],
            item['description'],
            item['price'],
            item['heroImage'],
            json.dumps(item['images']),  # Store the list as JSON string
            item['productCondition'],
            item['isInBox'],
            item['currency'],
            item['priority'],
            item['reasonDiscount'],
            item['additionalInfo'],
            item['articlesPrice'],
            item['unitId']
            ))

            # Check if the entry is new
            if cursor.rowcount > 0:
                print("New entry added:")
                print(item)
                notify_bot(item)

    else:
        print("Request failed with status code:", response.status_code)

# Commit the changes and close the connection
conn.commit()
conn.close()
