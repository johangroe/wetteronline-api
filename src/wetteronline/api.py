import requests
import json
import bs4
import typing
import ast
import html
## non std lib: requests, bs4, lxml


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
        raw_html = html.unescape(requests.get(f"https://www.wetteronline.de/{url}", allow_redirects = False).text)
        #self.debug_raw_html = raw_html
        weatherutils = WeatherUtils(markup = raw_html)
        self.temperature_now = weatherutils.temperature_now(url)
        self.forecast_24h = weatherutils.forecast_24h(url)
        self.forecast_4d = weatherutils.forecast_4d(url)



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
        soup = bs4.BeautifulSoup(html.unescape(r.text), "lxml")
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
            return html.unescape(requests.get(f"https://www.wetteronline.de/{url}", allow_redirects = False).text)
        else:
            return self.markup

    def temperature_now(self, url: str):
        """
        Returns the momentary temperature of the given `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
        """
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        temp = soup.find("span", class_="air-temp").string.strip().replace("°","")
        return int(temp)

    def forecast_24h(self, url: str):
        """
        Returns the full 24h forecast of the given `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
        """
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        hourlyContainer = soup.find("div", class_="hours-list").find_all("wo-forecast-hour")
        returndict = {}
    
        for i in range(24):
            hour = hourlyContainer[i].find("wo-date-hour").string.strip().replace(" ","")
            temp = int(hourlyContainer[i].find(class_="temperature").string.strip())
            rain_raw = hourlyContainer[i].find(class_="description").string.replace("\xa0", "").strip()
            sky = hourlyContainer[i].find("img", class_="symbol")["alt"]
            
            ## precipitation as float
            rain = int(rain_raw.replace("%", "")) / 100
            
            returndict[hour] = {
                "temperature": temp,
                "rain": rain,
                "sky": sky
            }

        return returndict

    def forecast_4d(self, url: str):
        """
        Returns the full 4 day forecast of the given `url`. Note that `url` is not a full URL, but a fragment like returned by `location.url`!
        """
        soup = bs4.BeautifulSoup(self.get_markup(url), "lxml")
        ## get dates first
        returndict = {}
        table = soup.find("table")

        for i in table.find_all("th"):
            date = i.find("span", class_="screen-reader-only").string
            if "," in list(date):
                date = date.split(", ")[1]
            returndict[date] = {}

        weathertable = table.tbody
        
        ## maxtemp
        taglist = list(weathertable.find_all("wo-medium-term-weather-temperatures"))
        for i in range(len(taglist)):
            tag = taglist[i].find(class_="max").find("div", class_="temperature").string.strip()
            returndict[list(returndict)[i]]["maxTemperature"] = int(tag)

        ## mintemp
        taglist = list(weathertable.find_all("wo-medium-term-weather-temperatures"))
        for i in range(len(taglist)):
            tag = taglist[i].find(class_="min").find("div", class_="temperature").string.strip()
            returndict[list(returndict)[i]]["minTemperature"] = int(tag)

        ## sunhours
        taglist = list(weathertable.find_all("wo-weather-characteristics-sun"))
        for i in range(len(taglist)):
            tag = taglist[i].find("div", class_="description").string.strip()
            returndict[list(returndict)[i]]["sunHours"] = int(tag.lstrip().rstrip(" h\n"))

        ## precipitation probability
        taglist = list(weathertable.find_all("wo-weather-characteristics-precipitation"))
        for i in range(len(taglist)):
            tag = taglist[i].find("div", class_="description").string.strip()
            ## precipitation as float
            tag = int(tag.replace("%", "")) / 100
            returndict[list(returndict)[i]]["precipitationProbability"] = tag

        return returndict