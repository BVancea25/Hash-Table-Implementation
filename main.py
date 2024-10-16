import random
from datetime import datetime
import csv

male_names = ["Andrei", "Mihai", "Alexandru", "Gabriel", "Stefan", "Ion", "Darius", "Vlad","Bogdan","Dragos","Raul","Marius","David","Ciprian","Calin","Robert"]
female_names = ["Maria", "Elena", "Ioana", "Ana", "Gabriela", "Cristina", "Diana", "Irina","Andreea","Alexandra","Dana","Mirela","Iustina","Adriana"]
family_names = ["Popescu", "Ionescu", "Dumitrescu", "Georgescu", "Stan", "Marinescu", "Nicolae", "Moldovan","Pop","Vancea","Pop","Lupan"]


# Populația pe judete anul 2021
judete = {
    "01": 325941,
    "02": 410143, 
    "03": 569932, 
    "04": 601387, 
    "05": 551297,
    "06":295988,
    "07":392821,
    "08":546615,
    "09":281452,
    "10":404979,
    "11":246588,
    "12":283458,
    "13":679141,
    "14":655997,
    "15":200042,
    "16":479404,
    "17":599442,
    "18":496892,
    "19":262066,
    "20":314685,
    "21":291950,
    "22":361657,
    "23":250816,
    "24":760774,
    "25":542704,
    "26":452475,
    "27":234339,
    "28":518193,
    "29":454203,
    "30":383280,
    "31":695119,
    "32":330668,
    "33":212224,
    "34":388362,
    "35":642551,
    "36":323544,
    "37":650533,
    "38":193355,
    "39":374700,
    "40":341861,
    "41":335312,  
    "42": 265353,
    "43":359927,
    "44":486903,
    "45":334810,
    "46":300448,
    "47":395488
}
pop_total = sum(judete.values())

# Probabilități județe bazate pe populație
judete_prob = {k: v / pop_total for k, v in judete.items()}

# Generare lună și zi validă
def genereaza_data_nasterii(an):
    luna = random.randint(1, 12)
    if luna in [4, 6, 9, 11]:
        zi = random.randint(1, 30)
    elif luna == 2:
        if an % 4 == 0 and (an % 100 != 0 or an % 400 == 0):
            zi = random.randint(1, 29)  # An bisect
        else:
            zi = random.randint(1, 28)
    else:
        zi = random.randint(1, 31)
    return f"{luna:02d}", f"{zi:02d}"

# Calculul cifrei de control
def calculeaza_cifra_control(cnp_fara_control):
    control_weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    suma = sum(int(cnp_fara_control[i]) * control_weights[i] for i in range(12))
    rest = suma % 11
    return "1" if rest == 10 else str(rest)

# Generare CNP
def genereaza_cnp_nume():
    # 1. Determinăm sexul și secolul
    sex_secol = random.choices([1, 2, 5, 6], weights=[14, 16, 34, 36])[0]
    
    # 2. Generăm anul nașterii
    if sex_secol in [1, 2]:
        an = random.randint(1900, 1999)
    else:
        an = random.randint(2000, datetime.now().year)
    an_str = f"{an % 100:02d}"

    # 3. Generăm luna și ziua nașterii
    luna, zi = genereaza_data_nasterii(an)

    # 4. Alegem județul pe baza distribuției populației
    județ = random.choices(list(judete.keys()), weights=judete_prob.values())[0]

    # 5. Generăm un număr de ordine
    nnn = f"{random.randint(1, 999):03d}"

    # 6. Construim CNP-ul fără cifra de control
    cnp_fara_control = f"{sex_secol}{an_str}{luna}{zi}{județ}{nnn}"

    # 7. Calculăm cifra de control
    cifra_control = calculeaza_cifra_control(cnp_fara_control)

    if sex_secol in [1, 5]:  # barbat
        prenume = random.choice(male_names)
    else:  # femeie
        prenume = random.choice(female_names)

    nume_familie = random.choice(family_names)

    
    nume_complet = f"{nume_familie} {prenume}"

    # 8. Returnăm CNP-ul complet
    cnp_complet=cnp_fara_control + cifra_control

    return cnp_complet,nume_complet


with open("cnpuri.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["CNP", "Full Name"])  # Write the header

    for _ in range(1_000_000):
        cnp, nume_complet = genereaza_cnp_nume()
        writer.writerow([cnp, nume_complet])

print("CNP-uri și nume complete generate cu succes!")
