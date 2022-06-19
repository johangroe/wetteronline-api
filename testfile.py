import endpoint


#l = endpoint.location("gotha")
#print(l.url)
#print(l.autosuggests)
w = endpoint.weather("wetter/gotha")

print(w.temperature_now)
print(w.forecast_24h[list(w.forecast_24h)[0]])
#for i in w.forecast_24h:
#    print(i, w.forecast_24h[i])
#    print()
#print(type(w.forecast_24h))

#single = w.forecast_24h[list(w.forecast_24h)[0]]
#print(list(w.forecast_24h)[0])
#for i in list(single):
#    print(f"{i}: {single[i]}")

#with open("outfile2.html", "w") as f:
#    f.write(w.debug_raw_html)

#with open("outfile3.html", "w") as f:
#    f.write(str(w.forecast_24h))

print(w.forecast_4d)
#print(type(w.forecast_4d["19.06."]["maxTemp"]))
#w.forecast_4d