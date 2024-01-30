#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import os
 
try:
    from termcolor import cprint
except ImportError:
    def cprint(*args, **kwargs):
        print(*args)
 
kelimeler = ["vantilatör", "adaptör", "kalem", "fare", "telefon", "kulaklık", "pervane", "merdane", "kestane"]
 
 
def oyun_hazirlik():
    global secilen_kelime, gorunen_kelime, can
    import random
    secilen_kelime = random.choice(kelimeler)
    gorunen_kelime = ["-"] * len(secilen_kelime)
    can = 5
 
 
def harf_al():
    devam = True
    while devam:
        harf = input("Bir harf giriniz: ")
        if harf.lower() == "quit":
            cprint("Gidiyor gönlümün efendisi...", color="red", on_color="on_blue")
            exit()
        elif len(harf) == 1 and harf.isalpha() and harf not in gorunen_kelime:
            devam = False
        else:
            cprint("Hatalı Giriş", color="red", on_color="on_grey")
 
    # noinspection PyUnboundLocalVariable
    return harf.lower()
 
 
def oyun_dongusu():
    global gorunen_kelime, can
    while can > 0 and secilen_kelime != "".join(gorunen_kelime):
        cprint("kelime: " + "".join(gorunen_kelime), color="cyan", attrs=["bold"])
        cprint("can   : <" + "❤" * can + " " * (5 - can) + ">", color="cyan", attrs=["bold"])
 
        girilen_harf = harf_al()
        pozisyonlar = harf_kontrol(girilen_harf)
        if pozisyonlar:
            for p in pozisyonlar:
                gorunen_kelime[p] = girilen_harf
        else:
            can -= 1
 
 
def harf_kontrol(girilen_harf):
    poz = []
    for index, h in enumerate(secilen_kelime):
        if h == girilen_harf:
            poz.append(index)
    return poz
 
 
def skor_tablosunu_goster():
    
    veri = ayar_oku()
    cprint("Skor\t\tKullanıcı", color="white", on_color="on_grey")
    cprint("------------------------", color="white", on_color="on_grey")
    for skor, kullanici in veri["skorlar"]:
        cprint("|"+str(skor) +"\t\t"+ kullanici+" "*(9-len(kullanici))+"|", color="white", on_color="on_grey")
    cprint("------------------------", color="white", on_color="on_grey")
 
 
def skor_tablosunu_guncelle():
    veri = ayar_oku()
    veri["skorlar"].append((can, veri["son_kullanan"]))
    veri["skorlar"].sort(key=lambda skor_tuplei: skor_tuplei[0], reverse=True)
    veri["skorlar"] = veri["skorlar"][:5]
    ayar_yaz(veri)
 
 
def oyun_sonucu():
    if can > 0:
        cprint("Kazandınız", color="yellow", on_color="on_red")
        skor_tablosunu_guncelle()
    else:
        cprint("Kaybettiniz", color="red", on_color="on_yellow")
    skor_tablosunu_goster()
 
 
def dosyay_kontrol_et_yoksa_olustur():
    yaz = False
    if os.path.exists("ayarlar.json"):
        try:
            ayar_oku()
        except ValueError as e:
            cprint("Hata: ValueError(" + ",".join(e.args) + ")", color="red", on_color="on_blue", attrs=["bold"])
            os.remove("ayarlar.json")
            yaz = True
    else:
        yaz = True
 
    if yaz:
        ayar_yaz({"skorlar": [], "son_kullanan": ""})
 
 
def ayar_oku():
    with open("ayarlar.json") as f:
        return json.load(f)
 
 
def ayar_yaz(veri):
    with open("ayarlar.json", "w") as f:
        json.dump(veri, f)
 
 
def kullanici_adini_guncelle():
    veri = ayar_oku()
    veri["son_kullanan"] = input("Kullanıcı Adınız: ")
    while not veri["son_kullanan"] or len(veri["son_kullanan"]) > 9:
        veri["son_kullanan"] = input("lykpython ile 9 karakter uzunluğunda yazın: ")
    ayar_yaz(veri)
 
 
def kullanici_kontrol():
    veri = ayar_oku()
    print("Son giriş yapan: " + veri["son_kullanan"])
    if not veri["son_kullanan"]:
        kullanici_adini_guncelle()
    elif input("Bu siz misiniz?(e/h) ").lower() == "h":
        kullanici_adini_guncelle()
 
 
def main():
    tekrar_edecek_mi = True
    dosyay_kontrol_et_yoksa_olustur()
    cprint("Merhaba, Adam Asmacaya hoşgeldiniz.", color="cyan", on_color="on_magenta", attrs=["bold"])
    cprint("Yardım: Oyun sırasında quit diyerek çıkabilirsiniz", color="cyan", on_color="on_magenta", attrs=["bold"])
    cprint("-"*30, color="cyan", on_color="on_magenta", attrs=["bold"])
    skor_tablosunu_goster()
    kullanici_kontrol()
    while tekrar_edecek_mi:
        oyun_hazirlik()
        oyun_dongusu()
        oyun_sonucu()
        if input("Devam?(e/h) ").lower() == "h":
            tekrar_edecek_mi = False
    cprint("Gidiyor gönlümün efendisi...", color="red", on_color="on_blue")
  
main()


# In[ ]:





# In[ ]:




