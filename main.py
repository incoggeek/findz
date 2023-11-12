import requests,json,time,validators
from art import tprint,text2art

#Tool Banner
def tprint(text):
    t = text2art(text)
    print(t)

def get_valid_url():
    while True:
        url = input("URL: ")
        if validators.url(url):
            return url
        else:
            print("Invalid URL. Please enter a valid URL.")

def connection_request(url):
    try:
        headers = {
            'API-Key': 'USE_YOUR_API_KEY',
            'Content-Type': 'application/json'
        }

        data = {"url": url, "visibility": "public"}

        response = requests.post('https://urlscan.io/api/v1/scan/',
                                 headers=headers,
                                 data=json.dumps(data))
        
    except requests.exceptions.RequestException as e:
        print(f"Error during establishing connection")
        return None

    return response

def crawl_website(api_link):
    countdown = 15

    while countdown > 0:
        print(f"\rCRAWLING {url} ", end="", flush=True)
        time.sleep(1)
        countdown -= 1

    api_result = requests.get(api_link)
    return api_result

def print_links(links):
    try:
        if len(links) > 0:
            print("\n----LINKS FOUND ON WEBSITE---\n")
            for link in links:
                href_value = link.get("href", "Unknown Href")
                print(f'-> {href_value}')

    except (TypeError, KeyError) as e:
        print(f"Key or Type error while accessing links")

def print_website_tech(meta_att):
    print("\n---WEBSITE BUILT WITH---\n")

    try:
        processors_data = meta_att.get('processors', {}).get('wappa', {}).get('data', [])

        for item in processors_data:
            app_name = item.get('app', 'Error encountered while retriving data')
            print(app_name)

    except (KeyError, TypeError):
        print("Error: Key not found in response!")


def print_website_details(page_att):
    print("\n---WEBSITE DETAILS---\n")

    keys_to_print = ['domain', 'server', 'ip', 'asn', 'asnname']

    for key in keys_to_print:
        value = page_att.get(key, f"Unknown {key.capitalize()}")
        print(f"{key.capitalize()}: {value}")


if __name__ == "__main__":
    tprint('FINDZ')
    print('\tv1.0')
    print('\tBy incoggeek')

    url = get_valid_url()

    requests_data = connection_request(url)

    # Check if the request was successful
    if requests_data and requests_data.status_code == 200:
        # Parse the JSON response
        response_data = requests_data.json()

        # Access a specific key within the response JSON
        if 'api' in response_data:
            api_link = response_data['api']
            api_result = crawl_website(api_link)

            # Fetching links on the website
            if api_result.status_code == 200:
                data_att = api_result.json()['data']
                print_links(data_att['links'])

                # Fetching technology the website is built with
                meta_att = api_result.json()['meta']
                print_website_tech(meta_att)

                # Fetching server details
                page_att = api_result.json()['page']
                print_website_details(page_att)

            else:
                print('Request was not successful')

    else:
        print('Something went wrong!')