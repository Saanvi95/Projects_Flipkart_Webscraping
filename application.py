from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from flask_cors import CORS, cross_origin
import requests
from urllib.request import urlopen
import logging
import csv

logging.basicConfig(filename='scrap.log', level=logging.INFO, format='%(name)s %(levelname)s %(message)s ')

application = Flask(__name__)
app = application

@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            urlClient = urlopen(flipkart_url)
            flipkartPage = urlClient.read()
            urlClient.close()
            flipkart_html = bs(flipkartPage, 'html.parser')
            bigbox = flipkart_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del bigbox[0:3]
            product_link = "https://www.flipkart.com" + bigbox[0].div.div.div.a['href']
            prodReq = requests.get(product_link)
            prodReq.encoding = 'utf-8'
            prodHtml = bs(prodReq.text, 'html.parser')
            prodAll = prodHtml.find_all('div', {'class': 'col JOpGWq'})
            reviewAll = "https://www.flipkart.com" + prodAll[0].find_all('a')[-1]['href']
            reviewPage = bs(requests.get(reviewAll).text, 'html.parser')
            revPageList = reviewPage.find_all("a", {"class": "ge-49M"})
            reviews = []

            for i in revPageList:
                try:
                    pageLink = bs(requests.get("https://www.flipkart.com" + i['href']).text, 'html.parser')
                    commentBoxes = pageLink.find_all('div', {'class': '_1AtVbE col-12-12'})
                    del commentBoxes[0:4]
                    del commentBoxes[-1]
                except:
                    logging.error("Review page link issue")

                for commentbox in commentBoxes:
                    try:
                        name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    except:
                        logging.error("Name not found")
                    try:
                        heading = commentbox.div.find_all('p', {'class': '_2-N8zT'})[0].text
                    except:
                        logging.error("No heading")
                    try:
                        rating = commentbox.div.div.find_all('div', {'class': '_3LWZlK _1BLPMq'})[0].text
                    except:
                        logging.error("No rating")
                    try:
                        custComment = commentbox.div.find_all('div', {'class': 't-ZTKy'})[0].div.div.text
                    except:
                        logging.error("No customer comment")

                    mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": heading, "Comment": custComment}
                    reviews.append(mydict)

            # Save data to a CSV file
            filename = searchString + ".csv"
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Product", "Name", "Rating", "CommentHead", "Comment"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reviews)

            return render_template('result.html', reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            logging.error('The exception message is : ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
