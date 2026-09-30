from urllib.parse import urlparse


def extract_features(url):

    parsed = urlparse(url)

    features = {
        "url_length": len(url),

        "has_https": int(parsed.scheme == "https"),

        "num_dots": url.count("."),

        "num_hyphens": url.count("-"),

        "num_slashes": url.count("/"),

        "num_digits": sum(c.isdigit() for c in url),

        "num_special_chars": sum(
            not c.isalnum() for c in url
        ),

        "num_subdomains": (
            max(
                0,
                len(parsed.hostname.split(".")) - 2
            )
            if parsed.hostname
            else 0
        )
    }

    return features


if __name__ == "__main__":

    url = "https://google.com"

    features = extract_features(url)

    print(features)
