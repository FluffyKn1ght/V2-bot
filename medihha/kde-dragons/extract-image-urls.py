from typing import List

from bs4 import BeautifulSoup


def main():
    with open("wikipage.html", "r") as fp:
        wiki_page: str = fp.read()

    soup = BeautifulSoup(wiki_page, "lxml")

    gallery_boxes = soup.find_all("li", class_="gallerybox")

    thumb_urls: list[str] = []
    for gallery_box in gallery_boxes:
        img_element = gallery_box.find("div", class_="thumb").find("a", class_="mw-file-description").find("img")  # type: ignore
        thumb_urls.append(img_element["src"])  # type: ignore

    full_urls: list[str] = []
    for thumb_url in thumb_urls:
        split_url = thumb_url.replace("/thumb", "").split("/")[:-1]

        url = ""
        for chunk in split_url:
            url += chunk
            url += "/"

        full_urls.append(f"https://community.kde.org{url[:-1]}")

    with open("image_urls.txt", "w") as fp:
        for full_url in full_urls:
            fp.write("\n")
            fp.write(full_url)


if __name__ == "__main__":
    main()
