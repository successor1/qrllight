def getAddress(address):
  import requests
  import json
  request = requests.get('https://testnet-explorer.theqrl.org/api/a/'+address)
  response = request.text
  getAddressResp = json.loads(response)
  jsonResponse = getAddressResp
  print(jsonResponse)


getAddress("Q0105001477cd64905f7e9ef8d21f43f8342e825bc554f999bb59cedec98fb8eeaaa3e570808063")