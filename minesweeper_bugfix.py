import pygame
import random
pygame.init()
pozboja=(192,192,192)
rubboja=(128,128,128)
print("Preporuka je da se ugasi Shell kada zelite promjeniti broj kucica ili mina")
sirina=int(input("Upiši koliko ćeš kućica imati u širinu: "))
print("------------------------------------------------------------")
while sirina<1 or sirina>30:
    print("Širina ne može biti manja od 1, niti veca od 30")
    print("------------------------------------------------------------")
    sirina=int(input("Upiši koliko ćeš kućica imati u širinu: "))
    print("------------------------------------------------------------")
visina=int(input("Upiši koliko ćeš kućica imati u visinu: "))
print("------------------------------------------------------------")
while visina<1 or visina>30:
    print("Visina ne može biti manja od 1!, niti veca od 30")
    print("------------------------------------------------------------")
    visina=int(input("Upiši koliko ćeš kućica imati u visinu: "))
    print("------------------------------------------------------------")
brojmina=int(input("Upiši broj mina koji želiš imati: "))
while brojmina<1 or brojmina>sirina*visina-1:
    if brojmina>sirina*visina:
        print("Broj mina ne može biti veći od broja kućica minus jedan!")
        print("------------------------------------------------------------")
    elif brojmina<0:
        print("Broj mina ne može biti manji od 1!\n")
        print("------------------------------------------------------------")
    brojmina=int(input("Upiši broj mina koji želiš imati: "))
    print("------------------------------------------------------------")
kucica=32
rub=16
gorerub=100
ekransirina=kucica*sirina+rub*2
ekranvisina=kucica*visina+gorerub
display=pygame.display.set_mode((ekransirina, ekranvisina))
pygame.display.set_caption("Minesweeper")
spr_praznakucica=pygame.image.load("sprajt/nis.png")
spr_zastava=pygame.image.load("sprajt/zastava.png")
spr_kucica=pygame.image.load("sprajt/kucica.png")
spr_kuc1=pygame.image.load("sprajt/1.png")
spr_kuc2=pygame.image.load("sprajt/2.png")
spr_kuc3=pygame.image.load("sprajt/3.png")
spr_kuc4=pygame.image.load("sprajt/4.png")
spr_kuc5=pygame.image.load("sprajt/5.png")
spr_kuc6=pygame.image.load("sprajt/6.png")
spr_kuc7=pygame.image.load("sprajt/7.png")
spr_kuc8=pygame.image.load("sprajt/8.png")
spr_mina=pygame.image.load("sprajt/mina.png")
spr_minakrivo=pygame.image.load("sprajt/minakrivo.png")
spr_minastisnuo=pygame.image.load("sprajt/minastisnuo.png")
mreza=[]
mine=[]
def pisiText(txt, s, yOff=0):
    text=pygame.font.SysFont("Calibri",s,True).render(txt,True,(0,0,0))
    rect=text.get_rect()
    rect.center=(sirina*kucica/2+rub,visina*kucica/2+gorerub+yOff)
    display.blit(text,rect)
