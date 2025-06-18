import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = input('[+] Movie Name : ')
url = f"https://app.arabypros.com/api/search/{s}/0/4F5A9C3D9A86FA54EACEDDD635185/d506abfd-9fe2-4b71-b979-feff21bcad13/"
headers = {'User-Agent': "okhttp/4.8.0", 'Accept-Encoding': "gzip"}

try:
    res = requests.get(url, headers=headers, verify=False).json()
    for m in res['posters']:
        n = m['title']
        id = m['id']
        print(f'[+] [ Name : {n} ] [ ID : {id} ]')

    id = input('id : ')
    url = f"https://app.arabypros.com/api/movie/source/by/{id}/4F5A9C3D9A86FA54EACEDDD635185/d506abfd-9fe2-4b71-b979-feff21bcad13/"
    headers = {
        'User-Agent': "okhttp/4.8.0",
        'Accept-Encoding': "gzip",
        'if-modified-since': "Mon, 23 Dec 2024 21:42:48 GMT"
    }

    res2 = requests.get(url, headers=headers, verify=False).json()
    for l in res2:
        print(f"[+] [ Link : {l['url']} ]")  # Using double quotes for the f-string

except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
except KeyError as e:
    print(f"Error parsing response - missing key: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
