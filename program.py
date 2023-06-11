import pygame
import random

# jednostavna igrica u kojoj kontrolirate jedan kvadrat. tipkama W, A, S i D pomičete kvadrat. ne smijete se zabiti u rubove ekrana ili druge, crvene kvadratiće.
def moje():

    # incijalizacija prozora igre. 
    pygame.init()

    # objekt prozora se pohranjuje u varijablu screen.
    # ova funkcija ga incijalizira sa rezolucijom 1200x800
    screen = pygame.display.set_mode((1200, 800))

    # pygame objekt Clock() omogućava funkciju timera. 
    # objekt je potrebno inicijalizirati izvan scopea glavne petlje.
    clock = pygame.time.Clock()

    # varijabla koja kontrolira tijek glavne petlje.
    running = True

    # varijabla dt označava "delta time", protkelo vrijeme između dva framea.
    dt = 0

    # inicijaliziramo početnu poziciju igrača u sredini prozora.
    # x koordinata se dobije dijeljenjem širine na 2, a y dijeljenjem visine na 2. 
    # objekt prozora vodi računa o informacijama o sebi.
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    # broj redova od 10 piksela.
    rows = screen.get_width() / 10

    # broj stupaca od 10 piksela.
    columns = screen.get_height() / 10

    # inicijaliziranje brzine igrača. trenutno prazan dvodimenzionalni vektor.
    velocity = pygame.Vector2()

    # timer koji će nam govoriti kada je prošla 1 sekunda.
    # potreban za logiku randomizacije položaja prepreki.
    time_since_reset = 0

    # lista koja sadržava sve blokove
    # blokovi su nam prepreke
    blocks = [ ]
    
    # for petlja sa 5 ponavljanja.
    # u listu blokova za početak dodajemo 5 blokova stvorenih na nasumičnim mjestima na ekranu.
    # koordinate svakog bloka su raspoređene po redovima i stupcima koje smo odredili.
    for i in range(5):
        blocks.append(pygame.Rect(10 * random.randint(2, rows - 1), 10 * random.randint(1, columns - 1), 10, 10))
    
    # objekt samog igrača kojeg ćemo kasnije unutar scopea glavne petlje
    # definirati kao objekt kvadrata.
    player = 0

    # glavna petlja igre.
    # petlja se izvodi sve dok 'running' ne postane false.
    # vrijednost varijable 'running' uvjetovana je gubitkom ili gašenjem prozora na tipku X
    while running:

        # većina enginea za igrice ima neku vrstu 'eventova' odnosno događaja unutar prozora.
        # ovom petljom osluškujemo za događaj 'QUIT' koji se dogodi kada se pritisne tipka X.
        # u tom slučaju želimo ugasiti čitavi prozor.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # frame buffer se čisti tako što cijeli ekran napravimo crnim na početku svakog novog frame.
        screen.fill("black")

        # definiranje objekta igrača.
        # igrač je sada službeno pravoktunik na poziciji 'player_pos', visine i širine 20 piksela.
        player = pygame.Rect(player_pos.x, player_pos.y, 20, 20)

        # taj pravokutnik se sada crta na ekranu.
        # draw funkcija na ekranu crta objekt.
        # određujemo ekran, boju (u ovom slučaju pravokutnika) i objekt pravokutnika.
        pygame.draw.rect(screen, "green", player)

        # detektiramo koju tipku na tipkovnici pritišćemo.
        keys = pygame.key.get_pressed()

        # mijenjamo komponente brzine ovisno o smjeru u kojem idemo.
        # u računalnim programima, koordinate 0,0 su u gornjem lijevom kutu i šire se desno i dolje
        # za razliku od kartezijskog koordinatnog sustava u kojemu se šire na sve 4 strane.
        # tako da ako se želimo kretati prema gore, moramo oduzimati od y koordinate.
        if keys[pygame.K_w]:
            velocity.y = -700 * dt # svaku brzinu množimo sa 'delta time' tako da dobijemo ujednačeno i glatko pomicanje. 
            velocity.x = 0
        if keys[pygame.K_s]:
            velocity.y = 700 * dt
            velocity.x = 0
        if keys[pygame.K_a]:
            velocity.x = -700 * dt
            velocity.y = 0
        if keys[pygame.K_d]:
            velocity.x = 700 * dt
            velocity.y = 0
        
        # na položaj igrača nadodajemo brzinu.
        # ovo zapravo nije potrebno i moguće je samo 
        # player_pos += 700 * dt ali ovako brzina se primjenjuje na igrača a prije primjenjivanja može se modificirati po potrebi
        # u ovoj igri ako se dotaknu rubovi, program se zaustavi ali moglo bi se napraviti da se lik zaustavi.
        # to bi se napravilo tako da pri dodiru, brzina se stavi na 0.
        # tu promjenu bi radili prije samog primjenjivanja brzine na igrača.
        player_pos += velocity
        
        # boolean varijabla koja vraća true ako su igračeve koordinate izvan koordinata igračeg prostora (ekrana)
        outside = (player_pos.x < 0 or player_pos.x >= screen.get_width()) or (player_pos.y < 0 or player_pos.y >= screen.get_width())
        
        # ako je igrač izvan ekrana, program se obustavlja.
        if outside:
            running = False # gubitnici nemaju pravo nastaviti igru.

        # brojimo vrijeme koje je prošlo nakon svakog framea.
        # konstantno povećanje
        time_since_reset += dt

        # moramo prvo odrediti koliko blokova ima.
        # pošto smo na početku dodali ih 5, ova varijabla je ovdje 5.
        # potrebno nam je jer je ideja da svake sekunde se stvori nova prepreka, a postojeće prepreke se nasumično rasporede.
        # svake sekunde povećavamo broj blokova.
        block_count = len(blocks)
        
        # ako je protekla 1 sekunda, želimo nadodati još blokova i rasporediti postojeće.
        if time_since_reset > 1:
            blocks.clear() # čistimo listu postojećih blokova.

            # petlja for koja se izvodi onoliko puta koliko je bilo blokova.
            # blokove raspoređujemo na ekranu tako što ih sve obrišemo i stvorimo opet na novom položaju.
            # ovo je loše rješenje.
            # bolje bi bilo da je svaki blok objekt koji ima svoj položaj i da onda svake sekunde mjenjamo taj položaj.
            for i in range(block_count):
                blocks.append(pygame.Rect(10 * random.randint(2, rows - 1), 10 * random.randint(1, columns - 1), 10, 10))

            # povrh postojećih blokova, želimo stvoriti još jedan novi.
            blocks.append(pygame.Rect(10 * random.randint(2, rows - 1), 10 * random.randint(1, columns - 1), 10, 10))

            # broj blokova incrementamo za 1 jer smo dodali jedan.
            block_count += 1

            # vrijeme od zadnjeg resetiranja vraćamo na 0
            time_since_reset = 0

        # for petlja kroz sve postojeće blokove.
        for block in blocks:

            # ako igrač se sudara sa nekim od blokova, obustavljamo cijeli program.
            # boolean funkcija 'colliderect' prima kao argument objekt drugog pravokutnika za kojeg provjeravamo sudaranje.
            if player.colliderect(block):
                running = False # sudaramo se sa nekim od blokova, obustavljamo glavnu petlju i gubimo.
                break
            
            # kad smo već u ovoj petlji, možemo i iskoristiti priliku da nacrtamo sve blokove.
            pygame.draw.rect(screen, "red", block)

        # ova funkcija ažurira frame buffer.
        # jednostavnije, ova funkcija ažurira stanje na ekranu - crta sve nove frameove.
        pygame.display.flip()

        # računanje vremena proteklog između svakog framea. program se pokreće u 60 frameova po sekundi.
        dt = clock.tick(60) / 1000

    # izlazimo iz programa u potpunosti.
    pygame.quit()

def main():
    moje()

if __name__ == "__main__":
    main()