class Mreza:
    def __init__(self, xmreza, ymreza, type):
        self.xmreza=xmreza
        self.ymreza=ymreza
        self.stisnuo=False
        self.minastisnuo=False
        self.minakrivo=False
        self.zastava=False
        self.rect=pygame.Rect(rub+self.xmreza*kucica,gorerub+self.ymreza*kucica,kucica,kucica)
        self.izn=type
    def drawGrid(self):
        if self.minakrivo:
            display.blit(spr_minakrivo,self.rect)
        else:
            if self.stisnuo:
                if self.izn==-1:
                    if self.minastisnuo:
                        display.blit(spr_minastisnuo,self.rect)
                    else:
                        display.blit(spr_mina,self.rect)
                else:
                    if self.izn==0:
                        display.blit(spr_praznakucica,self.rect)
                    elif self.izn==1:
                        display.blit(spr_kuc1,self.rect)
                    elif self.izn==2:
                        display.blit(spr_kuc2,self.rect)
                    elif self.izn==3:
                        display.blit(spr_kuc3,self.rect)
                    elif self.izn==4:
                        display.blit(spr_kuc4,self.rect)
                    elif self.izn==5:
                        display.blit(spr_kuc5,self.rect)
                    elif self.izn==6:
                        display.blit(spr_kuc6,self.rect)
                    elif self.izn==7:
                        display.blit(spr_kuc7,self.rect)
                    elif self.izn==8:
                        display.blit(spr_kuc8,self.rect)

            else:
                if self.zastava:
                    display.blit(spr_zastava, self.rect)
                else:
                    display.blit(spr_kucica, self.rect)
    def revealGrid(self):
            self.stisnuo=True
            if self.izn==0:
                for x in range(-1,2):
                    if self.xmreza+x>= 0 and self.xmreza+x<sirina:
                        for y in range(-1,2):
                            if self.ymreza+y>=0 and self.ymreza+y<visina:
                                if not mreza[self.ymreza+y][self.xmreza+x].stisnuo:
                                    mreza[self.ymreza+y][self.xmreza+x].revealGrid()
            elif self.izn==-1:
                for m in mine:
                    if not mreza[m[1]][m[0]].stisnuo:
                        mreza[m[1]][m[0]].revealGrid()
    def updateValue(self):
        if self.izn!=-1:
            for x in range(-1, 2):
                if self.xmreza+x >= 0 and self.xmreza+x<sirina:
                    for y in range(-1,2):
                        if self.ymreza+y>=0 and self.ymreza+y<visina:
                            if mreza[self.ymreza+y][self.xmreza+x].izn==-1:
                                self.izn+=1
def gameLoop():
    gamestanje="Playing"
    mineostalo=brojmina
    global mreza
    mreza=[]
    global mine
    t=0
    mine=[[random.randrange(0,sirina),
           random.randrange(0,visina)]]
    for c in range(brojmina-1):
        pos=[random.randrange(0,sirina),
             random.randrange(0,visina)]
        isti=True
        while isti:
            for i in range(len(mine)):
                if pos==mine[i]:
                    pos=[random.randrange(0,sirina),random.randrange(0,visina)]
                    break
                if i==len(mine)-1:
                    isti=False
        mine.append(pos)
    for j in range(visina):
        linija=[]
        for i in range(sirina):
            if [i,j] in mine:
                linija.append(Mreza(i,j,-1))
            else:
                linija.append(Mreza(i,j,0))
        mreza.append(linija)
    for i in mreza:
        for j in i:
            j.updateValue()
    while gamestanje!="Exit":
        display.fill(pozboja)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gamestanje="Exit"
            if gamestanje=="Game Over" or gamestanje=="Win":
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_r:
                        gamestanje="Exit"
                        gameLoop()
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    for i in mreza:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button==1:
                                    j.revealGrid()
                                    if j.zastava:
                                        mineostalo+=1
                                        j.zastava=False
                                    if j.izn==-1:
                                        gamestanje="Game Over"
                                        j.minastisnuo=True
                                elif event.button==3:
                                    if not j.stisnuo:
                                        if j.zastava:
                                            j.zastava=False
                                            mineostalo+=1
                                        else:
                                            j.zastava=True
                                            mineostalo-=1
        w = True
        for i in mreza:
            for j in i:
                j.drawGrid()
                if j.izn!=-1 and not j.stisnuo:
                    w=False
        if w and gamestanje!="Exit":
            gamestanje="Win"
        if gamestanje!="Game Over" and gamestanje!="Win":
            t+=1
        elif gamestanje=="Game Over":
            pisiText("BOOM!",50)
            pisiText("Stisni R da opet izgubiš",35,50)
            for i in mreza:
                for j in i:
                    if j.zastava and j.izn!=-1:
                        j.minakrivo=True
        else:
            pisiText("Pobjedio si",50)
            pisiText("Stisni R da probaš opet",35,50)
        s=str(t//15)
        text = pygame.font.SysFont("Calibri",50).render(s,True,(0,0,0))
        display.blit(text,(rub,rub))
        text = pygame.font.SysFont("Calibri",50).render(mineostalo.__str__(),True,(0,0,0))
        display.blit(text,(ekransirina-rub-50,rub))
        pygame.display.update()
gameLoop()
pygame.quit()
quit()
