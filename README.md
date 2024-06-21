# tgsc-The-good-scent-company-scrapper
This is a scrapper of fragrances demo formulas on thegoodscentscompany.com based on Python. It will output two tables with the information of product demo formulas and the ingredients contained in it
Modules used:
requests

Input: the fragrance demo formula's url on the good scent company website, the User Agent part of your headers, the title of your output file

Output:
1. sourcecode.txt, which includes the source code of the url you provided
2. A csv file of "your_title + Informaiton.csv", which includes keys of [id, name, application, description, total]
id: the id of the fragrance to connect to "your_title + Ingredients.csv"
name: Name of the formula
application: Application of the formula on the website. Empty if no information on website
description: Description of the formula on the website. Empty if no description on website
total: total percentage of all the ingredients add together. Same with the total column in "your_title + Ingredients.csv"
3. A csv file of "your_title + Ingredeints.csv", which includes keys of [id, ingredients, percentage, 100 pct, website, total]
id:the id of the fragrance to connect to "your_title + Information.csv
ingredients: the ingredient of the fragrance formula
percentage: the percentage of ingredient in this formula
100 pct: the percentage of ingredient in this formula converted to per 100 percent
website: the website of this ingredient. For accords that appears as an ingredient of another accord, if you click this website, and then click the "Fragrance Demo Formula" on the page, and finally search for the name of the accord, you can find the formula of this accord.
total: total percentage of all the ingredients add together. Same with the total column in "your_title + Information.csv"

How to use:
1. Download the file and unzip it
2. add the tgscScrapper.py file to your project
3. install the requests on your project. Use "pip install requests".
4. import the module to your project with "from tgscScrapper import Scrapper"
5. establish the object with "test=Scrapper( your_url, User_Agent, your_title)". User Agent can be accessed through using Inspect on the Browser and click the "Network" tab. Refresh the page and click on the first row. Find the "User-Agent" in the "Headers" tab and copy the whole string and paste it into the function.
6. Call the function "test.scrape()"
7. Run the program

Tips:
Fragrance Demo Formulas of certain accord or including certain ingredients can be searched by "the good scent company+ name of accord" on google. For example, to find the demo formulas of the rose accord, one can use the keyword of "the good scent company rose" to search, and click on the rose fragrance site on the good scent company. And then click on the "Fragrance Demo Formula" button on the website, and you will find a website with the formulas about your accord or containing your ingredient. Use that url for the scrapping.
