import re


def getQuoraUsername(profileUrl: str) -> str:
    if not profileUrl:
        return None
    try:
        result = re.match(
            r"(http://|https://|)(www.|)(quora.com/profile/|)([A-Za-z0-9\-]+)/?(.*)",
            profileUrl,
        )
        if result:
            result = result.group(4)
        return result
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    url = "https://www.quora.com/profile/Saurabh-Vishwakarma-228"
    print(getQuoraUsername(url))
