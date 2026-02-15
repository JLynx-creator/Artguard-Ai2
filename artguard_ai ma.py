import streamlit as st
import hashlib
import json
import datetime
from PIL import Image, ImageDraw
import imagehash
import qrcode
from io import BytesIO

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")

# Kalici depolama
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.zincir = []
    st.session_state.hashler = set()
    st.session_state.resim_hashler = []
    st.session_state.ai_sayac = 0
    st.session_state.transfer_sayac = 0
    st.session_state.kullanicilar = {'admin': 'admin123'}
    st.session_state.giris_yapildi = False
    st.session_state.aktif_kullanici = None

# Giris kontrol
if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align:center;'>🎨 ArtGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#7f8c8d;'>Blockchain + AI ile Dijital Sanat Koruması</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Giriş Yap", "📝 Kayıt Ol"])
    
    with tab1:
        st.subheader("Giriş Yap")
        kullanici_adi = st.text_input("Kullanıcı Adı", key="login_user")
        sifre = st.text_input("Şifre", type="password", key="login_pass")
        
        if st.button("Giriş", use_container_width=True):
            if kullanici_adi in st.session_state.kullanicilar:
                if st.session_state.kullanicilar[kullanici_adi] == sifre:
                    st.session_state.giris_yapildi = True
                    st.session_state.aktif_kullanici = kullanici_adi
                    st.success(f"Hoş geldin {kullanici_adi}!")
                    st.rerun()
                else:
                    st.error("Şifre yanlış!")
            else:
                st.error("Kullanıcı bulunamadı!")
    
    with tab2:
        st.subheader("Yeni Hesap Oluştur")
        yeni_kullanici = st.text_input("Yeni Kullanıcı Adı", key="reg_user")
        yeni_sifre = st.text_input("Yeni Şifre", type="password", key="reg_pass")
        yeni_sifre2 = st.text_input("Şifre Tekrar", type="password", key="reg_pass2")
        
        if st.button("Kayıt Ol", use_container_width=True):
            if yeni_kullanici and yeni_sifre:
                if yeni_sifre == yeni_sifre2:
                    if yeni_kullanici not in st.session_state.kullanicilar:
                        st.session_state.kullanicilar[yeni_kullanici] = yeni_sifre
                        st.success("Hesap oluşturuldu! Giriş yapabilirsin.")
                    else:
                        st.error("Bu kullanıcı adı alınmış!")
                else:
                    st.error("Şifreler uyuşmuyor!")
            else:
                st.error("Tüm alanları doldur!")
    
    st.stop()

# Ana uygulama
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.aktif_kullanici}")
    st.markdown("---")
    secilen_dil = st.selectbox("🌍 Dil", ["Türkçe", "English"])
    st.markdown("---")
    tema = st.selectbox("🎨 Tema", ["Mor-Mavi", "Yeşil-Mavi", "Turuncu-Kırmızı", "Pembe-Mor", "Koyu Mod"])
    st.markdown("---")
    
    if st.button("🚪 Çıkış Yap", use_container_width=True):
        st.session_state.giris_yapildi = False
        st.session_state.aktif_kullanici = None
        st.rerun()

temalar = {
    "Mor-Mavi": {'g1': '#667eea', 'g2': '#764ba2'},
    "Turuncu-Kırmızı": {'g1': '#f46b45', 'g2': '#eea849'},
    "Yeşil-Mavi": {'g1': '#11998e', 'g2': '#38ef7d'},
    "Pembe-Mor": {'g1': '#ee0979', 'g2': '#ff6a00'},
    "Koyu Mod": {'g1': '#2c3e50', 'g2': '#34495e'}
}

t_renk = temalar[tema]

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, {t_renk['g1']} 0%, {t_renk['g2']} 100%);
    }}
    .main .block-container {{
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        max-width: 1200px;
        margin: 0 auto;
    }}
    h1 {{
        color: #2c3e50;
        text-align: center;
    }}
    h2 {{
        color: #34495e;
        border-bottom: 2px solid {t_renk['g1']};
        padding-bottom: 0.5rem;
    }}
    .stButton > button {{
        background: linear-gradient(90deg, {t_renk['g1']}, {t_renk['g2']});
        color: white;
        border-radius: 20px;
        padding: 0.6rem 2rem;
        border: none;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        font-weight: bold;
    }}
    .stProgress > div > div {{
        background-color: {t_renk['g1']};
    }}
