# %% [markdown]
# Use Cookie for Automatic Login

# %% [markdown]
# # Website: fctables.com
# # Verify whether login was successful: 1) e.g., vote for team Wolfsburg; 2) use the cookies received during log in to access https://www.fctables.com/tipster/my_bets/Links to an external site; 3) check whether user name and/or the word “Wolfsburg” appears on the page.  

# %%
from bs4 import BeautifulSoup
import requests
import time
import re

# %%
def main():
    
    ### Go to login page
    URL1 = "https://www.fctables.com/user/login/"

    session_requests = requests.session()

    time.sleep(5)

    res = session_requests.post(URL1, data = {"login_username" : "### insert user name",
                                            "login_password" : "### insert user password",
                                            "user_remeber" : "1",
                                            "login_action" : "1"},
                                    headers = dict(referer = "https://www.fctables.com/"),
                                    timeout = 15)

    cookies = session_requests.cookies.get_dict()

    ### Use cookie to login
    URL2 = 'https://www.fctables.com/tipster/my_bets/'
    page2 = session_requests.get(URL2, cookies=cookies)
            
    doc2 = BeautifulSoup(page2.content, 'html.parser')

    ### Print my cookie to screen
    print('My cookie:', cookies)

    ### Check if username is present
    print(bool(doc2.findAll(text = "JessicaChen"))) 

    ### Check if the bet I made is present
    print(bool(re.findall(r'\bWolfsburg\b', doc2.prettify())))
    print(bool(doc2.text.find("Wolfsburg"))) 

    ### print the page to screen
    print(doc2.prettify())

if __name__ == '__main__':
    main()


