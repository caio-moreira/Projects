import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import pandas as pd
import json


def get_social_media_search_html_list(name):
    """Returns a list containing the 3 Google search HTMLs,
    one for each social media website.

    We'll be using each one of those HTMLs to extract the URL
    for that person's social media pages.

    Parameters
    ----------
    name : str --
        Name of the person that we want to find social media presence.

    Returns
    -------
    list --
        List containing the HTMLs for each social media search.
    """

    name_for_url = name.replace(' ', '+')

    social_media = {
        'www.facebook.com': '',
        'www.instagram.com': ''
    }

    html_list = []

    for social in social_media:
        url = f'https://www.google.com/search?q={name_for_url}+{social}'

        html = requests.get(url)

        html_list.append(html)

    return html_list


def get_social_media_url(name, social_media_search_html_list):
    """Returns a list containing the all the social media URLs.

    Parameters
    ----------
    name : str --
        Name of the person that we want to find social media presence.

    social_media_search_html_list : list --
        List containing the HTMLs for each social media Google search.
        From each one of these this function extracts the social media URL
        from the respective HTML.

    Returns
    -------
    pandas.DataFrame --
        Single row DataFrame containing the URLs for each social media website.
    """

    social_media = {
        'pt-br.facebook.com': '',
        'www.instagram.com': ''
    }

    for social_media_html in social_media_search_html_list:
        bs = BeautifulSoup(social_media_html.text, 'html.parser')

        a_tags = bs.find_all('a')

        for item in a_tags:
            href = item.get('href')

            obj = re.search('https://', href)

            if obj is not None:
                full_url = href.replace('/url?q=', '')

                url = full_url.split('&')[0]
                url = url.split('%')[0]

                domain = urlparse(url)

                if domain.netloc in social_media.keys():
                    if (social_media[domain.netloc] == ''):
                        social_media.update({domain.netloc: url})
                        break

    social_media['Celebrity'] = name

    return pd.DataFrame(data=social_media, index=[0])


def get_facebook_followers(facebook_html):
    """Returns the number of followers that person has on Facebook.

    Parameters
    ----------
    facebook_html : requests.Response --
        HTML for the Facebook page.

    Returns
    -------
    int --
        Number of followers.
    """

    bs = BeautifulSoup(facebook_html.text, 'html.parser')

    # Here we simply get the value of the object that contains
    # 'pessoas estão seguindo isso' text, which is Brazilian Portuguese for
    # 'people are following this'. So, we get that text string from Facebook
    # that says 123.456.789 people are following this, isolate the number
    # and remove the dots, so that it can be converted into an integer.
    answer = bs.find(string=re.compile('pessoas estão seguindo isso'))

    return int(answer.split()[0].replace('.', ''))


def get_instagram_followers(instagram_html):
    """Returns the number of followers that person has on Instagram.

    Parameters
    ----------
    instagram_html : requests.Response --
        HTML for the Instagram page.

    Returns
    -------
    int --
        Number of followers.
    """

    bs = BeautifulSoup(instagram_html.text, 'html.parser')

    script_tags = bs.find_all('script')

    for tag in script_tags:
        tag_type = tag.get('type')

        if re.search('^window._sharedData = ', str(tag.string)):
            instagram_data = json.loads(tag.string.replace('window._sharedData = ', '').replace(';', ''))
            
            return instagram_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
