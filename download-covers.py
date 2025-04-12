import os
import requests
import json
import shutil
import filenames

token = os.environ.get('TOKEN')
artistId = os.environ.get('ARTIST_ID')

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def download_file(url: str, targetFileName: str):

    print(f"Downloading image from {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:

        fileLocation = f"covers/{targetFileName}.jpg"
        print(f"Saving image to {fileLocation}")
        with open(fileLocation, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)  

def get_artist_albums(artistId: str):
    url = f"https://api.spotify.com/v1/artists/{artistId}/albums"
    headers = {"Authorization": f"Bearer {token}"}

    # Get first page
    response = requests.get(url, headers=headers)
    print(response)
    print(response.text)

    responseJson = response.json()
    albums = responseJson["items"]

    # Get all remaining pages
    nextPageUrl = responseJson["next"]
    while nextPageUrl != None:
        responseJson = requests.get(nextPageUrl, headers=headers).json()
        albums = albums + responseJson["items"]

        nextPageUrl = responseJson["next"]

    return albums

def filter_for_relevant_albums(albums: list):
    excludedName = [
        "Super-Papagei 2004",
        "Der 5. Advent"
    ]

    return [album for album in albums if has_numbers(album["name"]) and album["name"] not in excludedName]


def normalize_album_name(albumName: str):
    normalizedAlbumName = filenames.slugify(albumName)
    normalizedAlbumName = normalizedAlbumName.replace('folge-', '')
    return normalizedAlbumName

def main():
    print(f"Using token {token}")
    print(f"Using artist ID {artistId}")

    albums = get_artist_albums(artistId)
    print(f"Loaded {len(albums)} albums")

    episodes = filter_for_relevant_albums(albums)
    print(f"Filtered to {len(episodes)} episodes")

    for episode in episodes:
        url = episode["images"][0]["url"]

        fileName = normalize_album_name(episode["name"])

        print(f'Downloading cover for "{fileName}" from "{url}"')
        download_file(url, fileName)

if __name__ == "__main__":
    main()



# sampleAlbum = albums[0]
# imageUrl = sampleAlbum["images"][0]["url"]
# download_file(imageUrl, "image.jpg")
