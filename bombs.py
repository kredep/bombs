# Her importeres alle pakker som blir benyttet
import sys # Brukes for sys.exit() for å raskt kunne avslutte hele programmet
from time import sleep
import os # Nødvendig for å bruke clear() funksjonen for å fjerne all tekst fra konsoll-vinduet
import random 
from colorama import Fore, Back, Style # Colorama gir farger i konsoll-vinduet
import math
from operator import itemgetter # itemgetter fra operator gjør at vi kan sortere en liste med dictionaries etter en key

# Liste som holder styr på rekorder, denne benyttes av flere enn én funksjon
highscores = []

def clear():
    '''
    Funksjon som fjerner all tekst fra terminalen (cmd), hentet fra nettet
    '''
    os.system('cls' if os.name=='nt' else 'clear')

def ny_highscore(navn, poeng, strlse, brett, vansklgrad, trekk):
    '''
    Funksjon som returnerer en dictionary med navn, poeng, brett-størrelse, antall brett, vanskelighetsgrad og antall trekk som innparametre
    '''
    rekord = {"navn": navn, "poeng": poeng, "størrelse": strlse, "brett": brett, "vansk": vansklgrad, "trekk": trekk}
    return rekord

def rekorder():
    '''
    Funksjon som printer alle rekorder
    '''
    clear()
    # Sjekker at det faktisk finnes én eller flere rekorder før vi printer dem
    if len(highscores) != 0:
        print(Fore.BLACK + Back.LIGHTGREEN_EX + "...:::::::::::::::::::::::::::::::::::::::::::::::::: Rekorder ::::::::::::::::::::::::::::::::::::::::::::::::::..." + Style.RESET_ALL)
        print()

        # Her sorteres highscore lista med dictionaries etter keyen 'poeng', reverse=True gjør at lista kommer i riktig rekkefølge med den høyeste først
        highscores.sort(key=itemgetter('poeng'), reverse=True)

        # for-løkke som printer alle elementene i highscore-lista
        for i in range(len(highscores)):
            print("{}. {} poeng av {} | Brett-størrelse: {}x{} | Antall brett: {} | Bomber per brett: {} | Samlet antall trekk: {}".format(i + 1, highscores[i]['poeng'], highscores[i]['navn'], highscores[i]['størrelse'], highscores[i]['størrelse'], highscores[i]['brett'], highscores[i]['vansk'], highscores[i]['trekk']))

        print()
        print(Fore.BLACK + Back.LIGHTGREEN_EX + "...::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::..." + Style.RESET_ALL)
        print()

        # Når spilleren er ferdig med å se rekordene, skriver man inn 'ferdig' og kommer tilbake til menyen
        done = input("Ferdig? Skriv 'ferdig': ")
        while done.lower() != "ferdig":
            print("Det ble feil.")
            done = input("Ferdig? Skriv 'ferdig': ")

    # Dersom det ikke er noen rekorder i lista
    else:
        print("Det er ingen rekorder ennå!")
        sleep(3)

def hjelp():
    '''
    Funksjon som gir spilleren starthjelp
    '''
    clear()
    print()
    print(Fore.BLACK + Back.LIGHTGREEN_EX + "..:::|| VELKOMMEN TIL BOMBS ||:::.." + Style.RESET_ALL)
    sleep(0.1)
    print()
    print("~ I dette spillet skal du samle poeng i et rutenett.")
    print("~ Poengene får du av å velge en rute der det ikke ligger en bombe.")
    print("~ Størrelsen på rutenettet og antall bomber i kan du selv velge!")
    print("~ Desto flere ruter du velger på et brett, desto mer poeng.")
    print("~ Desto flere bomber i et spill, desto mer poeng per gjetting.")
    print("~ Du kan når som helst starte ett nytt brett og beholde poengene dine.")
    print("~ Du kan gi deg når som helst!")
    print("~ Men dersom du eksplorerer, mister du ALLE poengene!")
    print("~ Lykke til!")
    print()

    # Spilleren må her skrive inn 'ferdig' for å returnere til hovedmenyen
    done = input("Ferdig? Skriv 'ferdig': ")
    while done.lower() != "ferdig":
        print("Det ble feil.")
        done = input("Ferdig? Skriv 'ferdig': ")

