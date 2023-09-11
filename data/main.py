import pygame
from pygame.locals import *
from sys import exit

# Inicializando o pygame
pygame.init()

'''
Setando a largura e a altura da tela, respectivamente.
Criando as dimensões da janela.
Adicionando título a janela de jogo.
'''
LARGURA, ALTURA = 1280, 720
PRETO = (0, 0, 0)
CINZA_ESCURO = (71, 74, 81)
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Órbita")

#Colocando imagem de fundo, som e sol.
imagem_fundo = pygame.image.load('assets/estrelas.jpg')
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))

musica_de_fundo = pygame.mixer.music.load('assets/Interestellar_MainTheme.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

sol = pygame.image.load('assets/sol.png').convert_alpha()
sol = pygame.transform.scale(sol, (200, 200))
x_sol = (LARGURA / 2) - 200 / 2
y_sol = (ALTURA / 2) - 200 / 2

# Classe que os objetos (planetas), serão instanciados.
class Planeta:
    def __init__(self, x, y, raio, cor, massa):
        self.x = x
        self.y = y

        self.raio = raio
        self.cor = cor
        self.massa = massa

'''
Função main, que conterá o loop do jogo.
Esse loop também procura por eventos.
'''
def main():
    rodar = True
    frames = pygame.time.Clock()

    while rodar:
        frames.tick(60)
        tela.fill(PRETO)

        for event in pygame.event.get():
            if event.type == QUIT:
                rodar = False

        tela.blit(imagem_fundo, (0, 0))
        tela.blit(sol, (x_sol, y_sol))
        pygame.display.flip()
                
    pygame.quit()
    exit()
    
main()