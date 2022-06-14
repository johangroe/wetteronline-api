import requests
import api

'''
r = requests.get("https://www.wetteronline.de/")


print(r.status_code)
print(r.headers)
#print(r.text)
with open("outfile.html", "w") as f:
    f.write(r.text)
#'''

client = api.WetterOnline()

#with open("outfile.html", "w") as f:
    #f.write(client.get_url("ernstroda"))

#print(client.location_get_url("yeet"))
print(client.location_autocomplete("asdf"))
