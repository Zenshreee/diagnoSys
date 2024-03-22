import requests


def download(url):
    """
    Download data from the given URL.
    """

    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None


def save_file(name, content):
    """
    Save the file to the local directory.
    """
    with open("../data" + name, "wb") as file:
        file.write(content)
    return None


def main():
    """
    Download and save the data from the given URL.
    """
    n = 20
    a = "https://api.fda.gov/download.json"
    response = requests.get(a)
    data = response.json()["results"]["drug"]["event"]["partitions"]
    i = 0
    while i < n:
        url = data[i]["file"]
        size = float(data[i]["size_mb"])
        records = data[i]["records"]
        if size >= 130 or records != 12000:
            i += 1
            n += 1
        else:
            content = download(url)
            if content:
                save_file(f"{i}.json.zip", content)
                print(f"Downloaded {i}.json.zip")
            else:
                print("Failed to download data")
            i += 1


if __name__ == "__main__":
    main()
