import pygame

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

def livre(r, d):
    novo = r.move(d[0] * T, d[1] * T)
    return novo.collidelist(paredes) < 0

def alinhado(r):
    return r.x % T == 0 and r.y % T == 0

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
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
