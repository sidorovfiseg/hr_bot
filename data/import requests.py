import requests
import json
photo = {'file': open(r"C:\Users\hajru\OneDrive\Изображения\246137_2.jpg", 'rb')}
response = requests.post("http://127.0.0.1:5000/nutrition", files=photo)
json.loads(response.text)