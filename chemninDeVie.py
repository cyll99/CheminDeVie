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
    print(containers)
    for container in containers:
        link = container.find_all('a')
        # print(link)
        page_audio = link[0]["href"]

        #Open the web page of each emission
        linked_response = requests.get(page_audio)
        linked_soup = BeautifulSoup(linked_response.content, 'html.parser')

        # Find all <a> tags with an href attribute that ends with ".mp3"
        mp3_links = linked_soup.find_all('source', src=lambda src: src.endswith('.mp3'))

        # Create a directory to store the downloaded files
        if not os.path.exists('audio_files'):
            os.makedirs('audio_files')


        file_url = mp3_links[0]["src"]
        file_name = file_url.split('/')[-1]
        file_path = os.path.join('C:\\Users\\Mydleyka\\Documents\\sideProjects\\deuteronome', file_name)

        try:
            with open(file_path, 'wb') as file:
                    response = requests.get(file_url)
                    print(file_url)
                    file.write(response.content)
                    
                    print(f'{file_name} downloaded')
        except:
            print("Somethings went wrong")
