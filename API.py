import requests
import json
import random
import time

# Headers - API keys (currently Yans)


CALL_STATUS_URL = "https://api.bland.ai/v1/calls/{call_id}"  # Used to check call status

class APIWrapper():
    def __init__(self, phone_num, alibi_data):
        self.headers = {
            'authorization': '<insert API Key here>',
            "Content-Type": "application/json"
        }
        self.alibi_data = alibi_data
        # Entering the user's phone number
        self.player_phone_number = "+44" + phone_num
        # This is to let player press buttons when call is finished
        self.call_in_progress = False

    # Call function
    def start_interview(self, person, pathway_id, murderer, dead_person, 
                        murder_weapon, location_of_death, person_role,
                        voice_name, alibis):
        alibis=alibis
        print(alibis)
        data = {
            "phone_number": self.player_phone_number,
            "task": f"You are being called by a detective about a recent murder that happened at a house in the {location_of_death}, the {dead_person} has been killed. They were killed with {murder_weapon}. please reply to the detective accordingly. You do not know who the muderer is",
            "voice": voice_name,
            "request_data": {
               "murderer": murderer,
               "victim": dead_person,
               "murder_weapon": murder_weapon,
               "location": location_of_death,
               "person_role": person_role,
               "time":"11AM, Thursday",
               "neighbor_alibi": alibis[0],
               "son_alibi": alibis[1],
               "mother_alibi": alibis[2],
               "father_alibi": alibis[3],
               "cook_alibi": alibis[4],
                "grandfather_alibi": alibis[5]
            },
            "record": True,
            "reduce_latency": True,
            "ivr_mode": True,
            "temperature": 0.5,
            "webhook": "https://webhook.site/72186de7-061a-4087-aae2-1b0f688589d5",
            "pathway_id": pathway_id
        }

        response = requests.post("https://api.bland.ai/v1/calls", json=data, headers=self.headers)

        # WARNING!!! THIS IS THE PART WHERE SOME REALLY UNHUMAN CODING PRACTICES ARE BEING USED!!!
        attempts = 0
        while response.status_code != 200 or attempts <=5:
            print(response.status_code)
            if response.status_code == 200:
                self.call_in_progress = True
                self.call_id = response.json().get("call_id")
                print(f"ATTEMPT {attempts}: Call to {person} successful: Call ID = {self.call_id}")
                break
            else:
                print(f"ATTEMPT {attempts}: Call to {person} failed: {response.text}")
                self.call_id = 0
                response = requests.post("https://api.bland.ai/v1/calls", json=data, headers=self.headers)
                attempts += 1
            if attempts == 5:
                break
            time.sleep(1)
        return self.call_id

    # Function to Check Call Status
    def check_call_status(self, call_id):
        """Checks the live status of a call using its call_id."""
        url = CALL_STATUS_URL.format(call_id=call_id)
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            call_data = response.json()
            return call_data.get("status", "Unknown")  # Returns call status
        else:
            print(f"ERROR MESSAGE: {response.text}")
            return "Error"


    # Live status monitor
    """def status_monitor(self):
        if self.call_id:
            status = self.check_call_status(call_id)
            while True:
                print(f"Current Status of Call ID {call_id}: {status}")
                time.sleep(5)  # Wait a few seconds before checking the status
                status = self.check_call_status(call_id)
                if status == "completed":
                    print("CALL COMPLETED")
                    break
    """