</style>
""", unsafe_allow_html=True)

sozluk = {
    'Türkçe': {
        'baslik': "🎨 ArtGuard AI",
        'altbaslik': "Dijital Sanat Koruma Sistemi | TÜBİTAK 4006",
        'istatistik': "📊 Sistem İstatistikleri",
        'eser': "Kayıtlı Eser", 'kullanici': "Kullanıcı", 'ai': "AI Tespit", 'transfer': "Transfer",
        'yukle': "📤 Eser Yükle", 'dosya': "Dosya seç",
        'hash': "Dosya Kimliği:", 'kopya': "🚨 KOPYA!", 'kopya_msg': "Bu eser kayıtlı!",
        'sahip': "Sahibi:", 'eser_adi': "Eser:",
        'yeni': "✅ Yeni Eser", 'kayit': "🎨 Blockchain'e Kaydet",
        'eser_input': "Eser Adı:", 'sahip_input': "Sahibi:",
        'telif': "Telif:", 'telif_default': "Tüm haklar saklıdır.",
        'kaydet': "KAYDET", 'tamam': "✅ Kaydedildi! Blok #",
        'indir': "📥 Sertifika İndir", 'doldur': "Tüm alanları doldur!",
        'kayitlar': "📊 Kayıtlar", 'toplam': "Toplam:",
        'blok': "Blok #", 'tarih': "Tarih:", 'yuzde': "Telif:",
        'telif_hakki': "Telif Hakkı:", 'yok': "Henüz kayıt yok!",
        'transfer_baslik': "🔄 Transfer", 'hangi': "Blok No:",
        'yeni_sahip': "Yeni Sahip:", 'transfer_btn': "Transfer",
        'transfer_ok': "✅ Tamam! %10 telif:", 'yaz': "Sahip adı yaz!",
        'kaydet_yukle': "💾 Veri Yönetimi", 'json_kaydet': "Yedekle",
        'json_indir': "İndir", 'json_yukle': "Geri Yükle",
        'yuklendi': "✅ Yüklendi!", 'hata': "Hata!",
        'not': "Blockchain ile sahiplik kanıtlı, AI ile benzerlik tespit edilir."
    },
    'English': {
        'baslik': "🎨 ArtGuard AI",
        'altbaslik': "Digital Art Protection | TÜBİTAK 4006",
        'istatistik': "📊 Statistics",
        'eser': "Registered", 'kullanici': "User", 'ai': "AI Alerts", 'transfer': "Transfers",
        'yukle': "📤 Upload", 'dosya': "Choose file",
        'hash': "File ID:", 'kopya': "🚨 COPY!", 'kopya_msg': "Registered!",
        'sahip': "Owner:", 'eser_adi': "Art:",
        'yeni': "✅ New", 'kayit': "🎨 Save",
        'eser_input': "Art Name:", 'sahip_input': "Owner:",
        'telif': "Copyright:", 'telif_default': "All rights reserved.",
        'kaydet': "SAVE", 'tamam': "✅ Saved! Block #",
        'indir': "📥 Download", 'doldur': "Fill all!",
        'kayitlar': "📊 Records", 'toplam': "Total:",
        'blok': "Block #", 'tarih': "Date:", 'yuzde': "Royalty:",
        'telif_hakki': "Copyright:", 'yok': "No records!",
        'transfer_baslik': "🔄 Transfer", 'hangi': "Block No:",
        'yeni_sahip': "New Owner:", 'transfer_btn': "Transfer",
        'transfer_ok': "✅ Done! 10%:", 'yaz': "Enter owner!",
        'kaydet_yukle': "💾 Data", 'json_kaydet': "Backup",
        'json_indir': "Download", 'json_yukle': "Restore",
        'yuklendi': "✅ Loaded!", 'hata': "Error!",
        'not': "Proves ownership with blockchain, detects similarity with AI."
    }
}

t = sozluk[secilen_dil]

st.title(t['baslik'])
st.caption(t['altbaslik'])
st.markdown("---")

st.subheader(t['istatistik'])
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(t['eser'], len(st.session_state.zincir))
with k2:
    st.metric(t['kullanici'], "1")
with k3:
    st.metric(t['ai'], st.session_state.ai_sayac)
with k4:
    st.metric(t['transfer'], st.session_state.transfer_sayac)

st.markdown("---")

def hash_hesapla(dosya_bytes):
    return hashlib.sha256(dosya_bytes).hexdigest()

def resim_hash_hesapla(resim):
    try:
        return imagehash.average_hash(resim)
    except:
        return None

def benzerlik_kontrol(yeni_hash):
    if yeni_hash is None:
        return None, 0
    en_yuksek = 0
    index = -1
    for i, eski_hash in enumerate(st.session_state.resim_hashler):
        if eski_hash is None:
            continue
        fark = yeni_hash - eski_hash
        benzerlik = 100 * (1 - fark / 64.0)
        if benzerlik > en_yuksek:
            en_yuksek = benzerlik
            index = i
    return index, en_yuksek

def sertifika_yap(blok, dil):
    w, h = 800, 600
    img = Image.new('RGB', (w, h), 'white')
    d = ImageDraw.Draw(img)
    c = (41, 128, 185)
    d.rectangle([10, 10, w-10, h-10], outline=c, width=5)
    d.rectangle([20, 20, w-20, h-20], outline=c, width=2)
    
    sahip_temiz = blok['owner'].replace('ş','s').replace('Ş','S').replace('ğ','g').replace('Ğ','G').replace('ü','u').replace('Ü','U').replace('ö','o').replace('Ö','O').replace('ç','c').replace('Ç','C').replace('ı','i').replace('İ','I')
    qr_veri = f"Block:{blok['index']}|Hash:{blok['file_hash'][:16]}|Owner:{sahip_temiz}"
    
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(qr_veri)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").resize((150, 150))
    img.paste(qr_img, (w - 180, 30))
    
    y = 60
    baslik = "BLOCKCHAIN CERTIFICATE" if dil == 'English' else "BLOCKCHAIN SERTIFIKASI"
    d.text((w//2 - 150, y), baslik, fill=c)
    y += 60
    d.text((50, y), f"Eser: {blok['art_name']}", fill='black')
    y += 40
    d.text((50, y), f"Sahip: {blok['owner']}", fill='black')
    y += 40
    d.text((50, y), f"Blok #{blok['index']}", fill='black')
    y += 40
    d.text((50, y), f"{blok['timestamp'][:19]}", fill='gray')
    y += 40
    d.text((50, y), f"Hash: {blok['file_hash'][:32]}...", fill='gray')
    y += 40
    d.text((50, y), blok['copyright_statement'][:60], fill='darkred')
    d.text((w//2 - 100, h - 50), "ArtGuard AI", fill='gray')
    return img

st.subheader(t['yukle'])
yuklenen = st.file_uploader(t['dosya'], type=['jpg', 'jpeg', 'png', 'pdf', 'mp3', 'wav', 'txt'])

if yuklenen:
    dosya_bytes = yuklenen.read()
    dosya_hash = hash_hesapla(dosya_bytes)
    
    st.info(f"**{t['hash']}** `{dosya_hash[:16]}...`")
    
    if dosya_hash in st.session_state.hashler:
        st.error(t['kopya'])
        st.warning(t['kopya_msg'])
        for item in st.session_state.zincir:
            if item['file_hash'] == dosya_hash:
                st.info(f"**{t['sahip']}** {item['owner']} | **{t['eser_adi']}** {item['art_name']}")
    else:
        st.success(t['yeni'])
        
        resim_hash_degeri = None
        
        if yuklenen.type.startswith('image'):
            try:
                resim_dosyasi = Image.open(yuklenen)
                resim_hash_degeri = resim_hash_hesapla(resim_dosyasi)
                
                if len(st.session_state.resim_hashler) > 0:
                    benzer_index, skor = benzerlik_kontrol(resim_hash_degeri)
                    
                    if skor > 90:
                        st.session_state.ai_sayac += 1
                        st.error(f"🚨 ÇOK YÜKSEK BENZERLİK!")
                        st.progress(int(skor)/100)
                        st.error(f"Benzerlik: {skor:.1f}%")
                        st.warning(f"Blok #{benzer_index} ile eşleşiyor")
                    elif skor > 80:
                        st.session_state.ai_sayac += 1
                        st.warning(f"⚠️ YÜKSEK BENZERLİK!")
                        st.progress(int(skor)/100)
                        st.warning(f"Benzerlik: {skor:.1f}%")
                    elif skor > 65:
                        st.info(f"ℹ️ Orta benzerlik: {skor:.1f}%")
                        st.progress(int(skor)/100)
            except:
                pass
        
        st.markdown("---")
        st.subheader(t['kayit'])
        
        col1, col2 = st.columns(2)
        with col1:
            eser_adi = st.text_input(t['eser_input'])
        with col2:
            sahip_adi = st.text_input(t['sahip_input'], value=st.session_state.aktif_kullanici)
        
        telif_yazisi = st.text_area(t['telif'], t['telif_default'], height=60)
        
        if st.button(t['kaydet'], use_container_width=True):
            if eser_adi and sahip_adi:
                yeni_blok = {
                    'index': len(st.session_state.zincir),
                    'timestamp': str(datetime.datetime.now()),
                    'art_name': eser_adi,
                    'owner': sahip_adi,
                    'file_hash': dosya_hash,
                    'royalty': 0.1,
                    'copyright_statement': telif_yazisi
                }
                
                st.session_state.zincir.append(yeni_blok)
                st.session_state.hashler.add(dosya_hash)
                st.session_state.resim_hashler.append(resim_hash_degeri)
                
                st.success(f"{t['tamam']}{yeni_blok['index']}")
                st.balloons()
                
                sertifika_resmi = sertifika_yap(yeni_blok, secilen_dil)
                buffer = BytesIO()
                sertifika_resmi.save(buffer, format='PNG')
                buffer.seek(0)
                
                st.download_button(t['indir'], buffer, f"cert_{yeni_blok['index']}.png", "image/png", use_container_width=True)
                st.image(sertifika_resmi, use_container_width=True)
            else:
                st.error(t['doldur'])

st.markdown("---")
st.header(t['kayitlar'])

if len(st.session_state.zincir) > 0:
    st.write(f"**{t['toplam']}** {len(st.session_state.zincir)}")
    
    for item in st.session_state.zincir:
        with st.expander(f"{t['blok']}{item['index']} - {item['art_name']}"):
            col_x, col_y = st.columns(2)
            with col_x:
                st.write(f"**Sahip:** {item['owner']}")
                st.write(f"**{t['tarih']}** {item['timestamp'][:19]}")
            with col_y:
                st.write(f"**Hash:** `{item['file_hash'][:16]}...`")
                st.write(f"**{t['yuzde']}** {item['royalty']*100}%")
else:
    st.info(t['yok'])

st.markdown("---")
st.header(t['transfer_baslik'])

if len(st.session_state.zincir) > 0:
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        secilen_blok = st.number_input(t['hangi'], 0, len(st.session_state.zincir)-1, 0)
    with col2:
        yeni_sahip = st.text_input(t['yeni_sahip'])
    with col3:
        st.write("")
        st.write("")
        if st.button(t['transfer_btn'], use_container_width=True):
            if yeni_sahip:
                eski = st.session_state.zincir[secilen_blok]['owner']
                st.session_state.zincir[secilen_blok]['owner'] = yeni_sahip
                st.session_state.transfer_sayac += 1
                st.success(f"{t['transfer_ok']} {eski}")
            else:
                st.error(t['yaz'])

st.markdown("---")
st.header(t['kaydet_yukle'])

col1, col2 = st.columns(2)

with col1:
    if st.button(t['json_kaydet'], use_container_width=True):
        veri = {
            'blockchain': st.session_state.zincir,
            'used_hashes': list(st.session_state.hashler),
            'phash_list': [str(h) if h else None for h in st.session_state.resim_hashler],
            'ai_warnings_count': st.session_state.ai_sayac,
            'transfers_count': st.session_state.transfer_sayac
        }
        json_veri = json.dumps(veri, indent=2, ensure_ascii=False)
        st.download_button(t['json_indir'], json_veri, "backup.json", "application/json", use_container_width=True)

with col2:
    json_dosyasi = st.file_uploader(t['json_yukle'], type=['json'])
    if json_dosyasi:
        try:
            veri = json.load(json_dosyasi)
            st.session_state.zincir = veri['blockchain']
            st.session_state.hashler = set(veri['used_hashes'])
            st.session_state.resim_hashler = [imagehash.hex_to_hash(h) if h else None for h in veri['phash_list']]
            st.session_state.ai_sayac = veri.get('ai_warnings_count', 0)
            st.session_state.transfer_sayac = veri.get('transfers_count', 0)
            st.success(t['yuklendi'])
            st.rerun()
        except:
            st.error(t['hata'])

st.markdown("---")
st.info(t['not'])
