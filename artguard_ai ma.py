import streamlit as st
import hashlib, json, datetime, os, time, random, string, base64
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import imagehash, qrcode
import matplotlib.pyplot as plt, matplotlib.patches as mp
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")
VF = 'veri.json'
TUZ = "nft2024xyz"

D = {
"tr": {
    "baslik":"🎨 ArtGuard AI","altyazi":"TÜBİTAK 4006 — Dijital Sanat Koruma",
    "giris":"Giriş Yap","hesap_ac":"Hesap Oluştur","cikis":"🚪 Çıkış",
    "tema":"🎨 Tema","dil":"🌐 Dil",
    "ana":"🏠 Ana Sayfa","kol":"🖼️ Koleksiyonum","pazar_s":"🛒 Pazar",
    "zincir":"⛓️ Blockchain","analiz":"📊 Analiz",
    "dogrula_s":"🔍 Doğrula","profil":"👤 Profil",
    "toplam_nft":"Toplam NFT","benim_nft":"Benim NFT","pazarda":"Pazarda",
    "toplam_blok":"Toplam Blok","zincir_gecerli":"Zincir Geçerli",
    "nasil":"Nasıl Çalışır?","blok_tek":"Blockchain","nft_surec":"NFT Süreci","telif":"Telif",
    "yukle":"📤 Yeni Eser Yükle","yukle_ipucu":"Resim yükle — AI benzerlik taraması çalışır.",
    "dosya_sec":"JPG / PNG seç",
    "nft_adi":"🎨 NFT Adı","fiyat":"💰 Fiyat (TL)","aciklama":"📝 Açıklama",
    "olustur_btn":"⛓️ NFT Oluştur","isim_bos":"İsim boş olamaz!","kayit_hata":"Kayıt hatası!",
    "ai_baslik":"ArtGuard AI","ai_alt":"Özgünlük Analizi","gorsel_bilgi":"📐 GÖRSEL BİLGİSİ",
    "oz_skor":"Özgünlük Skoru",
    "engel":"YÜKLEME ENGELLENDİ","uyari_benzer":"DİKKAT — Benzer İçerik",
    "ozgun":"ÖZGÜN ESER","ilk":"İLK ESER","ilk_acik":"Blockchain henüz boş!",
    "benzerlik_ile":"ile benzerlik","tarand":"NFT tarandı","esleme_yok":"Eşleşme yok",
    "nft_ok":"NFT Oluşturuldu!","eklendi":"blockchain'e eklendi","sertifika":"📥 Sertifika İndir",
    "zaten":"🚨 Bu dosya zaten kayıtlı!",
    "kol_bos":"Henüz NFT'n yok","kol_bos2":"Ana sayfadan ilk eserini ekle!",
    "sat":"💰 Sat","iptal_btn":"❌ İptal","transfer":"🔄 Transfer",
    "satista":"🟢 Satışta","koleksiyonda":"🔒 Koleksiyonda",
    "tr_baslik":"🔄 Transfer","alici":"Alıcı kullanıcı adı",
    "tr_et":"✅ Transfer Et","vazgec":"❌ Vazgeç",
    "bos":"Boş bırakma!","bulunamadi":"Kullanıcı bulunamadı!","kendin":"Kendinize transfer edilemez!",
    "tr_ok":"Transfer tamam!",
    "pazar_bos":"Pazar boş","pazar_bos2":"Koleksiyonundan NFT satışa çıkar!",
    "senin":"📌 Senin ilanın","bakiye_yok":"⚠️ Bakiye yetersiz",
    "satin_al":"🛒 Satın Al","satin_ok":"✅ Satın alındı!","bak_yok":"Bakiye yetersiz!",
    "blok_yok":"Henüz blok yok.","blok_gezgini":"Blockchain Gezgini",
    "blok_ara":"Blok Ara (Index)","tam_zincir":"Zincir Tablosu",
    "zincir_ok":"✅ Zincir Sağlam!","hash_dogrula":"🔍 Hash Bütünlüğü Doğrula",
    "nonce_grafik":"🔢 Bloklara Göre Nonce","nft_ist":"NFT İstatistikleri",
    "bakiye":"💰 Bakiye","bakiye_ekle":"💳 Ekle","son_isl":"📋 Son İşlemler","isl_yok":"Henüz işlem yok.",
    "uye":"Üye","kul_adi":"Kullanıcı Adı","sifre":"Şifre","sifre2":"Şifre Tekrar",
    "kisa":"Şifre çok kısa!","uyusmuyor":"Şifreler uyuşmuyor!","alindi":"Bu ad alınmış!",
    "hesap_ok":"Hesap oluşturuldu!","yanlis":"Kullanıcı adı veya şifre yanlış!",
    "blok_nasil":"🔗 Blockchain Nasıl Çalışır?",
    "blok_acik":"Her NFT bir blok oluşturur. Blok; sahip, hash ve önceki imzayı içerir. Zincir değiştirilemez.",
    "dog_baslik":"🔍 Dosya Doğrulama","dog_yukle":"Doğrulamak için dosya yükle (JPG/PNG/PDF)",
    "dosya_bilgi":"Dosya Bilgileri","dog_sonuc":"Blockchain Doğrulama",
    "dog_bulundu":"✅ Dosya blockchain'de bulundu! {count} blokta kayıtlı.",
    "dog_yok":"⚠️ Blockchain'de kayıt bulunamadı.",
    "alg_hash":"Algısal Hash","boyutlar":"Boyutlar","dosya_boyut":"Dosya Boyutu",
    "benzer_nftler":"Benzer NFT'ler","gorsel_analiz":"Görsel Analiz","benzerlik_skoru":"Benzerlik Skoru",
},
"en": {
    "baslik":"🎨 ArtGuard AI","altyazi":"TÜBİTAK 4006 — Digital Art Protection",
    "giris":"Log In","hesap_ac":"Create Account","cikis":"🚪 Logout",
    "tema":"🎨 Theme","dil":"🌐 Language",
    "ana":"🏠 Home","kol":"🖼️ My Collection","pazar_s":"🛒 Marketplace",
    "zincir":"⛓️ Blockchain","analiz":"📊 Analytics",
    "dogrula_s":"🔍 Verify","profil":"👤 Profile",
    "toplam_nft":"Total NFT","benim_nft":"My NFTs","pazarda":"On Market",
    "toplam_blok":"Total Blocks","zincir_gecerli":"Chain Valid",
    "nasil":"How It Works?","blok_tek":"Blockchain","nft_surec":"NFT Process","telif":"Copyright",
    "yukle":"📤 Upload Artwork","yukle_ipucu":"Upload image — AI similarity scan runs automatically.",
    "dosya_sec":"Select JPG / PNG",
    "nft_adi":"🎨 NFT Name","fiyat":"💰 Price (TL)","aciklama":"📝 Description",
    "olustur_btn":"⛓️ Create NFT","isim_bos":"Name cannot be empty!","kayit_hata":"Save error!",
    "ai_baslik":"ArtGuard AI","ai_alt":"Originality Analysis","gorsel_bilgi":"📐 IMAGE INFO",
    "oz_skor":"Originality Score",
    "engel":"UPLOAD BLOCKED","uyari_benzer":"WARNING — Similar Content",
    "ozgun":"ORIGINAL ARTWORK","ilk":"FIRST ARTWORK","ilk_acik":"Blockchain is empty!",
    "benzerlik_ile":"similarity with","tarand":"NFTs scanned","esleme_yok":"No match found",
    "nft_ok":"NFT Created!","eklendi":"added to blockchain","sertifika":"📥 Download Certificate",
    "zaten":"🚨 This file is already registered!",
    "kol_bos":"No NFTs yet","kol_bos2":"Upload your first artwork from home!",
    "sat":"💰 Sell","iptal_btn":"❌ Cancel","transfer":"🔄 Transfer",
    "satista":"🟢 For Sale","koleksiyonda":"🔒 In Collection",
    "tr_baslik":"🔄 Transfer","alici":"Recipient username",
    "tr_et":"✅ Transfer","vazgec":"❌ Cancel",
    "bos":"Cannot be empty!","bulunamadi":"User not found!","kendin":"Cannot transfer to yourself!",
    "tr_ok":"Transfer complete!",
    "pazar_bos":"Marketplace is empty","pazar_bos2":"List an NFT from your collection!",
    "senin":"📌 Your listing","bakiye_yok":"⚠️ Insufficient balance",
    "satin_al":"🛒 Buy","satin_ok":"✅ Purchased!","bak_yok":"Insufficient balance!",
    "blok_yok":"No blocks yet.","blok_gezgini":"Blockchain Explorer",
    "blok_ara":"Search Block (Index)","tam_zincir":"Chain Table",
    "zincir_ok":"✅ Chain is Intact!","hash_dogrula":"🔍 Verify Hash Integrity",
    "nonce_grafik":"🔢 Nonce per Block","nft_ist":"NFT Statistics",
    "bakiye":"💰 Balance","bakiye_ekle":"💳 Add","son_isl":"📋 Recent Transactions","isl_yok":"No transactions yet.",
    "uye":"Member since","kul_adi":"Username","sifre":"Password","sifre2":"Confirm Password",
    "kisa":"Password too short!","uyusmuyor":"Passwords don't match!","alindi":"Username taken!",
    "hesap_ok":"Account created!","yanlis":"Invalid username or password!",
    "blok_nasil":"🔗 How Does Blockchain Work?",
    "blok_acik":"Each NFT creates a block containing owner, file hash and previous signature. The chain cannot be altered.",
    "dog_baslik":"🔍 File Verification","dog_yukle":"Upload file to verify (JPG/PNG/PDF)",
    "dosya_bilgi":"File Info","dog_sonuc":"Blockchain Verification",
    "dog_bulundu":"✅ File found in blockchain! Registered in {count} block(s).",
    "dog_yok":"⚠️ Not found in blockchain. This file has not been registered as an NFT.",
    "alg_hash":"Perceptual Hash","boyutlar":"Dimensions","dosya_boyut":"File Size",
    "benzer_nftler":"Similar NFTs","gorsel_analiz":"Image Analysis","benzerlik_skoru":"Similarity Score",
},
}

