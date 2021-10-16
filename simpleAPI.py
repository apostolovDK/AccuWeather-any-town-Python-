from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.request
import re

HOST_NAME = "localhost"
SERVER_PORT = 8080
API_KEY="ICoGL5pn2KM2jCJwhotrZ4a1Up29o7ZC"


def get_location(country_code,city):
    search_address="http://dataservice.accuweather.com/locations/v1/cities/"+country_code+"/search?apikey="+API_KEY+"%20&q="+city+"&details=true"
    with urllib.request.urlopen(search_address) as search_address:
        #getting location key
        data=json.loads(search_address.read().decode())
    #extracting location key from the responce(json format)
    return data[0]['Key']

def get_date_time(country_code, city):
    location_key=get_location(country_code, city)
    current_forcast_url="http://dataservice.accuweather.com/currentconditions/v1/"+location_key+"?apikey="+API_KEY+"%20&details=true"
    with urllib.request.urlopen(current_forcast_url) as current_forcast_url:
        data=json.loads(current_forcast_url.read().decode())
    return "Current Time: " + data[0]['LocalObservationDateTime']+"\n\rCurrent Temperature:" + (str)(data[0]['Temperature']['Metric']['Value']) + data[0]['Temperature']['Metric']['Unit']


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search("/getWeather\?country=[A-Z]{2,3}&city=[A-Z]{1}[a-z]+[- ]?[A-Z]{1}[a-z]+$", self.path):
            data=self.path
            country_code=data[data.find("country=") + len("country=") : data.find("&city")]
            city=data[data.find("city=") + len("city=") :]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(get_date_time(country_code, city), "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOST_NAME, SERVER_PORT))

    try:
        webServer.serve_forever()
        webServer
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")