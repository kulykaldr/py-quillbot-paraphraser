#!/usr/bin/env python3
"""
Author: Anubhav
Date: 29.01.2020
The program will take a processed textfile as input, the file should have every sentence in a new line
Login info to get cookies:
Url: https://quillbot.com/
Email: prinusam.roy.9e@819760.com
Password: password
"""
import os.path
from json import loads
from urllib.parse import quote
import requests

API_URL = "https://rest.quillbot.com/api/paraphraser/single-paraphrase/2"
PARAMS = "?text={}&strength={}&autoflip={}&wikify={}&fthresh={}&inputLang={}&quoteIndex={}"


def setup_session():
    """Update headers for the session.
    Returns
    -------
    obj
        Requests Session
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Content-Type": "application/json, text/plain, */*"
        }
    )
    return session


def get_parameterized_url(text):
    """Gets parametrized url
    Parameters
    ----------
    text : str
    Returns
    -------
    url: str
        string containing url and quoted text
    """
    url_encoded_text = quote(text)
    autoflip = "false"
    fthresh = "9"
    strength = "3"
    wikify = "true"
    lang = "en"
    quote_input = "-1"
    url = API_URL + PARAMS.format(url_encoded_text, strength, autoflip, wikify, fthresh, lang, quote_input)
    return url


def paraphrasor(url, session):
    """Gets paraphrased text
    Parameters
    ----------
    url : str
        Complete url containing text
    session : class `requests.sessions.Session`
            Requests session.
            Provides cookie persistence, connection-pooling, and configuration.
    """
    # Cookies are configurable
    cookies = {
        # "qdid": "=279d869d-08d9-4317-949c-3f98540a0c69;",
        # "__stripe_mid": "25200b8f-357a-4c3a-8340-bbe628ff9c8e197af5;",
        "connect.sid": "s%3AEE4l96RBHFiDdoomkiDLm_vvs6OtgfJY.teYmuX6PR2W2gGZcG6X%2B5race6%2Bg3mkHcm13qcg%2BVeo;",
        # "__stripe_sid": "69bd89f6-53bc-4295-9086-a5ed42d0eb9613d28b"
    }

    req = session.get(url, cookies=cookies)
    if req.status_code == 200:
        json_text = loads(req.text)
        end = "\n\n"
        json_text = json_text['data']

        json_text = json_text[0] if len(json_text) == 1 else json_text
        print(f"\nData Sent: {json_text['sent']}", end)

        paras = [key for key in json_text if key.startswith("paras")]
        texts = list(
            {text.get("alt") for para in paras for text in json_text[para]}
        )

        return texts


def main():
    """main function the program starts
    """
    print("Quillbot Paraphrasing Tool")
    # line = input("Enter the text: ")
    line = "You can find all information about the services you are using with us here, as well as all payment details."

    session = setup_session()
    if len(line) > 700:
        print("line should be less than 700 characters, %s" % line)
    else:
        url = get_parameterized_url(line)
        texts = paraphrasor(url, session)
        print(texts)


if __name__ == "__main__":
    main()
