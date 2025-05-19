import pygame
import sys
import random
import os
import math
from datetime import date
from wnb_cursor import Cursor
import wnb_monster
from wnb_mana_sys import MagicGUI
pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Medieval Wizard Battle!")
font = pygame.font.Font('GUI/04B_03.ttf', 60)
evil_laugh = pygame.mixer.Sound("Audio/magician_laugh.mp3")
evil_death = pygame.mixer.Sound("Audio/magician_death.mp3")
ability_image = [   pygame.image.load(r'Sprites\Skills\empty.png').convert_alpha(),
                    pygame.image.load(r'Sprites\Skills\skill_fire.png').convert_alpha(),
                    pygame.image.load(r'Sprites\Skills\skill_ice.png').convert_alpha(),
                      pygame.image.load(r'Sprites\Skills\skill_electric.png').convert_alpha(),
                    pygame.image.load(r'Sprites\Skills\skill_none.png').convert_alpha()
    ]
player_image = [ pygame.image.load(r'GUI\player_mage_F0.png').convert_alpha(),
                    pygame.image.load(r'GUI\player_mage_F1.png').convert_alpha(),
                    pygame.image.load(r'GUI\mega_mage.png').convert_alpha()
    ]
clock = pygame.time.Clock()
cursor = Cursor(speed=5)
local_difficulty = 1
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
screen_width, screen_height = screen.get_size()
# Function to draw buttons in the game
def draw_button(text, rect, hovered):
    color = GRAY if not hovered else DARK_GRAY
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
def draw_text(surface, text, x, y, font_size=30, color=(255, 255, 255)):
    font = pygame.font.Font('GUI/04B_03.ttf', font_size)
    text_surface = font.render(text, True, color,)
    surface.blit(text_surface, (x, y))
def update_and_draw_cursor():
    cursor.update()
    cursor.draw(screen)
