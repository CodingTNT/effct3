import pygame
import os
import random
import time

pygame.init()

pygame.mixer.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Switchable Pages with Effects')

assets = [
    {"image": "cleaner.png", "rain_image": "cleaner1.png", "text": "GUESS WHO I AM"},
    {"image": "farmer.png", "rain_image": "farmer1.png", "text": "GUESS WHO I AM"},
    {"image": "cook.png", "rain_image": "cook2.png", "text": "GUESS WHO I AM"}, 
    {"image": "worker.png", "rain_image": "worker2.png", "text": "GUESS WHO I AM"}, 
]
click_sound_path = 'cartoon_pop.flac'


for asset in assets:
    if not os.path.exists(asset["image"]) or not os.path.exists(asset["rain_image"]):
        print(f"找不到文件: {asset['image']} 或 {asset['rain_image']}")
        exit()
if not os.path.exists(click_sound_path):
    print("找不到音效文件!")
    exit()


for asset in assets:
    asset["image"] = pygame.image.load(asset["image"])
    asset["rain_image"] = pygame.image.load(asset["rain_image"])
click_sound = pygame.mixer.Sound(click_sound_path)

font = pygame.font.Font(None, int(0.06 * screen_width))
small_font = pygame.font.Font(None, int(0.04 * screen_width)) 


rain_drops = []

def create_rain(x, y, rain_img_width, rain_img_height):
    num_drops = random.randint(10, 30)  
    for _ in range(num_drops):
        drop_x = x + random.randint(-50, 50)
        drop_y = y
        speed = random.randint(int(0.005 * screen_height), int(0.02 * screen_height))
        rain_drops.append([drop_x, drop_y, speed])


def draw_scene(background_img, rain_img, text, img_width, img_height, rain_img_width, rain_img_height):
    screen.fill((255, 255, 255))
    for x in range(0, screen_width, img_width):
        for y in range(0, screen_height, img_height):
            screen.blit(background_img, (x, y))

    rendered_text = font.render(text, True, (0, 0, 139))
    text_rect = rendered_text.get_rect(center=(screen_width // 2, screen_height // 2))
    pygame.draw.rect(screen, (0, 255, 0), text_rect.inflate(40, 20)) 
    screen.blit(rendered_text, text_rect)
    
    small_text = small_font.render("CLICK!", True, (0, 0, 139))  
    small_text_rect = small_text.get_rect(topleft=(10, 10))  
    small_text_bg_rect = pygame.Rect(
        small_text_rect.x - 10,
        small_text_rect.y - 5,
        small_text_rect.width + 20,
        small_text_rect.height + 10,
    )
    pygame.draw.rect(screen, (0, 255, 0), small_text_bg_rect)  
    screen.blit(small_text, small_text_rect)
 
    for drop in rain_drops[:]:
        drop[1] += drop[2]
        if drop[1] > screen_height:
            rain_drops.remove(drop)
        else:
            screen.blit(rain_img, (drop[0], drop[1]))

running = True
current_stage = 0
start_time = time.time()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            create_rain(mouse_x, mouse_y, 
                        assets[current_stage]["rain_image"].get_width(), 
                        assets[current_stage]["rain_image"].get_height())
            click_sound.play()

 
    if time.time() - start_time > 4:
        start_time = time.time()
        current_stage = (current_stage + 1) % len(assets)
        rain_drops.clear()  

    
    draw_scene(
        assets[current_stage]["image"],
        assets[current_stage]["rain_image"],
        assets[current_stage]["text"],
        assets[current_stage]["image"].get_width(),
        assets[current_stage]["image"].get_height(),
        assets[current_stage]["rain_image"].get_width(),
        assets[current_stage]["rain_image"].get_height(),
    )

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
