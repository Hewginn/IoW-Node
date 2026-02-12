
dict_list = []

while nev := input("Adja meg a nevet (0 a befejezeshez):") == "0":
    dict_tel = {"Nev":nev}
    dict_tel["Telefonszam"] = input("Adja meg a telefonszamot: ")
    dict_list.append(dict_tel)