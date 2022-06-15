import requests
import endpoint


#l = endpoint.location("gotha")
#print(l.url)
#print(l.autosuggests)
w = endpoint.weather("wetter/nagar")

print(w.temperature_now)

with open("outfile2.html", "w") as f:
    f.write(w.debug_raw_html)