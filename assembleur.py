
def binaire(nb, taile = 3):
    res = ''
    while nb > 0:
        res = str(nb % 2) + res
        nb //= 2
    while len(res) < taile:
        res = f'0{res}'
    return res

def lecture_ligne:
# utiliser join pour retourner les instruction dans un tableau 


def lecture_fichier(fichier):
    with open('test.txt' , 'r' , encoding='utf-8') as f:
        lignes = f.readlines()
        tab=[]
        for ligne in lignes:
            if ligne.strip() !='':
                tab.append(ligne.strip())
        return tab
    



#def decodeur_ligne():
#    if text=='OR':

print(lecture_fichier(0))