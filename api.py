import requests
import json
import bs4
import typing
import ast
import html


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
        weatherutils = WeatherUtils(markup = raw_html)
        self.temperature_now = weatherutils.temperature_now(url)
        self.forecast_24h = weatherutils.forecast_24h(url)



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
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        return soup.find("div", {"id": "nowcast-card-temperature"}).find("div", {"class":"value"}).text

    def forecast_24h(self, url: str):
        """
        Returns the full 24h forecast of the given `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
        """
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        scripts = soup.find("div", {"id": "hourly-container"}).find_all("script")
        returndict = {}
        for script in scripts:
            script = html.unescape(str(script).split("({")[1].split("})")[0].strip().replace(" ", ""))
            smallreturnlist = []
            for entry in script.split("\n"):
                smallreturnlist.append(f'"{entry.split(":")[0]}": {entry.split(":")[1]}')
            smallreturndict = ast.literal_eval("{" + "".join(smallreturnlist) + "}")

            ## delete useless keys
            for key in ["dayTime", "daySynonym", "docrootVersion", "windSpeedText", "windDirection"]:
                smallreturndict.pop(key, None)
            ## delete unknown keys
            for key in ["smog", "tierAppendix", "symbol", "symbolText", "windy"]:
                smallreturndict.pop(key, None)

            hour = smallreturndict.pop("hour")

            ## filter doubling hours, the website provides inconsistently between 24 and 47 datapoints
            ## yes, data may be lost here, but the api can assure 24h every call
            if hour in list(returndict):
                continue
            returndict[hour] = smallreturndict

        return returndict
