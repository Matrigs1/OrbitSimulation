import pygame
from pygame.locals import *
from sys import exit
import math
import pygame_gui
from pygame_gui.elements import UIButton

# Inicializando o pygame
pygame.init()

#Cores a serem utilizadas
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
AZUL = (100, 149, 237)
VERMELHO = (188, 39, 50)
CINZA_ESCURO = (80, 78, 81)

FONTE = pygame.font.SysFont("arial", 16)

# Setando a largura e a altura da tela, respectivamente.
LARGURA, ALTURA = 1280, 920
# Passando a largura e altura para o display.
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Órbita")

# Classe que os objetos (planetas), serão instanciados.
class Planeta:
    # Unidade de medida, que representa os kilometros da terra pro sol. Transformado em metros.
    AU = 149.6e6 * 1000
    # Constante gravitacional. É usado para achar a força de atração entre objetos.
    G = 6.67428e-11
    # Escalando os valores reais físicos para os pixels da janela. 1 AU é equivalente a 100 pixels.
    ESCALA = 250 / AU
    # Tempo que a simulação irá evoluir. Equivalente a 1 dia.
    INTERVALO_TEMPO = 3600*24

    def __init__(self, nome, x, y, raio, cor, massa):
        self.nome = nome
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa

        self.orbita = []
        self.sol = False
        self.distancia_sol = 0
        self.volta_completa = False
        self.anos = 0
        self.pausado = False

        # Velocidades do eixo x e y. Para que haja uma circulação dos planetas, os dois eixos precisam ser incrementados simultaneamente. Em relação ao sol.
        self.x_vel = 0
        self.y_vel = 0

    # Desenha os planetas na tela
    def desenhar(self, win):
        x = self.x * self.ESCALA + LARGURA / 2
        y = self.y * self.ESCALA + ALTURA / 2

        if len(self.orbita) > 2:
            atualizar_pontos = []
            for ponto in self.orbita:
                x, y = ponto
                x = x * self.ESCALA + LARGURA / 2
                y = y * self.ESCALA + ALTURA / 2
                atualizar_pontos.append((x, y))

            pygame.draw.lines(win, self.cor, False, atualizar_pontos, 2)

        pygame.draw.circle(win, self.cor, (x, y), self.raio)
        
        if not self.sol:
            distancia_texto = FONTE.render(f"{ self.nome } - Distância do sol: { round(self.distancia_sol/1000, 1) }km - Anos: {self.anos}", 1, BRANCO)
            win.blit(distancia_texto, (x - distancia_texto.get_width()/2, y - distancia_texto.get_height()/2))

    # Define a atração dos planetas.
    def atracao(self, outro):
        outro_x, outro_y = outro.x, outro.y
        distancia_x = outro_x - self.x
        distancia_y = outro_y - self.y
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)

        if outro.sol:
            self.distancia_sol = distancia

        forca = self.G * self.massa * outro.massa / distancia**2
        theta = math.atan2(distancia_y, distancia_x)
        forca_x = math.cos(theta) * forca
        forca_y = math.sin(theta) * forca
        return forca_x, forca_y

    # Atualiza a posição e a velocidade.
    def atualizar_posicao(self, planetas):
        total_fx = total_fy = 0
        for Planeta in planetas:
            if self == Planeta:
                continue

            fx, fy = self.atracao(Planeta)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.massa * self.INTERVALO_TEMPO
        self.y_vel += total_fy / self.massa * self.INTERVALO_TEMPO

        self.x += self.x_vel * self.INTERVALO_TEMPO
        self.y += self.y_vel * self.INTERVALO_TEMPO
        self.orbita.append((self.x, self.y))

        if len(self.orbita) > 2:
            # Calcula o vetor posição inicial
            vetor_inicial = pygame.Vector2(self.orbita[0])
            # Calcula o vetor posição atual
            vetor_atual = pygame.Vector2(self.x, self.y)

            # Calcula o ângulo entre os dois vetores em radianos
            angulo = vetor_atual.angle_to(vetor_inicial)

            # Verifica se o ângulo é próximo de um ciclo completo
            if 0 <= angulo < 10 and not self.volta_completa:
                self.anos += 1
                self.volta_completa = True
            elif angulo >= 10:
                self.volta_completa = False

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

# Controlar estado da simulação
simulacao_pausada = False

def pausar_simulacao(planetas):
    for planeta in planetas:
        planeta.pausado = True

def resumir_simulacao(planetas):
    for planeta in planetas:
        planeta.pausado = False

# Função principal
def main():
    rodar = True
    frames = pygame.time.Clock()
    
    #Inicializando planetas
    sol = Planeta("Sol", 0, 0, 30, AMARELO, 1.98892 * 10**30)
    sol.sol = True

    terra = Planeta("Terra", -1 * Planeta.AU, 0, 16, AZUL, 5.9742 * 10**24)
    terra.y_vel = 29.783 * 1000 

    marte = Planeta("Marte", -1.524 * Planeta.AU, 0, 12, VERMELHO, 6.39 * 10**23)
    marte.y_vel = 24.077 * 1000

    mercurio = Planeta("Mercúrio", 0.387 * Planeta.AU, 0, 8, CINZA_ESCURO, 3.30 * 10**23)
    mercurio.y_vel = -47.4 * 1000

    venus = Planeta("Venus", 0.723 * Planeta.AU, 0, 14, BRANCO, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planetas = [sol, terra, marte, mercurio, venus]
 
    # Inicializando pygame_gui
    gui = pygame_gui.UIManager((LARGURA, ALTURA))
    
    # Criando uma caixa branca ao redor do slider
    slider_box = pygame.Rect(20, 20, 200, 30)

    # Criando um slider de velocidade
    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect = slider_box,
        start_value = 0.1,
        value_range = (0.1, 20.0),
        manager = gui,
    )
    slider_label = pygame_gui.elements.UILabel(
        relative_rect = pygame.Rect((20, 50), (200, 30)),
        text = "Velocidade: 1x",
        manager = gui,
    )

    botao_pausar = UIButton(
    relative_rect=pygame.Rect((240, 20), (100, 30)),
    text="Pausar",
    manager=gui
    )

    botao_resumir = UIButton(
    relative_rect=pygame.Rect((350, 20), (100, 30)),
    text="Resumir",
    manager=gui
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
                    for planeta in planetas:
                        planeta.INTERVALO_TEMPO *= velocidade_rotacao
                        slider_label.set_text(f"Velocidade: {velocidade_rotacao}x")

                # Processando eventos de botões
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == slider.left_button:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, ui_element=slider))
                    elif event.ui_element == slider.right_button:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, ui_element=slider))
                    elif event.ui_element == botao_pausar:
                        pausar_simulacao(planetas)
                    elif event.ui_element == botao_resumir:
                        resumir_simulacao(planetas)

        # Desenhar a imagem de fundo primeiro
        tela.blit(imagem_fundo, (0, 0))

        if not simulacao_pausada:
            for planeta in planetas:
                if not planeta.pausado:
                    planeta.atualizar_posicao(planetas)
                planeta.desenhar(tela)

        # Atualizar a GUI
        gui.update(1 / 60.0)
        gui.draw_ui(tela)

        pygame.display.flip()

    pygame.quit()
    exit()

main()