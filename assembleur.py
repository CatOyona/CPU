dictionaire = {'UAL' : ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'SL', 'SR', 'ADDi', 'SUBi'], 'MEM' : ['LD',  'ST'], 'CTRL' : ['JMP', 'JEQU', 'JNEQ','JSUP', 'JINF']}
equivalence_type = [['UAL', '00'],['MEM', '01'],['CTRL', '11']]
equivalence_ope = [['ADD', '000'], ['ADDi', '000'], ['SUB', '001'], ['SUBi', '001'],['AND', '010'], ['OR', '011'], ['XOR', '100'], ['SL', '101'], ['SR', '110'], ['LD', '000'], ['ST', '001'], ['JMP', '000'], ['JEQU', '001'], ['JNEQ', '010'], ['JSUP', '011'], ['JINF', '100']]

def binaire(nb, taile = 3):
    res = ''
    while nb > 0:
        res = str(nb % 2) + res
        nb //= 2
    while len(res) < taile:
        res = f'0{res}'
    return res

def lecture_fichier(fichier):
    with open('test.txt' , 'r' , encoding='utf-8') as f:
        lignes = f.readlines()
        tab=[]
        for ligne in lignes:
            if ligne.strip() !='':
                tab.append(ligne.strip())
        return tab

def lecture_ligne (tab):
    for i in range(len(tab)):
        tab[i]=tab[i].split()
    return tab

def retourne_ope (tab):
    liste = []
    for i in range(len(tab)):
        for clés, valeurs in dictionaire.items() :
            for j in range(len(valeurs)):
                if tab[i][0]==valeurs[j]:
                    liste.append(clés)
    return liste

def convertir_type_ope (tab):
    liste = []
    for i in range(len(tab)):
        for j in range(len(equivalence_type)):
            if tab[i] == equivalence_type[j][0]:
                liste.append(equivalence_type[j][1])
    return liste

def convertir_ope (tab, chaine):
    for i in range(len(tab)) :
        for j in range(len(equivalence_ope)):
            if tab[i][0] == equivalence_ope[j][0]:
                chaine[i] = chaine[i] + equivalence_ope[j][1]
    return chaine
        
def immediate (tab, chaine):
    for i in range(len(tab)):
        if(tab[i][0]=='ADDi' or tab[i][0]=='SUBi'):
            chaine[i] = chaine[i] + '1'
        else :
            chaine[i] = chaine[i] + '0'
    return chaine

def convertir_registe (tab, chaine):
    for i in range (len(tab)):
        for j in range (1, len(tab[i])):
            chaine[i] += binaire(int(tab[i][j][-1]))
    return chaine

def convertir_nombre_immediat (tab, chaine):
    for i in range(len(tab)):
        if (tab[i][0]=='ADDi' or tab[i][0]=='SUBi'):
            chaine[i] += f'0{binaire(int(tab[i][-1]), 16)}'
        else :
            chaine[i] += '00000000000000000'
    return chaine

def ecrire (tab):
    chaine = ""
    for i in tab :
        i += '\n'
        chaine = chaine + i
    with open("resultat.txt", "w", encoding="utf-8") as f:
        f.write(chaine)


#def decodeur_ligne():
#    if text=='OR':
chaine_decompose = lecture_ligne(lecture_fichier(0))
type_ope = retourne_ope(lecture_ligne(lecture_fichier(0)))
type_binaire = convertir_type_ope(retourne_ope(lecture_ligne(lecture_fichier(0))))
type_et_ope_binaire = convertir_ope(chaine_decompose, type_binaire)
ope_immediate = immediate(chaine_decompose, type_et_ope_binaire)
registre = convertir_registe(chaine_decompose, ope_immediate)
final = convertir_nombre_immediat(chaine_decompose, registre)
ecrire(final)