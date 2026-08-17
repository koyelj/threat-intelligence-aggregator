import requests


def download_feed(url):

    try:

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException as error:

        raise RuntimeError(
            f"Failed to download feed: {error}"
        ) from error