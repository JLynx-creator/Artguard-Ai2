import streamlit as st
import hashlib
import json
import datetime
from PIL import Image, ImageDraw
import imagehash
import qrcode
from io import BytesIO
import base64
import os
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")

DATA_F = 'veri.json'

def hash_password(pwd):
    salt = "nft2024xyz"
    return hashlib.sha256((pwd + salt).encode()).hexdigest()

def load_data():
    data_file = DATA_F
    if not os.path.exists(data_file):
        initial_data = {
            'kullanicilar': {
                'admin': {
                    'sifre_hash': hash_password('admin123'),
                    'nftler': [],
                    'para': 1000,
                    'kayit_tarihi': str(datetime.datetime.now())
                }
            },
            'bloklar': [],
            'pazar': [],
            'islemler': []
        }
        try:
            save_data(initial_data)
        except:
            pass
        return initial_data
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("JSON hatasi - bos dosya olusturuluyor")
        return load_data()
    except Exception as e:
        print(f"Veri yukleme hatasi: {e}")
        return load_data()

def save_data(data_obj):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with open(DATA_F, 'w', encoding='utf-8') as f:
                json.dump(data_obj, f, ensure_ascii=False, indent=2)
            return True
        except PermissionError:
            print(f"Permission hatasi - deneme {attempt + 1}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Kaydetme hatasi {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return False
    return False

if 'veri' not in st.session_state:
    st.session_state.veri = load_data()
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False
if 'kullanici_adi' not in st.session_state:
    st.session_state.kullanici_adi = None

veri = st.session_state.veri

if st.session_state.giris_yapildi == False:
    st.markdown("<h1 style='text-align:center;'>🎨 ArtGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>NFT Pazari</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    sekme1, sekme2 = st.tabs(["Giris Yap", "Hesap Ac"])
    
    with sekme1:
        st.subheader("Giris Yap")
        kullanici_gir = st.text_input("Kullanici Adi", key="giris_kullanici")
        sifre_gir = st.text_input("Sifre", type="password", key="giris_sifre")
        
        if st.button("Giris", key="giris_buton"):
            if kullanici_gir in veri['kullanicilar']:
                user_info = veri['kullanicilar'][kullanici_gir]
                input_hash = hash_password(sifre_gir)
                if user_info['sifre_hash'] == input_hash:
                    st.session_state.giris_yapildi = True
                    st.session_state.kullanici_adi = kullanici_gir
                    st.success("Hosgeldiniz!")
                    st.rerun()
                else:
                    st.error("Sifre yanlis!")
            else:
                st.error("Kullanici bulunamadi!")
    
    with sekme2:
        st.subheader("Yeni Hesap")
        yeni_kullanici = st.text_input("Kullanici Adi", key="kayit_kullanici")
        yeni_sifre1 = st.text_input("Sifre", type="password", key="kayit_sifre1")
        yeni_sifre2 = st.text_input("Sifre Tekrar", type="password", key="kayit_sifre2")
        
        if st.button("Hesap Olustur", key="kayit_buton"):
            if yeni_kullanici and yeni_sifre1:
                if len(yeni_sifre1) < 4:
                    st.error("Sifre en az 4 karakter olmali!")
                elif yeni_sifre1 != yeni_sifre2:
                    st.error("Sifreler uyusmuyor!")
                elif yeni_kullanici in veri['kullanicilar']:
                    st.error("Bu kullanici adi alinmis!")
                else:
                    veri['kullanicilar'][yeni_kullanici] = {
                        'sifre_hash': hash_password(yeni_sifre1),
                        'nftler': [],
                        'para': 500,
                        'kayit_tarihi': str(datetime.datetime.now())
                    }
                    if save_data(veri):
                        st.success("Hesap olusturuldu!")
                    else:
                        st.error("Kayit hatasi!")
            else:
                st.error("Tum alanlari doldurun!")
    
    st.stop()

aktif_kullanici = veri['kullanicilar'][st.session_state.kullanici_adi]

with st.sidebar:
    st.markdown("## 👤 " + st.session_state.kullanici_adi)
    st.markdown("💰 Bakiye: " + str(aktif_kullanici['para']) + " TL")
    st.markdown("🎨 NFT Sayisi: " + str(len(aktif_kullanici['nftler'])))
    st.markdown("---")
    
    sayfa_secim = st.radio("Sayfalar", ["Ana Sayfa", "NFT Koleksiyonum", "NFT Pazari", "Blockchain Kayitlari", "📊 Blockchain Analizi", "Profil"])
    
    st.markdown("---")
    if st.button("Cikis Yap"):
        st.session_state.giris_yapildi = False
        st.session_state.kullanici_adi = None
        st.rerun()

def file_hash_calc(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

def block_hash_calc(block_data):
    combined = str(block_data['numara']) + block_data['zaman'] + block_data['sahip'] + block_data['dosya_hash']
    if block_data['numara'] > 0:
        combined += block_data['onceki_hash']
    return hashlib.sha256(combined.encode()).hexdigest()

def img_hash_calc(img_obj):
    try:
        return str(imagehash.average_hash(img_obj))
    except:
        return None

def similarity_check(new_img_hash):
    max_similarity = 0
    match_index = -1
    
    for i, block in enumerate(veri['bloklar']):
        if 'resim_hash' not in block or block['resim_hash'] is None:
            continue
            
        try:
            old_hash = imagehash.hex_to_hash(block['resim_hash'])
            new_hash = imagehash.hex_to_hash(new_img_hash)
            diff = new_hash - old_hash
            similarity = 100 * (1 - diff / 64.0)
            
            if similarity > max_similarity:
                max_similarity = similarity
                match_index = i
        except:
            pass
    
    return match_index, max_similarity

def blockchain_gorsel_olustur():
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        blok_sayisi = len(veri['bloklar'])
        if blok_sayisi == 0:
            ax.text(5, 5, "Henüz blok yok", ha='center', va='center', fontsize=16)
            return fig
        
        max_goster = min(blok_sayisi, 8)
        y_pos = 8
        
        for i in range(max_goster):
            blok = veri['bloklar'][i]
            
            renk = '#4CAF50' if i == 0 else '#2196F3'
            rect = patches.Rectangle((1, y_pos), 8, 0.8, linewidth=2, edgecolor=renk, facecolor='lightgray')
            ax.add_patch(rect)
            
            ax.text(1.5, y_pos + 0.4, f"Blok #{blok['numara']}", fontsize=10, weight='bold')
            ax.text(1.5, y_pos + 0.1, f"Sahip: {blok['sahip'][:10]}...", fontsize=8)
            ax.text(6, y_pos + 0.4, f"Hash: {blok['blok_hash'][:12]}...", fontsize=8)
            ax.text(6, y_pos + 0.1, f"Tarih: {blok['zaman'][:10]}", fontsize=8)
            
            if i > 0:
                ax.arrow(5, y_pos + 0.8, 0, 0.2, head_width=0.1, head_length=0.1, fc='red', ec='red')
            
            y_pos -= 1.2
        
        ax.set_title("Blockchain Görselleştirme", fontsize=16, weight='bold', pad=20)
        return fig
        
    except Exception as e:
        print(f"Gorsel hatasi: {e}")
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(5, 5, "Gorsel olusturulamadi", ha='center', va='center', fontsize=16)
        return fig

def timeline_gorsel_olustur(nft_numarasi):
    try:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.axis('off')
        
        ilgili_islemler = []
        for islem in veri['islemler']:
            if islem.get('nft_no') == nft_numarasi:
                ilgili_islemler.append(islem)
        
        if not ilgili_islemler:
            ax.text(5, 2.5, "Bu NFT için işlem bulunamadı", ha='center', va='center', fontsize=14)
            return fig
        
        x_pos = 1
        colors = {'mint': 'green', 'transfer': 'blue', 'satis': 'red'}
        
        for islem in ilgili_islemler:
            renk = colors.get(islem['tip'], 'gray')
            
            circle = patches.Circle((x_pos, 2.5), 0.3, color=renk, alpha=0.7)
            ax.add_patch(circle)
            
            ax.text(x_pos, 3.2, islem['tip'].upper(), ha='center', fontsize=10, weight='bold')
            ax.text(x_pos, 1.8, islem['zaman'][:10], ha='center', fontsize=8)
            
            if islem.get('alan'):
                ax.text(x_pos, 1.2, f"→ {islem['alan']}", ha='center', fontsize=8)
            
            x_pos += 2
        
        ax.set_title(f"NFT #{nft_numarasi} Timeline", fontsize=16, weight='bold', pad=20)
        return fig
        
    except Exception as e:
        print(f"Timeline hatasi: {e}")
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.text(7, 4, "Timeline olusturulamadi", ha='center', va='center', fontsize=14)
        return fig

def sertifika_olustur(blok_data):
    genislik = 800
    yukseklik = 600
    
    resim = Image.new('RGB', (genislik, yukseklik), 'white')
    cizim = ImageDraw.Draw(resim)
    
    mavi_renk = (41, 128, 185)
    
    cizim.rectangle([10, 10, genislik-10, yukseklik-10], outline=mavi_renk, width=5)
    cizim.rectangle([20, 20, genislik-20, yukseklik-20], outline=mavi_renk, width=2)
    
    qr_veri = "NFT#" + str(blok_data['numara']) + "|" + blok_data['blok_hash'][:16]
    qr_kod = qrcode.QRCode(version=1, box_size=5, border=2)
    qr_kod.add_data(qr_veri)
    qr_kod.make(fit=True)
    qr_resim = qr_kod.make_image(fill_color="black", back_color="white")
    qr_resim = qr_resim.resize((150, 150))
    resim.paste(qr_resim, (genislik - 180, 30))
    
    y_konum = 60
    cizim.text((genislik//2 - 150, y_konum), "NFT SERTİFİKASI", fill=mavi_renk)
    y_konum = y_konum + 60
    cizim.text((50, y_konum), "Eser Adi: " + blok_data['isim'], fill='black')
    y_konum = y_konum + 40
    cizim.text((50, y_konum), "Sahip: " + blok_data['sahip'], fill='black')
    y_konum = y_konum + 40
    cizim.text((50, y_konum), "Token No: #" + str(blok_data['numara']), fill='black')
    y_konum = y_konum + 40
    cizim.text((50, y_konum), "Tarih: " + blok_data['zaman'][:19], fill='gray')
    
    return resim

if sayfa_secim == "Ana Sayfa":
    st.title("🏠 Ana Sayfa")
    st.markdown("---")
    
    toplam_nft = len(veri['bloklar'])
    benim_nft = len(aktif_kullanici['nftler'])
    pazardaki = len(veri['pazar'])
    
    kolon1, kolon2, kolon3 = st.columns(3)
    
    with kolon1:
        st.metric("Toplam NFT", toplam_nft)
    with kolon2:
        st.metric("Benim NFT", benim_nft)
    with kolon3:
        st.metric("Pazarda", pazardaki)
    
    st.markdown("---")
    st.subheader("📤 Yeni Eser Yukle")
    
    yuklenen_dosya = st.file_uploader("Dosya Sec", type=['jpg', 'jpeg', 'png'])
    
    if yuklenen_dosya:
        dosya_baytlari = yuklenen_dosya.read()
        dosya_hash = file_hash_calc(dosya_baytlari)
        
        kopya_var_mi = False
        for blok in veri['bloklar']:
            if blok['dosya_hash'] == dosya_hash:
                kopya_var_mi = True
                st.error("🚨 BU DOSYA ZATEN KAYITLI!")
                st.info("Sahip: " + blok['sahip'] + " | Eser: " + blok['isim'])
                break
        
        if kopya_var_mi == False:
            sol_kolon, sag_kolon = st.columns([2, 1])
            
            with sol_kolon:
                st.image(yuklenen_dosya, width=400)
            
            with sag_kolon:
                st.success("✅ Yeni Dosya")
                st.code(dosya_hash[:20] + "...")
                
                # AI benzerlik kontrol - cakisma tespiti
                if yuklenen_dosya.type.startswith('image'):
                    try:
                        resim = Image.open(yuklenen_dosya)
                        resim_hash = img_hash_calc(resim)
                        
                        if resim_hash != None and len(veri['bloklar']) > 0:
                            benzer_idx, benzerlik_skoru = similarity_check(resim_hash)
                            
                            if benzerlik_skoru > 85:
                                st.warning("⚠️ BENZER RESIM BULUNDU!")
                                st.warning("Benzerlik: %" + str(round(benzerlik_skoru, 1)))
                                st.warning("Benzer NFT: #" + str(benzer_idx))
                            elif benzerlik_skoru > 70:
                                st.info("ℹ️ Orta benzerlik: %" + str(round(benzerlik_skoru, 1)))
                    except Exception as ai_err:
                        print(f"AI kontrol hatasi: {ai_err}")
                        # AI hata olursa sessiz gec
            
            st.markdown("---")
            
            # nft bilgileri al
            bilgi_kolon1, bilgi_kolon2 = st.columns(2)
            
            with bilgi_kolon1:
                nft_isim = st.text_input("NFT Ismi")
            with bilgi_kolon2:
                nft_fiyat = st.number_input("Fiyat (TL)", min_value=0, value=100)
            
            nft_aciklama = st.text_area("Aciklama", height=80)
            
            # olustur butonu
            if st.button("🔗 NFT Olustur", use_container_width=True):
                if nft_isim == None or nft_isim == "":
                    st.error("NFT ismi bos olamaz!")
                else:
                    # onceki blok hash al
                    onceki_blok_hash = ""
                    if len(veri['bloklar']) > 0:
                        son_blok = veri['bloklar'][-1]
                        onceki_blok_hash = son_blok['blok_hash']
                    
                    # yeni blok olustur
                    yeni_blok = {
                        'numara': len(veri['bloklar']),
                        'zaman': str(datetime.datetime.now()),
                        'isim': nft_isim,
                        'sahip': st.session_state.kullanici_adi,
                        'dosya_hash': dosya_hash,
                        'onceki_hash': onceki_blok_hash,
                        'fiyat': nft_fiyat,
                        'aciklama': nft_aciklama,
                        'satista': False,
                        'resim_veri': base64.b64encode(dosya_baytlari).decode()
                    }
                    
                    # resim hash ekle - AI kontrol icin
                    if yuklenen_dosya.type.startswith('image'):
                        try:
                            resim = Image.open(yuklenen_dosya)
                            yeni_blok['resim_hash'] = img_hash_calc(resim)
                        except Exception as img_err:
                            print(f"Resim hash hatasi: {img_err}")
                            yeni_blok['resim_hash'] = None
                    else:
                        yeni_blok['resim_hash'] = None
                    
                    # blok hash hesapla - kacinci blok oldugu onemli
                    yeni_blok['blok_hash'] = block_hash_calc(yeni_blok)
                    
                    # blockchain'e ekle
                    veri['bloklar'].append(yeni_blok)
                    
                    # kullaniciya ekle
                    aktif_kullanici['nftler'].append(yeni_blok['numara'])
                    
                    # islem kaydi - mint islemi
                    yeni_islem = {
                        'tip': 'mint',
                        'nft_no': yeni_blok['numara'],
                        'gonderen': None,
                        'alan': st.session_state.kullanici_adi,
                        'fiyat': 0,
                        'zaman': str(datetime.datetime.now())
                    }
                    veri['islemler'].append(yeni_islem)
                    
                    # veritabanina kaydet
                    if not save_data(veri):
                        st.error("Kayit hatasi!")
                        st.rerun()
                    
                    st.success("✅ NFT olusturuldu! Token #" + str(yeni_blok['numara']))
                    st.balloons()
                    
                    # sertifika indir
                    sertifika = sertifika_olustur(yeni_blok)
                    sertifika_buffer = BytesIO()
                    sertifika.save(sertifika_buffer, format='PNG')
                    sertifika_buffer.seek(0)
                    
                    st.download_button(
                        "📥 Sertifika Indir",
                        sertifika_buffer,
                        "sertifika_" + str(yeni_blok['numara']) + ".png",
                        "image/png"
                    )

# NFT KOLEKSIYONUM SAYFASI
elif sayfa_secim == "NFT Koleksiyonum":
    st.title("🎨 NFT Koleksiyonum")
    st.markdown("---")
    
    if len(aktif_kullanici['nftler']) == 0:
        st.info("Henuz NFT'niz yok. Ana sayfadan eser yukleyin!")
    else:
        # grid duzeni
        satirda_kac = 3
        toplam_nft_sayisi = len(aktif_kullanici['nftler'])
        
        # satirlar halinde goster
        for satir_no in range(0, toplam_nft_sayisi, satirda_kac):
            satirda_kolonlar = st.columns(satirda_kac)
            
            for kolon_no in range(satirda_kac):
                if satir_no + kolon_no < toplam_nft_sayisi:
                    nft_numarasi = aktif_kullanici['nftler'][satir_no + kolon_no]
                    nft_bilgi = veri['bloklar'][nft_numarasi]
                    
                    with satirda_kolonlar[kolon_no]:
                        # kart arka plani
                        st.markdown("<div style='background:white;padding:10px;border-radius:10px;'>", unsafe_allow_html=True)
                        
                        # resim goster
                        if 'resim_veri' in nft_bilgi:
                            resim_bytes = base64.b64decode(nft_bilgi['resim_veri'])
                            st.image(resim_bytes)
                        
                        # bilgiler
                        st.markdown("**" + nft_bilgi['isim'] + "**")
                        st.caption("Token #" + str(nft_bilgi['numara']))
                        st.caption("💰 " + str(nft_bilgi['fiyat']) + " TL")
                        
                        # butonlar
                        buton_kolon1, buton_kolon2 = st.columns(2)
                        
                        with buton_kolon1:
                            if nft_bilgi['satista'] == False:
                                if st.button("Sat", key="sat_buton_" + str(nft_numarasi)):
                                    nft_bilgi['satista'] = True
                                    veri['pazar'].append(nft_numarasi)
                                    kayit_et(veri)
                                    st.success("Pazara eklendi!")
                                    st.rerun()
                        
                        with buton_kolon2:
                            if st.button("Transfer", key="transfer_buton_" + str(nft_numarasi)):
                                st.session_state['transfer_nft'] = nft_numarasi
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        
        # transfer modal
        if 'transfer_nft' in st.session_state:
            st.markdown("---")
            st.subheader("🔄 NFT Transfer")
            
            transfer_edilecek_nft = veri['bloklar'][st.session_state['transfer_nft']]
            st.write("**Eser:** " + transfer_edilecek_nft['isim'])
            
            alici_kullanici = st.text_input("Alici Kullanici Adi")
            
            if st.button("Transfer Et"):
                if alici_kullanici == None or alici_kullanici == "":
                    st.error("Alici kullanici adi bos olamaz!")
                elif alici_kullanici not in veri['kullanicilar']:
                    st.error("Kullanici bulunamadi!")
                elif alici_kullanici == st.session_state.kullanici_adi:
                    st.error("Kendinize transfer yapamazsiniz!")
                else:
                    # mevcut kullanicidan kaldir
                    aktif_kullanici['nftler'].remove(st.session_state['transfer_nft'])
                    
                    # yeni kullaniciya ekle
                    veri['kullanicilar'][alici_kullanici]['nftler'].append(st.session_state['transfer_nft'])
                    
                    # blockchain guncelle
                    transfer_edilecek_nft['sahip'] = alici_kullanici
                    
                    # islem kaydi
                    transfer_islem = {
                        'tip': 'transfer',
                        'nft_no': st.session_state['transfer_nft'],
                        'gonderen': st.session_state.kullanici_adi,
                        'alan': alici_kullanici,
                        'fiyat': 0,
                        'zaman': str(datetime.datetime.now())
                    }
                    veri['islemler'].append(transfer_islem)
                    
                    # kaydet
                    kayit_et(veri)
                    
                    st.success("Transfer tamamlandi!")
                    del st.session_state['transfer_nft']
                    st.rerun()

# NFT PAZARI SAYFASI
elif sayfa_secim == "NFT Pazari":
    st.title("🛒 NFT Pazari")
    st.markdown("---")
    
    if len(veri['pazar']) == 0:
        st.info("Pazarda satilik NFT yok.")
    else:
        # grid
        satirda_kac_tane = 3
        toplam_pazar_sayisi = len(veri['pazar'])
        
        for satir in range(0, toplam_pazar_sayisi, satirda_kac_tane):
            pazar_kolonlari = st.columns(satirda_kac_tane)
            
            for kolon in range(satirda_kac_tane):
                if satir + kolon < toplam_pazar_sayisi:
                    pazar_nft_no = veri['pazar'][satir + kolon]
                    pazar_nft = veri['bloklar'][pazar_nft_no]
                    
                    with pazar_kolonlari[kolon]:
                        st.markdown("<div style='background:white;padding:10px;'>", unsafe_allow_html=True)
                        
                        if 'resim_veri' in pazar_nft:
                            img_data = base64.b64decode(pazar_nft['resim_veri'])
                            st.image(img_data)
                        
                        st.markdown("**" + pazar_nft['isim'] + "**")
                        st.caption("Satici: " + pazar_nft['sahip'])
                        st.markdown("### 💰 " + str(pazar_nft['fiyat']) + " TL")
                        
                        # satin alma veya iptal
                        if pazar_nft['sahip'] != st.session_state.kullanici_adi:
                            if st.button("Satin Al", key="al_" + str(pazar_nft_no)):
                                # para kontrol
                                if aktif_kullanici['para'] >= pazar_nft['fiyat']:
                                    # odeme yap
                                    aktif_kullanici['para'] = aktif_kullanici['para'] - pazar_nft['fiyat']
                                    
                                    # satici para al (%10 komisyon)
                                    satici_kazanc = pazar_nft['fiyat'] * 0.9
                                    veri['kullanicilar'][pazar_nft['sahip']]['para'] = veri['kullanicilar'][pazar_nft['sahip']]['para'] + satici_kazanc
                                    
                                    # nft transfer
                                    veri['kullanicilar'][pazar_nft['sahip']]['nftler'].remove(pazar_nft_no)
                                    aktif_kullanici['nftler'].append(pazar_nft_no)
                                    pazar_nft['sahip'] = st.session_state.kullanici_adi
                                    pazar_nft['satista'] = False
                                    veri['pazar'].remove(pazar_nft_no)
                                    
                                    # islem kaydi
                                    satis_islem = {
                                        'tip': 'satis',
                                        'nft_no': pazar_nft_no,
                                        'gonderen': pazar_nft['sahip'],
                                        'alan': st.session_state.kullanici_adi,
                                        'fiyat': pazar_nft['fiyat'],
                                        'zaman': str(datetime.datetime.now())
                                    }
                                    veri['islemler'].append(satis_islem)
                                    
                                    # kaydet
                                    kayit_et(veri)
                                    
                                    st.success("Satin alma basarili!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("Bakiye yetersiz!")
                        else:
                            if st.button("Satisi Iptal Et", key="iptal_" + str(pazar_nft_no)):
                                pazar_nft['satista'] = False
                                veri['pazar'].remove(pazar_nft_no)
                                kayit_et(veri)
                                st.success("Iptal edildi!")
                                st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

# BLOCKCHAIN KAYITLARI
elif sayfa_secim == "Blockchain Kayitlari":
    st.title("📊 Blockchain Kayitlari")
    st.markdown("---")
    
    if len(veri['bloklar']) == 0:
        st.info("Henuz blok yok.")
    else:
        st.write("Toplam Blok Sayisi: " + str(len(veri['bloklar'])))
        
        if len(veri['bloklar']) > 0:
            son_blok = veri['bloklar'][-1]
            st.write("Son Blok Hash: `" + son_blok['blok_hash'][:20] + "...`")
        
        st.markdown("---")
        
        # tum bloklari listele (tersten)
        for blok in reversed(veri['bloklar']):
            with st.expander("Blok #" + str(blok['numara']) + " - " + blok['isim']):
                blok_kolon1, blok_kolon2 = st.columns([1, 2])
                
                with blok_kolon1:
                    if 'resim_veri' in blok:
                        blok_resim = base64.b64decode(blok['resim_veri'])
                        st.image(blok_resim, width=200)
                
                with blok_kolon2:
                    st.write("**Sahip:** " + blok['sahip'])
                    st.write("**Zaman:** " + blok['zaman'][:19])
                    st.write("**Blok Hash:** `" + blok['blok_hash'][:20] + "...`")
                    
                    if blok['onceki_hash'] != "":
                        st.write("**Onceki Hash:** `" + blok['onceki_hash'][:20] + "...`")
                    else:
                        st.write("**Onceki Hash:** Genesis Block")
                    
                    st.write("**Dosya Hash:** `" + blok['dosya_hash'][:20] + "...`")
                    st.write("**Fiyat:** " + str(blok['fiyat']) + " TL")

# BLOCKCHAIN ANALIZI SAYFASI
elif sayfa_secim == "📊 Blockchain Analizi":
    st.title("📊 Blockchain Analizi")
    st.markdown("---")
    
    st.subheader("🔗 Blockchain Görselleştirme")
    
    try:
        fig = blockchain_gorsel_olustur()
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        img = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        st.image(img, use_container_width=True)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        st.download_button("📥 Blockchain Görseli İndir", buf, "blockchain.png", "image/png")
        
    except Exception as e:
        st.error("Görsel oluşturulamadı!")
        st.write(f"Hata: {e}")
    
    st.markdown("---")
    
    st.subheader("🕐 NFT Timeline Analizi")
    
    if len(veri['bloklar']) > 0:
        secili_nft = st.selectbox("NFT Seç", [f"NFT #{blok['numara']} - {blok['isim']}" for blok in veri['bloklar']])
        nft_numarasi = int(secili_nft.split('#')[1].split(' ')[0])
        
        try:
            timeline_fig = timeline_gorsel_olustur(nft_numarasi)
            timeline_canvas = FigureCanvasAgg(timeline_fig)
            timeline_canvas.draw()
            timeline_img = Image.frombytes('RGB', timeline_canvas.get_width_height(), timeline_canvas.tostring_rgb())
            st.image(timeline_img, use_container_width=True)
            
            timeline_buf = BytesIO()
            timeline_fig.savefig(timeline_buf, format='png', dpi=150, bbox_inches='tight')
            timeline_buf.seek(0)
            st.download_button("📥 Timeline İndir", timeline_buf, f"timeline_{nft_numarasi}.png", "image/png")
            
        except Exception as e:
            st.error("Timeline oluşturulamadı!")
            st.write(f"Hata: {e}")
    else:
        st.info("Henüz NFT oluşturulmamış!")
    
    st.markdown("---")
    
    st.subheader("📊 Sistem İstatistikleri")
    
    kol1, kol2, kol3, kol4 = st.columns(4)
    
    with kol1:
        st.metric("Toplam Blok", len(veri['bloklar']))
    with kol2:
        st.metric("Toplam İşlem", len(veri['islemler']))
    with kol3:
        st.metric("Aktif Kullanıcı", len(veri['kullanicilar']))
    with kol4:
        st.metric("Pazardaki NFT", len(veri['pazar']))
    
    st.markdown("---")
    
    st.subheader("🔍 Blockchain Bilgileri")
    
    if len(veri['bloklar']) > 0:
        st.write("**Son Blok:**")
        son_blok = veri['bloklar'][-1]
        st.code(f"""
Blok Numarası: {son_blok['numara']}
Sahip: {son_blok['sahip']}
Oluşturulma: {son_blok['zaman']}
Blok Hash: {son_blok['blok_hash']}
Önceki Hash: {son_blok.get('onceki_hash', 'Genesis')}
Dosya Hash: {son_blok['dosya_hash']}
        """)
        
        st.write("**Hash Bütünlüğü Kontrolü:**")
        hash_kontrol = st.button("Hash Bütünlüğü Doğrula")
        
        if hash_kontrol:
            bolum_sorunlu = False
            for i, blok in enumerate(veri['bloklar']):
                if i > 0:
                    onceki_blok = veri['bloklar'][i-1]
                    if blok['onceki_hash'] != onceki_blok['blok_hash']:
                        st.error(f"Blok #{blok['numara']} hash uyumsuzluğu!")
                        bolum_sorunlu = True
            
            if not bolum_sorunlu:
                st.success("✅ Tüm blok hash'leri uyumlu!")
    else:
        st.info("Henüz blockchain verisi yok!")

# PROFIL SAYFASI
elif sayfa_secim == "Profil":
    st.title("👤 Profil")
    st.markdown("---")
    
    profil_kolon1, profil_kolon2 = st.columns([1, 2])
    
    with profil_kolon1:
        st.image("https://via.placeholder.com/200", width=200)
        st.markdown("### " + st.session_state.kullanici_adi)
        st.caption("Uye Tarihi: " + aktif_kullanici['kayit_tarihi'][:10])
    
    with profil_kolon2:
        st.markdown("### Hesap Bilgileri")
        st.metric("💰 Bakiye", str(aktif_kullanici['para']) + " TL")
        st.metric("🎨 NFT Sayisi", len(aktif_kullanici['nftler']))
        
        st.markdown("---")
        st.markdown("### Cuzdan Islemleri")
        
        ekleme_miktari = st.number_input("Eklemek istediginiz miktar (TL)", min_value=0, value=500, step=50)
        if st.button("Bakiye Ekle"):
            # bakiye kontrol - mantikli mi?
            if ekleme_miktari <= 0:
                st.error("Sifirdan buyuk olmali!")
            else:
                aktif_kullanici['para'] += ekleme_miktari
                if not save_data(veri):
                    st.error("Veri kaydedilemedi!")
                    st.rerun()
                st.success(f"{ekleme_miktari} TL eklendi!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Islem Gecmisi")
        
        # kullanicinin islemleri - filtrele
        kullanici_islemleri = []
        for islem in veri['islemler']:
            if islem.get('gonderen') == st.session_state.kullanici_adi or islem.get('alan') == st.session_state.kullanici_adi:
                kullanici_islemleri.append(islem)
        
        if len(kullanici_islemleri) == 0:
            st.info("Henuz islem yok.")
        else:
            # son 10 islem
            son_islemler = kullanici_islemleri[-10:]
            son_islemler.reverse()
            
            for islem in son_islemler:
                islem_tipi = islem.get('tip', 'BILINMIYOR').upper()
                nft_no = islem.get('nft_no', 0)
                zaman = islem.get('zaman', 'BILINMIYOR')[:19]
                
                st.write(f"**{islem_tipi}** - NFT #{nft_no} - {zaman}")

st.markdown("---")
st.caption("ArtGuard AI | TÜBİTAK 4006 Projesi")
