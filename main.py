from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from gender_guesser.detector import Detector
import json

detector = Detector()
api_id = 27852650
api_hash = '814e1427ac6750710128ed4bb5a09899'
group_link = 'https://t.me/pogromista'

client = TelegramClient(StringSession(), api_id, api_hash)
client.start()


entity = client.get_entity(group_link)
participants = client.get_participants(entity)


user_info_dict = {}


for participant in participants:
    if participant.username:
        user_info_dict[participant.username] = {
            "name": participant.first_name,
            "last_name": participant.last_name
        }


with open("user_info.json", "w", encoding="utf-8") as json_file:
    json.dump(user_info_dict, json_file, ensure_ascii=False)


with open("male.txt", "w", encoding="utf-8") as male_file, open("female.txt", "w", encoding="utf-8") as female_file:
    for username, info in user_info_dict.items():
        first_name = info.get("name", "")
        gender = detector.get_gender(first_name)

        if gender == "male":
            male_file.write(username + "\n")
        elif gender == "female":
            female_file.write(username + "\n")

client.disconnect()
