import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from wtforms import TextAreaField
from bs4 import BeautifulSoup
import requests
import smtplib



def search(entered_string):
    all_data = dict()
    try:
        # amazon
        modified_string = "+".join(entered_string.split())
        html_text = f'https://www.amazon.in/s?k={modified_string}&ref=nb_sb_noss_2'

        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        webpage = requests.get(html_text, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "lxml")

        if soup.find("div",
                     class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"):
            search_results = soup.find_all("div",
                                           class_="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")[
                             :3]
        else:
            search_results = soup.find_all("div",
                                           class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20")[
                             :3]

        amazon_data = dict()
        count = 1
        for i in search_results:
            info_dict = dict()
            info_dict["name"] = str(i.find("h2").text)
            info_dict["price"] = 'Rs. '+str(i.find("span", attrs={"class": 'a-price-whole'}).text)
            info_dict["source_link"] = "https://www.amazon.in" + str(
                i.find("a", attrs={"class": 'a-link-normal s-no-outline'})["href"])
            info_dict["image_link"] = str(i.find("img", attrs={"class": 's-image'})["src"])
            amazon_data[f"product {count}"] = info_dict
            count += 1

        all_data["amazon"] = amazon_data

        # snapdeal
        modified_string = "%20".join(entered_string.split())
        html_text = f"https://www.snapdeal.com/search?keyword={modified_string}&santizedKeyword=&catId=&categoryId=0&suggested=true&vertical=p&noOfResults=20&searchState=&clickSrc=suggested&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=ALL&url=&utmContent=&dealDetail=&sort=rlvncy"
        r = requests.get(html_text)
        htmlcontent = r.content
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        itemclass = soup.find_all("div", class_='col-xs-6 favDp product-tuple-listing js-tuple')[:3]
        snapdeal_data = dict()
        count = 1
        for i in itemclass:
            info_dict = dict()
            info_dict['link'] = str(i.find('a', class_='dp-widget-link')['href'])
            info_dict['name'] = str(i.find('p', class_='product-title').text)
            info_dict['price'] = str(i.find('span', class_='lfloat product-price').text)
            info_dict['imagelink'] = str(i.find('img', class_='product-image')['src'])
            snapdeal_data[f"product {count}"] = info_dict
            count += 1
        all_data["snapdeal"] = snapdeal_data

        # For Flipkart
        modified_string = "%20".join(entered_string.split())

        html_text = requests.get(
            f"https://www.flipkart.com/search?q={modified_string}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off").text
        print(
            f"https://www.flipkart.com/search?q={modified_string}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")

        soup = BeautifulSoup(html_text, 'lxml')

        flipkart_data = dict()

        if soup.find("a", class_="_1fQZEK"):

            search_results = soup.find_all("a", class_="_1fQZEK")[:3]
            count = 1
            for i in search_results:
                info_dict = dict()
                info_dict["name"] = str(i.find("div", class_="_4rR01T").get_text())
                info_dict["price"] = str(i.find("div", class_="_30jeq3 _1_WHN1").get_text())
                info_dict["source_link"] = "https://www.flipkart.com" + str(i['href'])
                info_dict["image_link"] = str(i.find("img")['src'])
                flipkart_data[f"product {count}"] = info_dict
                count += 1

        elif soup.find(class_="_4ddWXP"):

            search_results = soup.find_all("div", class_="_4ddWXP")[:3]
            count = 1
            for i in search_results:
                info_dict = dict()
                info_dict["name"] = str(i.find("a", class_="s1Q9rs")['title'])
                info_dict["price"] = str(i.find("div", class_="_30jeq3").get_text())
                info_dict["source_link"] = "https://www.flipkart.com" + str(i.find("a", class_="_2rpwqI")['href'])
                info_dict["image_link"] = str(i.find("img")['src'])
                flipkart_data[f"product {count}"] = info_dict
                count += 1

        else:
            search_results = soup.find_all("div", class_="_1xHGtK _373qXS")[:3]
            count = 1
            for i in search_results:
                info_dict = dict()
                info_dict["name"] = str(i.find("a", class_="IRpwTa")['title'])
                info_dict["price"] = str(i.find("div", class_="_30jeq3").get_text())
                info_dict["source_link"] = "https://www.flipkart.com" + str(i.find("a", class_="_3bPFwb")['href'])
                info_dict["image_link"] = str(i.find("img")['src'])
                flipkart_data[f"product {count}"] = info_dict
                count += 1
        all_data["flipkart"] = flipkart_data
        return all_data
    except:
        return 'Not Found'




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)






@app.route('/')
def test():
    return render_template("index.html", searched=False, found=True)






@app.route('/search', methods=["POST", "GET"])
def item_search():
    item = request.form['hero-field']
    found = True
    if request.method=="POST":
        table = search(item)
        if table=='Not Found':
            found=False
    return render_template("index.html", table=table, searched=True, found=found)




@app.route('/contact_us', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        messege = request.form.get('ckeditor')
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login("uditsmss@gmail.com", "ankitsaha007")
            connection.sendmail(from_addr="uditsmss@gmail.com", to_addrs="uditeeiot@gmail.com", msg=f"\nfrom {name}, email:{email}, number:{number}\n{messege}")
        return render_template("contact.html", sent=True)
    return render_template("contact.html", sent=False)



@app.route('/info')
def info():
    return render_template("info.html")



if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0')

