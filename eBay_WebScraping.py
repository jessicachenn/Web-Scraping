# %% [markdown]
# Compute fraction of Amazon gift cards on eBay that sells above face value:

# %%
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm as tqdm
import requests
import time
import re

# %%
def main():

    header = {"user-agent": "Mozilla/5.0"}

    url  = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1&_pgn='
    url_01 = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1'

    def saveString(html, filename="text.html"):
            try:
                file = open(filename,"w")
                file.write(str(html))
                file.close()
            except Exception as ex:
                print('Error: ' + str(ex))

    def loadString(f="test.html"):
            try:
                html = open(f, "r", encoding='utf-8').read()
                return(html)
            except Exception as ex:
                print('Error: ' + str(ex))

                

    ### Save the search result page as amazon_gift_card_01.html file

    page_01 = requests.get(url_01, headers = header)
    soup_01 = BeautifulSoup(page_01.text, "html.parser")
    saveString(soup_01.prettify(), f'amazon_gift_card_01.html')



    ### Save the first ten pages of the search result as html files
    
    links = []
    for i in range(1,11):
        page = url + str(i)
        links.append(page) ### add page numbers to the url

    for i,url in enumerate(links):
        page = requests.get(url, headers = header)
        soup = BeautifulSoup(page.text, "html.parser")
        saveString(soup.prettify(), f'amazon_gift_card_{i+1}.html')
        time.sleep(10)
    


    ### Identify and print to screen the title, price, and shipping price of each item
    # Product titles and face values

    t = []
    face_value = []

    def replace_empty_lists(lst):
        return [([0] if not inner else inner) 
                for inner in lst]

    for i,book in enumerate(links):
        soup = loadString(f'amazon_gift_card_{i+1}.html')
        soup = BeautifulSoup(soup, "html.parser")
        titles = soup.find_all('div', class_='s-item__title')
        titles = titles[1:]
        for item in titles:
            title = item.text.replace("New Listing", "").strip()
            t.append(title)
            fv = re.findall(r'([\$|][0-9]{1,})', title) ### find face value
            fv = [x.replace("$", "") for x in fv] ###remove dollar signs
            face_value.append(fv)
    face_value = replace_empty_lists(face_value) ### replace empty lists with zeros

    final_fv = []
    for i in face_value:
        if len(i) > 1:
            max_fv = max(i) ### find the maximum face values values 
        else:
            max_fv = i
        final_fv.append(max_fv)


    final_fv = [float(x) if isinstance(x, str) else [float(y) for y in x] for x in final_fv]
    final_fv = [[x] if not isinstance(x, list) else x for x in final_fv]



    # Price

    p1 = []
    product_price = []

    for i,book in enumerate(links):
        soup = loadString(f'amazon_gift_card_{i+1}.html')
        soup = BeautifulSoup(soup, "html.parser")
        prices = soup.find_all('span', class_ = 's-item__price')
        prices = prices[1:]
        for item in prices:
            price = item.select_one('span.POSITIVE').text.strip()
            p1.append(price)
            price_ = [float(x) for x in re.findall(r'([0-9.]+)', price)]### find price
            product_price.append(price_)



    # Shipping price

    p2 = []
    shipping_price = []

    def replace_empty_lists(lst):
        return [([0] if not inner else inner) 
                for inner in lst]

    for i,book in enumerate(links):
        soup = loadString(f'amazon_gift_card_{i+1}.html')
        soup = BeautifulSoup(soup, "html.parser")
        shipping = soup.find_all('span', class_ = 's-item__shipping s-item__logisticsCost')
        for item in shipping:
            shipping = item.text.strip()
            p2.append(shipping)
            shipping_ = [float(x) for x in re.findall(r'([0-9.]+)', shipping)] ### find shipping price
            shipping_price.append(shipping_)
    shipping_price = replace_empty_lists(shipping_price) ### replace empty lists with zeros



    ### Print the title, price, and shipping price of each item to screen

    for i, (l1, l2, l3) in enumerate(zip(t, p1, p2)):
        print(f'{i + 1}. {l1}, {l2}, {l3}')


    
    ### Determine if a gift card sells above face value (face value > combined cost of product price and shipping price)

    total_cost = []

    for A, B in zip(product_price, shipping_price):
        cost = []
        for a, b in zip(A, B):
            cost.append(a + b)
        total_cost.append(cost)

    above_face_value = 0
    below_face_value = 0
    error = 0

    print('\n')
    print("Gift cards that were sold above face value:")

    for A, B, C in zip(final_fv, total_cost, t):
        if 0.0 not in A:
            for a, b, c in zip(A, B, C):
                if a > b:
                    above_face_value += 1
                    print(C)
                else:
                    below_face_value += 1
        else:
            error += 1

    print('\n')
    print('Number of giftcards that are sold above face value:', above_face_value)
    print('Number of giftcards that are sold at or below face value:', below_face_value)

    ### IMPORTANT NOTE:
    ### the total number of giftcards here only includes the ones from which we were able to extract the face values
    ### some numbers extracted may have been errors due to imperfect regex statement

    ### Calculate approximate error and accuracy
    approx_error = 1 - error / (above_face_value + below_face_value)
    fraction = above_face_value / (above_face_value + below_face_value)
    print('The accuracy of extracting face value from product titles is approximate:', round(approx_error, 2))
    print('The fraction of Amazon gift cards sold above face value:', round(fraction, 2))

    print('\n')
    print('We can speculate that many people may have received free giftcards from others and do not intend to use the giftcards themselves. For those people, selling the giftcards at a price lower than the face value is a still a net monetary gain.')

if __name__ == '__main__':
    main()

# %%
def main():
    URL1 = "https://www.fctables.com/user/login/"

    session_requests = requests.session()

    time.sleep(5)

    res = session_requests.post(URL1, data = {"login_username" : "JessicaChen",
                                            "login_password" : "1234567890",
                                            "user_remeber" : "1",
                                            "login_action" : "1"},
                                    headers = dict(referer = "https://www.fctables.com/"),
                                    timeout = 15)

    cookies = session_requests.cookies.get_dict()

    URL2 = 'https://www.fctables.com/tipster/my_bets/'
    page2 = session_requests.get(URL2, cookies=cookies)
            
    doc2 = BeautifulSoup(page2.content, 'html.parser')

    print('My cookie:', cookies)
    print(bool(doc2.findAll(text = "JessicaChen"))) 
    print(bool(re.findall(r'\bWolfsburg\b', doc2.prettify())))
    print(bool(doc2.text.find("Wolfsburg"))) 
    print(doc2.prettify())


if __name__ == '__main__':
    main()


