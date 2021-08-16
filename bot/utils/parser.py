import re


def extract_links(text):
    pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return [i[0] for i in re.findall(pattern, text)]


def extract_quora_username(text):
    pattern = r"(http://|https://|)(www.|)(quora.com/profile/|)([A-Za-z0-9\-]+)/?(.*)"
    match = re.match(pattern, text)
    if match is None:
        return None
    else:
        return match.group(4)


def create_profile_link(username):
    return "https://www.quora.com/profile/" + username
