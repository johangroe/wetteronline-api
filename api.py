import requests
import json
import bs4
import typing



def location(location: str):
    """
    Requests the exact URL and any autosuggests for `location`.
    """
    return Location(location)


def weather(url: str):
    """
    Requests weather data for `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
    """
    return Weather(url)


class Location:
    def __repr__(self):
        return "<WetterOnline Location object>"

    def __init__(self, location: str):
        self.url = LocationUtils().url(location)
        self.autosuggests = LocationUtils().autosuggest(location)


class Weather:
    def __repr__(self):
        return "<WetterOnline Weather object>"

    def __init__(self, url: str):
        raw_html = requests.get(f"https://www.wetteronline.de/{url}", allow_redirects = False).text
        self.debug_raw_html = raw_html
        self.temperature_now = WeatherUtils(markup = raw_html).temperature_now(url)
        pass


class LocationUtils:
    def __repr__(self):
        return "<WetterOnline LocationUtils object>"

    def __init__(self):
        pass

    def url(self, location) -> typing.Union[bool, str]:
        """
        Returns the specific weather URL of a given `location`, if the `location` is not found returns `False`.
        """
        r = requests.get(f"https://www.wetteronline.de/search?ireq=true&pid=p_search&searchstring={location}", allow_redirects = False)
        #print("-----")
        #print(r.status_code)
        #print(r.headers)
        #print("-----")
        soup = bs4.BeautifulSoup(r.text, "lxml")
        try:
            if soup.find("a").get("href").startswith("/wetter/") or soup.find("a").get("href").startswith("/?gid"):
                return soup.find("a").get("href").lstrip("/")
            else:
                return False
        except:
            return False


    def autosuggest(self, location) -> typing.Union[bool, list]:
        """
        Returns a list of autosuggests of a given `location`, if the `location` is not found returns `False`.
        """
        r = requests.get(f"https://www.wetteronline.de/autosuggest?ireq=true&pid=a_autosuggest&s={location}", allow_redirects = False)
        #print("-----")
        #print(r.status_code)
        #print(r.headers)
        #print("-----")
        returnlist = []
        for i in r.json():
            if "id" in list(i):
                returnlist.append(i["n"])
        if returnlist == []:
            return False
        else:
            return returnlist


class WeatherUtils:
    def __repr__(self):
        return "<WetterOnline WeatherUtils object>"

    def __init__(self, markup = None):
        """
        Initialize `markup` with valid HTML, else fresh markup is requested whenever `WeatherUtils()` is called.
        """
        self.markup = markup
        pass

    def get_markup(self, url: str) -> str:
        if self.markup == None:
            return requests.get(f"https://www.wetteronline.de/{url}", allow_redirects = False).text
        else:
            return self.markup

    def temperature_now(self, url: str):
        """
        Returns the momentary temperature of the given `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
        """

        #r = requests.get(f"https://www.wetteronline.de/{url}", allow_redirects = False)
        #print("-----")
        #print(f"https://www.wetteronline.de/{url}")
        #print(r.status_code)
        #print(r.headers)
        #print("-----")
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        return soup.find("div", {"id": "nowcast-card-temperature"}).find("div", {"class":"value"}).text
    
    def forecast_24h(self, url: str):
        pass
