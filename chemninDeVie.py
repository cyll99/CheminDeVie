import requests
from bs4 import BeautifulSoup
import os

# url = 'https://www.cheminsdevie.info/livre/deuteronome/'

for i in range(1, 2):
    url = 'https://www.cheminsdevie.info/livre/deuteronome/page/' + str(i) + '/'


    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the webpage using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
  
    # Find the container of every emission
    containers = soup.find_all("div", {"class" : "liste-emissions"})
    for container in containers:
        link = container.find_all('a')
        # print(link)
        page_audio = link[0]["href"]

        print("page audio: ", page_audio)

        #Open the web page of each emission
        linked_response = requests.get(page_audio)
        linked_soup = BeautifulSoup(linked_response.content, 'html.parser')

        # Find all <a> tags with an href attribute that ends with ".mp3"
        mp3_links = linked_soup.find_all('source', src=lambda src: src.endswith('.mp3'))

        directory = 'audio_files\\deuteronome'
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
            with open(file_path, 'wb') as file:
                    print(f"Downloadind {file_name}....")
                    response = requests.get(file_url)
                    file.write(response.content)
                    
                    print(f'{file_name} downloaded')
        except:
            print("Somethings went wrong. File not downloaded")
