from flask import render_template, flash
from flaskblog import app
from flaskblog.forms import CheckForm
from flaskblog.models import Articles
from flaskblog import db
from bs4 import BeautifulSoup as soup
from selenium import webdriver


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/coin', methods=['GET', 'POST'])
def coin():
    form = CheckForm()

    headerArr = []
    paragraphArr = []

    if form.validate_on_submit():
        # Scrapper

        cryptoName = (str(form.crypto_name.data)).lower()

        url = 'https://coinmarketcap.com/currencies/' + cryptoName + '/news/'

        driver = webdriver.Firefox()
        driver.get(url)

        page = driver.page_source
        page_soup = soup(page, 'html.parser')

        headers = page_soup.findAll("h3", {"class": "sc-1q9q90x-0", "class": "gEZmSc"})
        paragraphs = page_soup.findAll("p", {"class": "sc-1eb5slv-0", "class": "svowul-3", "class": "ddtKCV"})

        exists = check(cryptoName)

        for i in range(0, min(len(headers), len(paragraphs))):
            header = headers[i].text.strip()
            paragraph = paragraphs[i].text.strip()

            if not exists and len(header) > 0 and len(paragraph) > 0:
                new_article = Articles(f'{cryptoName}', f'{header}', f'{paragraph}')
                db.session.add(new_article)
                db.session.commit()

        for row in db.session.query(Articles).filter_by(crypto_name=cryptoName):
            headerArr.append(row.header)
            paragraphArr.append(row.paragraph)

        if len(headerArr) != 0:
            flash(f'Successfully pulled {form.crypto_name.data}!', 'success')
        else:
            flash(f'Couldn\'t find {form.crypto_name.data}!', 'warning')

    return render_template('coin.html', title='Check', form=form, headerArr=headerArr, paragraphArr=paragraphArr)


def check(cryptoName):
    for row in db.session.query(Articles).filter_by(crypto_name=cryptoName):
        if row.crypto_name == cryptoName:
            return True
    return False
