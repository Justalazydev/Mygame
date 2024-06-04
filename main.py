import pygame
import time
from pygame import mixer
"""
def fake_installation():
    pygame.init()
    icon_image = pygame.image.load(icon.png')
    pygame.display.set_icon(icon_image)
    width, height = 800, 200
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Installation Progress")

    black = (0, 0, 0)
    white = (255, 255, 255)

    progress_font = pygame.font.SysFont(None, 36)

    completion_font = pygame.font.SysFont(None, 48)

    running = True
    progress = 0

    while running and progress <= 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)

        message = f"Installing mithical woods {progress}% complete"
        text = progress_font.render(message, True, white)
        screen.blit(text, (50, height // 2 - text.get_height() // 2))

        pygame.display.flip()

        time.sleep(1)
        progress += 5

    screen.fill(black)
    completion_message = "               Installation complete!"
    completion_text = completion_font.render(completion_message, True, white)
    screen.blit(completion_text, (50, height // 2 - completion_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)

    screen.fill(black)
    completion_message = "               Installation complete!"
    completion_text = completion_font.render(completion_message, True, white)
    screen.blit(completion_text, (50, height // 2 - completion_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
"""


def load_sprite_sheet(sheet, frame_width, frame_height):
    sheet_rect = sheet.get_rect()
    frames = []
    for y in range(0, sheet_rect.height, frame_height):
        for x in range(0, sheet_rect.width, frame_width):
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            if frame_rect.right <= sheet_rect.width and frame_rect.bottom <= sheet_rect.height:
                frames.append(sheet.subsurface(frame_rect))
    return frames


def main_game():
    pygame.init()
    mixer.init()
    mixer.music.load("assets/music/greenlands.mp3")
    mixer.music.set_volume(1)
    mixer.music.play(-1)
    greenland = pygame.mixer.Sound("assets/music/greenlands.mp3")
    greenland.play()
    icon_image = pygame.image.load('icon.png')
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Load sprite sheets
    idle_down_sprite_sheet = pygame.image.load(
        "assets/charater/idle/playerdownidle.png").convert_alpha()
    idle_lr_sprite_sheet = pygame.image.load(
        "assets/charater/idle/playerleftrightidle.png").convert_alpha()
    idle_up_sprite_sheet = pygame.image.load(
        "assets/charater/idle/playerupidle.png").convert_alpha()
    walk_down_sprite_sheet = pygame.image.load(
        "assets/charater/moving/playerwalkdown.png").convert_alpha()
    walk_lr_sprite_sheet = pygame.image.load(
        "assets/charater/moving/playerrightandleftwalk.png").convert_alpha()
    walk_up_sprite_sheet = pygame.image.load(
        "assets/charater/moving/playerupwalk.png").convert_alpha()
    slash_sprite_sheet = pygame.image.load(
        "assets/charater/slash/playerdownslash.png").convert_alpha(
        )  # Load slash sprite sheet

    # Process sprite sheets into frames
    idle_down_frames = load_sprite_sheet(idle_down_sprite_sheet, 48, 30)
    idle_lr_frames = load_sprite_sheet(idle_lr_sprite_sheet, 48, 30)
    idle_up_frames = load_sprite_sheet(idle_up_sprite_sheet, 48, 30)
    walk_down_frames = load_sprite_sheet(walk_down_sprite_sheet, 48, 30)
    walk_lr_frames = load_sprite_sheet(walk_lr_sprite_sheet, 48, 30)
    walk_lr_frames_flipped = [
        pygame.transform.flip(frame, True, False) for frame in walk_lr_frames
    ]
    walk_up_frames = load_sprite_sheet(walk_up_sprite_sheet, 48, 30)
    slash_frames = load_sprite_sheet(slash_sprite_sheet, 48, 30)

    scale_factor = 2
    idle_down_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in idle_down_frames
    ]
    idle_lr_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in idle_lr_frames
    ]
    idle_up_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in idle_up_frames
    ]
    walk_down_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in walk_down_frames
    ]
    walk_lr_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in walk_lr_frames
    ]
    walk_lr_frames_flipped = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in walk_lr_frames_flipped
    ]
    walk_up_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in walk_up_frames
    ]
    slash_frames = [
        pygame.transform.scale(frame, (frame.get_width() * scale_factor,
                                       frame.get_height() * scale_factor))
        for frame in slash_frames
    ]  # Scale slash frames

    # Initialize player settings
    player_rect = pygame.Rect(screen.get_width() / 2,
                              screen.get_height() / 2, 50, 100)
    move_speed = 150

    idle_player_index = 0
    idle_time_since_last_frame = 0
    idle_animation_speed = 0.2
    walk_player_index = 0
    walk_time_since_last_frame = 0
    walk_animation_speed = 0.1
    last_move_direction = 'down'
    is_slashing = False
    slash_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Trigger slash animation
                    is_slashing = True
                    slash_index = 0
        screen.fill("blue")

        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0

        if keys[pygame.K_w] and player_rect.top > 0:
            move_y -= move_speed
            last_move_direction = 'up'
        if keys[pygame.K_s] and player_rect.bottom < screen.get_height():
            move_y += move_speed
            last_move_direction = 'down'
        if keys[pygame.K_a] and player_rect.left > 0:
            move_x -= move_speed
            last_move_direction = 'left'
        if keys[pygame.K_d] and player_rect.right < screen.get_width():
            move_x += move_speed
            last_move_direction = 'right'

        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071

        player_rect.x += move_x * dt
        player_rect.y += move_y * dt

        if is_slashing:
            if slash_index < len(slash_frames):
                current_image = slash_frames[slash_index]
                slash_index += 1
            else:
                is_slashing = False
        elif move_x == 0 and move_y == 0:
            idle_time_since_last_frame += dt
            if idle_time_since_last_frame >= idle_animation_speed:
                idle_player_index = (idle_player_index + 1) % len(
                    idle_down_frames if last_move_direction ==
                    'down' else idle_up_frames if last_move_direction ==
                    'up' else idle_lr_frames)
                idle_time_since_last_frame = 0

            if last_move_direction == 'down':
                current_image = idle_down_frames[idle_player_index]
            elif last_move_direction == 'up':
                current_image = idle_up_frames[idle_player_index]
            else:
                current_image = idle_lr_frames[idle_player_index]
                if last_move_direction == 'left':
                    current_image = pygame.transform.flip(
                        current_image, True, False)

        else:
            walk_time_since_last_frame += dt
            if walk_time_since_last_frame >= walk_animation_speed:
                walk_player_index = (walk_player_index + 1) % len(
                    walk_down_frames if last_move_direction ==
                    'down' else walk_lr_frames if last_move_direction in
                    ['left', 'right'] else walk_up_frames)
                walk_time_since_last_frame = 0

            if last_move_direction == 'down':
                current_image = walk_down_frames[walk_player_index]
            elif last_move_direction == 'up':
                current_image = walk_up_frames[walk_player_index]
            elif last_move_direction == 'left':
                current_image = walk_lr_frames_flipped[walk_player_index]
            else:
                current_image = walk_lr_frames[walk_player_index]

        screen.blit(current_image, player_rect.topleft)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


pygame.quit()

if __name__ == "__main__":
    main_game()
