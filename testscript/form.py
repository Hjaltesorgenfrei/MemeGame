from socket import timeout
import requests

with open("IMG.JPG","rb") as file:
    data = {'visualFile': ("IMG.JPG", file.read(), "image/jpeg") }
    body = {'toptext': "", 'bottomtext':""}
    request = requests.Request('POST',"https://api.mads.monster/Upload/Memes", files= data, data=body ).prepare()
    print(request.body[:300])
    s = requests.Session()
    response = s.send(request)
    print(response)
    print(response.content)