def spill():
    '''
    - Selve spill-funksjonen.
    - Først blir spilleren spurt om:
        - Brett-størrelse
        - Vanskelighetsgrad
    - Videre består funksjonen av to while-løkker inni hverandre:
        - Løkke 1:
            - Sørger for at spilleren kan spille så mange brett en ønsker
            - Sørger for at alle verdier vi trenger til rutenettet blir generert
        - Løkke 2:
            - Sørger for at spilleren kan gjøre så mange trekk på et brett som en vil
            - Sørger for å printe rutenettet, ta imot input fra spilleren og avgjøre om spilleren lever eller ei
    '''
    print("Da starter vi!")

    # Spilleren velger størrelse på brettet
    # 'dim' forteller dimensjonene (dim*dim) til brettet, spilleren skal straks endre på denne
    dim = 0

    # Så lenge 'dim' ikke er mellom eller lik 2-26 må spilleren velge 'på nytt' med løkka under
    while dim not in range(2,27):
        # Her brukes try og except som en sikkerhet slik at dersom spilleren ikke skriver et tall, vil ikke programmet kræsje
        try:
            dim = int(input('Velg brett-størrelse (2-26):'))
            if dim not in range(2,27):
                print("Brett-størrelsen må være et tall mellom 2 og 26!")
                print()
        except ValueError: # Dersom inputen ikke var et tall
            print("Brett-størrelsen må være et tall mellom 2 og 26!")
            print()
    print("Supert!")
    sleep(0.5)

    # 'difficulty' angir vanskelighetsgraden (antall bomber, miner)
    difficulty = 0

    # Vanskelighetsgraden avhenger av dimensjonene, 'dim', maks antall bomber blir da dim*dim-1, men range tar ikke med den siste verdien så derfor blir det range(1,dim*dim)
    while difficulty not in range(1,dim*dim):
        try:
            # Spilleren velger vanskelighetsgrad
            difficulty = int(input('Velg vanskelighetsgrad (Antall bomber) (1-{}): '.format(dim*dim-1)))
            if difficulty not in range(1,dim*dim):
                print("Vanskelighetsgraden må være et tall mellom 1 og {}!".format(dim*dim-1))
                print()
        except ValueError:
            print("Vanskelighetsgraden må være et tall mellom 1 og {}!".format(dim*dim-1))
            print()
    print("Flott!")
    print()

    # Holder styr på poengene
    points = 0

    # Boolean som avgjør om spilleren lever eller ei
    dead = False

    # 'brett' og 'trekk' holder styr på antall brett og trekk for statistikk når man lagrer en rekord
    brett = 0 
    trekk = 0 
    
    # while-løkke nr. 1 som gjør at spilleren kan spille evig med brett så lenge man overlever
    while True:
        brett += 1
        
        # Under genereres koordinatene
        # Koordinatene lagres i tre lister
            # En liste med dictionaries der hvert koordinat har en verdi som blir printet i rutenettet, standard her er 'X'
            # En liste med kun koordinatene
            # En liste med kun koordinatene, men den er reversert, eks: A1 blir 1A istedenfor. Dette brukes for at spilleren kan skrive både A1 eller 1A

        koordinater = [] # Liste med dictionaries
        nett = [] # Liste med koordinater
        nettrev = [] # Liste med koordinater i revers
        # Koordinatene genereres
        abc = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z") # Alle mulige verdier langs y-aksen
        # for-løkke nr.1 i range dim
        for i in range(dim):
            # for-løkke nr.2 i range dim, dermed får vi essensielt dim*dim her, som er rutenettet vårt.
            for x in range(1, dim+1):
                koord = str(abc[i] + str(x)) # koordinat-STRENGEN genereres, først hentes en verdi fra abc-lista og blir satt sammen med x verdien, eks: D3 eller M18
                koordrev = str(x) + str(abc[i]) # koordinat-strengen genereses i revers
                xy = {koord: "X"} # Dictionariene som legges i koordinater-lista genereres, eks: {A5: "X"}
                koordinater.append(xy) # Dictionaryen blir lagt i koordinater-lista
                nett.append(koord) # Strengen med koordinatet legges i nett-lista
                nettrev.append(koordrev) # Strengen med koordinatet i revers legges i nettrev-lista

        # 'mines' holder styr på koordinatene til bombene
        mines = []

        # Lista med kun koordinater kopieres til en liste som det skal trekkes fra ved hjelp av 'nett[:]'
        bomblist = nett[:]

        # Antall bomber (miner) skal være lik vanskelighetsgraden, difficulty
        for i in range(difficulty):
            random.shuffle(bomblist)
            cur = bomblist[0] # Første verdi i lista trekkes
            mines.append(cur)
            del(bomblist[0]) # Verdien som ble trukket slettes, slik at den ikke kan trekkes igjen

        # Liste der alle plukkede koordinater lagres for å sjekke for duplikate svar
        plukket = []

        # while-løkke som gjør at spilleren kan fortsette på den gjeldene brettet så lenge en ønsker
        while True:
            trekk += 1
            clear()

            # Her printes litt info mens spilleren spiller
            print("Størrelse: {}x{}".format(dim, dim))
            print("Antall bomber: {}".format(difficulty))
            print("Antall brett: {}".format(brett))
            print("Totalt antall trekk: {}".format(trekk))
            # Her kan man sette inn 'print(mines)' og man vil da kunne se hvor minene ligger mens man spiller
            print(Fore.CYAN + Back.LIGHTYELLOW_EX + "Poeng: {}".format(points))
            print(Fore.BLACK + Back.LIGHTGREEN_EX)

            # Koden nedenfor tar av seg problemet med at tall over eller lik 10 gir 2 siffer, altså må mellomrommet i rutenettet bli større når det skjer
            if dim < 10:
                borderSize = dim * 2 + 1 # Angir antall tegn rutenettet tar opp langs x-aksen slik at man kan generere en kantlinje
            elif dim >= 10:
                borderSize = (9 * 2 + 1) + ((dim - 9) * 3)

            # for-løkke som genererer den øvre kanten
            for i in range(borderSize):
                print(":", end="") # end="" gjør at vi får én linje
            print(Style.RESET_ALL)

            print(Fore.BLACK + Back.LIGHTYELLOW_EX + " ", end="")

            # Genererer øvre linje av rutenettet, eks: 1 2 3 4 5 osv...
            for i in range(dim):
                print("", i+1, end="")
            print()

            # num settes til null, denne er viktig for riktig index ved generering av rutenett
            num = 0

            # for-løkke nr.1 i range dim
            for i in range(dim):
                # Her printes riktig bokstav til riktig linje, 'end=""' gjør at neste print vil fortsette på samme linje
                print(abc[i], end="")
                # for-løkke nr.2 i range dim, disse to løkkene gjør at koden under kjøres dim*dim antall ganger, altså alle punktene vi trenger i rutenettet
                for x in range(dim):
                    var_num = num + x # var_num angir hvilken dictionary som skal hentes fra 'koordinater'-
                    # x < 9 betyr at vi kun trenger ett mellomrom mellom hvert punkt i rutenettetlista
                    if x < 9:
                        print(" ", end="")
                    # x > 8 betyr at vi trenger to stk mellomrom mellom hvert punkt i rutenettet
                    elif x > 8:
                        print("  ", end="")
                    print(koordinater[var_num][nett[var_num]], end="") # Verdien hentes fra riktig dictionary i 'koordinater'-lista og printes
                num += dim # Sørger for at neste linje får riktig tall slik at riktig verdi hentes (riktig index)
                print()
            
            # for-løkke som genererer den nedre kanten
            print(Fore.BLACK + Back.LIGHTGREEN_EX, end="")
            for i in range(borderSize):
                print(":", end="")
            print(Style.RESET_ALL)
            print()


            # Spilleren skal her gjette hvilket koordinat som en tror er trygt
            # Bruker '.upper()' bak strengen for å sette alle bokstaver til store, slik at den ikke bryr seg om spilleren bruker store eller små bokstaver
            guess = input('Skriv inn koordinater: ').upper()


            # while-løkke som sjekker at spillerens svar er et gyldig svar, og lar spilleren skrive inn på nytt dersom det ikke er det
            while guess not in nett and guess not in nettrev and guess != "EXIT":
                print("Det er ikke et gyldig koordinat!")
                sleep(2)
                guess = input('Skriv inn koordinater: ').upper()

            # Snarvei for å avslutte programmet
            if guess == "EXIT":
                sys.exit()


            # Sjekker om spilleren har skrevet inn koordinatet i 'revers' eks: 1A i stedet for A1
                # Hvis dette stemmer blir det satt til 'riktig' vei, 1A blir da A1, viktig at dette kommer før vi sjekker om svaret er en mine
            if guess in nettrev:
                guess = nett[nettrev.index(guess)]


            # Sjekker om spilleren skrev inn koordinatet til en mine
                # Hvis sant, dead settes lik True og while-løkken opphører ved 'break'
            if guess in mines:
                print(Back.LIGHTRED_EX + "KABOOM! Du døde!")
                sleep(1)
                print("Spillet er over!")
                sleep(2)
                print()
                print("Lykke til neste gang!" + Back.BLACK)
                sleep(1.5)

                dead = True # Enderer variabelen som forteller om spilleren er død til 'True'
                break

            # Her sjekkes det om spilleren allerede har vært på koordinatet som ble skrevet fra før, hvis dette stemmer må spilleren skrive inn på nytt
            elif guess in plukket:
                print("Det koordinatet har du allerede vært på!")
                trekk -= 1 # Siden spilleren allerde har vært på koordinatet regnes ikke trekket som et ordentlig trekk og vi tar tilbake trekket
                sleep(2)
            else:
                # Dersom koordinatet er gyldig og ikke en mine, så vil 'X' verdien i dictionaryen byttes til 'O' og bli synlig i rutenettet ved neste runde
                picked = nett.index(guess)
                koordinater[picked][guess] = Back.LIGHTMAGENTA_EX + "O" + Back.LIGHTYELLOW_EX + Fore.BLACK # Endrer standardverdien 'X' til 'O' i dictionaryen siden spilleren overlevde
                plukket.append(guess)
                print("Du lever!")
                sleep(0.3)
                
                # Poengene kalkuleres basert på antall bomber delt på antall tilgjengelige ruter, dette multipliseres så med 1000 og rundes opp med math.ceil slik at vi får hele tall
                points += math.ceil(1000 * difficulty / ((dim*dim) - len(plukket)))
                print("Du har nå {} poeng!".format(points))

                # Spilleren får valget om å fortsette på gjeldene brett eller ikke
                again = input('Våger du å fortsette på brettet? (j/n) Svar: ')

                while again.lower() != "n" and again.lower() != "j" and again.lower() != "exit":
                    print("Vennligst bruk 'j/n'!")
                    sleep(2)
                    again = input('Våger du å fortsette på brettet? (j/n) Svar: ')
                if again == "n": # Ved svar lik 'n' brukes break for å opphøre while-løkka, ellers fortsetter løkka
                    break
                elif again == "exit":
                    sys.exit()

        # Sjekker om spilleren er død, såfall vil man ikke kunne fortsette eller lagre en rekord
        if dead == False:
            # Dersom spilleren lever får man valget om å starte et nytt brett, DER MAN BEHOLDER POENGENE, eller lagre en rekord
            fortsett_spill = input("Vil du fortsette på et nytt brett? (j/n) Svar: ")

            while fortsett_spill.lower() != "n" and fortsett_spill.lower() != "j" and fortsett_spill.lower() != "exit":
                print("Vennligst bruk 'j/n'!")
                sleep(1)
                fortsett_spill = input("Vil du fortsette på et nytt brett? (j/n) Svar: ")

            if fortsett_spill == "exit":
                sys.exit()

            if fortsett_spill != "j":
                # Spilleren skriver inn navn og rekorden lagres i highscores-lista
                print("Takk for at du spilte!")
                sleep(1)
                navn = input('Skriv inn navn: ')
                highscores.append(ny_highscore(navn, points, dim, brett, difficulty, trekk))
                return
            # Bruker else da eneste alternativ her er at spilleren skrev 'n'
            else:
                # Spilleren valgte å starte nytt brett, while-løkken starter på ny
                print("Starter nytt brett!")
                sleep(1)
        else:
            return

# Start-meny med alle kommandoer
    # 'while True' gjør at spilleren vil bli returnert her etter at en funksjon er ferdig (sitter fast der)
while True:
    clear()
    print()
    print(Fore.BLACK + Back.LIGHTGREEN_EX + "..:::|| VELKOMMEN TIL BOMBS ||:::.." + Style.RESET_ALL)
    print()
    print("Tilgjenglige kommandoer:")
    print("   ~ Spill")
    print("   ~ Rekorder")
    print("   ~ Hjelp")
    print("   ~ Exit")
    print("Hva ønsker du å gjøre?")
    command = input('Kommando: ').lower() # Bruker .lower() for å gjøre at testene ikke bryr seg om store og små bokstaver ved å sette alle store bokstaver til små

    if command == "spill":
        spill() # Starter et spill
    elif command == "rekorder":
        rekorder() # Printer rekordene
    elif command == "hjelp":
        hjelp() # Gir spilleren starthjelp
    elif command == "exit":
        # command lik exit opphever while-løkka ved 'break' og programmet avsluttes da det ikke er mer kode igjen å kjøre
        break
