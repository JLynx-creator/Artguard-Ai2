import streamlit as st
import hashlib
import json
import datetime
from PIL import Image, ImageDraw
import imagehash
import qrcode
from io import BytesIO

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")

# baslangic verileri - session state kullaniyoruz cunku sayfa yenilenince kaybolmasin
if 'basladi_mi' not in st.session_state:
    st.session_state.basladi_mi = True
    st.session_state.zincir = []  # blockchain listesi
    st.session_state.hashler = set()
    st.session_state.resim_hash = []
    st.session_state.ai_uyari = 0
    st.session_state.transfer = 0
    st.session_state.users = {'admin': 'admin123'}  # default hesap
    st.session_state.login = False
    st.session_state.current_user = None

# giris ekrani
if not st.session_state.login:
    st.markdown("<h1 style='text-align:center;'>🎨 ArtGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#7f8c8d;'>Blockchain + AI ile Dijital Sanat Koruması</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Giriş", "📝 Kayıt"])
    
    with tab1:
        st.subheader("Giriş Yap")
        user = st.text_input("Kullanıcı", key="l1")
        pw = st.text_input("Şifre", type="password", key="l2")
        
        if st.button("Giriş"):
            if user in st.session_state.users:
                if st.session_state.users[user] == pw:
                    st.session_state.login = True
                    st.session_state.current_user = user
                    st.success("Hoşgeldin " + user)
                    st.rerun()
                else:
                    st.error("yanlis sifre!")  # typo - kucuk harf
            else:
                st.error("kullanici yok")
    
    with tab2:
        st.subheader("Hesap Aç")
        new_user = st.text_input("Kullanıcı adı", key="r1")
        new_pw = st.text_input("Şifre gir", type="password", key="r2")
        new_pw2 = st.text_input("Tekrar yaz", type="password", key="r3")
        
        if st.button("Kayıt"):
            if new_user and new_pw:
                if new_pw == new_pw2:
                    if new_user not in st.session_state.users:
                        st.session_state.users[new_user] = new_pw
                        st.success("tamam oldu!")
                    else:
                        st.error("bu isim var")
                else:
                    st.error("sifreler ayni degil")
            else:
                st.error("bos birakma")
    
    st.stop()

# sidebar menu
with st.sidebar:
    st.markdown("## 👤 " + st.session_state.current_user)
    st.markdown("---")
    lang = st.selectbox("🌍 Dil", ["Türkçe", "English"])
    st.markdown("---")
    theme_choice = st.selectbox("🎨 Tema", ["Mor-Mavi", "Yeşil-Mavi", "Turuncu-Kırmızı", "Pembe-Mor", "Koyu Mod", "Altın-Sarı", "Gümüş-Şehir", "Deniz-Mavin", "Gün Batımı", "Orman-Yeşil", "Lacivert-Gümüş", "Mercan-Turkuaz", "Eflatun-Gri", "Ateş-Kırmızı", "Buz-Mavi"], index=6)
    st.markdown("---")
    
    if st.button("Çıkış"):
        st.session_state.login = False
        st.session_state.current_user = None
        st.rerun()

# tema renkleri
themes = {
    "Mor-Mavi": ['#667eea', '#764ba2'],
    "Turuncu-Kırmızı": ['#f46b45', '#eea849'],
    "Yeşil-Mavi": ['#11998e', '#38ef7d'],
    "Pembe-Mor": ['#ee0979', '#ff6a00'],
    "Koyu Mod": ['#2c3e50', '#34495e'],
    "Altın-Sarı": ['#f7971e', '#ffd200'],
    "Gümüş-Şehir": ['#bdc3c7', '#2c3e50'],
    "Deniz-Mavin": ['#2193b0', '#6dd5ed'],
    "Gün Batımı": ['#ff6b6b', '#feca57'],
    "Orman-Yeşil": ['#134e5e', '#71b280'],
    "Lacivert-Gümüş": ['#4b6cb7', '#182848'],
    "Mercan-Turkuaz": ['#ff6b9d', '#c44569'],
    "Eflatun-Gri": ['#8e44ad', '#95a5a6'],
    "Ateş-Kırmızı": ['#ff416c', '#ff4b2b'],
    "Buz-Mavi": ['#4facfe', '#00f2fe']
}

color = themes[theme_choice]
c1 = color[0]
c2 = color[1]

