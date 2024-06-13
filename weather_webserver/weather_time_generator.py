import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import time

# Get the current time in the Asia/Kolkata timezone
current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

# Define the city for the weather search
city = "hyderabad"

# Construct the URL for the Google weather search
url = f"https://www.google.com/search?q=weather+{city}"

# Make a request to the URL and get the content
response = requests.get(url)
html = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract temperature information
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

# Print the weather information
while True:
    print("Temperature:", temp)
    print("The current time in India is:", current_time)
    time.sleep(2)