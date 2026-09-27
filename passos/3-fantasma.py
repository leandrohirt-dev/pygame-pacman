import pygame
import math

pygame.init()
tela = pygame.display.set_mode((600, 400))
relogio = pygame.time.Clock()
T = 40
mapa = [
    "###############",
    "#......#......#",
    "#.##.#.#.#.##.#",
    "#....#...#....#",
    "#.##...#...##.#",
    "#....#.#.#....#",
    "#.##.#...#.##.#",
    "#.#..#.#.#..#.#",
    "#.............#",
    "###############",
]
paredes = []
pontos = []
for y, linha in enumerate(mapa):
    for x, c in enumerate(linha):
        r = pygame.Rect(x * T, y * T, T, T)
        if c == "#":
            paredes.append(r)
        else:
            pontos.append(r.inflate(-32, -32))
pac = pygame.Rect(7 * T, 8 * T, T, T)
direcao = quer = (0, 0)
setas = {
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
}
fantasmas = [
    [pygame.Rect(13 * T, T, T, T), (-1, 0), "red", 0],
]

def livre(r, d):
    novo = r.move(d[0] * T, d[1] * T)
    return novo.collidelist(paredes) < 0

def alinhado(r):
    return r.x % T == 0 and r.y % T == 0

def escolher(r, d, alvo):
    opcoes = []
    for o in setas.values():
        prox = r.move(o[0] * T, o[1] * T)
        if o != (-d[0], -d[1]) and livre(r, o):
            perto = math.dist(prox.center, alvo)
            opcoes.append((perto, o))
    return min(opcoes)[1]

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key in setas:
                quer = setas[evento.key]

    if alinhado(pac) and livre(pac, quer):
        direcao = quer
    if not alinhado(pac) or livre(pac, direcao):
        pac.x += direcao[0] * 5
        pac.y += direcao[1] * 5
    i = pac.collidelist(pontos)
    if i >= 0:
        pontos.pop(i)

    dx, dy = direcao
    for f in fantasmas:
        r, d, cor, n = f
        if alinhado(r):
            alvo = pac.move(dx * T * n, dy * T * n)
            f[1] = d = escolher(r, d, alvo.center)
        r.x += d[0] * 4
        r.y += d[1] * 4

    tela.fill("black")
    for r in paredes:
        pygame.draw.rect(tela, "mediumblue", r)
    for p in pontos:
        pygame.draw.circle(tela, "wheat", p.center, 4)
    cx, cy = pac.center
    pygame.draw.circle(tela, "yellow", (cx, cy), 17)
    a = pygame.time.get_ticks() // 80 % 3 * 8
    p1 = (cx + dx * 20 - dy * a, cy + dy * 20 + dx * a)
    p2 = (cx + dx * 20 + dy * a, cy + dy * 20 - dx * a)
    pygame.draw.polygon(tela, "black", [(cx, cy), p1, p2])
    for r, d, cor, n in fantasmas:
        pygame.draw.circle(tela, cor, r.center, 17)
        corpo = r.inflate(-6, -20).move(0, 8)
        pygame.draw.rect(tela, cor, corpo)
        for lado in (-7, 7):
            x, y = r.move(lado, -3).center
            pygame.draw.circle(tela, "white", (x, y), 6)
            pupila = (x + d[0] * 3, y + d[1] * 3)
            pygame.draw.circle(tela, "blue", pupila, 3)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
