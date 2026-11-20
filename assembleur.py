dictionaire = {'UAL' : ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'SL', 'SR', 'ADDi', 'SUBi'], 'MEM' : ['LD',  'ST'], 'CTRL' : ['JMP', 'JEQU', 'JNEQ','JSUP', 'JINF', 'CALL','RET']}
equivalence_type = [['UAL', '00'],['MEM', '01'],['CTRL', '11']]
equivalence_ope = [['ADD', '000'], ['ADDi', '000'], ['SUB', '001'], ['SUBi', '001'],['AND', '010'], ['OR', '011'], ['XOR', '100'], ['SL', '101'], ['SR', '110'], ['LD', '000'], ['ST', '001'], ['JMP', '000'], ['JEQU', '001'], ['JNEQ', '010'], ['JSUP', '011'], ['JINF', '100'], ['CALL', '101'], ['RET', '110']]

def binaire(nb, taile = 3):
    """
    Convertit l'entier nb en chaîne binaire complétée par des zéros à gauche jusqu'à taile bits.s
    """

    res = ''
    while nb > 0:
        res = str(nb % 2) + res
        nb //= 2
    while len(res) < taile:
        res = f'0{res}'
    return res

def lecture_fichier(fichier):
    """
    Lit le fichier assembleur et renvoie la liste de ses lignes, sans espaces
    en début/fin de ligne et sans les lignes vides.
    """

    with open(fichier, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
        tab = []
        for ligne in lignes:
            if ligne.strip() != '':
                tab.append(ligne.strip())
        return tab

def lecture_ligne (tab):
    """
    Découpe chaque ligne de `tab` en mots (opération, opérandes).
 
    Exemple : 'ADD R1 R2 R3' -> ['ADD', 'R1', 'R2', 'R3'].
    Modifie tab sur place et le renvoie.
    """

    for i in range(len(tab)):
        tab[i]=tab[i].split()
    return tab

def retourne_ope (tab):
    """
    Renvoie, pour chaque instruction, son type ('UAL', 'MEM' ou 'CTRL')
    d'après le dictionnaire des opérations.
    """

    liste = []
    for i in range(len(tab)):
        for clés, valeurs in dictionaire.items() :
            for j in range(len(valeurs)):
                if tab[i][0]==valeurs[j]:
                    liste.append(clés)
    return liste

def convertir_type_ope (tab):
    """
    Convertit la liste de types ('UAL', 'MEM', 'CTRL') en codes binaires
    sur 2 bits ('00', '01', '11'). C'est le début du mot de chaque instruction.
    """

    liste = []
    for i in range(len(tab)):
        for j in range(len(equivalence_type)):
            if tab[i] == equivalence_type[j][0]:
                liste.append(equivalence_type[j][1])
    return liste

def convertir_ope (tab, chaine):
    """
    Ajoute à chaque chaîne de `chaine` le code binaire de l'opération (3 bits)
    de l'instruction correspondante de tab.
    """

    for i in range(len(tab)) :
        for j in range(len(equivalence_ope)):
            if tab[i][0] == equivalence_ope[j][0]:
                chaine[i] = chaine[i] + equivalence_ope[j][1]
    return chaine
        
def immediate (tab, chaine):
    """
    Ajoute le bit « immédiat » : 1 pour ADDi et SUBi, 0 pour les autres instructions.
    """

    for i in range(len(tab)):
        if(tab[i][0]=='ADDi' or tab[i][0]=='SUBi'):
            chaine[i] = chaine[i] + '1'
        else :
            chaine[i] = chaine[i] + '0'
    return chaine

def convertir_registe(tab, chaine):
    """
    Ajoute à chaque chaîne les 9 bits des champs registres : DR, SR1, SR2 (3 bits chacun).
 
    - Instruction de saut : DR = 000, SR1 = 1er registre, SR2 = 2e registre
      (l'adresse du saut est gérée par convertir_nombre_immediat).
    - ADDi / SUBi : le dernier opérande est une constante, SR2 est mis à 000.
    - Autres instructions : un champ par registre dans l'ordre des opérandes.
    Seul le dernier chiffre du nom de registre est utilisé (R3 -> 3).
    """

    for i in range(len(tab)):
        op = tab[i][0]
        if op in ('CALL', 'RET'):
            chaine[i] += '000000000'
        elif op in dictionaire['CTRL']:
            chaine[i] += '000' + binaire(int(tab[i][1][-1])) + binaire(int(tab[i][2][-1]))
        else:
            fin = len(tab[i])
            immediat = op in ('ADDi', 'SUBi')
            if immediat:
                fin -= 1                      
            for j in range(1, fin):
                chaine[i] += binaire(int(tab[i][j][-1]))
            if immediat:
                chaine[i] += '000'            
    return chaine


def convertir_nombre_immediat (tab, chaine):
    """
    Ajoute les 17 derniers bits de l'instruction : l'adresse de saut (sauts),
    un 0 suivi de la constante sur 16 bits (ADDi / SUBi), ou des zéros (autres).
    """

    for i in range(len(tab)):
        op = tab[i][0]
        if op == 'RET':
            chaine[i] += '00000000000000000'
        elif op in dictionaire['CTRL']:
            chaine[i] += binaire(int(tab[i][-1]), 17)          
        elif op in ('ADDi', 'SUBi'):
            chaine[i] += f'0{binaire(int(tab[i][-1]), 16)}'
        else :
            chaine[i] += '00000000000000000'
    return chaine
 
def ecrire(tab, fichier):
    """
    Écrit le fichier chargeable dans la RAM de Logisim (format « v2.0 raw »).
 
    Chaque chaîne de tab est ici de la forme type(2) ope(3) imm(1) DR(3) SR1(3) SR2(3) cst(17).
    Elle est réorganisée en un mot de 32 bits (bits 31 -> 0), écrit en hexadécimal
    sur 8 chiffres, un mot par ligne :
    - saut         : adresse (bits 31..16) | 0 | SR2 | SR1 | DR | imm | ope | type
    - ADDi / SUBi  : 0000 | constante (bits 27..12) | SR1 | DR | imm | ope | type
    - autres       : 17 zéros | SR2 | SR1 | DR | imm | ope | type
    """

    with open(fichier, "w", encoding="utf-8") as f:
        f.write("v2.0 raw\n")
        for s in tab:
            type_, ope, flag = s[0:2], s[2:5], s[5]
            dr, sr1, sr2 = s[6:9], s[9:12], s[12:15]
            imm = s[15:32]                                 
            if type_ == '11':                               
                mot = imm[1:] + '0' + sr2 + sr1 + dr + flag + ope + type_
            elif flag == '1':                               
                mot = '0000' + imm[1:] + sr1 + dr + flag + ope + type_
            else:                                           
                mot = '0' * 17 + sr2 + sr1 + dr + flag + ope + type_
            f.write(f"{int(mot, 2):08x}\n")



def traduire(fichier_entree, fichier_sortie):
    """
    Traduit un fichier assembleur en fichier mémoire pour Logisim.
 
    Enchaîne la lecture et le découpage des lignes, la construction de chaque
    instruction (type, opération, bit immédiat, registres, constante ou adresse),
    puis l'écriture du résultat dans `fichier_sortie`.
    """

    chaine_decompose = lecture_ligne(lecture_fichier(fichier_entree))
    type_ope  = retourne_ope(chaine_decompose)
    type_binaire = convertir_type_ope(type_ope)
    type_et_ope_binaire = convertir_ope(chaine_decompose, type_binaire)
    ope_immediate = immediate(chaine_decompose, type_et_ope_binaire)
    registre = convertir_registe(chaine_decompose, ope_immediate)
    final = convertir_nombre_immediat(chaine_decompose, registre)
    ecrire(final, fichier_sortie)


traduire("test1.asm", "resultat1.txt")
traduire("test2.asm", "resultat2.txt")
traduire("test3.asm", "resultat3.txt")
traduire("test4.asm", "resultat4.txt")
traduire("test5.asm", "resultat5.txt")
traduire("test6.asm", "resultat6.txt")