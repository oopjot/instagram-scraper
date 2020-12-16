from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from uuid import uuid4
import time
import json

path = "path do chromedrivera"
login = "login do insta"
password = "haslo do insta"
post_counter = 5 # nie wiem czy wiecej niz 10-12 smignie 

user = input("Username: ")

driver = webdriver.Chrome(path)
driver.get(f"http://www.instagram.com/{user}/")
time.sleep(2)

cookies_element = driver.find_element_by_class_name("aOOlW.bIiDR")
cookies_element.click()

userData = {}

#username
username_element = driver.find_element_by_class_name("_7UhW9.fKFbl.yUEEX.KV-D4.fDxYl")
userData["userName"] = username_element.text

#profile picture
profile_pic_element = driver.find_element_by_class_name("_6q-tv")
userData["profilePicture"] = profile_pic_element.get_attribute("src")

#posts followers following
posts_number_element = driver.find_elements_by_class_name("g47SY")
counter = 0
for element in posts_number_element:
    if counter == 0:
        userData["posts"] = int(element.text.replace(",", "").replace("m", "00000").replace(".", "").replace("k", "000"))
    if counter == 1:
        userData["followers"] = int(element.text.replace(",", "").replace("m", "00000").replace(".", "").replace("k", "000"))
    if counter == 2:
        userData["following"] = int(element.text.replace(",", "").replace("m", "00000").replace(".", "").replace("k", "000"))
    counter += 1

#name
try:
    name_element = driver.find_element_by_class_name("rhpdm")
    userData["name"] = name_element.text
except:
    userData["name"] = ""

#bio
try: 
    bio_element = driver.find_element_by_xpath("//div[@class='-vDIg']/span")
    userData["bio"] = bio_element.text
except:
    userData["bio"] = ""

#website
try: 
    website_element = driver.find_element_by_class_name("yLUwa")
    userData["website"] = website_element.text
except:
    userData["website"] = ""

#user posts

    #logging in
post_boxes = driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")
post_boxes[0].click()
login_boxes = driver.find_elements_by_class_name("_2hvTZ.pexuQ.zyHYP")
login_boxes[0].send_keys(login)
login_boxes[1].send_keys(password)
login_boxes[1].send_keys(Keys.ENTER)
time.sleep(3)

driver.find_element_by_class_name("cmbtv").click()
time.sleep(1)

    #iterating posts
post_boxes = driver.find_elements_by_class_name("v1Nh3.kIKUG._bz0w")
user_posts = []
for box in post_boxes:
    post = {}
    box.click()
    post["_uid"] = str(uuid4())
    post["user"] = {
        "username": user,
        "profilepicture": userData["profilePicture"]
    }
    time.sleep(2)
    try:
        post["uri"] = driver.find_element_by_class_name("_97aPb").find_element_by_xpath(".//video").get_attribute("poster")
    except:
        post["uri"] = driver.find_element_by_class_name("_97aPb").find_element_by_xpath(".//img").get_attribute("src")

    post["miniatureUri"] = post["uri"]
    post_comments = driver.find_elements_by_class_name("C7I1f")
    print(post_comments)
    if post_comments:
        post["description"] = post_comments[0].find_elements_by_xpath(".//span")[-1].text
        post["comments"] = []
        if len(post_comments) > 1:
            for comment in post_comments[1:]:
                newComment = {}
                newComment["addedBy"] = comment.find_elements_by_xpath(".//span")[0].text
                newComment["profilePicture"] = comment.find_element_by_xpath(".//img").get_attribute("src")
                newComment["comment"] = comment.find_elements_by_xpath(".//span")[-1].text
                post["comments"].append(newComment)
        else:
            post["comments"] = []
    else:
        post["comments"] = []
        post["description"] = ""
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    user_posts.append(post)
    post_counter -= 1
    if post_counter == 0:
        break

userData["userPosts"] = user_posts

time.sleep(1)
driver.close()

with open(f"data/{user}.json", "w") as file:
    json.dump(userData, file, indent=4, ensure_ascii=False)