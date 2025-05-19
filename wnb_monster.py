import time
import pygame
import random

from main import screen
from main import GameController
screen_width = 1980
screen_height = 1280

class Pigeon:
    ENTITY_CAP = 20
    entity_count = 0
    def __init__(self, x, y,speed,ai_value,tip):
        self.x = x
        self.y = y
        self.tip=tip
        self.ai_value = ai_value  # 0: flies around, 1: flies up from the hat, then can dive
        self.speed = speed
        self.is_moving = True
        self.ritual=1
        self.clicked_count = 0
        self.clicked_lim = 1
        self.steps=0
        self.direction = -1
        self.fly_height = (screen_height // 2) - random.choice([540,460,340])
        self.turn_after=100
        self.sprite = [pygame.image.load(r'Sprites\Pigeon\pigeon_left_0.png'),
                       pygame.image.load(r'Sprites\Pigeon\pigeon_left_1.png'),
                       pygame.image.load(r'Sprites\Pigeon\pigeon_right_0.png'),
                       pygame.image.load(r'Sprites\Pigeon\pigeon_right_1.png'),
                       pygame.image.load(r'Sprites\Pigeon\pigeon_down.png'),
                       pygame.image.load(r'Sprites\Pigeon\pigeon_final.png')
                    ]  # Load the static image for the bird
        self.image = self.sprite[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Set the initial position of the bird
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = True
        Pigeon.entity_count +=1
    def update(self):
        # If clicked_count reaches 1, set the monster as inactive
        if self.clicked_count >= self.clicked_lim:
            self.is_active = False
            self.remove()

        if self.is_active:  # Only update if active
            if self.ai_value == 0:
                self.wander_left_right()
            elif self.ai_value == 1:
                self.fly_up()
            elif self.ai_value == 2:
                self.dive()
        self.draw(screen)
    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, self.rect.topleft)

    def wander_left_right(self):
        if self.steps > self.turn_after or self.rect.x > screen_width + 200:
            self.direction *= -1
            self.steps = 0
            self.turn_after=random.choice([50,  75, 25 , 120])
        self.rect.x += self.direction * self.speed
        self.steps += 1
        if self.direction == -1 :
            self.image = self.sprite[0] if self.steps > 10 else self.sprite[1]
        else:
            self.image = self.sprite[2] if self.steps > 10 else self.sprite[3]
        if 30 < self.steps < 35:
            random.seed(self.rect.x)
            attack_chance = random.randrange(1,200)
            if attack_chance > 190:
                self.ai_value = 2

    def fly_up(self):
        if self.rect.y > self.fly_height :
            self.rect.y -= self.speed
            self.steps +=1
        else :
            self.speed=random.choice([1,2,3])
            self.ai_value = 0
        if self.steps > self.turn_after or self.rect.x > screen_width + 200:
            self.direction *= -1
            self.steps = 0
            self.turn_after=random.choice([50,  75, 25 , 120])
        self.rect.x += self.direction * self.speed
        self.steps += 1
        if self.direction == -1 :
            self.image = self.sprite[0] if self.steps > 10 else self.sprite[1]
        else:
            self.image = self.sprite[2] if self.steps > 10 else self.sprite[3]

    def dive(self):
        self.image = self.sprite[4]

        if self.rect.y < 650 :
            self.rect.y += 10
        else:
            self.image = self.sprite[5]
            self.clicked_lim=64
            self.death_sequence()

    def death_sequence(self):
        self.ritual=-1
        self.steps +=1
        if self.steps >= 300:
            self.is_active = False

    def get_ritual(self):
        return self.ritual

    def check_collision(self,cursor):
        if cursor.check_collision(self.rect):
            return True
        return False
    def check_criteria(self, criteria):
        self.clicked_count += 1
        return True

    def remove(self):
        Pigeon.entity_count -= 1
        del self

class TopHat:
    BIRD_CAP=14
    BIRDS = 0
    def __init__(self, x, y,ai_value,tip):
        self.x = x
        self.y = y
        self.tip = tip
        self.ai_value = ai_value
        self.last_clicked = 0
        self.clicked_count = 0
        self.steps=0
        self.spawn_counter = 0
        self.spawn_after = 200
        self.weakness = random.choice([1, 2, 3])
        self.spritepack = [ None,
                            pygame.image.load(r'Sprites\Hat\magic_hat_F.png'),
                           pygame.image.load(r'Sprites\Hat\magic_hat_I.png'),
                           pygame.image.load(r'Sprites\Hat\magic_hat_E.png'),]
        self.image = self.spritepack[self.weakness]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.birds = []
        self.is_active = True # Monster is active by default
        random.seed(self.rect.x)
    def update(self):
        for monster in self.birds:
            monster.update()
            if monster.is_active:
                monster.draw(screen)
            else:
                monster.remove()
        # If clicked_count reaches 1, set the monster as inactive
        if self.clicked_count >= 1:
            self.is_active = False
        if self.is_active:
            self.draw(screen)
        else:
            self.remove()
        if self.is_active:
            if self.ai_value == 0:
                # Only update if active
                self.steps += random.randint(1, 3)
                if self.steps > self.spawn_after and self.spawn_counter < 3 and Pigeon.entity_count < Pigeon.ENTITY_CAP and TopHat.BIRDS < TopHat.BIRD_CAP:
                    self.spawn_counter += 1
                    self.steps=0
                    self.birds.append(Pigeon(self.rect.x, self.rect.y, random.choice([1,2,3]),1,"bird"))
                    TopHat.BIRDS += 1
            if self.ai_value==1:
                self.dive()
        for _ in self.birds:
            _.update()
            if not _.is_active:
                self.spawn_counter -=1
                TopHat.BIRDS -= 1
    def check_collision(self,cursor):
        if cursor.check_collision(self.rect):
            return True
        return False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, self.rect.topleft)
        # Draw pigeons even if TopHat is not active anymore
        for bird in self.birds:
            if bird.is_active:
                bird.draw(surface)

    def check_criteria(self, criteria):
        current_time = time.time()
        if (self.last_clicked is None or current_time - self.last_clicked > 1)  and self.weakness==criteria :
            self.last_clicked = current_time
            self.clicked_count += 1
            return True
        return False
    def dive(self):
        if self.rect.y < 650 :
            self.rect.y += 10
        else:
            self.ai_value=0
    def remove(self):
        self.rect.x = -4000
        self.rect.y = -2000
        del self

