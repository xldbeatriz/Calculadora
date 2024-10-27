import pygame
import random

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Dinossauro")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 40
        self.velocity_y = 0
        self.on_ground = True
        self.jump_count = 0  # Contador para os pulos

    def update(self):
        keys = pygame.key.get_pressed()

        # Lógica de pulo
        if keys[pygame.K_SPACE]:
            if self.on_ground:  # Se está no chão, faz o primeiro pulo
                self.velocity_y = -10  # Pulo normal
                self.on_ground = False
                self.jump_count = 1  # Primeiro pulo
            elif self.jump_count == 1:  # Se já está no ar e pode fazer o segundo pulo
                self.velocity_y = -20  # Pulo mais alto para passar obstáculos
                self.jump_count += 1  # Incrementa o contador de pulos

        # Gravidade
        self.velocity_y += 1  # Aumenta a velocidade para simular gravidade
        self.rect.y += self.velocity_y
        
        # Verifica se o jogador está no chão
        if self.rect.y >= HEIGHT - 40:
            self.rect.y = HEIGHT - 40
            self.on_ground = True
            self.velocity_y = 0
            self.jump_count = 0  # Reseta o contador ao tocar o chão

# Classe do Obstáculo (Cacto)
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - 40

    def update(self):
        self.rect.x -= 5  # Move o cacto para a esquerda
        if self.rect.x < -20:
            self.rect.x = WIDTH + random.randint(0, 100)  # Reposiciona o cacto

# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    player = Player()
    all_sprites = pygame.sprite.Group()
    cacti = pygame.sprite.Group()
    all_sprites.add(player)

    for _ in range(5):  # Adiciona 5 cactos
        cactus = Cactus()
        all_sprites.add(cactus)
        cacti.add(cactus)

    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    
    while True:  # Loop principal do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if game_over and event.type == pygame.KEYDOWN:
                # Reinicia o jogo se o jogador pressionar uma tecla
                if event.key == pygame.K_SPACE:
                    main()  # Reinicia o jogo
                    return

        if not game_over:
            # Atualiza
            all_sprites.update()

            # Verifica colisões
            if pygame.sprite.spritecollideany(player, cacti):
                game_over = True  # Finaliza o jogo em caso de colisão

            # Atualiza a pontuação
            score += 1  # Aumenta a pontuação a cada iteração do loop

        # Desenha
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Mostra a pontuação
        score_text = f"Pontos: {score}"
        text_surface = font.render(score_text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        # Se o jogo estiver acabado, mostra a tela de Game Over
        if game_over:
            game_over_text = "GAME OVER! Pressione Espaço para reiniciar."
            go_surface = font.render(game_over_text, True, WHITE)
            screen.blit(go_surface, (WIDTH // 2 - go_surface.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
