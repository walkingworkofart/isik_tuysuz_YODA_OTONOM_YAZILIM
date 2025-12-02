import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

# Odevimde time fonksiyonunu egitim setinde gormedigimden ve bazi bolumlerde tikandigimdan
# AI yardimi alinmistir.

cam = cv2.VideoCapture("video2.mp4") #video secimi
yuz = cv2.CascadeClassifier('facedetection.xml') #xml dosyasini ekleme
baslangic = None #sayac icin baslangic zamani tanimi
sure = 0 #gecen sure tanimi
koordinat_gecmisi = [] #koordinat gecmisi icin bos bir liste olusturuyoruz
koordinat_sayisi = 60 # cizilecek maksimum koordinat sayisini belirliyoruz

if not cam.isOpened(): #Videonun calisip calismadigini kontrol islemi
    print("Video acilamadi.")
    exit()


while True: #goruntu alma ve videoyu okuma islemi
    ret, frame = cam.read()

    if not ret:
        print("Video okunamadi.")
        break 

    griton = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #daha iyi bir sonuc icin goruntuyu griye cevirme islemi
    yuzler = yuz.detectMultiScale(griton,1.3,1) #videodaki yuzu tanima islemi
    yuz_bulundu = False #sayac icin yuzun ekranda olup olmadigini tanimlamamiz lazim, en basta False
    #olarak belirledik ancak islem icerisinde True oldugunda sayac baslama islemini yapacagiz.
    

    koordinats = "Koordinatlar: Yuz Bulunamadi" #merkez koordinatlarini yazdirmadan once en basta kadrajdan
    #ciktiginda yuzun bulunamadigini gostermek icin bir metin tanimi yapmamiz lazim.

    for x,y,w,h in yuzler: #tanimlanan yuzun koordinatlari, genisligi ve yuksekligi
        yuz_bulundu = True #yuz tanima dongusunun icerisinde yuzun ekranda oldugunun bilgisini
        #verebilmek icin tanimladigimiz kodun false dan true ya cevrilmesini sagliyoruz.
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3) #bounding box
        merkezx= x+w//2 # merkez noktanin x koordinati
        merkezy= y+h//2 # merkez noktanin y koordinati
        koordinats = f"Koordinatlar: {merkezx}, {merkezy} " #degisken merkez koordinatlarini yazdirabilmek
        #icin string formatina ceviriyoruz (int olarak yazdiramiyoruz)
        cv2.circle(frame,(merkezx,merkezy),5,(0,0,255),-1) #bounding box merkezine bir nokta koyduk

    if yuz_bulundu: #yuz ekranda bulunduysa
        koordinat_gecmisi.append((merkezx,merkezy)) #mevcut framedeki box'ın merkez koordinatlarini listeye ekle
        if len(koordinat_gecmisi) > koordinat_sayisi: #eger koordinat gecmisinde 60' dan az koordinat varsa
            koordinat_gecmisi.pop(0) #listenin basindaki (ilk koordinatlari) gecmisten sil (bu sekilde liste surekli guncel kalacak)

        if baslangic is None: #sayma baslamadiysa
            baslangic = time.time() #sayaci baslat
        sure = time.time() - baslangic

    else: #eger yuz ekranda degilse
        baslangic = None #sayaci sifirla
        sure = 0
        koordinat_gecmisi = [] #koordinat gecmisini sifirla

    for i in range(1, len(koordinat_gecmisi)): #for dongusuyle listedeki butun koordinatlari tek tek tanimlama islemi
        ilknokta = koordinat_gecmisi[i-1]
        ikincinokta = koordinat_gecmisi[i]

        cv2.line(frame,ilknokta,ikincinokta,(255,255,0),2) #tum tanimlanan noktalarin arasina cizgi cekme islemi

    saniye = f"Sayac: {sure}" #degisken sayma islemini str formatina dondurme
    cv2.putText(frame,saniye,(1180,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2) #sayaci yazdirma

    cv2.putText(frame,koordinats,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2) #koordinatlari yazdirma

    cv2.imshow("pencere",frame) #pencerenin icerisine goruntuyu ekleme

    if ret == 0: 
        break

    if cv2.waitKey(10) & 0xFF == ord("q"): #cikis islemi
        break

cam.release() #videoyu serbest birakma islemi
cv2.destroyAllWindows() #tum pencereleri kapatma islemi