# CSS - biraz karisik yazdim
css_style = "<style>.stApp{background:linear-gradient(135deg," + c1 + "," + c2 + ");}"
css_style = css_style + ".main .block-container{background:white;border-radius:20px;padding:2rem;box-shadow:0 10px 40px rgba(0,0,0,0.3);max-width:1200px;margin:0 auto;}"
css_style = css_style + "h1{color:#2c3e50;text-align:center;}"
css_style = css_style + "h2{color:#34495e;border-bottom:2px solid " + c1 + ";padding-bottom:0.5rem;}"
css_style = css_style + ".stButton>button{background:linear-gradient(90deg," + c1 + "," + c2 + ");color:white;border-radius:20px;padding:0.6rem 2rem;border:none;}"
css_style = css_style + "</style>"
st.markdown(css_style, unsafe_allow_html=True)

# metinler sozluk
txt = {
    'Türkçe': {
        'baslik': "🎨 ArtGuard AI",
        'alt': "TÜBİTAK 4006",
        'stat': "📊 İstatistikler",
        'eser': "Eser", 'user': "Kullanıcı", 'ai': "AI", 'trans': "Transfer",
        'upload': "📤 Yükle", 'file': "Dosya",
        'hash': "Hash:", 'copy': "🚨 KOPYA!", 'copy_msg': "Kayıtlı!",
        'owner': "Sahip:", 'art': "Eser:",
        'new': "✅ Yeni", 'save_title': "🎨 Kaydet",
        'art_name': "Eser:", 'owner_name': "Sahip:",
        'copyright': "Telif:", 'copyright_default': "Tüm haklar saklı.",
        'save_btn': "KAYDET", 'ok': "✅ OK! #",
        'download': "İndir", 'fill': "Doldur!",
        'records': "📊 Kayıtlar", 'total': "Toplam:",
        'block': "#", 'date': "Tarih:", 'fee': "Telif:",
        'no_data': "Veri yok!",
        'transfer_title': "🔄 Transfer", 'which': "Blok:",
        'new_owner': "Yeni Sahip:", 'transfer_btn': "Transfer",
        'transfer_ok': "✅ OK! 10%:", 'enter': "Yaz!",
        'data': "💾 Veri", 'backup': "Yedekle",
        'json_down': "İndir", 'load': "Yükle",
        'loaded': "✅ OK!", 'error': "Hata!",
        'note': "Blockchain + AI sistemi"
    },
    'English': {
        'baslik': "🎨 ArtGuard AI",
        'alt': "TUBITAK 4006",
        'stat': "📊 Stats",
        'eser': "Arts", 'user': "User", 'ai': "AI", 'trans': "Transfers",
        'upload': "📤 Upload", 'file': "File",
        'hash': "Hash:", 'copy': "🚨 COPY!", 'copy_msg': "Registered!",
        'owner': "Owner:", 'art': "Art:",
        'new': "✅ New", 'save_title': "🎨 Save",
        'art_name': "Name:", 'owner_name': "Owner:",
        'copyright': "Copyright:", 'copyright_default': "All rights reserved.",
        'save_btn': "SAVE", 'ok': "✅ OK! #",
        'download': "Download", 'fill': "Fill!",
        'records': "📊 Records", 'total': "Total:",
        'block': "#", 'date': "Date:", 'fee': "Fee:",
        'no_data': "No data!",
        'transfer_title': "🔄 Transfer", 'which': "Block:",
        'new_owner': "New Owner:", 'transfer_btn': "Transfer",
        'transfer_ok': "✅ OK! 10%:", 'enter': "Write!",
        'data': "💾 Data", 'backup': "Backup",
        'json_down': "Download", 'load': "Load",
        'loaded': "✅ OK!", 'error': "Error!",
        'note': "Blockchain + AI system"
    }
}

t = txt[lang]

st.title(t['baslik'])
st.caption(t['alt'])
st.markdown("---")

# istatistikler
st.subheader(t['stat'])
c1, c2, c3, c4 = st.columns(4)

c1.metric(t['eser'], len(st.session_state.zincir))
c2.metric(t['user'], "1")
c3.metric(t['ai'], st.session_state.ai_uyari)
c4.metric(t['trans'], st.session_state.transfer)

st.markdown("---")

# hash hesapla fonksiyonu
def calculate_hash(file_data):
    h = hashlib.sha256(file_data)
    return h.hexdigest()

# resim hash
def img_hash(img):
    try:
        h = imagehash.average_hash(img)
        return h
    except:
        return None

