import argparse
import requests
import tarfile
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="data downloading")
    parser.add_argument('--dataset', choices=["yelp", "formality", "decipher", "caption", "all"], 
        default="decipher", help='dataset to use')

    args = parser.parse_args()

    if not os.path.exists("data"):
        os.makedirs("data")

    os.chdir("data")

    yelp_id = "1IxiyjuTc_syRaqoZg6enS5013NdVrvvg"
    decipher_id = "1O3sMoM1_RItTCFnSnr7Ac57OeqAy3JCZ"
    formality_id = "10btlMqGpBrShRMI5KrRrU-w2gAAWLVGK"
    caption_id = "1pwvsgNMsdgXRbkMrg-HawFycNKvfihqC"

    if args.dataset == "yelp":
        file_id = [yelp_id]
    elif args.dataset == "formality":
        file_id = [formality_id]
    elif args.dataset == "decipher":
        file_id = [decipher_id]
    elif args.dataset == "caption":
        file_id = [caption_id]
    else:
        file_id = [yelp_id, formality_id, decipher_id, caption_id]

    destination = "datasets.tar.gz"

    for file_id_e in file_id:
        download_file_from_google_drive(file_id_e, destination)  
        tar = tarfile.open(destination, "r:gz")
        tar.extractall()
        tar.close()
        os.remove(destination)

    os.chdir("../")

