import os
import os.path
import cv2

# Declaração das imagens tanto invertidas quanto normais
imgPapel = cv2.resize(cv2.imread("papel.png", 0), (0, 0), None, 0.400, 0.400)
imgTesoura = cv2.resize(cv2.imread("tesoura.png", 0), (0, 0), None, 0.400, 0.400)
imgPedra = cv2.resize(cv2.imread("pedra.png", 0), (0, 0), None, 0.400, 0.400)
imgInvertidaPapel = cv2.flip(imgPapel, -1)
imgInvertidaTesoura = cv2.flip(imgTesoura, -1)
imgInvertidaPedra = cv2.flip(imgPedra, -1)

# Declaração das variaveis globais que vão ser ultilizadas no programa
cor = [34, 139, 34]
font = cv2.FONT_HERSHEY_TRIPLEX
pontosJogadorUm = 0
pontosJogadorDois = 0
ultimaEscolhaJogadorUm = ""
ultimaEscolhaJogadorDois = ""
ultimoVencedor = ""

# METODO PARA IDENTIFICAR A JOGADA DE CADA PARTICIPANTE
def escolhaJogador(imgCinza, imgRgb, imgPapel, imgTesoura, imgPedra):
    matchPapel = cv2.matchTemplate(imgCinza, imgPapel, cv2.TM_SQDIFF_NORMED)
    matchTesoura = cv2.matchTemplate(imgCinza, imgTesoura, cv2.TM_SQDIFF_NORMED)
    matchPedra = cv2.matchTemplate(imgCinza, imgPedra, cv2.TM_SQDIFF_NORMED)

    valorMinMatchPapel, _, posicaoMatchPapel, _ = cv2.minMaxLoc(matchPapel)
    valorMinMatchTesoura, _, posicaoMatchTesoura, _ = cv2.minMaxLoc(matchTesoura)
    valorMinMatchPedra, _, posicaoMatchPedra, _ = cv2.minMaxLoc(matchPedra)

    _, alturaTemplatePapel = imgPapel.shape[::-1]
    _, alturaTemplateTesoura = imgTesoura.shape[::-1]
    _, alturaTemplatePedra = imgPedra.shape[::-1]

    if valorMinMatchPapel < 0.019:
        drawPosition = (
            posicaoMatchPapel[0],
            posicaoMatchPapel[1] + alturaTemplatePapel + 30,
        )
        cv2.putText(imgRgb, "Papel", drawPosition, font, 0.7, cor, 1, cv2.LINE_AA)
        return ["Papel", posicaoMatchPapel]
    elif valorMinMatchTesoura < 0.030:
        drawPosition = (
            posicaoMatchTesoura[0],
            posicaoMatchTesoura[1] + alturaTemplateTesoura + 30,
        )
        cv2.putText(imgRgb, "Tesoura", drawPosition, font, 0.7, cor, 1, cv2.LINE_AA)
        return ["Tesoura", posicaoMatchTesoura]
    elif valorMinMatchPedra < 0.012:
        drawPosition = (
            posicaoMatchPedra[0],
            posicaoMatchPedra[1] + alturaTemplatePedra + 20,
        )
        cv2.putText(imgRgb, "Pedra", drawPosition, font, 0.7, cor, 1, cv2.LINE_AA)
        return ["Pedra", posicaoMatchPedra]
    else:
        return ["Jogada nao encontrada!", [0, 0]]

# METODO PARA IDENTIFICAR O VENCEDOR DA RODADA E CONFERIR A PONTUACAO DE CADA UM
def escolheVencedor(jogadaUm, jogadaDois):
    global pontosJogadorUm
    global pontosJogadorDois

    if (
        (jogadaUm == "Tesoura" and jogadaDois == "Papel")
        or (jogadaUm == "Papel" and jogadaDois == "Pedra")
        or (jogadaUm == "Pedra" and jogadaDois == "Tesoura")
    ):
        pontosJogadorUm += 1
        return "Jogador 1 ganhou!"
    elif (
        (jogadaUm == "Papel" and jogadaDois == "Tesoura")
        or (jogadaUm == "Pedra" and jogadaDois == "Papel")
        or (jogadaUm == "Tesoura" and jogadaDois == "Pedra")
    ):
        pontosJogadorDois += 1
        return "Jogador 2 ganhou"
    else:
        return "Deu nada pae"

# METODO PARA IDENTIFICAR O TERMINO DA RODADA
def novaRodada(escolhaJogadorUm, escolhaJogadorDois):
    global ultimaEscolhaJogadorUm
    global ultimaEscolhaJogadorDois

    if (
        escolhaJogadorUm != ultimaEscolhaJogadorUm
        or escolhaJogadorDois != ultimaEscolhaJogadorDois
    ):
        ultimaEscolhaJogadorUm = escolhaJogadorUm
        ultimaEscolhaJogadorDois = escolhaJogadorDois
        return True

    return False

# METODO "MAIN" QUE CONTEM A LEITURA DO VIDEO E ULTIZAÇÃO DOS METODOS
def videoJogo(img):
    global ultimoVencedor

    imgReduzida = cv2.resize(img, (0, 0), None, 0.400, 0.400)
    imgCinza = cv2.cvtColor(imgReduzida, cv2.COLOR_BGR2GRAY)

    imgLargura = imgReduzida.shape[1]

    escolhaJogadorUm, matchJogadorUm = escolhaJogador(
        imgCinza, imgReduzida, imgPapel, imgTesoura, imgPedra
    )
    escolhaJogadorDois, matchJogadorDois = escolhaJogador(
        imgCinza, imgReduzida, imgInvertidaPapel, imgInvertidaTesoura, imgInvertidaPedra
    )

    isNewRound = novaRodada(escolhaJogadorUm, escolhaJogadorDois)

    if isNewRound:
        jogadorVencedor = escolheVencedor(escolhaJogadorUm, escolhaJogadorDois)
        ultimoVencedor = jogadorVencedor

    cv2.putText(
        imgReduzida,
        str("Pontos J1: ") + str(pontosJogadorUm),
        (int(imgLargura / 2) - 150, 20),
        font,
        0.5,
        cor,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        imgReduzida,
        str("Pontos J2: ") + str(pontosJogadorDois),
        (int(imgLargura / 2) - 30, 20),
        font,
        0.5,
        cor,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        imgReduzida,
        ultimoVencedor,
        (int(imgLargura / 2) - 150, 50),
        font,
        0.7,
        cor,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        imgReduzida,
        "Jogador 1",
        (matchJogadorUm[0], (matchJogadorUm[1] - 30)),
        font,
        0.7,
        cor,
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        imgReduzida,
        "Jogador 2",
        (matchJogadorDois[0], (matchJogadorDois[1] - 30)),
        font,
        0.7,
        cor,
        1,
        cv2.LINE_AA,
    )

    return imgReduzida


vc = cv2.VideoCapture("pedra-papel-tesoura.mp4")

if vc.isOpened():
    open, frame = vc.read()
else:
    open = False

while open:
    img = videoJogo(frame)

    cv2.imshow("Checkpoint - 02 | Jokenpo", img)

    open, frame = vc.read()
    key = cv2.waitKey(10)
    if key == 27:
        break

cv2.destroyWindow("Checkpoint - 02 | Jokenpo")
vc.release()
