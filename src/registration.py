"""Register a face with the CodeProject.AI Server so it can be recognised later.

Usage:
    python registration.py <image_path> "<Person Name>"

Example:
    python registration.py photos/zong-han.jpg "Zong Han"
"""

import sys
import requests
from options import Options


def register_face(img_path, user_id):

    opts = Options()

    with open(img_path, "rb") as f:
        image_data = f.read()

    response = requests.post(opts.endpoint("vision/face/register"),
                             files={"image": image_data},
                             data={"userid": user_id}).json()

    print(f"Registration response: {response}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    register_face(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
