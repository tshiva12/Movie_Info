from selenium import webdriver
import time, requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def movie():
    chromeOptions = webdriver.ChromeOptions()
    preferences = {"download.default_directory" : "G:\\MSIT\\1-1\\Movie info"}
    chromeOptions.add_experimental_option("prefs", preferences)
    chromedriver = "C:\\Program Files\\Chrome\\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
    # browser.maximize_window()

    # browser.get("https://en.wikipedia.org/wiki/List_of_Telugu_films_of_2020")
    # time.sleep(5)

    # Movie_list = ['Sarileru Neekevvaru', 'Ala Vaikunthapurramuloo', 'Disco Raja', 'World Famous Lover', 'Arjun Reddy']
    Movie_list = ['Interstellar_(film)', 'The_Prestige_(film)', 'Batman_Begins', 'The_Dark_Knight_(film)', 'The_Dark_Knight_Rises']    # for i in range(1, 6):
    #   m = browser.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' +str(i)+']/td[1]')
    #   Movie_list.append(m.text.replace("*", ""))
    # print(Movie_list)
    final_dic = {}
    image_list = []
    for each in Movie_list:
        each = each.replace(" ", "_")
        browser.get("https://en.wikipedia.org/wiki/"+each+"")
        time.sleep(1)
        src = browser.find_element_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[2]/td/a/img').get_attribute("src")
        # image_list.append(src)

        r = requests.get("https://en.wikipedia.org/wiki/"+each+"")
        soup = BeautifulSoup(r.text, "html.parser")
        soup.prettify()
        table = soup.findAll('table')[0]
        dic = {}
        count = 1
        # for tr in table.findAll("tr"):
        #   if count > 3:
        #       # print(tr.find("th").text)
        #       # print(tr.find("td").text)
        #       dic[tr.find("th").text] = tr.find("td").text.replace("\xa0"," ").replace("\n"," ")
        #   count  = count + 1
        # print(dic)
        # print("--------------------------------------------")
        # break
        dic['Movie Name'] = [each]
        for tr in table.findAll("tr"):
            if count > 3:
                # print(tr.find("th").text)
                # print(tr.find("td").text)
                lis = []
                inp = tr.find("td").text.replace("\xa0"," ").replace("\n"," ")
                if '[' in inp:
                    ind = inp.index("[")
                    lis.append(inp[:ind])
                else:
                    lis.append(inp)
                dic[tr.find("th").text] = lis
                # dic[tr.find("th").text] = tr.find("td").text.replace("\xa0"," ").replace("\n"," ").replace("<br />", " ").strip()
            count  = count + 1
        # print(dic)
        final_dic[src] = dic
        # print("=============================")
        print(final_dic)
        print("---------------------------------") 
    
    return render_template('result.html', result = final_dic)




if __name__ == '__main__':
    app.run(debug = True)