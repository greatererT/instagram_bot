from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import operator
from selenium.webdriver.common.action_chains import ActionChains


def getuserlist(filepath): #IMPORTANT fomrat must be all usernames seperated by a space and nothing else.
    try:
        file = open(filepath,'r')
        filetext=file.read()
        file.close()
        return filetext
    except:
        print("file not found. try again.")
        return getuserlist(input())
    
usernamelist = getuserlist(input("enter text file path: ")).split()


options = Options()
#IMPORTANT: enter the location of firefox in your computer here.
options.binary_location = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options=options)
driver2 = webdriver.Firefox(options=options)

class userinfo:
    def __init__(self, username, posts, followers, following, totallikes):
        self.Username = username
        self.Posts = posts
        self.Followers = followers
        self.Following = following
        self.Totallikes = totallikes



userslist = []


def getinfo(username): #returns an instance of the userinfo class. returns 0 if there is an error. 
    driver.get("https://www.instagram.com/"+username+"/")
    try:
        WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.CLASS_NAME ,"_ac2a"))
        info = driver.find_elements(By.CLASS_NAME, "_ac2a")
    except:
        print("error getting info of: "+username)
        return 0

    followers = info[1].text
    followers = followers.replace(",", "")
    followers = followers.replace(".", "")
    if followers.find("K") !=-1:
        followers = followers.replace("K", "")
        followers = int(followers)*1000
    elif followers.find("M")!=-1:
        followers = followers.replace("M", "")
        followers = int(followers)*1000000

    
    
    
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, "//div[contains(@class, '_aa8k')]/a[contains(@class, 'xe8uvvx')]"))
    posts = driver.find_elements(By.XPATH, "//div[contains(@class, '_aa8k')]/a[contains(@class, 'xe8uvvx')]")
    totallikes = 0
    for i in range(3):
        postlink = posts[i].get_attribute('href')
        driver2.get(postlink)
        WebDriverWait(driver2, 20).until(lambda d: d.find_element(By.XPATH,"//span[contains(text(), 'likes') and contains(@class, 'xeuugli') and @style='line-height: 18px;']"))
        cantfind = True
        while(cantfind):
            try:
                likes = driver2.find_element(By.XPATH,"//span[contains(text(), 'likes') and contains(@class, 'xeuugli') and @style='line-height: 18px;']").text
                cantfind = False
                totallikes += int(likes[:-6].replace(",",""))
            except:
                driver.implicitly_wait(1)

    return(userinfo(username, info[0].text, followers, info[2].text, totallikes))










currentuser = 0
for username in usernamelist:
    currentuser = getinfo(username)
    userslist.append(currentuser)

mode = input("information gathered. to sort by likes on posts, input 0. \n to sort by followers, input 1.")


while(True):

    if mode=="0":
        userslist = sorted(userslist, key=operator.attrgetter("Totallikes"))
        for user in userslist:
            print("username:"+user.Username + ", Likes:"+ str(user.Totallikes))
        break
    elif mode=="1":
        userslist = sorted(userslist, key=operator.attrgetter("Followers"))
        for user in userslist:
            print("username:"+user.Followers + ", Followers:"+ str(user.Followers))
        break
    else:
        input("incorrect input, try again.")
