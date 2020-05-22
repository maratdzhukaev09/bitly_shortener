import requests, os, argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

def count_clicks(token, link):
    response_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    headers =  {'Authorization': f'Bearer {token}'}

    response = requests.get(response_url, headers=headers)
    response.raise_for_status() 

    clicks_count = response.json()['total_clicks']
  
    return clicks_count

def shorten_link(token, url):
    response_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers =  {'Authorization': f'Bearer {token}'}
    json = {'long_url': url}

    response = requests.post(response_url, headers=headers, json=json)
    response.raise_for_status() 

    link = response.json()['id']

    return link
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Count clicks on bitlinks'
    )
    parser.add_argument('url', help='Full url or bitlink')
    args = parser.parse_args()

    token = os.getenv('API_BITLY_TOKEN')
    url =  args.url
    url_error = f'Ошибка, ваша ссылка ({url}) неверна.'

    try:
        if url.startswith('http'):
            bitlink = shorten_link(token, url)
        else:
            bitlink = url
        clicks_count = count_clicks(token, bitlink)
    except requests.exceptions.HTTPError:
        bitlink = url_error
        count_clicks = url_error
    
    print('Битлинк:', bitlink)
    print('Количество кликов:', clicks_count)

