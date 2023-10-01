import pygame
from pygame.locals import *
from sys import exit
import math
import pygame_gui

# Inicializando o pygame
pygame.init()

# Setando a largura e a altura da tela, respectivamente.
LARGURA, ALTURA = 1280, 720
PRETO = (0, 0, 0)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Órbita")

# Classe que os objetos (planetas), serão instanciados.
class Planeta:
    def __init__(self, x, y, raio_orbita, raio, cor, massa):
        self.x = x
        self.y = y
        self.raio_orbita = raio_orbita
        self.raio = raio
        self.cor = cor
        self.massa = massa
        self.angulo = 0
        self.velocidade_angular = 0.02  # Velocidade inicial
        self.velocidade_maxima = 25.0

    def atualizar_posicao(self):
        self.x = x_sol + self.raio_orbita * math.cos(self.angulo)
        self.y = y_sol + self.raio_orbita * math.sin(self.angulo)
        self.angulo += self.velocidade_angular

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

# Carregando imagens e som
imagem_fundo = pygame.image.load('assets/estrelas.jpg')
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

musica_de_fundo = pygame.mixer.music.load('assets/Interestellar_MainTheme.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sol = pygame.image.load('assets/sol.png').convert_alpha()
sol = pygame.transform.scale(sol, (200, 200))
x_sol = (LARGURA / 2) - 200 / 2
y_sol = (ALTURA / 2) - 200 / 2

# Função principal
def main():
    rodar = True
    frames = pygame.time.Clock()

    # Inicializando planetas
    terra = Planeta(x_sol, y_sol, 250, 10, (0, 0, 255), 1.0)

    # Inicializando pygame_gui
    gui = pygame_gui.UIManager((LARGURA, ALTURA))

    # Criando uma caixa branca ao redor do slider
    slider_box = pygame.Rect(20, 20, 200, 30)

    # Criando um slider de velocidade
    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=slider_box,
        start_value=1.0,
        value_range=(0.1, 25.0),
        manager=gui,
    )
    slider_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, 50), (200, 30)),
        text="Velocidade: 1x",
        manager=gui,
    )

    while rodar:
        frames.tick(60)
        tela.fill(PRETO)

        for event in pygame.event.get():
            if event.type == QUIT:
                rodar = False

            # Processando eventos da GUI
            gui.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Obtendo o valor do slider
                    velocidade_rotacao = slider.get_current_value()
                    terra.velocidade_angular = 0.02 * velocidade_rotacao
                    slider_label.set_text(f"Velocidade: {velocidade_rotacao}x")

                # Processando eventos de botões
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == slider.left_button:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, ui_element=slider))
                    elif event.ui_element == slider.right_button:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, ui_element=slider))

        # Desenhar a imagem de fundo primeiro
        tela.blit(imagem_fundo, (0, 0))

        # Atualizar a posição da Terra
        terra.atualizar_posicao()

        # Desenhar a linha de órbita
        pygame.draw.circle(tela, (255, 255, 255), (int(x_sol), int(y_sol)), 250, 1)

        # Desenhar o planeta Terra
        terra.desenhar(tela)

        tela.blit(sol, (x_sol, y_sol))

        # Atualizar a GUI
        gui.update(1 / 60.0)
        gui.draw_ui(tela)

        pygame.display.flip()

    pygame.quit()
    exit()

main()