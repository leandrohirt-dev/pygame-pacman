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

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill("black")
    for r in paredes:
        pygame.draw.rect(tela, "mediumblue", r)
    for p in pontos:
        pygame.draw.circle(tela, "wheat", p.center, 4)
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
