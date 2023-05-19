import requests
from bs4 import BeautifulSoup
import os

import tqdm

book = input("Enter the book you want to download: ")

for i in range(1, 10):
    url = f'https://www.cheminsdevie.info/livre/{book}/page/' + str(i) + '/'


    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the webpage using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        # Find the container of every emission
        containers = soup.find_all("div", {"class" : "liste-emissions"})
        for container in containers:
            link = container.find_all('a')
            for page in link:
                page_audio = page["href"]


                #Open the web page of each emission
                linked_response = requests.get(page_audio)
                linked_soup = BeautifulSoup(linked_response.content, 'html.parser')

                # Find all <a> tags with an href attribute that ends with ".mp3"
                mp3_links = linked_soup.find_all('source', src=lambda src: src.endswith('.mp3'))

               
                directory = f'audio_files\\{book}'
                # Create a directory to store the downloaded files
                if not os.path.exists(directory):
                    os.makedirs(directory)


                file_url = mp3_links[0]["src"]

                file_name = file_url.split('/')[-1]
                file_path = os.path.join(directory, file_name)

                    # Check if the file already exists
                if os.path.exists(file_path):
                    print(f'Skipped {file_name} - File already exists')
                    continue


                try:
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 1024  # 1 KB
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, ncols=80)

                    with open(file_path, 'wb') as file:
                            print(f"Downloadind {file_name}....")
                            response = requests.get(file_url)
                            for data in response.iter_content(block_size):
                                progress_bar.update(len(data))
                                file.write(data)
                                file.write(response.content)
                            
                            print(f'{file_name} downloaded')
                except:
                    print("Somethings went wrong. File not downloaded")
    except:
        print("Page could not be loaded...")