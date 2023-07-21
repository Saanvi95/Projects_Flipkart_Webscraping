import streamlit as st
from bs4 import BeautifulSoup as bs
import requests
import logging
import pymongo
import csv

st.title('Flipkart Web Scraper')

# Function to perform web scraping
def scrape_data(search_string):
    # ... Your web scraping code ...

    # Process the scraped data
    data = []  # Create a list to store the scraped data
    for review in reviews:
        data.append(
            {
                "Product": review["Product"],
                "Name": review["Name"],
                "Rating": review["Rating"],
                "CommentHead": review["CommentHead"],
                "Comment": review["Comment"],
            }
        )

    # Save data to a CSV file
    filename = search_string + ".csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product", "Name", "Rating", "CommentHead", "Comment"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)

    # Return the scraped data
    return data

# Streamlit app starts here
search_string = st.text_input('Enter the product to search on Flipkart:', '')

if st.button('Scrape and Save'):
    if search_string:
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            # ... Continue with the rest of your web scraping code ...

            # You can call the scrape_data function passing the search_string here
            # and store the returned data in a variable `data`.

            # Display the scraped data in a DataFrame
            st.write(f"Scraped data for '{search_string}':")
            st.dataframe(data)

            # Display a download link for the CSV file
            st.write(f"Download the CSV file: [Download {search_string}.csv](./{filename})")
            
        except Exception as e:
            st.error('Something went wrong. Please try again later.')
            logging.error('The exception message is:', e)
    else:
        st.warning('Please enter a product to search.')