# Settings screen for adjusting sensitivity
def settings():
    running = True
    sensitivity = 5  # Default sensitivity (1 = slow, 10 = fast)
    global local_difficulty

    # Button setup
    minus_rect = pygame.Rect(380, 250, 50, 50)
    plus_rect = pygame.Rect(530, 250, 50, 50)
    minus1_rect = pygame.Rect(380, 600, 50, 50)
    plus1_rect = pygame.Rect(530, 600, 50, 50)

    back_text = font.render("Press ESC to return", True, WHITE)
    settings_background = pygame.image.load(r'GUI\info_background.png')
    settings_background = pygame.transform.scale(settings_background, (screen_width, screen_height))
    while running:
        screen.blit(settings_background, (0, 0))

        # --- Labels ---
        label_text = font.render("Sensitivity", True, WHITE)
        label1_text = font.render("Difficulty", True, WHITE)
        screen.blit(label_text, (screen.get_width() // 2 - label_text.get_width() // 2, 150))
        screen.blit(label1_text, (screen.get_width() // 2 - label1_text.get_width() // 2, 500))

        # --- Display values ---
        sens_display = font.render(f"-  {sensitivity}  +", True, WHITE)
        diff_display = font.render(f"-  {local_difficulty}  +", True, WHITE)
        screen.blit(sens_display, (screen.get_width() // 2 - sens_display.get_width() // 2, 250))
        screen.blit(diff_display, (screen.get_width() // 2 - diff_display.get_width() // 2, 600))

        # --- Draw buttons ---
        for rect in [minus_rect, plus_rect, minus1_rect, plus1_rect]:
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

        # --- Button signs ---
        minus_sign = font.render("-", True, BLACK)
        plus_sign = font.render("+", True, BLACK)
        screen.blit(minus_sign, minus_rect.center)
        screen.blit(plus_sign, plus_rect.center)
        screen.blit(minus_sign, minus1_rect.center)
        screen.blit(plus_sign, plus1_rect.center)

        # --- Back text ---
        screen.blit(back_text, (30, screen.get_height() - 60))

        cursor.update()
        cursor.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cursor.speed = sensitivity
                return sensitivity, local_difficulty

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if minus_rect.collidepoint(cursor.pos) and sensitivity > 1:
                    sensitivity -= 1
                elif plus_rect.collidepoint(cursor.pos) and sensitivity < 10:
                    sensitivity += 1
                if minus1_rect.collidepoint(cursor.pos) and local_difficulty > 1:
                    local_difficulty -= 1
                elif plus1_rect.collidepoint(cursor.pos) and local_difficulty < 5:
                    local_difficulty += 1

# Main menu screen
def main_menu():
    running = True
    button_width, button_height = 300, 80
    spacing = 30
    num_buttons = 5  # Start, Settings, Scores, Info, Quit
    start_y = screen_height // 2 - (button_height + spacing) * (num_buttons - 1) // 2

    background_main = pygame.image.load(r'GUI/menu_background.png').convert()
    background_main = pygame.transform.scale(background_main, (screen_width, screen_height))

    buttons = {
        "Start": pygame.Rect(screen_width // 2 - button_width // 2, start_y, button_width, button_height),
        "Settings": pygame.Rect(screen_width // 2 - button_width // 2, start_y + (button_height + spacing), button_width, button_height),
        "Scores": pygame.Rect(screen_width // 2 - button_width // 2, start_y + 2 * (button_height + spacing), button_width, button_height),
        "Info": pygame.Rect(screen_width // 2 - button_width // 2, start_y + 3 * (button_height + spacing), button_width, button_height),
        "Quit": pygame.Rect(screen_width // 2 - button_width // 2, start_y + 4 * (button_height + spacing), button_width, button_height),
    }

    while running:
        hover_pos = cursor.get_pos()
        screen.blit(background_main, (0, 0))
        for name, rect in buttons.items():
            hovered = rect.collidepoint(hover_pos)
            draw_button(name, rect, hovered)
        update_and_draw_cursor()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if cursor.active:
            for name, rect in buttons.items():
                if rect.colliderect(cursor.rect):
                    if name == "Start":
                        play()
                    elif name == "Settings":
                        settings()
                    elif name == "Scores":
                        scoreboard()
                    elif name == "Info":
                        info_menu()
                    elif name == "Quit":
                        pygame.quit()
                        sys.exit()

        clock.tick(60)

def scoreboard():
    running = True
    scores = read_scores(r"GUI\highscores.dat")
    background_score = pygame.image.load(r'GUI\score_background.png').convert()
    background_score = pygame.transform.scale(background_score, (screen_width, screen_height))
    text_center = screen_width // 3
    while running:
        screen.blit(background_score, (0,0))  # Or load a custom scoreboard background

        draw_text(screen, f"Top Scores", text_center, 40)
        for i, (score, date_str) in enumerate(scores):
            text = f"{i+1}. {score} pts - {date_str}"
            draw_text(screen, f"{text}", text_center, 100 + i * 60)

        update_and_draw_cursor()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to main menu

        clock.tick(60)


def info_menu():
    running = True
    clock = pygame.time.Clock()
    background_info = pygame.image.load(r'GUI\info_background.png').convert()
    background_info = pygame.transform.scale(background_info, (screen_width, screen_height))
    # Load and scale images
    images = [
        pygame.transform.scale(pygame.image.load("GUI/Story_Img.png"), (400, 300)),
        pygame.transform.scale(pygame.image.load("GUI/Magic_Guide_Img.png"), (400, 300)),
        pygame.transform.scale(pygame.image.load("GUI/Player_Action_Img.png"), (400, 300))
    ]

    paragraphs = [
        "You're a master magician who guards Littleroot Town.",
        "Unfortunately, a group of vile mages besieges your village every night!",
        "To fight the Mages, cast spells of different elements. ",
        "Press [Z] to draw a spell and change elements. Press [X] to stop chanting. ",
        "Your [MANA] (top left) decreases while chanting or attacking. Manage it wisely!",
        "Press [T] to end your run early. You can increase the difficulty in the Settings menu.",
    ]



    while running:
        screen.blit(background_info, (0, 0))
        for i in range(3):
            x = 80 + i * 440
            screen.blit(images[i], (x, 100))
            counter = 0
            for line_text in paragraphs:
                draw_text(screen, line_text, 10, 500 + 50*counter , font_size=22, color=(220, 220, 220))
                counter += 1
                if counter > 5 :
                    counter = 0

        cursor.update()
        cursor.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def render_wrapped_text_lines(text, font_size, x, y, max_width):
    font_obj = pygame.font.Font(None, font_size)
    words = text.split(' ')
    lines = []
    line = ''
    current_y = y

    for word in words:
        test_line = f"{line} {word}".strip()
        if font_obj.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append((line, x, current_y))
            current_y += font_obj.get_height() + 4
            line = word
    if line:
        lines.append((line, x, current_y))
    return lines
# Play screen where the game action happens
def play():
    # Play Screen
    background_play = pygame.image.load(r'GUI/play_background.png').convert()
    background_play = pygame.transform.scale(background_play, (screen_width, screen_height))
    clawL= pygame.image.load(r'GUI/left_claw.png').convert_alpha()
    clawR = pygame.image.load(r'GUI/right_claw.png').convert_alpha()
    running = True
    char_pos = pygame.Vector2(screen_width // 2, screen_height - 50)
    char_size = 40
    last_update_time = 0
    timer_update_time = 0
    player_avatar= player_image[0]
    score_x= 64
    score_y= 64
    wave_x = 1200
    wave_y = 64
    time_y = 10
    timer = 260 - 10 * local_difficulty
    softlock_check = 220
    magic_system = MagicGUI(screen,cursor)
    play_music_loop("Audio/PuppetStrings.mp3")
    play_music_loop("Audio/PuppetMaster.mp3")
    no_noise = pygame.mixer.Sound("Audio/silent_snd.mp3")
    fire_noise = pygame.mixer.Sound("Audio/fire_snd.mp3")
    ice_noise = pygame.mixer.Sound("Audio/ice_snd.mp3")
    ele_noise = pygame.mixer.Sound("Audio/electric_snd.mp3")
    soundsgroup = {
        0: no_noise,
        1: fire_noise,
        2: ice_noise,
        3: ele_noise,
        4: no_noise
    }
    for sound in soundsgroup.values():
        sound.set_volume(0.3)
    bar_width_max = 500
    bar_height = 36
    bar_pos = (0, 0)
    bar_value = 100
    score_play = 0
    wave_counter = 1
    enemy = []
    dots = []
    spawn_trigger = True
    last_wave = True
    magic_level=0
    mega_mage_state = False
    current_power = 0
    last_power = 0
    target_score = [ 0, 15 + 5 * local_difficulty , 990 + 10 * local_difficulty, 5400 + 600 * local_difficulty, 8000 + 2000 * local_difficulty, "INF"]
    while running:
        click_sound = soundsgroup[current_power]
        char_pos.x = cursor.pos.x
        if wave_counter == 1 and score_play > 15 + 5 * local_difficulty :
            wave_counter += 1
            spawn_trigger = True
        if wave_counter == 2 and score_play > 990 + 10 * local_difficulty :
            wave_counter += 1
            spawn_trigger = True
        if wave_counter == 3 and score_play > 5400 + 600 * local_difficulty :
            wave_counter += 1
            spawn_trigger = True
        if wave_counter == 4 and score_play > 8000 + 2000 * local_difficulty :
            wave_counter += 1
            spawn_trigger = True
        if wave_counter == 5 and last_wave == True :
            spawn_trigger = True
        if wave_counter == 1 and spawn_trigger:
            for i in range(1, 10):
                enemy.append(wnb_monster.Pigeon(random.randint(0, screen_width - 100), 800, 1, 1, tip="bird"))
            spawn_trigger = False
        if wave_counter == 2 and spawn_trigger:
            for i in range(1, 4):
                enemy.append(wnb_monster.TopHat(random.randint(0, screen_width - 100), 0, 1, tip="hatter"))
            spawn_trigger = False
        if wave_counter == 3 and spawn_trigger:
            enemy.append(wnb_monster.HoodedWiz(screen_width - 600, screen_height , 2, 1, tip="boss"))
            pygame.mixer.music.stop()
            play_music_loop("Audio/PuppetMaster.mp3")
            spawn_trigger = False
        if wave_counter == 4 and spawn_trigger:
            for i in range(1, 4):
                enemy.append(wnb_monster.TopHat(random.randint(0, screen_width - 100), 0, 1, tip="hatter"))
            spawn_trigger = False
        if wave_counter == 5 and spawn_trigger:
            last_wave = False
            enemy.append(wnb_monster.HoodedWiz(screen_width - 600, screen_height, 1, 1, tip="boss"))
            enemy.append(wnb_monster.HoodedWiz(screen_width - 400, screen_height , 3, 1, tip="boss"))
            pygame.mixer.music.stop()
            play_music_loop("Audio/PuppetMaster.mp3")
            spawn_trigger = False
        if cursor.active:
            mouse_held_last_frame = 0
        else:
            mouse_held_last_frame = 1
        if cursor.active and not mouse_held_last_frame:
            click_sound.play()
            dots.append([cursor.rect.center, 20])

        for dot in dots[:]:
            dot[1] -= 1
            if dot[1] <= 0:
                dots.remove(dot)

        current_power = magic_system.loaded_spell
        if (last_power != 0) and (current_power != last_power):
            mega_mage_state, magic_level = boosted(magic_level)
        last_power = current_power
        score_play, bar_value = handle_monster_clicks(enemy, cursor, current_power, score_play, bar_value)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.key.get_pressed()[pygame.K_x]:
            magic_system.is_active= False
        if pygame.key.get_pressed()[pygame.K_z] and bar_value > 10:
            magic_system.is_active = True
        if pygame.key.get_pressed()[pygame.K_t]:
            timer = 1
        if bar_value > 500 :
            bar_value = 500
        for monster in enemy:
            if monster.tip=="boss":
                if monster.ai_value==2:
                    evil_laugh.play()
                    monster.ai_value = 0
                    if wnb_monster.HoodedWiz.HATCAP < 2 * wave_counter :
                        enemy.append(wnb_monster.TopHat(monster.rect.x, monster.rect.y + 200 ,1,tip="hatter"))
                elif monster.is_active:
                    score_play -= 1
                elif not monster.is_active:
                    monster.remove()
            monster.update()
        screen.blit(background_play, (0, 0))
        for pos, _ in dots:
            screen.blit(ability_image[current_power], pos)
        #draw background first
        draw_power(current_power)
        draw_text(screen, f"SCORE: {score_play} / {target_score[wave_counter]}", score_x, score_y )
        draw_text(screen, f"WAVE: {wave_counter}", wave_x, wave_y)
        draw_text(screen, f"TIME {timer}", wave_x, time_y)

        for monster in enemy:
            monster.draw(screen)
        if bar_value < 1 :
            magic_system.is_active = False
            magic_level = 0
            mega_mage_state = False
        if magic_system.is_active:
            if mega_mage_state :
                player_avatar = player_image[2]
                score_play += 3
                bar_value -= 1
            else:
                player_avatar = player_image[1]
            magic_system.update()
            magic_system.draw()
        else:
            if mega_mage_state :
                player_avatar = player_image[2]
            else:
                player_avatar = player_image[0]
        update_and_draw_cursor()
        level_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if level_time - timer_update_time > 1000:
            timer_update_time = level_time
            timer -= 1
            if timer <= 0:
                timer=120
                pygame.mixer.music.stop()
                print (f' {score_play}')
                update_scores("GUI\highscores.dat", score_play)
                score_play=0
                running=False
                main_menu()
            if timer == softlock_check and timer > 10:
                softlock_check -= 20
                enemy.append(wnb_monster.TopHat( screen_width//2 , 0, 1, tip="hatter"))
        if current_time - last_update_time >= 500:
            last_update_time = current_time
            if magic_system.is_active:
                bar_value = max(bar_value -10 , 0)
            elif bar_value < 500 and not mega_mage_state :
                bar_value = max(bar_value +5 , 0)
        # Draw red background bar
        pygame.draw.rect(screen, (255, 0, 0), (*bar_pos, bar_width_max, bar_height))
        # Draw blue foreground bar
        pygame.draw.rect(screen, (0, 0, 255), (*bar_pos, bar_value, bar_height))

        """PLAYER CHARACTER"""
            # Draw character (simple circle)
        screen.blit(player_avatar, (int(char_pos.x), int(char_pos.y - 256 )))
        if mega_mage_state:
            draw_claws(screen, cursor.pos, clawL, clawR , cursor.active)
        pygame.display.flip() #update the display
    pygame.quit()
# The mana bar drawing function outside of play()
def draw_power(powerup):
    screen.blit(ability_image[powerup], (700, 32))
    if powerup == 4 :
        draw_text(screen, f"none", 850, 64)
    if powerup == 1 :
        draw_text(screen, f"fire", 850, 64)
    if powerup == 2 :
        draw_text(screen, f"ice", 850, 64)

    if powerup == 3 :
        draw_text(screen, f"electric", 850, 64)
def boosted(magic_level):
    magic_level += 1
    if magic_level >= 3:
        return True, magic_level
    return False, magic_level

def draw_claws(screen, cursor_pos, image1, image2, is_clicked):
    x, y = cursor_pos
    tick=pygame.time.get_ticks()
    # Idle bobbing motion
    offset = math.sin(tick * 0.01) * 60  # oscillate with sine wave
    pos1 = (x - 350, y - 30 + offset)
    pos2 = (x + 350, y - 30 - offset)
    screen.blit(image1, pos1)
    screen.blit(image2, pos2)

def read_scores(filename):
    scores = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                try:
                    score_str, date_str = line.strip().split()
                    scores.append((int(score_str), date_str))
                except ValueError:
                    continue  # skip malformed lines
    return sorted(scores, reverse=True)[:10]

def update_scores(filename, scoreval):
    today = date.today().isoformat()
    scores = read_scores(filename)

    # Add new score and sort
    scores.append((scoreval, today))
    scores = sorted(scores, reverse=True)[:10]

    # Write back to file
    with open(filename, 'w') as f:
        for score, date_str in scores:
            f.write(f"{score} {date_str}\n")

def handle_monster_clicks(enemy_list, point, current_power, score, mana):
    mouse_pressed = pygame.mouse.get_pressed()
    if not mouse_pressed[0]:
        return score, mana  # Skip if left mouse not clicked

    monsters_to_remove = []

    for monster in enemy_list:
        # Handle direct monster click
        if monster.check_collision(point) and monster.check_criteria(current_power):
            if monster.tip == "bird":
                score += 5
                mana += 20
                wnb_monster.TopHat.BIRDS -= 1
            elif monster.tip == "hatter":
                score += 50
                mana -= 50
                wnb_monster.HoodedWiz.HATCAP -= 1
            elif monster.tip == "boss":
                score += 1000
                mana -= 80
                evil_death.play()
            if not monster.is_active:
                monsters_to_remove.append(monster)

        # Handle TopHat's bird interactions
        if monster.tip == "hatter":
            for bird in monster.birds:
                if bird.is_active and bird.check_collision(point):
                    score += 25 * bird.get_ritual()
                    mana += 10
                    bird.check_criteria("A")
                    wnb_monster.TopHat.BIRDS -= 1#

    # Remove inactive monsters
    for m in monsters_to_remove:
        if m in enemy_list:
            enemy_list.remove(m)

    return score, mana
def play_music_loop(file_path):
    volume = 0.2
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)  # Volume: 0.0 to 1.0
    pygame.mixer.music.play(-1)

# GameController class for managing states
class GameController:
    def __init__(self):
        self.state = "main_menu"  # Start with the main menu

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        if self.state == "main_menu":
            main_menu()
        elif self.state == "settings":
            settings()
        elif self.state == "play":
            play()
        elif self.state == "Info":
            info_menu()
        elif self.state == "scores":
            scoreboard()

    def change_state(self, new_state):
        self.state = new_state

if __name__ == "__main__":
    game_controller = GameController()
    while True:
        game_controller.handle_events()
        game_controller.update()
