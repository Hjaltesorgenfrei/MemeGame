from socket import timeout
import requests
import os

for f in os.listdir("./images"):
    with open(f"./images/{f}","rb") as file:
        filend = f.split(".")[1]
        if filend not in ["jpg","jpeg","png"]:
            continue
        if filend == "jpg": 
            filend = "jpeg"
        data = {'visualFile': (f, file.read(), f"image/{filend}") }
        body = {'toptext': "", 'bottomtext':""}
        request = requests.Request('POST',"https://api.mads.monster/Upload/Memes", files= data, data=body ).prepare()
        print(request.body[:300])
        s = requests.Session()
        response = s.send(request)
        response.raise_for_status()
        print(response)
        print(response.content)
    os.remove(f"./images/{f}")
    

"""
<input type="file"
    id="file_picker" name="avatar"
    accept="image/png, image/jpeg">
<button onclick="submitImage('file_picker')">Submit Image</button> 
"""