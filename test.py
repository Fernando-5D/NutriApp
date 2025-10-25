import requests
params = {
    "apiKey": "560b5599d9b249caa849357d7fa64044", 
    "(post body)": """{
        \"username\": \"admin\", 
        \"firstName\": \"luis\", 
        \"lastName\": \"fernando\", 
        \"email\": \"admin@mail.com\"
    }"""
}

solicitud = requests.post('https://api.spoonacular.com/users/connect', params=params)
if solicitud.status_code == 200:
    data = solicitud.json()
    print(data)
else:
    print("Error: " + solicitud.status_code)
