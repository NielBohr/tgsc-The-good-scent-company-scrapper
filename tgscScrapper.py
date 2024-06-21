import time
from time import sleep
import random
import requests
import csv
import re
import json
from datetime import datetime
import os
import random
class Scrapper:
    def __init__(self, url, headers, title):
        self.url = url
        self.headers = headers
        self.title = title

    def searchsingle(self,start, end, content):
        if end != "" and start != "":
            pattern = re.compile(f'{re.escape(start)}(.*?){re.escape(end)}', re.DOTALL)
        elif end == "":
            pattern = re.compile(f'{re.escape(start) + r'\s*(.*)'}')
        elif start == "":
            pattern = re.compile(f'{r'^(.*?)' + re.escape(end)}')
        result = re.search(pattern, content).group(1)
        return result

    def searchmultiple(self,start, end, content):
        if end != "" and start != "":
            pattern = re.compile(f'{re.escape(start)}(.*?){re.escape(end)}', re.DOTALL)
        elif end == "":
            pattern = re.compile(f'{re.escape(start) + r'\s*(.*)'}')
        elif start == "":
            pattern = re.compile(f'{r'^(.*?)' + re.escape(end)}')
        matches = pattern.findall(content)
        result = {}
        reslist = []
        for i, match in enumerate(matches, 0):
            result[i] = match
        for i in result.values():
            reslist.append(i)
        return reslist

    def writehtml(self,url, title, headers):
        try:
            # Fetch HTML content
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html = response.text
                # Write HTML content to file
                with open(title + ".txt", "w", errors="ignore", encoding="utf-8") as fp:
                    fp.write(html)
                print(f"HTML content from {url} \n written to {title + ".txt"}")
                return html
            else:
                print(f"Failed to fetch HTML from {url}.\n Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while writing HTML from {url} \n to {title}: {e}")

    # Input: string
    # ourput: string
    # Use: read and return the content of a file named input
    def readhtml(self,title):
        with open(title, "r", encoding="utf-8") as fp:
            content = fp.read()
        return content

    # Input: string of title, dictionary of information, list of keys
    # Output: None
    # Use: append the information to a csv named of string of title
    def append_csv(self,title, information, keys):
        with open(title, "a", encoding="utf_8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=keys)
            writer.writerows(information)

    def datamining(self,html):
        all_information = []
        all_ingredients = []
        item = self.searchmultiple("<tr><td", "Total</td></tr>", html)

        for i in range(0, len(item)):
            information = {}
            name = self.searchsingle('class="dmow1" colspan="3">', '</td></tr>', item[i])
            try:
                application = self.searchsingle('<tr><td class="dmow3" colspan="3">Application: ', '</td></tr>', item[i])
            except:
                application = ""
            try:
                description = self.searchsingle('<tr><td class="dmow2" colspan="3">', '</td></tr>', item[i])
                if "href" in description:
                    description = self.searchsingle('">', "</a>", description)
            except:
                description = ""
            line = self.searchmultiple("<tr>", "", item[i])
            for j in line:
                if "</tr>" not in j:
                    total = self.searchsingle('<td class="dmow5">', '</td>', j)
            information["id"] = i
            information["name"] = name
            information["application"] = application
            information["description"] = description
            information["total"] = total
            all_information.append(information)

        for i in range(0, len(item)):
            ing = self.searchmultiple('<tr><td class="dmow5">', '</td></tr>', item[i])
            for j in range(0, len(ing)):
                ingredients = {}
                try:
                    website = self.searchsingle('<a href="', '">', ing[j])
                except:
                    website = ""
                percentage = self.searchsingle('', '</td>', ing[j])
                content = self.searchsingle('colspan="2">', '', ing[j])
                if "<sup>" in content:
                    content = content.replace("<sup>&reg;</sup>", "")
                if "href" in content:
                    content = self.searchsingle('.html">', "</a>", content)
                if "dmow9" in content:
                    content = self.searchsingle('"dmow9">', '</span>', content)
                ingredients["id"] = i
                ingredients["ingredients"] = content
                ingredients["percentage"] = percentage
                ingredients["website"] = website
                ingredients["total"] = all_information[i]["total"]
                try:
                    ingredients["100 pct"] = round(
                        float(ingredients["percentage"]) / float(ingredients["total"]) * 100, 2)
                except:
                    pass
                all_ingredients.append(ingredients)
        return all_information, all_ingredients

    def scrape(self):
        headers = {"User-Agent": self.headers}
        url = self.url
        title = self.title
        self.writehtml(self.url, "sourcecode", self.headers)
        html = self.readhtml("sourcecode.txt")
        all_information, all_ingredients = self.datamining(html)
        print(all_information, all_ingredients)
        key = ["id", 'name', 'application', 'description', 'total']
        ingkey = ['id', 'ingredients', 'percentage', '100 pct', 'website', 'total']
        with open(self.title + "Information.csv", "w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=key)
            writer.writeheader()
        with open(self.title + "Ingredients.csv", "w", encoding="utf-8", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=ingkey)
            writer.writeheader()
        self.append_csv(self.title + "Information.csv", all_information, key)
        self.append_csv(self.title + "Ingredients.csv", all_ingredients, ingkey)
