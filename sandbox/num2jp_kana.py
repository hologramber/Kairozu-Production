from random import *

def num2jp_kana(num_start, num_end):

    num_numeric = randint(num_start, num_end)  # Pick a random number between start and end inclusive

    kana1to9 = ['いち', 'に', 'さん', 'よん', 'ご', 'ろく', 'なな', 'はち', 'きゅう']
    kana10to90 = ['じゅう', 'にじゅう', 'さんじゅう', 'よんじゅう', 'ごじゅう', 'ろくじゅう', 'ななじゅう', 'はちじゅう', 'きゅうじゅう']
    kana100to900 = ['ひゃく', 'にひゃく', 'さんびゃく', 'よんひゃく', 'ごひゃく', 'ろっぴゃく', 'ななひゃく', 'はっぴゃく', 'きゅうひゃく']
    kana1000to9000 = ['せん', 'にせん', 'さんぜん', 'よんせん', 'ごせん', 'ろくせん', 'ななせん', 'はっせん', 'きゅうせん']
    kana10kto90k = ['いちまん', 'にまん', 'さんまん', 'よんまん', 'ごまん', 'ろくまん', 'ななまん', 'はちまん', 'きゅうまん']

    def collect_ones(ones):
        if int(ones) == 0:
            num = ''
        else:
            num = kana1to9[int(ones) - 1]
        return num

    def collect_tens(tens):
        if int(tens) == 0:
            num = ''
        else:
            num = kana10to90[int(tens) - 1]
        return num

    def collect_hundreds(hundreds):
        if int(hundreds) == 0:
            num = ''
        else:
            num = kana100to900[int(hundreds) - 1]
        return num

    def collect_thousands(thousands):
        if int(thousands) == 0:
            num = ''
        else:
            num = kana1000to9000[int(thousands) - 1]
        return num

    num_components = list(str(num_numeric))

    if len(num_components) == 1:
        num_kana = kana1to9[num_numeric - 1]
    elif len(num_components) == 2:
        num_b = kana10to90[int(num_components[0])-1]
        num_a = collect_ones(num_components[1])
        num_kana = num_b + num_a
    elif len(num_components) == 3:
        num_c = kana100to900[int(num_components[0])-1]
        num_b = collect_tens(num_components[1])
        num_a = collect_ones(num_components[2])
        num_kana = num_c + num_b + num_a
    elif len(num_components) == 4:
        num_d = kana1000to9000[int(num_components[0])-1]
        num_c = collect_hundreds(num_components[1])
        num_b = collect_tens(num_components[2])
        num_a = collect_ones(num_components[3])
        num_kana = num_d + num_c + num_b + num_a
    elif len(num_components) == 5:
        num_e = kana10kto90k[int(num_components[0])-1]
        num_d = collect_thousands(num_components[1])
        num_c = collect_hundreds(num_components[2])
        num_b = collect_tens(num_components[3])
        num_a = collect_ones(num_components[4])
        num_kana = num_e + num_d + num_c + num_b + num_a
    elif len(num_components) == 6:
        num_f = collect_tens(num_components[0])
        num_e = collect_ones(num_components[1]) + 'まん'
        num_d = collect_thousands(num_components[2])
        num_c = collect_hundreds(num_components[3])
        num_b = collect_tens(num_components[4])
        num_a = collect_ones(num_components[5])
        num_kana = num_f + num_e + num_d + num_c + num_b + num_a
    elif len(num_components) == 7:
        num_g = collect_hundreds(num_components[0])
        num_f = collect_tens(num_components[1])
        num_e = collect_ones(num_components[2]) + 'まん'
        num_d = collect_thousands(num_components[3])
        num_c = collect_hundreds(num_components[4])
        num_b = collect_tens(num_components[5])
        num_a = collect_ones(num_components[6])
        num_kana = num_g + num_f + num_e + num_d + num_c + num_b + num_a
    elif len(num_components) == 8:
        num_h = collect_thousands(num_components[0])
        num_g = collect_hundreds(num_components[1])
        num_f = collect_tens(num_components[2])
        num_e = collect_ones(num_components[3]) + 'まん'
        num_d = collect_thousands(num_components[4])
        num_c = collect_hundreds(num_components[5])
        num_b = collect_tens(num_components[6])
        num_a = collect_ones(num_components[7])
        num_kana = num_h + num_g + num_f + num_e + num_d + num_c + num_b + num_a

    return num_numeric, num_kana

