import pygame
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

OPTIONS = ['pedra', 'papel', 'tesoura']

WIN_CONDITIONS = {
    'pedra': 'tesoura',
    'papel': 'pedra',
    'tesoura': 'papel'
}

WIDTH, HEIGHT = 600, 600
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pedra, Papel, Tesoura')
clock = pygame.time.Clock()

gestures_images = {
    'pedra': pygame.transform.scale(pygame.image.load('pedra.png').convert_alpha(), (200, 200)),
    'papel': pygame.transform.scale(pygame.image.load('papel.png').convert_alpha(), (200, 200)),
    'tesoura': pygame.transform.scale(pygame.image.load('tesoura.png').convert_alpha(), (200, 200))
}

heart_image = pygame.transform.scale(pygame.image.load('coracao.png').convert_alpha(), (30, 30))
win_sound = pygame.mixer.Sound('vitoria.wav')
lose_sound = pygame.mixer.Sound('derrota.wav')
draw_sound = pygame.mixer.Sound('empate.wav')

font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 50)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_button(text, font, color, bg_color, surface, x, y, width, height):
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x + width/2, y + height/2))
    surface.blit(text_obj, text_rect)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Empate"
    elif WIN_CONDITIONS[user_choice] == computer_choice:
        return "Você venceu!"
    else:
        return "Você perdeu!"

def main():
    user_choice = None
    computer_choice = None
    result_message = None

    player_lives = 3
    computer_lives = 3

    while True:
        window.fill(WHITE)  
        for i in range(player_lives):
            window.blit(heart_image, (20 + i * 40, 20))

        for i in range(computer_lives):
            window.blit(heart_image, (WIDTH - 50 - i * 40, 20))
        
        if user_choice is None:
            button_width, button_height = 150, 50
            total_width = len(OPTIONS) * button_width + (len(OPTIONS) - 1) * 20
            start_x = CENTER_X - total_width / 2
            button_y = CENTER_Y + 200
            draw_text(f"ESCOLHA UMA OPÇÃO PARA JOGAR",  font, BLACK, window, CENTER_X, CENTER_Y)

            for idx, option in enumerate(OPTIONS):
                draw_button(option, font, BLACK, GRAY, window, start_x + idx * (button_width + 20), button_y, button_width, button_height)

        else:
            draw_text(f"Você escolheu {user_choice}", font, BLACK, window, CENTER_X, CENTER_Y - 150)
            draw_text(f"O computador escolheu {computer_choice}", font, BLACK, window, CENTER_X, CENTER_Y + 50)
            window.blit(gestures_images[user_choice], (CENTER_X - 250, CENTER_Y - 150))
            window.blit(gestures_images[computer_choice], (CENTER_X + 50, CENTER_Y - 150))
            button_width, button_height = 150, 50
            total_width = len(OPTIONS) * button_width + (len(OPTIONS) - 1) * 20
            start_x = CENTER_X - total_width / 2
            button_y = CENTER_Y + 200

            for idx, option in enumerate(OPTIONS):
                    draw_button(option, font, BLACK, GRAY, window, start_x + idx * (button_width + 20), button_y, button_width, button_height)

            if result_message:
                draw_text(result_message, font, BLACK, window, CENTER_X, CENTER_Y + 150)

        pygame.display.update()  # Atualize a tela

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for idx, option in enumerate(OPTIONS):
                    button_rect = pygame.Rect(CENTER_X - total_width / 2 + idx * (button_width + 20), button_y, button_width, button_height)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        user_choice = option
                        computer_choice = random.choice(OPTIONS)
                        result_message = determine_winner(user_choice, computer_choice)

                        if result_message == "Você venceu!":
                            win_sound.play()
                            computer_lives -= 1
                        elif result_message == "Você perdeu!":
                            lose_sound.play()
                            player_lives -= 1
                        elif result_message == "Empate":
                            draw_sound.play()
                        if player_lives == 0 or computer_lives == 0:                            
                            window.fill(WHITE)
                            draw_text(result_message, font2, RED, window, CENTER_X, CENTER_Y - 200)
                            if result_message == "Você venceu!":
                                draw_text(f"Você escolheu {user_choice}", font, BLACK, window, CENTER_X, CENTER_Y - 150)
                                draw_text(f"O computador escolheu {computer_choice}", font, BLACK, window, CENTER_X, CENTER_Y + 50)
                                window.blit(gestures_images[user_choice], (CENTER_X - 250, CENTER_Y - 150))
                                window.blit(gestures_images[computer_choice], (CENTER_X + 50, CENTER_Y - 150))
                            elif result_message == "Você perdeu!":
                                draw_text(f"Você escolheu {user_choice}", font, BLACK, window, CENTER_X, CENTER_Y - 150)
                                draw_text(f"O computador escolheu {computer_choice}", font, BLACK, window, CENTER_X, CENTER_Y + 50)
                                window.blit(gestures_images[computer_choice], (CENTER_X - 250, CENTER_Y - 150))
                                window.blit(gestures_images[user_choice], (CENTER_X + 50, CENTER_Y - 150))
                            
                            pygame.display.update()
                            pygame.time.wait(7000)  
                            user_choice = None
                            computer_choice = None
                            result_message = None
                            player_lives = 3
                            computer_lives = 3
                            break

        if player_lives == 0 or computer_lives == 0:
            continue 

if __name__ == "__main__":
    main()