# benzerlik bul
def check_similar(new_h):
    if new_h == None:
        return None, 0
    max_sim = 0
    idx = -1
    for i in range(len(st.session_state.resim_hash)):
        old_h = st.session_state.resim_hash[i]
        if old_h == None:
            continue
        diff = new_h - old_h
        similarity = 100 * (1 - diff / 64.0)
        if similarity > max_sim:
            max_sim = similarity
            idx = i
    return idx, max_sim

# sertifika yap
def make_cert(block_data, language):
    width = 800
    height = 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    blue = (41, 128, 185)
    
    # cerceve ciz
    draw.rectangle([10, 10, width-10, height-10], outline=blue, width=5)
    draw.rectangle([20, 20, width-20, height-20], outline=blue, width=2)
    
    # turkce karakter temizle
    owner_clean = block_data['owner']
    owner_clean = owner_clean.replace('ş','s').replace('Ş','S')
    owner_clean = owner_clean.replace('ğ','g').replace('Ğ','G')
    owner_clean = owner_clean.replace('ü','u').replace('Ü','U')
    owner_clean = owner_clean.replace('ö','o').replace('Ö','O')
    owner_clean = owner_clean.replace('ç','c').replace('Ç','C')
    owner_clean = owner_clean.replace('ı','i').replace('İ','I')
    
    qr_data = "Block:" + str(block_data['index']) + "|Hash:" + block_data['file_hash'][:16] + "|Owner:" + owner_clean
    
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((150, 150))
    image.paste(qr_image, (width - 180, 30))
    
    y_pos = 60
    if language == 'English':
        title = "BLOCKCHAIN CERTIFICATE"
    else:
        title = "BLOCKCHAIN SERTIFIKASI"
    
    draw.text((width//2 - 150, y_pos), title, fill=blue)
    y_pos = y_pos + 60
    draw.text((50, y_pos), "Eser: " + block_data['art_name'], fill='black')
    y_pos = y_pos + 40
    draw.text((50, y_pos), "Sahip: " + block_data['owner'], fill='black')
    y_pos = y_pos + 40
    draw.text((50, y_pos), "Blok #" + str(block_data['index']), fill='black')
    y_pos = y_pos + 40
    draw.text((50, y_pos), block_data['timestamp'][:19], fill='gray')
    y_pos = y_pos + 40
    draw.text((50, y_pos), "Hash: " + block_data['file_hash'][:32] + "...", fill='gray')
    y_pos = y_pos + 40
    copyright_text = block_data['copyright_statement']
    if len(copyright_text) > 60:
        copyright_text = copyright_text[:60]
    draw.text((50, y_pos), copyright_text, fill='darkred')
    
    draw.text((width//2 - 100, height - 50), "ArtGuard AI", fill='gray')
    
    return image

st.subheader(t['upload'])
uploaded = st.file_uploader(t['file'], type=['jpg', 'jpeg', 'png', 'pdf', 'mp3', 'wav', 'txt'])

if uploaded:
    file_bytes = uploaded.read()
    file_hash = calculate_hash(file_bytes)
    
    st.info("**" + t['hash'] + "** `" + file_hash[:16] + "...`")
    
    # kopya kontrol
    if file_hash in st.session_state.hashler:
        st.error(t['copy'])
        st.warning(t['copy_msg'])
        for item in st.session_state.zincir:
            if item['file_hash'] == file_hash:
                st.info("**" + t['owner'] + "** " + item['owner'] + " | **" + t['art'] + "** " + item['art_name'])
    else:
        st.success(t['new'])
        
        img_hash_value = None
        
        # eger resimse AI kontrol
        if uploaded.type.startswith('image'):
            try:
                img_file = Image.open(uploaded)
                img_hash_value = img_hash(img_file)
                
                if len(st.session_state.resim_hash) > 0:
                    similar_idx, score = check_similar(img_hash_value)
                    
                    if score > 90:  # cok yuksek benzerlik
                        st.session_state.ai_uyari = st.session_state.ai_uyari + 1
                        st.error("🚨 ÇOK BENZER!")
                        st.progress(int(score)/100)
                        st.error("Benzerlik: " + str(round(score, 1)) + "%")
                        st.warning("Blok #" + str(similar_idx) + " ile aynı")
                    elif score > 80:
                        st.session_state.ai_uyari = st.session_state.ai_uyari + 1
                        st.warning("⚠️ YÜKSEK BENZER!")
                        st.progress(int(score)/100)
                        st.warning("Benzerlik: " + str(round(score, 1)) + "%")
                    elif score > 65:
                        st.info("ℹ️ Benzerlik: " + str(round(score, 1)) + "%")
                        st.progress(int(score)/100)
            except Exception as e:
                pass  # hata olursa gec
        
        st.markdown("---")
        st.subheader(t['save_title'])
        
        col_1, col_2 = st.columns(2)
        with col_1:
            art_name = st.text_input(t['art_name'])
        with col_2:
            owner_name = st.text_input(t['owner_name'], value=st.session_state.current_user)
        
        copyright_text = st.text_area(t['copyright'], t['copyright_default'], height=60)
        
        if st.button(t['save_btn']):
            if art_name and owner_name:
                # yeni blok olustur
                new_block = {}
                new_block['index'] = len(st.session_state.zincir)
                new_block['timestamp'] = str(datetime.datetime.now())
                new_block['art_name'] = art_name
                new_block['owner'] = owner_name
                new_block['file_hash'] = file_hash
                new_block['royalty'] = 0.1
                new_block['copyright_statement'] = copyright_text
                
                st.session_state.zincir.append(new_block)
                st.session_state.hashler.add(file_hash)
                st.session_state.resim_hash.append(img_hash_value)
                
                st.success(t['ok'] + str(new_block['index']))
                st.balloons()
                
                # sertifika olustur
                cert_img = make_cert(new_block, lang)
                buf = BytesIO()
                cert_img.save(buf, format='PNG')
                buf.seek(0)
                
                st.download_button(t['download'], buf, "cert_" + str(new_block['index']) + ".png", "image/png")
                st.image(cert_img)
            else:
                st.error(t['fill'])

st.markdown("---")
st.header(t['records'])

if len(st.session_state.zincir) > 0:
    st.write("**" + t['total'] + "** " + str(len(st.session_state.zincir)))
    
    for item in st.session_state.zincir:
        with st.expander(t['block'] + str(item['index']) + " - " + item['art_name']):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Sahip:** " + item['owner'])
                st.write("**" + t['date'] + "** " + item['timestamp'][:19])
            with col_b:
                st.write("**Hash:** `" + item['file_hash'][:16] + "...`")
                st.write("**" + t['fee'] + "** " + str(item['royalty']*100) + "%")
else:
    st.info(t['no_data'])

st.markdown("---")
st.header(t['transfer_title'])

if len(st.session_state.zincir) > 0:
    col_x, col_y, col_z = st.columns([2, 2, 1])
    with col_x:
        selected_block = st.number_input(t['which'], 0, len(st.session_state.zincir)-1, 0)
    with col_y:
        new_owner = st.text_input(t['new_owner'])
    with col_z:
        st.write("")
        st.write("")
        if st.button(t['transfer_btn']):
            if new_owner:
                old_owner = st.session_state.zincir[selected_block]['owner']
                st.session_state.zincir[selected_block]['owner'] = new_owner
                st.session_state.transfer = st.session_state.transfer + 1
                st.success(t['transfer_ok'] + " " + old_owner)
            else:
                st.error(t['enter'])

st.markdown("---")
st.header(t['data'])

col_left, col_right = st.columns(2)

with col_left:
    if st.button(t['backup']):
        data = {}
        data['blockchain'] = st.session_state.zincir
        data['used_hashes'] = list(st.session_state.hashler)
        hash_list = []
        for h in st.session_state.resim_hash:
            if h:
                hash_list.append(str(h))
            else:
                hash_list.append(None)
        data['phash_list'] = hash_list
        data['ai_warnings_count'] = st.session_state.ai_uyari
        data['transfers_count'] = st.session_state.transfer
        
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(t['json_down'], json_data, "backup.json", "application/json")

with col_right:
    json_file = st.file_uploader(t['load'], type=['json'])
    if json_file:
        try:
            data = json.load(json_file)
            st.session_state.zincir = data['blockchain']
            st.session_state.hashler = set(data['used_hashes'])
            
            hash_list = []
            for h in data['phash_list']:
                if h:
                    hash_list.append(imagehash.hex_to_hash(h))
                else:
                    hash_list.append(None)
            st.session_state.resim_hash = hash_list
            
            st.session_state.ai_uyari = data.get('ai_warnings_count', 0)
            st.session_state.transfer = data.get('transfers_count', 0)
            st.success(t['loaded'])
            st.rerun()
        except Exception as e:
            st.error(t['error'])

st.markdown("---")
st.info(t['note'])
