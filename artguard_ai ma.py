import streamlit as st
import hashlib as hl
import json as js
import datetime as dt
from PIL import Image, ImageDraw
import imagehash as ih
import qrcode as qr
from io import BytesIO
import base64 as b64
import os as os_mod
import time as tm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
import random
import string

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")

DATA_F = 'veri.json'

def hash_password(pwd):
    salt = "nft2024xyz"
    try:
        return hl.sha256((pwd + salt).encode()).hexdigest()
    except Exception as e:
        print(f"Hash error: {e}")
        return hl.sha256(pwd.encode()).hexdigest()

def load_data():
    data_file = DATA_F
    if not os_mod.path.exists(data_file):
        initial_data = {
            'kullanicilar': {
                'admin': {
                    'sifre_hash': hash_password('admin123'),
                    'nftler': [],
                    'para': 1000,
                    'kayit_tarihi': str(dt.datetime.now())
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
            return js.load(f)
    except js.JSONDecodeError:
        print("JSON hatasi - bos dosya olusturuluyor")
        initial_data = {
            'kullanicilar': {
                'admin': {
                    'sifre_hash': hash_password('admin123'),
                    'nftler': [],
                    'para': 1000,
                    'kayit_tarihi': str(dt.datetime.now())
                }
            },
            'bloklar': [],
            'pazar': [],
            'islemler': []
        }
        save_data(initial_data)
        return initial_data
    except Exception as e:
        print(f"Veri yukleme hatasi: {e}")
        initial_data = {
            'kullanicilar': {
                'admin': {
                    'sifre_hash': hash_password('admin123'),
                    'nftler': [],
                    'para': 1000,
                    'kayit_tarihi': str(dt.datetime.now())
                }
            },
            'bloklar': [],
            'pazar': [],
            'islemler': []
        }
        save_data(initial_data)
        return initial_data

def save_data(data_obj):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with open(DATA_F, 'w', encoding='utf-8') as f:
                js.dump(data_obj, f, ensure_ascii=False, indent=2)
            return True
        except PermissionError:
            print(f"Permission hatasi - deneme {attempt + 1}")
            tm.sleep(0.1)
        except Exception as e:
            print(f"Kaydetme hatasi {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                return False
    return False

def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
                    yeni_id = generate_random_id()
                    veri['kullanicilar'][yeni_kullanici] = {
                        'sifre_hash': hash_password(yeni_sifre1),
                        'nftler': [],
                        'para': 500,
                        'kayit_tarihi': str(dt.datetime.now()),
                        'user_id': yeni_id
                    }
                    if save_data(veri):
                        st.success("Hesap olusturuldu!")
                        st.balloons()
                    else:
                        st.error("Hesap olusturulamadi!")
            else:
                st.error("Bosluk birakma!")
    
    st.stop()

aktif_kullanici = veri['kullanicilar'][st.session_state.kullanici_adi]

with st.sidebar:
    st.markdown("## 👤 " + st.session_state.kullanici_adi)
    st.markdown("💰 Bakiye: " + str(aktif_kullanici['para']) + " TL")
    st.markdown("🎨 NFT Sayisi: " + str(len(aktif_kullanici['nftler'])))
    st.markdown("---")
    
    if 'secili_tema' not in st.session_state:
        st.session_state.secili_tema = "Gümüş-Şehir"
    
    tema_secimi = st.selectbox("🎨 Tema", 
        ["Mor-Mavi", "Turuncu-Kırmızı", "Yeşil-Mavi", "Pembe-Mor", "Koyu Mod", 
         "Altın-Sarı", "Gümüş-Şehir", "Deniz-Mavin", "Gün Batımı", "Orman-Yeşil", 
         "Lacivert-Gümüş", "Mercan-Turkuaz", "Eflatun-Gri", "Ateş-Kırmızı", "Buz-Mavi"],
        index=["Mor-Mavi", "Turuncu-Kırmızı", "Yeşil-Mavi", "Pembe-Mor", "Koyu Mod", 
               "Altın-Sarı", "Gümüş-Şehir", "Deniz-Mavin", "Gün Batımı", "Orman-Yeşil", 
               "Lacivert-Gümüş", "Mercan-Turkuaz", "Eflatun-Gri", "Ateş-Kırmızı", "Buz-Mavi"].index(st.session_state.secili_tema)
    )
    
    if tema_secimi != st.session_state.secili_tema:
        st.session_state.secili_tema = tema_secimi
        st.rerun()
    
    st.markdown("---")
    
    sayfa_secim = st.radio("Sayfalar", ["Ana Sayfa", "NFT Koleksiyonum", "NFT Pazari", "Blockchain Kayitlari", "📊 Blockchain Analizi", "Profil"])
    
    st.markdown("---")
    if st.button("Cikis Yap"):
        st.session_state.giris_yapildi = False
        st.session_state.kullanici_adi = None
        st.rerun()

temalar = {
    "Mor-Mavi": {'g1': '#667eea', 'g2': '#764ba2'},
    "Turuncu-Kırmızı": {'g1': '#f46b45', 'g2': '#eea849'},
    "Yeşil-Mavi": {'g1': '#11998e', 'g2': '#38ef7d'},
    "Pembe-Mor": {'g1': '#ee0979', 'g2': '#ff6a00'},
    "Koyu Mod": {'g1': '#2c3e50', 'g2': '#34495e'},
    "Altın-Sarı": {'g1': '#f7971e', 'g2': '#ffd200'},
    "Gümüş-Şehir": {'g1': '#bdc3c7', 'g2': '#2c3e50'},
    "Deniz-Mavin": {'g1': '#2193b0', 'g2': '#6dd5ed'},
    "Gün Batımı": {'g1': '#ff6b6b', 'g2': '#feca57'},
    "Orman-Yeşil": {'g1': '#134e5e', 'g2': '#71b280'},
    "Lacivert-Gümüş": {'g1': '#4b6cb7', 'g2': '#182848'},
    "Mercan-Turkuaz": {'g1': '#ff6b9d', 'g2': '#c44569'},
    "Eflatun-Gri": {'g1': '#8e44ad', 'g2': '#95a5a6'},
    "Ateş-Kırmızı": {'g1': '#ff416c', 'g2': '#ff4b2b'},
    "Buz-Mavi": {'g1': '#4facfe', 'g2': '#00f2fe'}
}

secilen_tema = temalar[st.session_state.secili_tema]
c1 = secilen_tema['g1']
c2 = secilen_tema['g2']

css_style = f"<style>.stApp{{background:linear-gradient(135deg,{c1},{c2});}}"
css_style += ".main .block-container{background:white;border-radius:20px;padding:2rem;box-shadow:0 10px 40px rgba(0,0,0,0.3);max-width:1200px;margin:0 auto;}"
css_style += "h1{color:#2c3e50;text-align:center;}"
css_style += "h2{color:#34495e;border-bottom:2px solid " + c1 + ";padding-bottom:0.5rem;}"
css_style += ".stButton>button{background:linear-gradient(90deg," + c1 + "," + c2 + ");color:white;border-radius:20px;padding:0.6rem 2rem;border:none;}"
css_style += "</style>"
st.markdown(css_style, unsafe_allow_html=True)

def file_hash_calc(file_bytes):
    try:
        return hl.sha256(file_bytes).hexdigest()
    except Exception as e:
        print(f"File hash error: {e}")
        return hl.sha256(str(file_bytes).encode()).hexdigest()

def block_hash_calc(block_data):
    try:
        combined = str(block_data['numara']) + block_data['zaman'] + block_data['sahip'] + block_data['dosya_hash']
        if block_data['numara'] > 0:
            combined += block_data['onceki_hash']
        return hl.sha256(combined.encode()).hexdigest()
    except Exception as e:
        print(f"Block hash error: {e}")
        return generate_random_id()

def img_hash_calc(img_obj):
    try:
        return ih.average_hash(img_obj)
    except Exception as e:
        print(f"Image hash error: {e}")
        return None

def similarity_check(new_img_hash):
    max_similarity = 0
    match_index = -1
    
    if new_img_hash is None:
        return match_index, max_similarity
    
    try:
        for i, blok in enumerate(veri['bloklar']):
            if 'resim_hash' in blok and blok['resim_hash'] is not None:
                try:
                    old_hash = ih.hex_to_hash(str(blok['resim_hash']))
                    diff = new_img_hash - old_hash
                    similarity = 100 * (1 - diff / 64.0)
                    
                    if similarity > max_similarity:
                        max_similarity = similarity
                        match_index = i
                except Exception as hash_err:
                    print(f"Hash karsilastirma hatasi: {hash_err}")
                    continue
    except Exception as e:
        print(f"Similarity check error: {e}")
        pass
    
    return match_index, max_similarity

def blockchain_gorsel_olustur():
    try:
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        blok_sayisi = len(veri['bloklar'])
        if blok_sayisi == 0:
            ax.text(6, 6, "Henüz blok yok", ha='center', va='center', fontsize=18, weight='bold')
            return fig
        
        max_goster = min(blok_sayisi, 6)
        y_pos = 10
        
        for i in range(max_goster):
            blok = veri['bloklar'][i]
            
            if i == 0:
                renk = '#27ae60'
                border_renk = '#229954'
            else:
                renk = '#3498db'
                border_renk = '#2980b9'
            
            rect = patches.Rectangle((2, y_pos), 8, 1.2, linewidth=3, edgecolor=border_renk, facecolor=renk, alpha=0.8)
            ax.add_patch(rect)
            
            ax.text(2.5, y_pos + 0.8, f"🔗 BLOK #{blok['numara']}", fontsize=12, weight='bold', color='white')
            ax.text(2.5, y_pos + 0.5, f"👤 {blok['sahip'][:12]}...", fontsize=10, color='white')
            ax.text(2.5, y_pos + 0.2, f"💰 {blok['fiyat']} TL", fontsize=10, color='white')
            
            ax.text(6, y_pos + 0.8, f"📅 {blok['zaman'][:10]}", fontsize=9, color='white')
            ax.text(6, y_pos + 0.5, f"🔐 {blok['blok_hash'][:14]}...", fontsize=8, color='white')
            ax.text(6, y_pos + 0.2, f"📁 {blok['dosya_hash'][:14]}...", fontsize=8, color='white')
            
            if i > 0:
                ax.annotate('', xy=(6, y_pos + 1.2), xytext=(6, y_pos + 2.2),
                           arrowprops=dict(arrowstyle='->', lw=3, color='#e74c3c', alpha=0.7))
            
            y_pos -= 2.0
        
        ax.set_title("🔗 BLOCKCHAIN GÖRSELLEŞTİRME", fontsize=20, weight='bold', pad=30, color='#2c3e50')
        ax.add_patch(patches.Rectangle((0, 0), 12, 12, facecolor='#ecf0f1', alpha=0.3))
        
        return fig
        
    except Exception as e:
        print(f"Gorsel hatasi: {e}")
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.text(7, 6, "Görsel oluşturulamadı", ha='center', va='center', fontsize=16)
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
        ax.text(7, 4, "Timeline oluşturulamadı", ha='center', va='center', fontsize=14)
        return fig

def sertifika_olustur(blok_data):
    try:
        genislik = 800
        yukseklik = 600
        
        resim = Image.new('RGB', (genislik, yukseklik), 'white')
        cizim = ImageDraw.Draw(resim)
        
        mavi_renk = (41, 128, 185)
        
        cizim.rectangle([10, 10, genislik-10, yukseklik-10], outline=mavi_renk, width=5)
        cizim.rectangle([20, 20, genislik-20, yukseklik-20], outline=mavi_renk, width=2)
        
        sahip_temiz = blok_data['sahip']
        for k, v in [('ş','s'), ('Ş','S'), ('ğ','g'), ('Ğ','G'), ('ü','u'), ('Ü','U'), ('ö','o'), ('Ö','O'), ('ç','c'), ('Ç','C'), ('ı','i'), ('İ','I')]:
            sahip_temiz = sahip_temiz.replace(k, v)
        
        eser_temiz = blok_data['isim']
        for k, v in [('ş','s'), ('Ş','S'), ('ğ','g'), ('Ğ','G'), ('ü','u'), ('Ü','U'), ('ö','o'), ('Ö','O'), ('ç','c'), ('Ç','C'), ('ı','i'), ('İ','I')]:
            eser_temiz = eser_temiz.replace(k, v)
        
        qr_veri = "NFT#" + str(blok_data['numara']) + "|" + blok_data['blok_hash'][:16] + "|Owner:" + sahip_temiz
        qr_kod_obj = qr.QRCode(version=1, box_size=5, border=2)
        qr_kod_obj.add_data(qr_veri)
        qr_kod_obj.make(fit=True)
        qr_resim = qr_kod_obj.make_image(fill_color="black", back_color="white")
        qr_resim = qr_resim.resize((150, 150))
        resim.paste(qr_resim, (genislik - 180, 30))
        
        y_konum = 60
        cizim.text((genislik//2 - 150, y_konum), "NFT SERTIFIKASI", fill=mavi_renk)
        y_konum = y_konum + 60
        cizim.text((50, y_konum), "Eser Adi: " + eser_temiz, fill='black')
        y_konum = y_konum + 40
        cizim.text((50, y_konum), "Sahip: " + sahip_temiz, fill='black')
        y_konum = y_konum + 40
        cizim.text((50, y_konum), "Token No: #" + str(blok_data['numara']), fill='black')
        y_konum = y_konum + 40
        cizim.text((50, y_konum), "Tarih: " + blok_data['zaman'][:19], fill='gray')
        
        return resim
    except Exception as e:
        print(f"Sertifika hatasi: {e}")
        genislik = 800
        yukseklik = 600
        resim = Image.new('RGB', (genislik, yukseklik), 'white')
        cizim = ImageDraw.Draw(resim)
        cizim.text((50, 50), f"NFT #{blok_data['numara']}", fill='black')
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
    
    yuklenen_dosya = st.file_uploader("Dosya Sec", type=['jpg', 'jpeg', 'png'], key="dosya_yukle")
    
    if yuklenen_dosya:
        yuklenen_dosya.seek(0)
        dosya_baytlari = yuklenen_dosya.read()
        dosya_hash = file_hash_calc(dosya_baytlari)
        
        st.write(f"**Dosya Hash:** `{dosya_hash}`")
        st.code(dosya_hash)
        
        kopya_var_mi = False
        kopya_bilgi = None
        
        for blok in veri['bloklar']:
            if blok['dosya_hash'] == dosya_hash:
                kopya_var_mi = True
                kopya_bilgi = blok
                break
        
        if kopya_var_mi:
            st.error("🚨 BU DOSYA ZATEN KAYITLI!")
            st.info("Sahip: " + kopya_bilgi['sahip'] + " | Eser: " + kopya_bilgi['isim'])
            
            st.markdown("---")
            st.warning("Bu dosyadan NFT zaten oluşturulmuş!")
            st.info(f"Mevcut NFT: #{kopya_bilgi['numara']} - {kopya_bilgi['isim']}")
        else:
            sol_kolon, sag_kolon = st.columns([2, 1])
            
            with sol_kolon:
                yuklenen_dosya.seek(0)
                st.image(yuklenen_dosya, width=400)
            
            with sag_kolon:
                st.success("✅ Yeni Dosya")
                st.code(dosya_hash[:20] + "...")
                
                if yuklenen_dosya.type.startswith('image'):
                    try:
                        yuklenen_dosya.seek(0)
                        resim = Image.open(yuklenen_dosya)
                        resim_hash = img_hash_calc(resim)
                        
                        if resim_hash is not None and len(veri['bloklar']) > 0:
                            benzer_idx, benzerlik_skoru = similarity_check(resim_hash)
                            
                            if benzerlik_skoru > 85:
                                st.warning("⚠️ BENZER RESIM BULUNDU!")
                                st.warning("Benzerlik: %" + str(round(benzerlik_skoru, 1)))
                                st.warning("Benzer NFT: #" + str(benzer_idx))
                            elif benzerlik_skoru > 65:
                                st.info("ℹ️ Benzerlik: %" + str(round(benzerlik_skoru, 1)))
                    except Exception as ai_err:
                        print(f"AI kontrol hatasi: {ai_err}")
            
            st.markdown("---")
            
            bilgi_kolon1, bilgi_kolon2 = st.columns(2)
            
            with bilgi_kolon1:
                nft_isim = st.text_input("NFT Ismi")
            with bilgi_kolon2:
                nft_fiyat = st.number_input("Fiyat (TL)", min_value=0, value=100)
            
            nft_aciklama = st.text_area("Aciklama", height=80)
            
            if st.button("🔗 NFT Olustur", use_container_width=True):
                if not nft_isim or nft_isim == "":
                    st.error("NFT ismi bos olamaz!")
                else:
                    onceki_blok_hash = ""
                    if len(veri['bloklar']) > 0:
                        son_blok = veri['bloklar'][-1]
                        onceki_blok_hash = son_blok['blok_hash']
                    
                    yeni_blok = {
                        'numara': len(veri['bloklar']),
                        'zaman': str(dt.datetime.now()),
                        'isim': nft_isim,
                        'sahip': st.session_state.kullanici_adi,
                        'dosya_hash': dosya_hash,
                        'onceki_hash': onceki_blok_hash,
                        'fiyat': nft_fiyat,
                        'aciklama': nft_aciklama,
                        'satista': False,
                    }
                    
                    if yuklenen_dosya.type.startswith('image'):
                        try:
                            yuklenen_dosya.seek(0)
                            resim = Image.open(yuklenen_dosya)
                            resim_hash_obj = img_hash_calc(resim)
                            yeni_blok['resim_hash'] = str(resim_hash_obj) if resim_hash_obj is not None else None
                        except Exception as img_err:
                            print(f"Resim hash hatasi: {img_err}")
                            yeni_blok['resim_hash'] = None
                    else:
                        yeni_blok['resim_hash'] = None
                    
                    yuklenen_dosya.seek(0)
                    yeni_blok['resim_veri'] = b64.b64encode(yuklenen_dosya.read()).decode()
                    
                    yeni_blok['blok_hash'] = block_hash_calc(yeni_blok)
                    
                    veri['bloklar'].append(yeni_blok)
                    
                    aktif_kullanici['nftler'].append(yeni_blok['numara'])
                    
                    yeni_islem = {
                        'tip': 'mint',
                        'nft_no': yeni_blok['numara'],
                        'gonderen': None,
                        'alan': st.session_state.kullanici_adi,
                        'fiyat': 0,
                        'zaman': str(dt.datetime.now())
                    }
                    veri['islemler'].append(yeni_islem)
                    
                    if not save_data(veri):
                        st.error("Kayit hatasi!")
                    else:
                        st.success("✅ NFT olusturuldu! Token #" + str(yeni_blok['numara']))
                        st.balloons()
                        
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
                    
                    st.rerun()

elif sayfa_secim == "NFT Koleksiyonum":
    st.title("🎨 NFT Koleksiyonum")
    st.markdown("---")
    
    if len(aktif_kullanici['nftler']) == 0:
        st.info("Henuz NFT'niz yok. Ana sayfadan eser yukleyin!")
    else:
        satirda_kac = 3
        toplam_nft_sayisi = len(aktif_kullanici['nftler'])
        
        for satir_no in range(0, toplam_nft_sayisi, satirda_kac):
            satirda_kolonlar = st.columns(satirda_kac)
            
            for kolon_no in range(satirda_kac):
                if satir_no + kolon_no < toplam_nft_sayisi:
                    nft_numarasi = aktif_kullanici['nftler'][satir_no + kolon_no]
                    nft_bilgi = veri['bloklar'][nft_numarasi]
                    
                    with satirda_kolonlar[kolon_no]:
                        st.markdown("<div style='background:white;padding:10px;border-radius:10px;'>", unsafe_allow_html=True)
                        
                        if 'resim_veri' in nft_bilgi:
                            resim_bytes = b64.b64decode(nft_bilgi['resim_veri'])
                            st.image(resim_bytes)
                        
                        st.markdown("**" + nft_bilgi['isim'] + "**")
                        st.caption("Token #" + str(nft_bilgi['numara']))
                        st.caption("💰 " + str(nft_bilgi['fiyat']) + " TL")
                        
                        buton_kolon1, buton_kolon2 = st.columns(2)
                        
                        with buton_kolon1:
                            if nft_bilgi['satista'] == False:
                                if st.button("Sat", key="sat_buton_" + str(nft_numarasi)):
                                    nft_bilgi['satista'] = True
                                    veri['pazar'].append(nft_numarasi)
                                    save_data(veri)
                                    st.success("Pazara eklendi!")
                                    st.rerun()
                        
                        with buton_kolon2:
                            if st.button("Transfer", key="transfer_buton_" + str(nft_numarasi)):
                                st.session_state['transfer_nft'] = nft_numarasi
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        
        if 'transfer_nft' in st.session_state:
            st.markdown("---")
            st.subheader("🔄 NFT Transfer")
            
            transfer_edilecek_nft = veri['bloklar'][st.session_state['transfer_nft']]
            st.write("**Eser:** " + transfer_edilecek_nft['isim'])
            
            alici_kullanici = st.text_input("Alici Kullanici Adi")
            
            if st.button("Transfer Et"):
                if not alici_kullanici or alici_kullanici == "":
                    st.error("Alici kullanici adi bos olamaz!")
                elif alici_kullanici not in veri['kullanicilar']:
                    st.error("Kullanici bulunamadi!")
                elif alici_kullanici == st.session_state.kullanici_adi:
                    st.error("Kendinize transfer yapamazsiniz!")
                else:
                    aktif_kullanici['nftler'].remove(st.session_state['transfer_nft'])
                    
                    veri['kullanicilar'][alici_kullanici]['nftler'].append(st.session_state['transfer_nft'])
                    
                    transfer_edilecek_nft['sahip'] = alici_kullanici
                    
                    transfer_islem = {
                        'tip': 'transfer',
                        'nft_no': st.session_state['transfer_nft'],
                        'gonderen': st.session_state.kullanici_adi,
                        'alan': alici_kullanici,
                        'fiyat': 0,
                        'zaman': str(dt.datetime.now())
                    }
                    veri['islemler'].append(transfer_islem)
                    
                    save_data(veri)
                    
                    st.success("Transfer tamamlandi!")
                    del st.session_state['transfer_nft']
                    st.rerun()

elif sayfa_secim == "NFT Pazari":
    st.title("🛒 NFT Pazari")
    st.markdown("---")
    
    if len(veri['pazar']) == 0:
        st.info("Pazarda satilik NFT yok.")
    else:
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
                            img_data = b64.b64decode(pazar_nft['resim_veri'])
                            st.image(img_data)
                        
                        st.markdown("**" + pazar_nft['isim'] + "**")
                        st.caption("Satici: " + pazar_nft['sahip'])
                        st.markdown("### 💰 " + str(pazar_nft['fiyat']) + " TL")
                        
                        if pazar_nft['sahip'] != st.session_state.kullanici_adi:
                            if st.button("Satin Al", key="al_" + str(pazar_nft_no)):
                                if aktif_kullanici['para'] >= pazar_nft['fiyat']:
                                    satici_adi = pazar_nft['sahip']
                                    
                                    aktif_kullanici['para'] = aktif_kullanici['para'] - pazar_nft['fiyat']
                                    
                                    satici_kazanc = pazar_nft['fiyat'] * 0.9
                                    veri['kullanicilar'][satici_adi]['para'] = veri['kullanicilar'][satici_adi]['para'] + satici_kazanc
                                    
                                    veri['kullanicilar'][satici_adi]['nftler'].remove(pazar_nft_no)
                                    aktif_kullanici['nftler'].append(pazar_nft_no)
                                    pazar_nft['sahip'] = st.session_state.kullanici_adi
                                    pazar_nft['satista'] = False
                                    veri['pazar'].remove(pazar_nft_no)
                                    
                                    satis_islem = {
                                        'tip': 'satis',
                                        'nft_no': pazar_nft_no,
                                        'gonderen': satici_adi,
                                        'alan': st.session_state.kullanici_adi,
                                        'fiyat': pazar_nft['fiyat'],
                                        'zaman': str(dt.datetime.now())
                                    }
                                    veri['islemler'].append(satis_islem)
                                    
                                    save_data(veri)
                                    
                                    st.success("Satin alma basarili!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("Bakiye yetersiz!")
                        else:
                            if st.button("Satisi Iptal Et", key="iptal_" + str(pazar_nft_no)):
                                pazar_nft['satista'] = False
                                veri['pazar'].remove(pazar_nft_no)
                                save_data(veri)
                                st.success("Iptal edildi!")
                                st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

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
        
        for blok in reversed(veri['bloklar']):
            with st.expander("Blok #" + str(blok['numara']) + " - " + blok['isim']):
                blok_kolon1, blok_kolon2 = st.columns([1, 2])
                
                with blok_kolon1:
                    if 'resim_veri' in blok:
                        blok_resim = b64.b64decode(blok['resim_veri'])
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

elif sayfa_secim == "📊 Blockchain Analizi":
    st.title("📊 Blockchain Analizi")
    st.markdown("---")
    
    st.subheader("🔗 Blockchain Görselleştirme")
    
    try:
        fig = blockchain_gorsel_olustur()
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img = Image.open(buf)
        st.image(img, use_container_width=True)
        
        buf.seek(0)
        st.download_button("📥 Blockchain Görseli İndir", buf, "blockchain.png", "image/png")
        
        plt.close(fig)
        
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
            timeline_buf = BytesIO()
            timeline_fig.savefig(timeline_buf, format='png', dpi=150, bbox_inches='tight')
            timeline_buf.seek(0)
            timeline_img = Image.open(timeline_buf)
            st.image(timeline_img, use_container_width=True)
            
            timeline_buf.seek(0)
            st.download_button("📥 Timeline İndir", timeline_buf, f"timeline_{nft_numarasi}.png", "image/png")
            
            plt.close(timeline_fig)
            
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
            if ekleme_miktari <= 0:
                st.error("Sifirdan buyuk olmali!")
            else:
                aktif_kullanici['para'] += ekleme_miktari
                if not save_data(veri):
                    st.error("Veri kaydedilemedi!")
                else:
                    st.success(f"{ekleme_miktari} TL eklendi!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Islem Gecmisi")
        
        kullanici_islemleri = []
        for islem in veri['islemler']:
            if islem.get('gonderen') == st.session_state.kullanici_adi or islem.get('alan') == st.session_state.kullanici_adi:
                kullanici_islemleri.append(islem)
        
        if len(kullanici_islemleri) == 0:
            st.info("Henuz islem yok.")
        else:
            son_islemler = kullanici_islemleri[-10:]
            son_islemler.reverse()
            
            for islem in son_islemler:
                islem_tipi = islem.get('tip', 'BILINMIYOR').upper()
                nft_no = islem.get('nft_no', 0)
                zaman = islem.get('zaman', 'BILINMIYOR')[:19]
                
                st.write(f"**{islem_tipi}** - NFT #{nft_no} - {zaman}")

st.markdown("---")
st.caption("ArtGuard AI | TÜBİTAK 4006 Projesi")
