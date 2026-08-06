import json
import traceback
import sys
from typing import Any

import requests
from PIL import Image


def main():
    image_urls: list[str] = []
    with open("image_urls.txt", "r") as fp:
        image_urls = fp.readlines()

    catalogue: list[dict[str, Any]] = []

    i = 0
    for image_url in image_urls:
        i += 1
        print(f"Processing image {i}/{len(image_urls)}...")

        print(f"    GET {image_url[:-1]} ...", end=" ")
        sys.stdout.flush()
        try:
            r = requests.get(image_url[:-1])
            print(r.status_code)
        except requests.RequestException:
            print("error!\n")
            traceback.print_exc()
            return

        try:
            print(
                f'    Image Content-Type is "{r.headers["Content-Type"]}" ...', end=" "
            )
            sys.stdout.flush()
        except KeyError:
            print(f"    Failed to extract Content-Type for some reason, skipping!")
            continue

        if r.headers["Content-Type"] == "image/png":
            print("OK")
        else:
            print("skipping")
            continue

        print("    Saving image to temporary file ...", end=" ")
        sys.stdout.flush()
        try:
            with open("temp.png", "wb") as fp:
                fp.write(r.content)
            print(f"OK ({len(r.content)} bytes)")
        except Exception:
            print("error!\n")
            traceback.print_exc()
            return

        print("    Opening PNG with Pillow ...", end=" ")
        sys.stdout.flush()
        try:
            img = Image.open("temp.png")
            print("OK")
        except Exception:
            print("error!\n")
            traceback.print_exc()
            return

        print("    Checking image size ...", end=" ")
        sys.stdout.flush()
        if img.size[0] > 1280 or img.size[1] > 1280:
            print(f"too large! ({img.size[0]}x{img.size[1]})\n    Downsizing image...")

            if img.size[0] > img.size[1]:
                larger_axis = 0
            else:
                larger_axis = 1
            print(f"        Larger axis is {"X" if larger_axis == 0 else "Y"}")

            downsize_multi = 1280 / img.size[larger_axis]
            new_size = (
                int(img.size[0] * downsize_multi),
                int(img.size[1] * downsize_multi),
            )

            print(
                f"        New resolution is {new_size[0]}x{new_size[1]} (downsize mutliplier {downsize_multi})"
            )

            print("        Resizing image ...", end=" ")
            sys.stdout.flush()
            img = img.resize(new_size, resample=Image.Resampling.BILINEAR)
            print("done")
        else:
            print(f"OK ({img.size[0]}x{img.size[1]})")

        print(f'    Saving image as "{image_url.split("/")[-1][:-1]}" ...', end=" ")
        sys.stdout.flush()
        try:
            img.save(image_url.split("/")[-1][:-1])
            print("OK")
        except Exception:
            print("error!\n")
            traceback.print_exc()
            return

        print("    Creating catalogue entry...")

        tags: list[str] = []
        if "konqi" in image_url.lower():
            tags.append("konqi")
        if "katie" in image_url.lower():
            tags.append("katie")
        if "kori" in image_url.lower():
            tags.append("kori")

        if not tags:
            tags.append("other")

        print(f"        Image tags: {tags}")

        catalogue.append(
            {"file": image_url.split("/")[-1][:-1], "url": image_url[:-1], "tags": tags}
        )

        print()

    print("Processed all images!")
    print('Saving catalogue as "catalogue.json" ... ', end=" ")
    sys.stdout.flush()
    try:
        with open("catalogue.json", "w") as fp:
            json.dump(catalogue, fp, indent=True)
    except Exception:
        print("error!\n")
        traceback.print_exc()
        return

    print(f"\nAll done, yippity yippie! :3")


if __name__ == "__main__":
    main()