class HoodedWiz:
    HATCAP = 0
    def __init__(self, x, y,speed,ai_value,tip):
        self.x = x
        self.y = y
        self.tip= tip
        self.ai_value = ai_value# 0: flies around, 1: flies up from the bottom
        self.speed = speed
        self.clicked_count = 0
        self.clicked_lim = 5
        self.steps=0
        self.direction = -1
        self.fly_height = screen_height //2 - 200
        self.turn_after=200
        self.hats = []
        self.spritepack = [ None,
                        pygame.image.load(r'Sprites\Magician\magician_F0.png'),
                        pygame.image.load(r'Sprites\Magician\magician_I0.png'),
                        pygame.image.load(r'Sprites\Magician\magician_L0.png'),
                       ]
                      # Load the static image for the bird
        self.attackpack = [ None,
                            pygame.image.load(r'Sprites\Magician\magician_F1.png'),
                            pygame.image.load(r'Sprites\Magician\magician_I1.png'),
                            pygame.image.load(r'Sprites\Magician\magician_L1.png')
        ]
        self.temp_image=0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = True
        self.weakness= random.choice([1,2,3])
        self.image = self.spritepack[self.weakness]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # If clicked_count reaches 1, set the monster as inactive
        if self.rect.x > screen_width-600 or self.rect.x < 0:
            self.rect.x = random.choice([screen_width - 1000, screen_width-1600])
            self.rect.y = screen_height
            self.ai_value=1
        elif self.rect.x < 0 :
            self.rect.x = 0
        self.speed=self.weakness * 1.5
        if self.clicked_count >= self.clicked_lim:
            self.is_active = False
        if self.is_active:  # Only update if active
            if self.ai_value == 0:
                self.wander_left_right()
            elif self.ai_value == 1:
                self.fly_up()
        self.draw(screen)

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, self.rect.topleft)

    def wander_left_right(self):
        if self.steps > self.turn_after or self.rect.x > screen_width + 200:
            self.direction *= -1
            self.steps = 0
            self.turn_after=300
        self.rect.x += self.direction * self.speed
        self.steps += 1
        if self.temp_image==0:
                self.image = self.spritepack[self.weakness]
        else:
            self.temp_image -= 1
        if 20 < self.steps < random.randint(100,300):
            random.seed(random.randint(1,300))
            attack_chance = random.randrange(1,400)
            if attack_chance > 390:
                self.ai_value = 2
                HoodedWiz.HATCAP += 1
                self.image =self.attackpack[self.weakness]
                self.temp_image=40

    def fly_up(self):
        if self.rect.y > self.fly_height :
            self.rect.y -= self.speed
        else :
            self.ai_value = 0

    def check_collision(self,cursor):
        """ Check for collision with the cursor. """
        if cursor.check_collision(self.rect):
            if self.clicked_count>=self.clicked_lim:
                self.remove()
            return True
        return False
    def check_criteria(self, criteria):
        current_time = time.time()
        if self.weakness == criteria:
            self.clicked_count += 1
            self.weakness = random.choice([1,2,3])
            return True
        return False

    def remove(self):
        self.rect.x= -2000
        self.rect.y = -2000
        del self