import getpass
import requests
from bs4 import BeautifulSoup
import os
import pdfkit

""""
Converts each pages into a pdf document
"""
def pdf_convert(url, directory):

   
    file_name = url.split('/')[-2] + ".pdf"

    file_path = os.path.join(directory, file_name)
   
           # Check if the file already exists
    if os.path.exists(file_path):
        print(f'Skipped {file_name} - File already exists')
        return
    
    # 1. Retrieve the HTML content of the web page
    response = requests.get(url)
    html_content = response.content

    # 2. Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # 3. Optional: Perform modifications on the HTML content if needed
    # For example, you can remove certain unwanted elements or make layout modifications

    # 4. Save the modified HTML content to a temporary file
    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

 

    try:
        pdfkit.from_file(temp_html_file, file_path)
    except:
        print()
    # 6. Remove the temporary HTML file
    os.remove(temp_html_file)

    print('Download completed. The PDF file has been saved as', file_name)


""""
Downloads audio file
"""

def download_audio(file_url, directory):

    file_name = file_url.split('/')[-1]
    file_path = os.path.join(directory, file_name)

        # Check if the file already exists
    if os.path.exists(file_path):
        print(f'Skipped {file_name} - File already exists')
        return


    try:
        with open(file_path, 'wb') as file:
                print(f"Downloading {file_name}....")
                response = requests.get(file_url)
                file.write(response.content)
                
                print(f'{file_name} downloaded')
    except:
        print("Somethings went wrong. File not downloaded")



def main():
    while True:
        print("Press q to exit")
        book = input("Enter the book you want to download (jude or 1-samuel): ")

        if book.lower() == 'q':
            break
        current_user = getpass.getuser() #get current user


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

                        page_name = page_audio.split('/')[-2]



                        #Open the web page of each emission
                        linked_response = requests.get(page_audio)
                        linked_soup = BeautifulSoup(linked_response.content, 'html.parser')

                        # Find all <a> tags with an href attribute that ends with ".mp3"
                        mp3_links = linked_soup.find_all('source', src=lambda src: src.endswith('.mp3'))

                        file_url = mp3_links[0]["src"]

                        directory = f'C:\\Users\\{current_user}\\Downloads\\audio_files\\{book}\\{page_name}'
                        # Create a directory to store the downloaded files
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        

                        download_audio(file_url, directory) # Downloads the audio file
                        pdf_convert(page_audio, directory)  # Downloads pdf file

                        
            except:
                print("Page could not be loaded...") 

if __name__ == "__main__":
    main()