from meowerclient import MeowerClient
import json

with open("token.json", "r+") as f:
    f.seek(0)
    data = json.load(f)
    f.close()

client = MeowerClient()
client.RUNCLIENT(data["token"])
