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
    print(f"Sprite sheet dimensions: {sheet_rect.width}x{sheet_rect.height}")
    frames = []
    for y in range(0, sheet_rect.height, frame_height):
        for x in range(0, sheet_rect.width, frame_width):
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            print(
                f"Extracting frame at: x={x}, y={y}, width={frame_width}, height={frame_height}"
            )
            if frame_rect.right <= sheet_rect.width and frame_rect.bottom <= sheet_rect.height:
                frames.append(sheet.subsurface(frame_rect))
    return frames

def main_game():
    pygame.init()
    mixer.init()

    try:
        mixer.music.load("assets/music/greenlands.mp3")
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading background music: {e}")
        pygame.quit()
        return

    try:
        icon_image = pygame.image.load('icon.png')
        pygame.display.set_icon(icon_image)
    except pygame.error as e:
        print(f"Error loading icon image: {e}")
        pygame.quit()
        return

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    def load_image(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading {path}: {e}")
            pygame.quit()
            return None

    idle_down_sprite_sheet = load_image(
        "assets/charater/idle/playerdownidle.png")
    idle_lr_sprite_sheet = load_image(
        "assets/charater/idle/playerleftrightidle.png")
    idle_up_sprite_sheet = load_image("assets/charater/idle/playerupidle.png")
    walk_down_sprite_sheet = load_image(
        "assets/charater/moving/playerwalkdown.png")
    walk_lr_sprite_sheet = load_image(
        "assets/charater/moving/playerrightandleftwalk.png")
    walk_up_sprite_sheet = load_image(
        "assets/charater/moving/playerupwalk.png")
    slash_sprite_sheet = load_image(
        "assets/charater/slash/playerdownslash.png")

    if not all([
            idle_down_sprite_sheet, idle_lr_sprite_sheet, idle_up_sprite_sheet,
            walk_down_sprite_sheet, walk_lr_sprite_sheet, walk_up_sprite_sheet,
            slash_sprite_sheet
    ]):
        print("Error: One or more sprite sheets failed to load.")
        return

    idle_down_frames = load_sprite_sheet(idle_down_sprite_sheet, 48, 30)
    idle_lr_frames = load_sprite_sheet(idle_lr_sprite_sheet, 48, 30)
    idle_up_frames = load_sprite_sheet(idle_up_sprite_sheet, 48, 30)
    walk_down_frames = load_sprite_sheet(walk_down_sprite_sheet, 48, 30)
    walk_lr_frames = load_sprite_sheet(walk_lr_sprite_sheet, 48, 30)
    walk_lr_frames_flipped = [
        pygame.transform.flip(frame, True, False) for frame in walk_lr_frames
    ]
    walk_up_frames = load_sprite_sheet(walk_up_sprite_sheet, 48, 30)

    slash_frames = load_sprite_sheet(slash_sprite_sheet, 48, 29)

    if len(slash_frames) == 0:
        print("Error: No frames found in slash sprite sheet.")
        return

    scale_factor = 2

    def scale_frames(frames, factor):
        return [
            pygame.transform.scale(
                frame,
                (frame.get_width() * factor, frame.get_height() * factor))
            for frame in frames
        ]

    idle_down_frames = scale_frames(idle_down_frames, scale_factor)
    idle_lr_frames = scale_frames(idle_lr_frames, scale_factor)
    idle_up_frames = scale_frames(idle_up_frames, scale_factor)
    walk_down_frames = scale_frames(walk_down_frames, scale_factor)
    walk_lr_frames = scale_frames(walk_lr_frames, scale_factor)
    walk_lr_frames_flipped = scale_frames(walk_lr_frames_flipped, scale_factor)
    walk_up_frames = scale_frames(walk_up_frames, scale_factor)
    slash_frames = scale_frames(slash_frames, scale_factor)

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
    slash_time_since_last_frame = 0
    slash_animation_speed = 0.41 / len(slash_frames)
    slash_offset = 0  # Offset for slash animation

    slash_offset_updated = False  # Flag to track if slash offset has been updated

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not is_slashing and last_move_direction == 'down':
                        is_slashing = True
                        slash_index = 0
                        slash_time_since_last_frame = 0
                        # Move slash animation down by 7 pixels
                        slash_offset = 7
                        slash_offset_updated = True  # Set flag to True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not is_slashing and last_move_direction == 'down':
                        is_slashing = True
                        slash_index = 0
                        slash_time_since_last_frame = 0
                        # Move slash animation down by 7 pixels
                        slash_offset = 7
                        slash_offset_updated = True  # Set flag to True

        screen.fill("blue")

        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0

        if not is_slashing:
            if keys[pygame.K_w] and player_rect.top > 0:
                move_y -= move_speed * dt
                last_move_direction = 'up'
            if keys[pygame.K_s] and player_rect.bottom < screen.get_height():
                move_y += move_speed * dt
                last_move_direction = 'down'
            if keys[pygame.K_a] and player_rect.left > 0:
                move_x -= move_speed * dt
                last_move_direction = 'left'
            if keys[pygame.K_d] and player_rect.right < screen.get_width():
                move_x += move_speed * dt
                last_move_direction = 'right'

        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071

        player_rect.x += move_x
        player_rect.y += move_y

        if is_slashing:
            slash_time_since_last_frame += dt
            if slash_time_since_last_frame >= slash_animation_speed:
                slash_time_since_last_frame = 0
                if slash_index < len(slash_frames):
                    current_image = slash_frames[slash_index]
                    slash_index += 1
                else:
                    is_slashing = False
                    slash_offset = 0  # Reset slash offset when animation ends
                    slash_offset_updated = False  # Reset flag
        else:
            # Reset slash offset if it's been updated and not slashing
            if slash_offset_updated:
                slash_offset = 0
                slash_offset_updated = False  # Reset flag

        if not is_slashing:
            if move_x == 0 and move_y == 0:
                idle_time_since_last_frame += dt
                if idle_time_since_last_frame >= idle_animation_speed:
                    idle_time_since_last_frame = 0
                    idle_player_index = (idle_player_index + 1) % len(
                        idle_down_frames if last_move_direction ==
                        'down' else idle_up_frames if last_move_direction ==
                        'up' else idle_lr_frames)

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
                    walk_time_since_last_frame = 0
                    walk_player_index = (walk_player_index + 1) % len(
                        walk_down_frames if last_move_direction ==
                        'down' else walk_lr_frames if last_move_direction in
                        ['left', 'right'] else walk_up_frames)

                if last_move_direction == 'down':
                    current_image = walk_down_frames[walk_player_index]
                elif last_move_direction == 'up':
                    current_image = walk_up_frames[walk_player_index]
                elif last_move_direction == 'left':
                    current_image = walk_lr_frames_flipped[walk_player_index]
                else:
                    current_image = walk_lr_frames[walk_player_index]

        # Adjust position based on slash offset
        screen.blit(current_image, (player_rect.x, player_rect.y + slash_offset))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main_game()