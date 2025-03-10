import pygame
from button import Button
import random
from API import APIWrapper

class Game:

    def __init__(self, screen, application):
        self.easter_egg_string = ""
        # Waiting or updating
        self.state = 'waiting'
        self.last_time_call_checked = pygame.time.get_ticks()

        self.screen = screen
        self.application = application
        if self.application.game_settings["phone_num"] == "":
            print("NO PHONE NUMBER SAVED!!!!!!!!!")
            print("USING DEFAULT PHONE NUMBER")

        self.phone_number = self.application.game_settings["phone_num"]
        print(f"PHONE NUMBER: {self.phone_number}")

        self.bg_image = pygame.image.load("assets/room1.png")
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        self.window_image = pygame.image.load("assets/window1.png")
        self.window_image = pygame.transform.scale(self.window_image, self.screen.get_size())

        self.shadow_image = pygame.image.load("assets/darkness1.png")
        self.shadow_image = pygame.transform.scale(self.shadow_image, self.screen.get_size())

        self.phone_image = pygame.image.load("assets/phone1.png")

        button_font = pygame.font.Font(None, 30)
        screen_width, screen_height = self.screen.get_size()

        
        self.character_pathways = {
            "mother": "2b68fe14-ef96-4286-8225-6c452042173c",
            "cook": "84c7b591-688f-4ac3-9919-88b341582fe5",
            "son": "30e10b43-55c3-477b-95f5-b35748b2b641",
            "father": "519b58fc-72f4-41f8-a783-ce2792178f76",
            "neighbour": "6debcfb7-ed84-4500-9564-fdfcfbe38d8e",
            "grandfather": "fb48ce5a-bbc9-425e-882f-32b4f836cea1",
            "easter_egg": "c9678bd1-4092-4acf-b244-22efa0e5b2d5"
        }

        self.character_sprites = {
            "mother": "assets/mother1.png",
            "cook": "assets/cook1.png",
            "son": "assets/son1.png",
            "father": "assets/son1.png",
            "neighbour": "assets/neighbour1.png",
            "grandfather": "assets/son1.png",
            "easter_egg": "assets/gernot1.png"
        }

        self.character_voices = {
            "mother": "Paige",
            "cook": "Brady",
            "son": "josh",
            "father": "Public - DONALD_T",
            "neighbour": "Allie",
            "grandfather": "Pryce",
            "easter_egg": "Karl"
        }

        self.alibi_data = {}
        self.phone_number = self.application.game_settings["phone_num"]
        self.api_caller = APIWrapper(self.phone_number, self.alibi_data)

        #################### BUTTONS LOGIC ###########################

        self._create_function_list()
        random.shuffle(self.lst_functions)

        num_buttons = 5 
        self.buttons = []
        spacing = 80  # Space between buttons
        total_width = num_buttons * 50 + (num_buttons - 1) * spacing
        start_x = (screen_width - total_width) // 2
        y_pos = screen_height - 90  # 40px above the bottom

        person_function = {
            "mother" : self._get_mother, 
            "cook" : self._get_cook, 
            "son" : self._get_son, 
            "father" : self._get_father, 
            "neighbour" : self._get_neighbour, 
            "grandfather" : self._get_grandfather
        }

        self.murderer_list = ['father', 'mother', 'son', 'neighbour', 'grandfather', 'cook']
        self.dead_person_list = ['father', 'mother', 'son', 'neighbour', 'grandfather', 'cook']
        self.murder_weapon_list = ['knife', 'strangulation', 'poison', 'baseball bat', 'pan']
        self.location_of_death_list = ['kitchen', 'bathroom', 'living room', 'garden', 'staircase', '']

        # selected variables
        self.murderer = random.choice(self.murderer_list)
        self.dead_person = random.choice([dead for dead in self.dead_person_list if dead != self.murderer])
        self.people = [alive for alive in self.murderer_list if alive != self.dead_person]
        self.location_of_death = random.choice(self.location_of_death_list)
        self.murder_weapon = random.choice(self.murder_weapon_list)
        self.alibis = []
        # Generate alibis
        self._alibi()

        i=0
        for person in self.people:
            self.buttons.append(
                Button(
                    x=start_x + i * (50 + spacing), y=y_pos, width=60, height=60,
                    text=str(i + 1), font=button_font, color=(0, 100, 200), hover_color=(0, 150, 255),
                    action=person_function[person]
                )
            )
            i+=1

        # Suspect
        self.buttons.append(
            Button(
                x=start_x, y=y_pos - 70, width=200, height=60,
                text=f'MURDERER!', font=button_font, color=(0, 100, 200), hover_color=(0, 150, 255),
                action=self.suspect
            )
        )
        
        self.buttons.append(
            Button(
                x=start_x + 750, y=80, width=60, height=60,
                text='CALL', font=button_font, color=(0, 200, 100), hover_color=(0, 150, 255),
                action=self._call_button)
        )
        
        # Easter button
        self.buttons.append(
            Button(
                x=0, y=0, width=50,height=50,text='',color=(123,123,123), font=button_font, hover_color=(255,255,255), action=self.get_easter_egg
            )
        )

        # Close
        self.buttons.append(
            Button(
                x=self.screen.get_width() - 50, y=0, width=50, height=50, text='close', color=(255,100,100), font=button_font, hover_color=(255,125,125), action=pygame.quit
            )
        )

        self._get_person(random.choice(self.people))

        print(f"MURDERER: {self.murderer}; MURDERED: {self.dead_person}")

    def suspect(self):
        print(self.murderer, self.current_person)
        if self.murderer == self.current_person:
            print("WIN")
            self.bg_image = pygame.image.load("assets/Gernot-Liebchen.png")
            self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())
            self.screen.blit(self.bg_image, (0,0))
            pygame.display.flip()
            pygame.time.delay(5000)
            pygame.quit()
        else:
            print("LOSE")
            pygame.quit()

    def _alibi(self):
        list_context_son_alibi = ["Alibi: The son could have been at home, playing video games, watching TV, or simply relaxing in his room. Family members or housemates could confirm that he was indoors, and there might be visible evidence like the game console or the TV being on at the time.",
        "Alibi: The son could have been at school, either attending classes or having lunch during midday. Teachers, classmates, or school staff could confirm his presence, and school attendance records could verify the time he was there.",
        "Alibi: The son might have been at a friend's house, playing video games, hanging out, or working on a school project. The friend’s parents or the friend themselves could confirm he was there, and there could be evidence of shared activities or photos taken during the visit.",
        "Alibi: The son could have been at the park, either playing sports like soccer or basketball, hanging out with friends, or just enjoying some outdoor time. Other park-goers, friends, or parents of friends could confirm his presence, and there could be video footage if available from security cameras.",
        "Alibi: The son might have been at the library, either studying, reading, or using a computer. Library staff, fellow students, or other library visitors could confirm his presence, and there might be check-in logs or library computer records showing his visit.",
        "Alibi: The son could have been at a sports practice, either for school or a local team, like football, basketball, or another sport. Coaches, teammates, or other parents could verify his presence, and practice schedules could confirm the time.",
        "Alibi: If the son enjoys arcade games, he could have been at a local arcade during midday. Arcade staff or friends could verify his presence, and there would be receipts or records of the games he played or money he spent.",
        "Alibi: The son might have been at the movie theater, watching a movie. Theater staff could confirm his presence, and ticket receipts or purchase records could verify the time of the movie.",
        "Alibi: The son could have been attending a friend’s birthday party, either at a house, park, or entertainment venue. The birthday child’s parents, other kids, or event staff could confirm his presence, and there might be party photos or videos as evidence."
        ]
        
        list_context_grandfather_alibi = ["Alibi: Grandad could be sitting at his regular coffee shop, enjoying a coffee while reading the newspaper or chatting with a group of his older friends. The staff or the other customers could confirm he was there, and there may even be a receipt for his order.",
        "Alibi: Grandad might be in his garden, planting flowers, trimming the hedges, or simply sitting outside enjoying the sun. neighbours or passersby might have seen him outside, and he could have been out there for hours. If it's a regular activity, they might remember seeing him.",
        "Alibi: Grandad might have been at the local senior center, taking part in an activity, class, or social gathering with other seniors. Staff, volunteers, or other attendees could confirm he was there, and there might be sign-in sheets or event records as proof.",
        "Alibi: Grandad might have been taking a walk around the neighbourhood or a nearby park, enjoying the fresh air and maybe even stopping to chat with people along the way. neighbours, park-goers, or even a passing jogger might have seen him. He could also have a walking partner who can confirm he was with them.",
        "Alibi: If he attends a midday service or helps out with community activities at the church, this could be a strong alibi. Fellow churchgoers or staff could verify that he was there, and the church may have logs for volunteer hours or service schedules.",
        "Alibi: Grandad might have been having lunch at the local pub, meeting some friends for a drink, or just having a quiet afternoon meal. The pub staff could verify his presence, and maybe the kitchen or bar staff would recall his order.",
        "Alibi: If Grandad enjoys a hobby like woodworking or crafting, he might be at a local workshop or community space dedicated to these activities. Fellow hobbyists or instructors could confirm that he was present, and any ongoing projects might provide proof of his time there.",
        "Alibi: If he was at the grocery store picking up essentials, the store's staff could confirm his purchase, and the time of the transaction could serve as proof of his whereabouts. He could also be seen by other customers if he was a regular shopper.",
        "Alibi: Grandad could have been at the pet store buying food or supplies for his dog, cat, or other pets. The store staff might remember him, and there could be a record of his purchase."
        ]
        
        list_context_mother_alibi = ["Alibi: The mother could be at home, doing housework like cleaning, organizing, or cooking lunch. Family members or roommates could confirm she was there. If there’s a home security camera or doorbell camera, it might show her movements.",
        "Alibi: The mother might have been at the grocery store shopping for household items. The store’s staff could confirm her visit, and there would be receipts or credit card transactions showing the time she was there.",
        "Alibi: The mother might have been at the school picking up her child, attending a school event, or volunteering in the classroom. Teachers, staff, or other parents could confirm she was there, and school records or sign-in sheets could provide additional verification.",
        "Alibi: The mother might have been visiting her parents or another relative, spending time with them. The family members could confirm her presence, and perhaps they even had a set plan for the visit at that time.",
        "Alibi: She could have been at the hair salon for a scheduled appointment. The salon staff would have records of her appointment, and they could confirm she was there during the time in question.",
        "Alibi: The mother might have been at the gym, attending a fitness class, or working out. The gym staff could confirm her attendance, and they may have a check-in system or class roster that can verify when she was there.",
        "Alibi: She could have been at a shopping mall, running errands, or just browsing stores. Store staff, mall security, or other shoppers might have seen her, and receipts or credit card transactions would back up the timeline.",
        "Alibi: She could have been at a restaurant having lunch with a friend or colleague. The restaurant staff would recognize her, and a receipt or payment history could confirm the time she was there.",
        "Alibi: She could have been at a spa, getting a massage, facial, or other relaxing treatment. The spa’s staff could confirm her appointment, and a receipt or booking confirmation would provide proof of her visit.",
        ]
        
        list_context_father_alibi = ["Alibi: The father could have been at home, either working from home (e.g., on his laptop or in his office) or doing household chores like laundry, cooking, or fixing something. Family members or housemates could confirm he was there, and home security cameras (if available) might also show his movements.",
        "Alibi: If the father works at an office, he could have been there during midday, either working at his desk or attending a meeting. Co-workers, bosses, or employees could confirm he was present, and office logs or emails might show that he was working during the specific time.",
        "Alibi: The father might have been at the gym, attending a workout class, lifting weights, or doing cardio. Gym staff could verify his attendance, and there might be a check-in system or class sign-in sheets showing he was there.",
        "Alibi: The father might have been at a coffee shop, either meeting a friend or enjoying some time alone with a cup of coffee. The coffee shop staff or other regulars could verify that he was there, and a receipt or credit card transaction could confirm the time.",
        "Alibi: The father might have been at the post office, mailing packages or picking up a parcel. Post office staff could confirm his visit, and there would be records of his transaction or even a timestamp on the parcel.",
        "Alibi: If he has children, the father could have been at the school, either dropping off or picking up the kids. Teachers, staff, or other parents could verify he was there, and school records or the time of day would provide an alibi.",
        "Alibi: The father could have been at the bank, either withdrawing money, paying bills, or handling other financial transactions. Bank staff could verify the time of his visit, and there would likely be transaction records or a bank receipt.",
        "Alibi: He could have been at a local pub, having lunch with friends or just unwinding. Pub staff or regulars could verify his presence, and a receipt or payment history could confirm the timing.",
        "Alibi: The father might have been at a sports bar, watching a game or chatting with friends. The bar staff could confirm he was there, and the timing of the game could back up his alibi."
        ]
        
        list_context_cook_alibi = ["Alibi: The family cook could have been in the kitchen, preparing lunch or dinner for the household. Family members, housemates, or anyone present could confirm that they were actively cooking or in the kitchen during the time of the incident. The cook might have even been in the middle of preparing a specific meal, and the kitchen could show evidence of ongoing work (dirty pots, food prep, etc.).",
        "Alibi: The cook might have been at a nearby farmer’s market, picking up fresh ingredients or seasonal produce for the family’s meals. Market vendors could confirm they were there, and there may be receipts or proof of purchase that can be used to verify the time.",
        "Alibi: If the cook is also involved in catering or freelance work, they could have been assisting at an event, preparing or serving food. Event organizers, clients, or other catering staff could confirm their attendance, and there would likely be schedules or event details to back up the alibi.",
        "Alibi: The cook could have been at the grocery store, shopping for ingredients needed to cook meals. Grocery store staff, other shoppers, or security footage could confirm the time they were there, and the cook might have receipts that prove the time of the visit.",
        "Alibi: If the cook was picking up specific cuts of meat or other specialty items, they might have been at the butcher’s shop. The butcher or staff could confirm the visit, and receipts or purchase records could serve as proof of their whereabouts.",
        "Alibi: The cook could have been at a bakery, picking up fresh bread, pastries, or other baked goods for the family’s meals. The bakery staff could confirm the time of their visit, and there may be receipts to verify the purchase.",
        "Alibi: The cook could have been at a local café, meeting a friend or a business associate to discuss recipes, catering jobs, or other culinary matters. Café staff or other patrons could confirm the cook’s visit, and a receipt or credit card record would back up the timing.",
        "Alibi: The cook could have been at a specialty store, buying kitchen tools, pots, pans, or other equipment needed for cooking. The store staff could confirm their visit, and receipts could serve as proof of the time they were there.",
        "Alibi: If the cook needed fresh seafood for a meal, they could have been at a local fish market. Market vendors could confirm their visit, and there may be receipts showing the time and date of purchase."
        ]
        
        list_context_neighbour_alibi = ["Alibi: The neighbour could have been at home, doing routine tasks like cleaning, cooking, or relaxing. Other neighbours or people in the area might have seen them at home, and if they live with family members or roommates, those individuals could confirm they were there. If there are security cameras nearby, it could show their movements.",
        "Alibi: The neighbour could have been visiting another neighbour’s house, either for a social visit or to help with something, like taking care of pets, helping with a task, or chatting. The other neighbour could confirm the visit, and if they were helping with something, the activity would help support the timeline.",
        "Alibi: The neighbour might have been at the post office, either mailing a package, picking up a letter, or handling other errands. Post office staff could verify their visit, and there would be transaction records to confirm their presence at a specific time.",
        "Alibi: The neighbour could have been at the park, walking, jogging, or spending time outdoors. Other park-goers or joggers could verify their presence, and if there are park security cameras, they could provide further confirmation.",
        "Alibi: The neighbour could have been at a doctor’s appointment, either for a routine checkup or a specialist visit. The doctor’s office or clinic could verify the time of the appointment, and medical staff could confirm they were there",
        "Alibi: The neighbour could have been at the library, either reading, studying, or attending a community event. Library staff or other patrons could confirm their presence, and there might be records of events or attendance logs showing when they were there.",
        "Alibi: The neighbour might have been at the bank, handling personal transactions like depositing money, withdrawing cash, or paying bills. The bank staff could verify their visit, and transaction logs or receipts could provide the necessary proof.",
        "Alibi: The neighbour could have been at the hardware store, buying tools, supplies for home improvement, or gardening materials. Store staff could confirm their visit, and there would likely be a receipt or purchase records showing when they were there.",
        "Alibi: If the neighbour had to pick up a prescription or other health-related items, they might have been at a pharmacy. The pharmacy staff could confirm their visit, and prescription records or receipts could serve as evidence."
        ]

        #creating each alibi for individual person
        neighbour_alibi = list_context_neighbour_alibi[random.randint(0, 8)]
        son_alibi = list_context_son_alibi[random.randint(0, 8)]
        mother_alibi = list_context_mother_alibi[random.randint(0, 8)]
        father_alibi = list_context_father_alibi[random.randint(0, 8)]
        cook_alibi = list_context_cook_alibi[random.randint(0, 8)]
        grandfather_alibi = list_context_grandfather_alibi[random.randint(0, 8)]
        
        self.alibis = [neighbour_alibi,son_alibi,mother_alibi,father_alibi,cook_alibi,grandfather_alibi]



    def _call_button(self):
        if self.state != 'calling':
            self.state = "calling"
            self.call = self.call_person(self.person, self.person_role)


    def _get_mother(self):
        self._get_person("mother")

    def _get_father(self):
        self._get_person("father")

    def _get_son(self):
        self._get_person("son")

    def _get_cook(self):
        self._get_person("cook")

    def _get_neighbour(self):
        self._get_person("neighbour")

    def _get_grandfather(self):
        self._get_person("grandfather")


    def _get_person(self, person):
        print(f"Getting {person} on scene")
        self.person = person   
        self.current_person = person
        if self.person == self.murderer:
            self.person_role = 'murderer'
        else:
            self.person_role = 'innocent'
        self.state = 'updating'
        sprite = self.character_sprites[person]
        self.sprite_image = pygame.image.load(sprite).convert_alpha()
        self.sprite_image = pygame.transform.scale(self.sprite_image, (600, 600))
        self.sprite_rect = self.sprite_image.get_rect()
        self.sprite_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.sprite_rect.x = 0
        self.sprite_rect.y = 150

        self.start_pos = [self.screen.get_width() - self.sprite_image.get_width() // 2, self.sprite_rect.y]
        self.end_pos = [self.screen.get_width() // 2 - self.sprite_image.get_width() // 2, self.sprite_rect.y]
        self.duration = 1000  # 2 seconds in milliseconds
        self.start_time = pygame.time.get_ticks()


    def move_sprite(self):
        if pygame.time.get_ticks() - self.start_time < self.duration:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            progress = elapsed_time / self.duration

            self.sprite_rect.x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
            self.sprite_rect.y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress

            self.screen.blit(self.sprite_image, self.sprite_rect)
        
        else:
            self.state = 'waiting'
       

    def call_person(self, person, person_role):
        #self.move_phone()
        print(f"CALLING:", person)
        ############# UNCOMMENT FOR CALLS ###########################
        self.call = self.api_caller.start_interview(
            person=person, pathway_id=self.character_pathways[self.person],
            murderer=self.murderer, dead_person=self.dead_person,
            murder_weapon=self.murder_weapon, location_of_death=self.location_of_death,
            person_role=person_role, voice_name=self.character_voices[person], alibis=self.alibis
        )
        pass

    def move_phone(self):
        self.phone_image = self.phone_image.convert_alpha()
        self.phone_image = pygame.transform.scale(self.phone_image, (300, 300))
        
        self.phone_rect = self.phone_image.get_rect()
        self.phone_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.phone_rect.x = 0
        self.phone_rect.y = 150

        start_pos = [(self.screen.get_width() - self.phone_image.get_width()) // 2, self.screen.get_height()]
        end_pos = [(self.screen.get_width() - self.phone_image.get_width()), 150]
        duration = 1000  # 2 seconds in milliseconds
        start_time = pygame.time.get_ticks()

        while True:
            if pygame.time.get_ticks() - start_time < duration:
                elapsed_time = pygame.time.get_ticks() - start_time
                progress = elapsed_time / duration

                self.phone_rect.x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
                self.phone_rect.y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

                self.screen.blit(self.phone_image, self.phone_rect)
            return


    def _create_function_list(self):
        self.lst_functions = [self._get_mother, self._get_cook, self._get_son, self._get_father, self._get_neighbour, self._get_grandfather]
        

    def draw_sprite(self):
        self.screen.blit(self.sprite_image, self.sprite_rect)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        if self.sprite_image and self.state == 'updating':
            self.move_sprite()
        else:
            self.draw_sprite()

    # Draw person's name
        if self.current_person:
            self._draw_person_name()

        self.screen.blit(self.window_image, (0, 0))

        for button in self.buttons:
            button.draw(self.screen)

    def _draw_person_name(self):
        """Displays the current person's name on the screen."""
        font = pygame.font.Font(None, 60)  # Adjust font size as needed
        text_surface = font.render(self.current_person, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2+30  , 150))  # Centered at top
        self.screen.blit(text_surface, text_rect)


    def get_easter_egg(self):
        print("GETT")
        sprite = self.character_sprites["easter_egg"]
        self.sprite_image = pygame.image.load(sprite).convert_alpha()
        self.sprite_image = pygame.transform.scale(self.sprite_image, (600, 600))
        self.sprite_rect = self.sprite_image.get_rect()
        self.sprite_rect.center = ((self.screen.get_width() - self.sprite_rect.width) // 2, self.screen.get_height() // 2)
        self.sprite_rect.x = 0
        self.sprite_rect.y = 150
        while True:
            if pygame.time.get_ticks() - self.start_time < 2000:
                elapsed_time = pygame.time.get_ticks() - self.start_time
                progress = elapsed_time / 2000

                self.sprite_rect.x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
                self.sprite_rect.y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress

                self.screen.blit(self.sprite_image, self.sprite_rect)
                pygame.time.delay(10)
                continue
            break
        self.call_person("easter_egg", None)


    def run(self):
        running = True
        self.last_time_call_checked = pygame.time.get_ticks()
        while running:
            # print(self.state)
            if self.state == 'calling' and pygame.time.get_ticks() - self.last_time_call_checked > 3000:
                print('calling')
                self.last_time_call_checked = pygame.time.get_ticks()
                self.move_phone()
                self.state = 'waiting'
                call_status = self.api_caller.check_call_status(self.call)
                print(f"CURRENT CALL: {call_status}")
                if call_status != 'in-progress':
                    self.state = 'waiting'
            
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.state == 'waiting':
                    for button in self.buttons:
                        button.handle_event(event)
                    

            pygame.display.flip()