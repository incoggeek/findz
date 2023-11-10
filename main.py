import requests, json,time

domain = input("URL: ")

headers = {'API-Key':'ff07f9c4-f296-4104-8264-47f0a8504e41',
        'Content-Type':'application/json'}
data = {"url": domain, 
        "visibility": "public"}
response = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, 
        data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:  
    # Parse the JSON response
    response_data = response.json()

    # Access a specific key within the response JSON
    # For example, if 'task' is a key in the response:
    if 'api' in response_data:
        api_link = response_data['api']

     # Delay in request to load
        countdown = 15

        while countdown > 0:
                print(f"\rCRAWLING {domain} ", end="", flush=True)
                time.sleep(1)
                countdown -= 1

     # Fetch the result using the 'api' link
        api_result = requests.get(api_link)
        

        # Feching links on website
        if api_result.status_code == 200:
            # Access the content of the response
            data_att = api_result.json()['data']

            if  0 < len(data_att['links']):
                
                print("\n----LINKS FOUND ON WEBSITE---\n")
                for i in data_att['links']:
                        print(f'-> {i['href']}')

        # Fetching tech the website built with
        meta_att = api_result.json()['meta']
        print("\n---WEBSITE BUILT WITH---\n")
        for i in meta_att['processors']['wappa']['data']:
             print(i['app'])

        # Fetching server details
        page_att = api_result.json()['page']
        print("\n---WEBSITE DETAILS---\n")
        print(page_att['domain'])
        print(page_att['server'])
        print(page_att['ip'])
        print(page_att['asn'])
        print(page_att['asnname'])

    else:
        print("Key 'api' not found in the response.")
else:
    print("Request was not successful. Status code:", response.status_code)