TEMALAR = {
    "Mor-Mavi":('#7c3aed','#2563eb'), "Gece":('#0f172a','#1e3a5f'),
    "Gün Batımı":('#f97316','#dc2626'), "Yeşil":('#059669','#0891b2'),
    "Pembe":('#db2777','#7c3aed'), "Buz":('#0ea5e9','#06b6d4'),
    "Orman":('#166534','#065f46'), "Mercan":('#e11d48','#f97316'),
}

def sifre_hashle(p):
    return hashlib.sha256((p + TUZ).encode()).hexdigest()

def bos_veri():
    return {
        'kullanicilar': {'admin': {'sifre_hash': sifre_hashle('admin123'), 'nftler': [], 'para': 1000, 'kayit_tarihi': str(datetime.datetime.now())}},
        'bloklar': [], 'pazar': [], 'islemler': []
    }

def veri_yukle():
    if not os.path.exists(VF):
        v = bos_veri(); veri_kaydet(v); return v
    try:
        return json.load(open(VF, 'r', encoding='utf-8'))
    except:
        v = bos_veri(); veri_kaydet(v); return v

def veri_kaydet(v):
    try:
        json.dump(v, open(VF, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        return True
    except:
        return False

def rid(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def dosya_hash(b):
    return hashlib.sha256(b).hexdigest()

def pow_mine(idx, zaman, vstr, onceki, zorluk=2):
    hedef = '0' * zorluk
    n = 0
    while True:
        h = hashlib.sha256(f"{idx}{zaman}{vstr}{onceki}{n}".encode()).hexdigest()
        if h.startswith(hedef):
            return h, n
        n += 1

def resim_hash_al(img):
    try:
        return imagehash.average_hash(img)
    except:
        return None

def phash_str(dosya_bytes):
    try:
        return str(imagehash.phash(Image.open(BytesIO(dosya_bytes)).convert('RGB')))
    except:
        return None

def gercek_benzerlik(yeni, bloklar):
    """Gerçek imagehash karşılaştırması — random değil, average_hash mesafesi."""
    max_s, max_i = 0.0, -1
    if yeni is None:
        return max_i, max_s
    for i, b in enumerate(bloklar):
        rh = b.get('resim_hash')
        if not rh:
            continue
        try:
            d = yeni - imagehash.hex_to_hash(rh)
            s = max(0.0, 100.0 * (1 - d / 64.0))
            if s > max_s:
                max_s, max_i = s, i
        except:
            pass
    return max_i, max_s

def kirp(raw, w=300, h=300):
    try:
        img = Image.open(BytesIO(raw)).convert("RGB")
        r = min(w / img.width, h / img.height)
        nw, nh = int(img.width * r), int(img.height * r)
        img = img.resize((nw, nh), Image.LANCZOS)
        z = Image.new("RGB", (w, h), (245, 245, 248))
        z.paste(img, ((w - nw) // 2, (h - nh) // 2))
        buf = BytesIO(); z.save(buf, "PNG"); buf.seek(0)
        return buf.read()
    except:
        return raw

def sertifika(blok):
    img = Image.new('RGB', (800, 500), '#0f0c29')
    d = ImageDraw.Draw(img)
    for i in range(2):
        d.rectangle([i*15, i*15, 800-i*15, 500-i*15], outline=['#302b63','#24243e'][i], width=3)
    d.rectangle([30,30,770,470], outline='#a78bfa', width=2)
    tr = lambda s: s.replace('ş','s').replace('ğ','g').replace('ü','u').replace('ö','o').replace('ç','c').replace('ı','i').replace('İ','I').replace('Ş','S').replace('Ğ','G').replace('Ü','U').replace('Ö','O').replace('Ç','C')
    sahip = tr(blok['sahip']); eser = tr(blok['isim'])
    d.text((400,80),"ArtGuard AI",fill='#a78bfa',anchor='mm')
    d.text((400,130),"NFT CERTIFICATE",fill='white',anchor='mm')
    d.line([(100,155),(700,155)],fill='#a78bfa',width=1)
    for i,(k,v2) in enumerate([("Title",eser),("Owner",sahip),("Token",f"#{blok['numara']}"),("Date",blok['zaman'][:19])]):
        d.text((120,190+i*55),f"{k}:",fill='#a78bfa'); d.text((240,190+i*55),v2,fill='white')
    qr_obj = qrcode.make(f"NFT#{blok['numara']}|{blok['blok_hash'][:16]}|{sahip}").resize((130,130))
    img.paste(qr_obj,(630,170))
    d.text((400,455),blok['blok_hash'][:32]+"...",fill='#6b7280',anchor='mm')
    return img

def blockchain_gorseli(bloklar):
    n = min(len(bloklar), 5)
    if n == 0:
        fig, ax = plt.subplots(figsize=(10,3)); ax.axis('off')
        ax.text(0.5, 0.5, "No blocks yet", ha='center', va='center', fontsize=14, color='#888', transform=ax.transAxes)
        fig.patch.set_facecolor('#f8f9fa'); return fig
    bh, oh = 2.0, 0.6
    th = n * bh + (n-1) * oh + 1.5
    fig, ax = plt.subplots(figsize=(12, th))
    fig.patch.set_facecolor('#f0f4f8'); ax.set_facecolor('#f0f4f8'); ax.axis('off')
    ax.set_xlim(0,10); ax.set_ylim(0,th)
    ax.text(5, th-0.4, "Blockchain — each block is linked to the previous one", ha='center', fontsize=11, color='#555', style='italic')
    y = th - 1.1
    for i in range(n):
        b = bloklar[i]
        rc = '#1abc9c' if i==0 else '#3498db'
        ec = '#16a085' if i==0 else '#2980b9'
        ax.add_patch(mp.FancyBboxPatch((0.4, y-bh+0.1), 9.1, bh-0.1, boxstyle="round,pad=0.05", linewidth=2, edgecolor=ec, facecolor=rc))
        ax.text(0.9, y-0.35, "🌱 Genesis" if i==0 else f"🔗 Block #{b['numara']}", fontsize=10, weight='bold', color='white')
        ax.text(0.9, y-0.72, f"👤 {b['sahip']}  |  🖼️ {b['isim']}  |  💰 {b['fiyat']} TL", fontsize=8.5, color='#ecf0f1')
        ax.text(0.9, y-1.07, f"📅 {b['zaman'][:10]}  |  Nonce: {b.get('nonce','—')}", fontsize=8, color='#bde8ff')
        ax.text(9.4, y-0.5, f"{b['blok_hash'][:20]}...", fontsize=7, color='#d6eaf8', ha='right', family='monospace')
        ax.text(9.4, y-0.85, f"← {b['onceki_hash'][:16]}..." if b['numara']>0 else "← Genesis", fontsize=6.5, color='#a8d8f0', ha='right', family='monospace')
        if i < n-1:
            m = y - bh + 0.1
            ax.annotate('', xy=(5, m-oh+0.05), xytext=(5,m), arrowprops=dict(arrowstyle='->', lw=2, color='#e74c3c', mutation_scale=18))
            ax.text(5.35, m-oh/2, "hash match", fontsize=7, color='#e74c3c', style='italic')
        y -= bh + oh
    if len(bloklar) > n:
        ax.text(5, 0.25, f"+ {len(bloklar)-n} more blocks", ha='center', fontsize=8, color='#999', style='italic')
    plt.tight_layout(pad=0.3)
    return fig

# session state
for k, v in [('veri',None),('giris',False),('kullanici',None),('dosya_ok',False),('transfer_nft',None),('secili_tema','Mor-Mavi'),('dil','tr'),('sayfa','ana')]:
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.veri is None:
    st.session_state.veri = veri_yukle()

veri = st.session_state.veri
L = D[st.session_state.dil]
c1, c2 = TEMALAR[st.session_state.secili_tema]

st.markdown(f"""<style>
.stApp{{background:linear-gradient(135deg,{c1},{c2});min-height:100vh}}
.main .block-container{{background:rgba(255,255,255,.97);border-radius:20px;padding:2rem;box-shadow:0 16px 48px rgba(0,0,0,.22);max-width:1200px;margin:1rem auto}}
.stButton>button{{background:linear-gradient(90deg,{c1},{c2});color:#fff!important;border:none!important;border-radius:10px;padding:.5rem 1.4rem;font-weight:600;transition:.15s}}
.stButton>button:hover{{opacity:.85;transform:translateY(-1px)}}
[data-testid="stSidebar"]{{background:linear-gradient(180deg,{c1}33,{c2}11)}}
[data-testid="stMetric"]{{background:#f8f9fa;border-radius:12px;padding:.8rem 1rem;border:1px solid #e8ecef}}
hr{{border-color:#e8ecef!important}}
</style>""", unsafe_allow_html=True)

# giriş
if not st.session_state.giris:
    st.markdown(f"<h1 style='text-align:center'>{L['baslik']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#888'>{L['altyazi']}</p>", unsafe_allow_html=True)
    ds = st.selectbox(L['dil'], ["🇹🇷 Türkçe","🇬🇧 English"], index=0 if st.session_state.dil=='tr' else 1, key="dil_giris")
    nd = 'tr' if '🇹🇷' in ds else 'en'
    if nd != st.session_state.dil:
        st.session_state.dil = nd; st.rerun()
    st.markdown("---")
    t1, t2 = st.tabs([L['giris'], L['hesap_ac']])
    with t1:
        u = st.text_input(L['kul_adi'], key="g_k")
        p = st.text_input(L['sifre'], type="password", key="g_s")
        if st.button(L['giris'], key="giris_btn"):
            if u in veri['kullanicilar'] and veri['kullanicilar'][u]['sifre_hash'] == sifre_hashle(p):
                st.session_state.giris = True; st.session_state.kullanici = u; st.rerun()
            else:
                st.error(L['yanlis'])
    with t2:
        u2 = st.text_input(L['kul_adi'], key="k_u")
        p2 = st.text_input(L['sifre'], type="password", key="k_s1")
        p3 = st.text_input(L['sifre2'], type="password", key="k_s2")
        if st.button(L['hesap_ac'], key="kayit_btn"):
            if not u2 or not p2: st.error(L['bos'])
            elif len(p2) < 4: st.error(L['kisa'])
            elif p2 != p3: st.error(L['uyusmuyor'])
            elif u2 in veri['kullanicilar']: st.error(L['alindi'])
            else:
                veri['kullanicilar'][u2] = {'sifre_hash':sifre_hashle(p2),'nftler':[],'para':500,'kayit_tarihi':str(datetime.datetime.now()),'id':rid()}
                veri_kaydet(veri); st.success(L['hesap_ok']); st.balloons()
    st.stop()

# sidebar
aktif = veri['kullanicilar'][st.session_state.kullanici]
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.kullanici}")
    st.markdown(f"💰 **{aktif['para']} TL**  |  🖼️ **{len(aktif['nftler'])} NFT**")
    st.markdown("---")
    ds = st.selectbox(L['dil'], ["🇹🇷 Türkçe","🇬🇧 English"], index=0 if st.session_state.dil=='tr' else 1)
    nd = 'tr' if '🇹🇷' in ds else 'en'
    if nd != st.session_state.dil:
        st.session_state.dil = nd; st.rerun()
    tema = st.selectbox(L['tema'], list(TEMALAR.keys()), index=list(TEMALAR.keys()).index(st.session_state.secili_tema))
    if tema != st.session_state.secili_tema:
        st.session_state.secili_tema = tema; st.rerun()
    st.markdown("---")
    sayfalar = [L['ana'],L['kol'],L['pazar_s'],L['zincir'],L['analiz'],L['dogrula_s'],L['profil']]
    keys =     ['ana',  'kol', 'pazar',    'zincir', 'analiz', 'dogrula',    'profil']
    for sb, sk in zip(sayfalar, keys):
        if st.button(sb, key=f"sb_{sk}", use_container_width=True):
            st.session_state.sayfa = sk; st.rerun()
    st.markdown("---")
    if st.button(L['cikis']):
        st.session_state.giris = False; st.session_state.kullanici = None; st.rerun()

sayfa = st.session_state.sayfa

# ── ANA SAYFA ─────────────────────────────────────────────────────────────────
if sayfa == 'ana':
    st.markdown(f"<h2>{L['ana']}</h2>", unsafe_allow_html=True)
    k1,k2,k3 = st.columns(3)
    k1.metric(L['toplam_nft'], len(veri['bloklar']))
    k2.metric(L['benim_nft'], len(aktif['nftler']))
    k3.metric(L['pazarda'], len(veri['pazar']))
    st.markdown("---")
    with st.expander(L['nasil']):
        t1,t2,t3 = st.tabs([L['blok_tek'],L['nft_surec'],L['telif']])
        with t1:
            st.markdown("- SHA-256 kriptografik hash\n- Proof-of-Work güvenlik\n- Değiştirilemez zincir" if st.session_state.dil=='tr' else "- SHA-256 cryptographic hash\n- Proof-of-Work security\n- Immutable chain")
        with t2:
            st.markdown("1. Resim yükle\n2. Hash üretilir\n3. Blockchain'e kaydedilir\n4. Sertifika oluşturulur" if st.session_state.dil=='tr' else "1. Upload image\n2. Hash generated\n3. Saved to blockchain\n4. Certificate created")
        with t3:
            st.markdown("- Timestamp oluşturma tarihini kanıtlar\n- Hash bütünlüğü kanıtlar\n- Blockchain değiştirilemez kayıt" if st.session_state.dil=='tr' else "- Timestamp proves creation date\n- Hash proves file integrity\n- Blockchain provides immutable proof")
    st.markdown(f"### {L['yukle']}")
    st.caption(L['yukle_ipucu'])
    f = st.file_uploader(L['dosya_sec'], type=['jpg','jpeg','png'], key="yukle")
    if f and not st.session_state.dosya_ok:
        f.seek(0); fbytes = f.read(); fhash = dosya_hash(fbytes)
        kopya = next((b for b in veri['bloklar'] if b['dosya_hash']==fhash), None)
        if kopya:
            st.markdown(f"""<div style='background:#fdedec;border:2px solid #e74c3c;border-radius:14px;padding:18px 22px'>
<b style='color:#c0392b;font-size:17px'>{L['zaten']}</b><br>
<span style='color:#555;font-size:13px'>NFT #{kopya['numara']} — {kopya['isim']} | {kopya['sahip']}</span></div>""", unsafe_allow_html=True)
        else:
            sol,sag = st.columns([3,2])
            with sol:
                f.seek(0); st.image(f, use_container_width=True, caption=f.name)
            with sag:
                f.seek(0); img = Image.open(f); rhash = resim_hash_al(img)
                engel = False
                st.markdown(f"""<div style='background:#f8f9fa;border-radius:12px;padding:12px 16px;margin-bottom:10px;border:1px solid #eaecf0'>
<div style='font-size:11px;color:#888;font-weight:600;letter-spacing:.5px;margin-bottom:6px'>{L['gorsel_bilgi']}</div>
<span style='background:white;border-radius:6px;padding:3px 9px;font-size:12px;border:1px solid #e0e0e0'>{img.width}×{img.height}px</span>
<span style='background:white;border-radius:6px;padding:3px 9px;font-size:12px;border:1px solid #e0e0e0;margin-left:6px'>{img.mode}</span>
<div style='margin-top:8px;font-size:11px;color:#aaa;font-family:monospace'>{fhash[:36]}...</div></div>""", unsafe_allow_html=True)
                st.markdown(f"""<div style='display:flex;align-items:center;gap:8px;margin-bottom:10px'>
<div style='background:linear-gradient(135deg,{c1},{c2});width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px'>🤖</div>
<div><div style='font-weight:700;font-size:14px'>{L['ai_baslik']}</div><div style='font-size:11px;color:#888'>{L['ai_alt']}</div></div></div>""", unsafe_allow_html=True)
                if rhash and veri['bloklar']:
                    bi,bs = gercek_benzerlik(rhash, veri['bloklar'])
                    oz = round(100-bs,1); bs = round(bs,1)
                    if bs > 85:   br,bm,bik,ba = '#e74c3c',L['engel'],'🚫','#fdedec'; engel=True
                    elif bs > 65: br,bm,bik,ba = '#f39c12',L['uyari_benzer'],'⚠️','#fef9e7'
                    else:         br,bm,bik,ba = '#27ae60',L['ozgun'],'✅','#eafaf1'
                    bacik = f"NFT #{bi} {L['benzerlik_ile']}" if bs>65 else L['esleme_yok']
                    st.markdown(f"""<div style='background:{ba};border:2px solid {br};border-radius:12px;padding:14px 16px'>
<div style='font-size:11px;color:#888;margin-bottom:2px'>{L['oz_skor']}</div>
<div style='font-size:28px;font-weight:800;color:{br}'>{oz}%</div>
<div style='background:#fff8;border-radius:4px;height:7px;margin:6px 0;overflow:hidden'>
<div style='height:100%;width:{oz}%;background:{br};border-radius:4px'></div></div>
<div style='font-size:13px;font-weight:700;color:{br}'>{bik} {bm}</div>
<div style='font-size:11px;color:#888;margin-top:3px'>{bacik} — {len(veri["bloklar"])} {L['tarand']}</div></div>""", unsafe_allow_html=True)
                elif rhash:
                    st.markdown(f"""<div style='background:#eaf4fb;border:2px solid #2980b9;border-radius:12px;padding:14px 16px'>
<div style='font-size:28px;font-weight:800;color:#2980b9'>%100</div>
<div style='font-size:13px;font-weight:700;color:#2980b9'>🌟 {L['ilk']}</div>
<div style='font-size:11px;color:#888;margin-top:3px'>{L['ilk_acik']}</div></div>""", unsafe_allow_html=True)
            if not engel:
                st.markdown("---")
                ci1,ci2 = st.columns(2)
                isim = ci1.text_input(L['nft_adi'], key="nft_isim")
                fiyat = ci2.number_input(L['fiyat'], min_value=0, value=100, step=50, key="nft_fiyat")
                aciklama = st.text_area(L['aciklama'], height=70, key="nft_aciklama")
                if st.button(L['olustur_btn'], use_container_width=True):
                    if not isim: st.error(L['isim_bos'])
                    else:
                        onceki = veri['bloklar'][-1]['blok_hash'] if veri['bloklar'] else ""
                        zaman_str = str(datetime.datetime.now())
                        pow_h, nonce_val = pow_mine(len(veri['bloklar']), zaman_str, isim+st.session_state.kullanici, onceki)
                        f.seek(0); img2 = Image.open(f); rh = resim_hash_al(img2)
                        f.seek(0); rph = phash_str(f.read())
                        yeni = {
                            'numara':len(veri['bloklar']),'zaman':zaman_str,'isim':isim,
                            'sahip':st.session_state.kullanici,'dosya_hash':fhash,
                            'onceki_hash':onceki,'fiyat':fiyat,'aciklama':aciklama,
                            'satista':False,'nonce':nonce_val,'blok_hash':pow_h,
                            'resim_hash':str(rh) if rh else None,'perceptual_hash':rph
                        }
                        f.seek(0); yeni['resim_veri'] = base64.b64encode(f.read()).decode()
                        veri['bloklar'].append(yeni); aktif['nftler'].append(yeni['numara'])
                        veri['islemler'].append({'tip':'mint','nft_no':yeni['numara'],'gonderen':None,'alan':st.session_state.kullanici,'fiyat':0,'zaman':zaman_str})
                        if veri_kaydet(veri):
                            st.session_state.dosya_ok = True
                            st.markdown(f"""<div style='background:linear-gradient(135deg,#1abc9c,#27ae60);border-radius:14px;padding:20px;text-align:center'>
<div style='font-size:28px'>🎉</div>
<div style='color:white;font-size:17px;font-weight:700'>{L['nft_ok']}</div>
<div style='color:#d5f5e3;font-size:13px;margin-top:4px'>Token #{yeni['numara']} — "{isim}" {L['eklendi']}</div>
<div style='background:#ffffff33;border-radius:6px;padding:4px 10px;display:inline-block;margin-top:8px;font-size:11px;color:white;font-family:monospace'>PoW Nonce: {nonce_val} | {pow_h[:24]}...</div></div>""", unsafe_allow_html=True)
                            st.balloons()
                            sb2 = BytesIO(); sertifika(yeni).save(sb2,'PNG'); sb2.seek(0)
                            st.download_button(L['sertifika'], sb2, f"certificate_{yeni['numara']}.png","image/png")
                            time.sleep(2); st.session_state.dosya_ok = False; st.rerun()
                        else:
                            st.error(L['kayit_hata'])
    elif st.session_state.dosya_ok:
        st.session_state.dosya_ok = False

# ── KOLEKSİYON ───────────────────────────────────────────────────────────────
elif sayfa == 'kol':
    st.markdown(f"<h2>{L['kol']}</h2>", unsafe_allow_html=True)
    if not aktif['nftler']:
        st.markdown(f"<div style='text-align:center;padding:50px;background:#f8f9fa;border-radius:16px;border:2px dashed #dde1e7'><div style='font-size:48px'>🎨</div><div style='font-size:18px;font-weight:600;color:#555;margin-top:8px'>{L['kol_bos']}</div><div style='color:#888;font-size:14px'>{L['kol_bos2']}</div></div>", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for idx, nft_no in enumerate(aktif['nftler']):
            b = veri['bloklar'][nft_no]
            with cols[idx % 3]:
                if b.get('resim_veri'):
                    st.image(kirp(base64.b64decode(b['resim_veri'])), use_container_width=True)
                dr = "#27ae60" if b['satista'] else "#3498db"
                dy = L['satista'] if b['satista'] else L['koleksiyonda']
                st.markdown(f"""<div style='padding:6px 2px 8px'>
<div style='font-size:15px;font-weight:700;color:#1a1a2e'>{b['isim']}</div>
<div style='display:flex;gap:6px;flex-wrap:wrap;margin-top:4px'>
<span style='background:#f0f4ff;color:#3498db;font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600'>#{b['numara']}</span>
<span style='background:#fff8e7;color:#e67e22;font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600'>💰 {b['fiyat']} TL</span>
<span style='color:{dr};font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600;border:1px solid {dr}'>{dy}</span>
</div></div>""", unsafe_allow_html=True)
                bc1,bc2 = st.columns(2)
                with bc1:
                    if not b['satista']:
                        if st.button(L['sat'], key=f"sat_{nft_no}", use_container_width=True):
                            b['satista']=True; veri['pazar'].append(nft_no); veri_kaydet(veri); st.rerun()
                    else:
                        if st.button(L['iptal_btn'], key=f"iptal_{nft_no}", use_container_width=True):
                            b['satista']=False
                            if nft_no in veri['pazar']: veri['pazar'].remove(nft_no)
                            veri_kaydet(veri); st.rerun()
                with bc2:
                    if st.button(L['transfer'], key=f"tr_{nft_no}", use_container_width=True):
                        st.session_state.transfer_nft = nft_no; st.rerun()
                st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)
        if st.session_state.transfer_nft is not None:
            st.markdown("---")
            st.markdown(f"### {L['tr_baslik']}")
            tb = veri['bloklar'][st.session_state.transfer_nft]
            st.write(f"**{tb['isim']}**")
            alici = st.text_input(L['alici'], key="tr_alici")
            ta,tb2 = st.columns(2)
            with ta:
                if st.button(L['tr_et'], use_container_width=True):
                    if not alici: st.error(L['bos'])
                    elif alici not in veri['kullanicilar']: st.error(L['bulunamadi'])
                    elif alici == st.session_state.kullanici: st.error(L['kendin'])
                    else:
                        nft_n = st.session_state.transfer_nft
                        aktif['nftler'].remove(nft_n); veri['kullanicilar'][alici]['nftler'].append(nft_n)
                        veri['bloklar'][nft_n]['sahip'] = alici
                        veri['islemler'].append({'tip':'transfer','nft_no':nft_n,'gonderen':st.session_state.kullanici,'alan':alici,'fiyat':0,'zaman':str(datetime.datetime.now())})
                        veri_kaydet(veri); st.session_state.transfer_nft = None
                        st.success(L['tr_ok']); st.rerun()
            with tb2:
                if st.button(L['vazgec'], use_container_width=True):
                    st.session_state.transfer_nft = None; st.rerun()

# ── PAZAR ─────────────────────────────────────────────────────────────────────
elif sayfa == 'pazar':
    st.markdown(f"<h2>{L['pazar_s']}</h2>", unsafe_allow_html=True)
    if not veri['pazar']:
        st.markdown(f"<div style='text-align:center;padding:50px;background:#f8f9fa;border-radius:16px;border:2px dashed #dde1e7'><div style='font-size:48px'>🏪</div><div style='font-size:18px;font-weight:600;color:#555;margin-top:8px'>{L['pazar_bos']}</div><div style='color:#888;font-size:14px'>{L['pazar_bos2']}</div></div>", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for idx, nft_no in enumerate(veri['pazar']):
            b = veri['bloklar'][nft_no]
            with cols[idx % 3]:
                if b.get('resim_veri'):
                    st.image(kirp(base64.b64decode(b['resim_veri'])), use_container_width=True)
                kendi = b['sahip'] == st.session_state.kullanici
                yeter = aktif['para'] >= b['fiyat']
                st.markdown(f"""<div style='padding:6px 2px 8px'>
<div style='font-size:15px;font-weight:700;color:#1a1a2e'>{b['isim']}</div>
<div style='font-size:12px;color:#888;margin-top:2px'>{L['senin'] if kendi else f"👤 {b['sahip']}"}</div>
<div style='font-size:22px;font-weight:800;color:#e67e22;margin-top:4px'>💰 {b['fiyat']} TL</div>
{"" if kendi or yeter else f"<div style='font-size:11px;color:#e74c3c'>{L['bakiye_yok']}</div>"}</div>""", unsafe_allow_html=True)
                if not kendi:
                    if st.button(L['satin_al'], key=f"al_{nft_no}", use_container_width=True):
                        if yeter:
                            satici = b['sahip']; aktif['para'] -= b['fiyat']
                            veri['kullanicilar'][satici]['para'] += b['fiyat']*0.9
                            veri['kullanicilar'][satici]['nftler'].remove(nft_no)
                            aktif['nftler'].append(nft_no); b['sahip']=st.session_state.kullanici
                            b['satista']=False; veri['pazar'].remove(nft_no)
                            veri['islemler'].append({'tip':'satis','nft_no':nft_no,'gonderen':satici,'alan':st.session_state.kullanici,'fiyat':b['fiyat'],'zaman':str(datetime.datetime.now())})
                            veri_kaydet(veri); st.success(L['satin_ok']); st.balloons(); st.rerun()
                        else:
                            st.error(L['bak_yok'])
                else:
                    if st.button(L['iptal_btn'], key=f"pazar_iptal_{nft_no}", use_container_width=True):
                        b['satista']=False; veri['pazar'].remove(nft_no); veri_kaydet(veri); st.rerun()
                st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# ── BLOCKCHAIN ────────────────────────────────────────────────────────────────
elif sayfa == 'zincir':
    st.markdown(f"<h2>{L['zincir']}</h2>", unsafe_allow_html=True)
    if not veri['bloklar']:
        st.info(L['blok_yok'])
    else:
        k1,k2,k3 = st.columns(3)
        k1.metric(L['toplam_blok'], len(veri['bloklar']))
        k2.metric(L['zincir_gecerli'], "✅")
        k3.metric("Son Hash", veri['bloklar'][-1]['blok_hash'][:12]+"...")
        st.markdown("---")
        arama = st.number_input(L['blok_ara'], min_value=0, max_value=len(veri['bloklar'])-1, value=0)
        b = veri['bloklar'][arama]
        st.markdown(f"""<div style='background:#f8f9fa;padding:1rem;border-radius:10px;border-left:4px solid {c1}'>
<h3>Block #{b['numara']} — {b['isim']}</h3>
Sahip: {b['sahip']} | Tarih: {b['zaman'][:19]} | Fiyat: {b['fiyat']} TL | Nonce: {b.get('nonce','—')}
</div>""", unsafe_allow_html=True)
        st.code(f"Blok Hash : {b['blok_hash']}\nÖnceki    : {b['onceki_hash'] or 'Genesis'}\nDosya     : {b['dosya_hash']}\npHash     : {b.get('perceptual_hash','—')}", language=None)
        st.markdown("---")
        st.markdown(f"### {L['tam_zincir']}")
        df = pd.DataFrame([{'#':b['numara'],'Eser':b['isim'],'Sahip':b['sahip'],'Nonce':b.get('nonce','—'),'Hash':b['blok_hash'][:12]+'...','Tarih':b['zaman'][:10]} for b in veri['bloklar']])
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        if st.button(L['hash_dogrula']):
            sorun = False
            for i, b in enumerate(veri['bloklar']):
                if i > 0 and b['onceki_hash'] != veri['bloklar'][i-1]['blok_hash']:
                    st.error(f"Block #{b['numara']} hash mismatch!"); sorun = True
            if not sorun:
                st.markdown(f"<div style='background:#eafaf1;border:2px solid #27ae60;border-radius:10px;padding:14px;text-align:center'><b style='color:#1e8449;font-size:16px'>{L['zincir_ok']}</b></div>", unsafe_allow_html=True)

# ── ANALİZ ────────────────────────────────────────────────────────────────────
elif sayfa == 'analiz':
    st.markdown(f"<h2>{L['analiz']}</h2>", unsafe_allow_html=True)
    st.markdown(f"""<div style='background:linear-gradient(135deg,#1f2937,#374151);border-radius:12px;padding:16px 20px;margin-bottom:18px'>
<b style='color:#a78bfa;font-size:15px'>{L['blok_nasil']}</b>
<p style='color:#d1d5db;font-size:13px;margin:6px 0 0'>{L['blok_acik']}</p></div>""", unsafe_allow_html=True)
    fig = blockchain_gorseli(veri['bloklar'])
    canvas = FigureCanvasAgg(fig); canvas.draw()
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=140, bbox_inches='tight'); buf.seek(0)
    st.image(Image.open(buf), use_container_width=True); buf.seek(0)
    st.download_button("📥 Download", buf, "blockchain.png", "image/png")
    plt.close(fig)
    st.markdown("---")
    if len(veri['bloklar']) > 1:
        st.markdown(f"### {L['nonce_grafik']}")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[b['numara'] for b in veri['bloklar']], y=[b.get('nonce',0) for b in veri['bloklar']], mode='lines+markers', line=dict(color=c1,width=3), marker=dict(size=8,color=c2)))
        fig2.update_layout(xaxis_title="Block #", yaxis_title="Nonce", template="plotly_white", height=300, margin=dict(t=10,b=20))
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")
    k1,k2,k3,k4 = st.columns(4)
    k1.metric(L['toplam_blok'], len(veri['bloklar']))
    k2.metric("İşlem" if st.session_state.dil=='tr' else "Transactions", len(veri['islemler']))
    k3.metric("Kullanıcı" if st.session_state.dil=='tr' else "Users", len(veri['kullanicilar']))
    k4.metric(L['pazarda'], len(veri['pazar']))
    if veri['bloklar']:
        st.markdown("---")
        st.markdown(f"### {L['nft_ist']}")
        sahipler = {}
        for b in veri['bloklar']:
            sahipler[b['sahip']] = sahipler.get(b['sahip'],0) + 1
        fig3 = go.Figure(go.Bar(x=list(sahipler.keys()), y=list(sahipler.values()), marker_color=c1))
        fig3.update_layout(template="plotly_white", height=280, margin=dict(t=10,b=20))
        st.plotly_chart(fig3, use_container_width=True)

# ── DOĞRULAMA ─────────────────────────────────────────────────────────────────
elif sayfa == 'dogrula':
    st.markdown(f"<h2>{L['dog_baslik']}</h2>", unsafe_allow_html=True)
    yukle_dog = st.file_uploader(L['dog_yukle'], type=['jpg','jpeg','png','pdf'], key="dog_yukle")
    if yukle_dog:
        icerik = yukle_dog.getvalue()
        fh = dosya_hash(icerik)
        st.markdown(f"""<div style='background:#f8f9fa;padding:1rem;border-radius:10px;border-left:4px solid {c1};margin-bottom:12px'>
<b style='font-size:15px'>{L['dosya_bilgi']}</b><br><br>
📄 <b>{yukle_dog.name}</b> &nbsp;|&nbsp; {round(len(icerik)/1024,1)} KB<br>
<span style='font-family:monospace;font-size:12px;color:#555'>SHA-256: {fh}</span>""", unsafe_allow_html=True)
        if yukle_dog.type.startswith('image'):
            ph = phash_str(icerik)
            st.markdown(f"<br><span style='font-family:monospace;font-size:12px;color:#888'>{L['alg_hash']}: {ph}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        bulunan = [(i, b) for i,b in enumerate(veri['bloklar']) if b['dosya_hash']==fh]
        if bulunan:
            st.success(L['dog_bulundu'].format(count=len(bulunan)))
            for i,b in bulunan:
                st.write(f"**Block #{i}:** {b['isim']} — {b['sahip']} — {b['zaman'][:19]}")
        else:
            st.warning(L['dog_yok'])
        if yukle_dog.type.startswith('image') and veri['bloklar']:
            img_dog = Image.open(BytesIO(icerik))
            rh_dog = resim_hash_al(img_dog)
            st.markdown("---")
            st.markdown(f"### {L['gorsel_analiz']}")
            m1,m2,m3 = st.columns(3)
            m1.metric(L['boyutlar'], f"{img_dog.width}×{img_dog.height}")
            m2.metric(L['dosya_boyut'], f"{round(len(icerik)/1024/1024,2)} MB")
            bi_d, bs_d = gercek_benzerlik(rh_dog, veri['bloklar'])
            m3.metric(L['benzerlik_skoru'], f"{round(bs_d,1)}%")
            st.image(img_dog, use_container_width=True)
            # tüm NFT'lere karşı gerçek benzerlik bar chart
            skorlar = []
            for i,b in enumerate(veri['bloklar']):
                rh2 = b.get('resim_hash')
                if not rh2 or not rh_dog:
                    continue
                try:
                    d = rh_dog - imagehash.hex_to_hash(rh2)
                    s = max(0.0, 100.0*(1 - d/64.0))
                    skorlar.append((s, i, b['isim']))
                except:
                    pass
            skorlar.sort(reverse=True)
            if skorlar:
                st.markdown(f"**{L['benzer_nftler']}:**")
                for s,i,isim in skorlar[:5]:
                    renk = '#e74c3c' if s>85 else ('#f39c12' if s>65 else '#27ae60')
                    st.markdown(f"""<div style='margin:4px 0;display:flex;align-items:center;gap:10px'>
<span style='min-width:140px;font-size:13px'>NFT #{i}: {isim[:18]}</span>
<div style='flex:1;background:#eee;border-radius:4px;height:12px;overflow:hidden'>
<div style='height:100%;width:{int(s)}%;background:{renk};border-radius:4px'></div></div>
<span style='font-size:13px;font-weight:700;color:{renk};min-width:48px'>{s:.1f}%</span></div>""", unsafe_allow_html=True)

# ── PROFİL ────────────────────────────────────────────────────────────────────
elif sayfa == 'profil':
    st.markdown(f"<h2>{L['profil']}</h2>", unsafe_allow_html=True)
    p1,p2 = st.columns([1,2])
    with p1:
        st.markdown(f"<div style='background:linear-gradient(135deg,{c1},{c2});border-radius:50%;width:80px;height:80px;display:flex;align-items:center;justify-content:center;font-size:36px;margin:0 auto'>👤</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center'>{st.session_state.kullanici}</h3>", unsafe_allow_html=True)
        st.caption(f"{L['uye']}: {aktif['kayit_tarihi'][:10]}")
    with p2:
        st.metric(L['bakiye'], f"{aktif['para']} TL")
        st.metric(L['benim_nft'], len(aktif['nftler']))
        st.markdown("---")
        ekle = st.number_input(L['bakiye']+" (TL)", min_value=0, value=500, step=50)
        if st.button(L['bakiye_ekle']):
            aktif['para'] += ekle; veri_kaydet(veri); st.success(f"{ekle} TL eklendi!"); st.rerun()
        st.markdown("---")
        st.markdown(f"**{L['son_isl']}**")
        islemler = [i for i in veri['islemler'] if i.get('gonderen')==st.session_state.kullanici or i.get('alan')==st.session_state.kullanici]
        if not islemler: st.info(L['isl_yok'])
        else:
            for i in reversed(islemler[-8:]):
                ikon = {'mint':'🌱','transfer':'🔄','satis':'💸'}.get(i['tip'],'📋')
                st.write(f"{ikon} **{i['tip'].upper()}** — NFT #{i['nft_no']} — {i['zaman'][:16]}")

st.markdown("---")
st.caption("ArtGuard AI | TÜBİTAK 4006 Projesi")
