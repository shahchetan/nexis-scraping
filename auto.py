from selenium import webdriver
import time, sys
import json,os

driver = None
win_handles = []

def reset():
    global win_handles
    win_handles = driver.window_handles
    if len(win_handles) == 2:
        driver.switch_to_window(win_handles[-1])
        driver.close()
    driver.switch_to_window(win_handles[0])
    driver.find_element_by_xpath('//*[@id="nexisnav_applicationmenu"]/ul/li[7]/button').click()
    time.sleep(10)
    win_handles = driver.window_handles
    # print(win_handles)
    driver.switch_to_window(win_handles[-1])
    time.sleep(5)
    iframe = driver.find_element_by_xpath("//iframe[@id='publicRecordsUrl']")
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//*[@href="FindAPerson.aspx"]').click()

def login():
    global win_handles
    username = driver.find_element_by_name("webId")
    password = driver.find_element_by_name("password")
    with open('config.json') as myfile:
        config_info = json.load(myfile)
    # print (config_info)
    user = config_info['username']
    passw = config_info['password']

    username.send_keys(user)
    password.send_keys(passw)

    driver.find_element_by_name("signin").click()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="nexisnav_applicationmenu"]/ul/li[7]/button').click()
    time.sleep(10)
    win_handles = driver.window_handles
    # print(win_handles)
    driver.switch_to_window(win_handles[-1])
    time.sleep(5)
    iframe = driver.find_element_by_xpath("//iframe[@id='publicRecordsUrl']")
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//*[@href="FindAPerson.aspx"]').click()


def fetch_html(id):

    lexid = driver.find_element_by_id("MainContent_Did")
    lexid.clear()
    lexid.send_keys(id)
    lexid.send_keys(u'\ue007')

    driver.find_element_by_xpath("//*[@id='MainContent_resultsViewLinks_fullListButton']").click()
    time.sleep(3)
    name = 'html/'+id+'.html'
    with open(name,'w+') as html_file:
        html_file.write(driver.page_source)

    driver.back()
    driver.back()
    driver.switch_to_window(win_handles[-1])
    time.sleep(3)
    iframe = driver.find_element_by_xpath("//iframe[@id='publicRecordsUrl']")
    driver.switch_to_frame(iframe)

def iterate(filename):
    with open(filename, 'r') as myfile:
        idlist = myfile.readlines()
    for id in idlist:
        try:
            fetch_html(id.strip())
        except Exception as e:
            print ("Error:",e," while downloading:", id.strip())
            with open('err.txt','a+') as errfile:
                errfile.write(id.strip()+"\n")
            reset()

def main(args):
    if len(args) == 2:
        global driver
        driver = webdriver.Chrome()
        driver.get('https://www.nexis.com')
        time.sleep(5)
        if not os.path.exists('html'):
            os.makedirs('html')
        login()
        iterate(args[1])
        driver.close()
    else:
        print ("Enter the file name containing lexis ids")

if __name__ == '__main__':
    main(sys.argv)
