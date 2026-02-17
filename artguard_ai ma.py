import streamlit as st
import hashlib, json, datetime, os, time, random, string, base64
from PIL import Image, ImageDraw
import imagehash, qrcode, matplotlib.pyplot as plt, matplotlib.patches as mp
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO

st.set_page_config(page_title="ArtGuard AI", page_icon="🎨", layout="wide")
VF = 'veri.json'
TUZ = "nft2024xyz"

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

def blok_hash(blok):
    t = str(blok['numara']) + blok['zaman'] + blok['sahip'] + blok['dosya_hash']
    if blok['numara'] > 0:
        t += blok['onceki_hash']
    return hashlib.sha256(t.encode()).hexdigest()

def resim_hash(img):
    try:
        return imagehash.average_hash(img)
    except:
        return None

def benzerlik_tara(yeni_hash, bloklar):
    max_s, max_i = 0, -1
    if yeni_hash is None:
        return max_i, max_s
    for i, b in enumerate(bloklar):
        if b.get('resim_hash'):
            try:
                fark = yeni_hash - imagehash.hex_to_hash(b['resim_hash'])
                s = 100 * (1 - fark / 64.0)
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
        zemin = Image.new("RGB", (w, h), (245, 245, 248))
        zemin.paste(img, ((w - nw) // 2, (h - nh) // 2))
        buf = BytesIO()
        zemin.save(buf, "PNG")
        buf.seek(0)
        return buf.read()
    except:
        return raw

def sertifika_olustur(blok):
    img = Image.new('RGB', (800, 500), '#0f0c29')
    d = ImageDraw.Draw(img)
    for i, c in enumerate(['#302b63', '#24243e']):
        d.rectangle([i * 15, i * 15, 800 - i * 15, 500 - i * 15], outline=c, width=3)
    d.rectangle([30, 30, 770, 470], outline='#a78bfa', width=2)
    temiz = lambda s: s.replace('ş','s').replace('ğ','g').replace('ü','u').replace('ö','o').replace('ç','c').replace('ı','i').replace('İ','I').replace('Ş','S').replace('Ğ','G').replace('Ü','U').replace('Ö','O').replace('Ç','C')
    sahip = temiz(blok['sahip'])
    eser = temiz(blok['isim'])
    d.text((400, 80), "ArtGuard AI", fill='#a78bfa', anchor='mm')
    d.text((400, 130), "NFT SERTIFIKASI", fill='white', anchor='mm')
    d.line([(100, 155), (700, 155)], fill='#a78bfa', width=1)
    bilgiler = [("Eser", eser), ("Sahip", sahip), ("Token", f"#{blok['numara']}"), ("Tarih", blok['zaman'][:19])]
    for i, (k, v2) in enumerate(bilgiler):
        d.text((120, 190 + i * 55), f"{k}:", fill='#a78bfa')
        d.text((220, 190 + i * 55), v2, fill='white')
    qr_obj = qrcode.make(f"NFT#{blok['numara']}|{blok['blok_hash'][:16]}|{sahip}").resize((130, 130))
    img.paste(qr_obj, (630, 170))
    d.text((400, 455), blok['blok_hash'][:32] + "...", fill='#6b7280', anchor='mm')
    return img

def blockchain_gorseli(bloklar):
    n = min(len(bloklar), 5)
    if n == 0:
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.axis('off')
        ax.text(0.5, 0.5, "Henüz NFT yok", ha='center', va='center', fontsize=14, color='#888', transform=ax.transAxes)
        fig.patch.set_facecolor('#f8f9fa')
        return fig
    bh, oh = 2.0, 0.6
    th = n * bh + (n - 1) * oh + 1.5
    fig, ax = plt.subplots(figsize=(12, th))
    fig.patch.set_facecolor('#f0f4f8')
    ax.set_facecolor('#f0f4f8')
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, th)
    ax.text(5, th - 0.4, "Blockchain — Her blok öncekine bağlı, değiştirilemez", ha='center', fontsize=11, color='#555', style='italic')
    y = th - 1.1
    for i in range(n):
        b = bloklar[i]
        renk = '#1abc9c' if i == 0 else '#3498db'
        krenk = '#16a085' if i == 0 else '#2980b9'
        g = mp.FancyBboxPatch((0.4, y - bh + 0.1), 9.1, bh - 0.1, boxstyle="round,pad=0.05", linewidth=2, edgecolor=krenk, facecolor=renk)
        ax.add_patch(g)
        etiket = "🌱 Genesis Blok" if i == 0 else f"🔗 Blok #{b['numara']}"
        ax.text(0.9, y - 0.35, etiket, fontsize=10, weight='bold', color='white')
        ax.text(0.9, y - 0.72, f"👤 {b['sahip']}  |  🖼️ {b['isim']}  |  💰 {b['fiyat']} TL", fontsize=8.5, color='#ecf0f1')
        ax.text(0.9, y - 1.07, f"📅 {b['zaman'][:10]}", fontsize=8, color='#bde8ff')
        ax.text(9.4, y - 0.5, f"{b['blok_hash'][:20]}...", fontsize=7, color='#d6eaf8', ha='right', family='monospace')
        ax.text(9.4, y - 0.85, f"← {b['onceki_hash'][:16]}..." if b['numara'] > 0 else "← Genesis", fontsize=6.5, color='#a8d8f0', ha='right', family='monospace')
        if i < n - 1:
            mid_y = y - bh + 0.1
            ax.annotate('', xy=(5, mid_y - oh + 0.05), xytext=(5, mid_y), arrowprops=dict(arrowstyle='->', lw=2, color='#e74c3c', mutation_scale=18))
            ax.text(5.35, mid_y - oh / 2, "hash eşleşiyor", fontsize=7, color='#e74c3c', style='italic')
        y -= bh + oh
    if len(bloklar) > n:
        ax.text(5, 0.25, f"+ {len(bloklar) - n} blok daha", ha='center', fontsize=8, color='#999', style='italic')
    plt.tight_layout(pad=0.3)
    return fig

# SESSION STATE
for k, v in [('veri', None), ('giris', False), ('kullanici', None), ('dosya_ok', False), ('transfer_nft', None)]:
    if k not in st.session_state:
        st.session_state[k] = v
if st.session_state.veri is None:
    st.session_state.veri = veri_yukle()
veri = st.session_state.veri

# TEMA & CSS
if 'secili_tema' not in st.session_state:
    st.session_state.secili_tema = "Mor-Mavi"
temalar = {
    "Mor-Mavi": ('#7c3aed', '#2563eb'), "Koyu Lacivert": ('#1e3a5f', '#0f172a'),
    "Gün Batımı": ('#f97316', '#dc2626'), "Yeşil": ('#059669', '#0891b2'),
    "Pembe": ('#db2777', '#7c3aed'), "Altın": ('#d97706', '#92400e'),
    "Buz": ('#0ea5e9', '#06b6d4'), "Gece": ('#1f2937', '#111827'),
    "Mercan": ('#e11d48', '#f97316'), "Orman": ('#166534', '#065f46')
}
c1, c2 = temalar[st.session_state.secili_tema]
st.markdown(f"""<style>
.stApp{{background:linear-gradient(135deg,{c1},{c2});min-height:100vh}}
.main .block-container{{background:rgba(255,255,255,.97);border-radius:20px;padding:2rem;box-shadow:0 16px 48px rgba(0,0,0,.22);max-width:1200px;margin:1rem auto}}
.stButton>button{{background:linear-gradient(90deg,{c1},{c2});color:#fff!important;border:none!important;border-radius:10px;padding:.5rem 1.4rem;font-weight:600;transition:.15s}}
.stButton>button:hover{{opacity:.85;transform:translateY(-1px)}}
[data-testid="stSidebar"]{{background:linear-gradient(180deg,{c1}33,{c2}11)}}
[data-testid="stMetric"]{{background:#f8f9fa;border-radius:12px;padding:.8rem 1rem;border:1px solid #e8ecef}}
.stProgress>div>div>div>div{{background:linear-gradient(90deg,{c1},{c2});border-radius:6px}}
hr{{border-color:#e8ecef!important}}
</style>""", unsafe_allow_html=True)

# GİRİŞ SAYFASI
if not st.session_state.giris:
    st.markdown("<h1 style='text-align:center'>🎨 ArtGuard AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888'>Dijital sanatı blockchain ile koru</p>", unsafe_allow_html=True)
    st.markdown("---")
    t1, t2 = st.tabs(["Giriş Yap", "Hesap Oluştur"])
    with t1:
        u = st.text_input("Kullanıcı Adı", key="g_k")
        p = st.text_input("Şifre", type="password", key="g_s")
        if st.button("Giriş", key="giris_btn"):
            if u in veri['kullanicilar'] and veri['kullanicilar'][u]['sifre_hash'] == sifre_hashle(p):
                st.session_state.giris = True
                st.session_state.kullanici = u
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre yanlış!")
    with t2:
        u2 = st.text_input("Kullanıcı Adı", key="k_u")
        p2 = st.text_input("Şifre", type="password", key="k_s1")
        p3 = st.text_input("Şifre Tekrar", type="password", key="k_s2")
        if st.button("Hesap Oluştur", key="kayit_btn"):
            if not u2 or not p2:
                st.error("Boş bırakma!")
            elif len(p2) < 4:
                st.error("Şifre çok kısa!")
            elif p2 != p3:
                st.error("Şifreler uyuşmuyor!")
            elif u2 in veri['kullanicilar']:
                st.error("Bu ad alınmış!")
            else:
                veri['kullanicilar'][u2] = {
                    'sifre_hash': sifre_hashle(p2), 'nftler': [], 'para': 500,
                    'kayit_tarihi': str(datetime.datetime.now()), 'id': rid()
                }
                veri_kaydet(veri)
                st.success("Hesap oluşturuldu!")
                st.balloons()
    st.stop()

# SIDEBAR
aktif = veri['kullanicilar'][st.session_state.kullanici]
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.kullanici}")
    st.markdown(f"💰 **{aktif['para']} TL**  |  🖼️ **{len(aktif['nftler'])} NFT**")
    st.markdown("---")
    tema = st.selectbox("🎨 Tema", list(temalar.keys()), index=list(temalar.keys()).index(st.session_state.secili_tema))
    if tema != st.session_state.secili_tema:
        st.session_state.secili_tema = tema
        st.rerun()
    st.markdown("---")
    sayfa = st.radio("📌 Sayfa", ["Ana Sayfa", "Koleksiyonum", "Pazar", "Blockchain", "Analiz", "Profil"])
    st.markdown("---")
    if st.button("🚪 Çıkış"):
        st.session_state.giris = False
        st.session_state.kullanici = None
        st.rerun()

# ANA SAYFA
if sayfa == "Ana Sayfa":
    st.markdown("<h2>🏠 Ana Sayfa</h2>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    k1.metric("⛓️ Toplam NFT", len(veri['bloklar']))
    k2.metric("🖼️ Benim NFT", len(aktif['nftler']))
    k3.metric("🛒 Pazarda", len(veri['pazar']))
    st.markdown("---")
    st.markdown("### 📤 Yeni Eser Yükle")
    st.caption("Resim yükle — AI benzerlik taraması otomatik çalışır.")
    f = st.file_uploader("JPG / PNG seç", type=['jpg', 'jpeg', 'png'], key="yukle")
    if f and not st.session_state.dosya_ok:
        f.seek(0)
        fbytes = f.read()
        fhash = dosya_hash(fbytes)
        kopya = next((b for b in veri['bloklar'] if b['dosya_hash'] == fhash), None)
        if kopya:
            st.markdown(f"""<div style='background:#fdedec;border:2px solid #e74c3c;border-radius:14px;padding:18px 22px'>
<b style='color:#c0392b;font-size:17px'>🚨 Bu dosya zaten kayıtlı!</b><br>
<span style='color:#555;font-size:13px'>NFT #{kopya['numara']} — {kopya['isim']} | Sahip: {kopya['sahip']}</span></div>""", unsafe_allow_html=True)
        else:
            sol, sag = st.columns([3, 2])
            with sol:
                f.seek(0)
                st.image(f, use_container_width=True, caption=f.name)
            with sag:
                f.seek(0)
                img = Image.open(f)
                rhash = resim_hash(img)
                engel = False
                st.markdown(f"""<div style='background:#f8f9fa;border-radius:12px;padding:12px 16px;margin-bottom:10px;border:1px solid #eaecf0'>
<div style='font-size:11px;color:#888;font-weight:600;letter-spacing:.5px;margin-bottom:6px'>📐 GÖRSEL BİLGİSİ</div>
<span style='background:white;border-radius:6px;padding:3px 9px;font-size:12px;border:1px solid #e0e0e0'>{img.width}×{img.height}px</span>
<span style='background:white;border-radius:6px;padding:3px 9px;font-size:12px;border:1px solid #e0e0e0;margin-left:6px'>{img.mode}</span>
<div style='margin-top:8px;font-size:11px;color:#aaa;font-family:monospace'>{fhash[:36]}...</div></div>""", unsafe_allow_html=True)
                st.markdown("""<div style='display:flex;align-items:center;gap:8px;margin-bottom:10px'>
<div style='background:linear-gradient(135deg,#7c3aed,#2563eb);width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px'>🤖</div>
<div><div style='font-weight:700;font-size:14px'>ArtGuard AI</div><div style='font-size:11px;color:#888'>Özgünlük Analizi</div></div></div>""", unsafe_allow_html=True)
                if rhash and veri['bloklar']:
                    bi, bs = benzerlik_tara(rhash, veri['bloklar'])
                    oz = round(100 - bs, 1)
                    bs = round(bs, 1)
                    if bs > 85:
                        brenk, bmetin, bikon, barka = '#e74c3c', 'YÜKLEME ENGELLENDİ', '🚫', '#fdedec'
                        engel = True
                    elif bs > 65:
                        brenk, bmetin, bikon, barka = '#f39c12', 'DİKKAT — Benzer İçerik', '⚠️', '#fef9e7'
                    else:
                        brenk, bmetin, bikon, barka = '#27ae60', 'ÖZGÜN ESER', '✅', '#eafaf1'
                    st.markdown(f"""<div style='background:{barka};border:2px solid {brenk};border-radius:12px;padding:14px 16px'>
<div style='font-size:11px;color:#888;margin-bottom:2px'>Özgünlük Skoru</div>
<div style='font-size:28px;font-weight:800;color:{brenk}'>{oz}%</div>
<div style='background:#fff8;border-radius:4px;height:7px;margin:6px 0;overflow:hidden'>
<div style='height:100%;width:{oz}%;background:{brenk};border-radius:4px'></div></div>
<div style='font-size:13px;font-weight:700;color:{brenk}'>{bikon} {bmetin}</div>
<div style='font-size:11px;color:#888;margin-top:3px'>{"NFT #" + str(bi) + " ile benzerlik" if bs > 65 else "Blockchain'de eşleşme yok"} — {len(veri["bloklar"])} NFT tarandı</div></div>""", unsafe_allow_html=True)
                elif rhash:
                    st.markdown("""<div style='background:#eaf4fb;border:2px solid #2980b9;border-radius:12px;padding:14px 16px'>
<div style='font-size:28px;font-weight:800;color:#2980b9'>%100</div>
<div style='font-size:13px;font-weight:700;color:#2980b9'>🌟 İLK ESER</div>
<div style='font-size:11px;color:#888;margin-top:3px'>Blockchain henüz boş!</div></div>""", unsafe_allow_html=True)
            if not engel:
                st.markdown("---")
                c1i, c2i = st.columns(2)
                isim = c1i.text_input("🎨 NFT Adı", placeholder="örn. Dijital Gün Batımı", key="nft_isim")
                fiyat = c2i.number_input("💰 Fiyat (TL)", min_value=0, value=100, step=50, key="nft_fiyat")
                aciklama = st.text_area("📝 Açıklama", height=70, key="nft_aciklama")
                if st.button("⛓️ NFT Oluştur ve Blockchain'e Kaydet", use_container_width=True):
                    if not isim:
                        st.error("İsim boş olamaz!")
                    else:
                        onceki = veri['bloklar'][-1]['blok_hash'] if veri['bloklar'] else ""
                        yeni = {
                            'numara': len(veri['bloklar']), 'zaman': str(datetime.datetime.now()),
                            'isim': isim, 'sahip': st.session_state.kullanici,
                            'dosya_hash': fhash, 'onceki_hash': onceki,
                            'fiyat': fiyat, 'aciklama': aciklama, 'satista': False
                        }
                        f.seek(0)
                        img2 = Image.open(f)
                        rh = resim_hash(img2)
                        yeni['resim_hash'] = str(rh) if rh else None
                        f.seek(0)
                        yeni['resim_veri'] = base64.b64encode(f.read()).decode()
                        yeni['blok_hash'] = blok_hash(yeni)
                        veri['bloklar'].append(yeni)
                        aktif['nftler'].append(yeni['numara'])
                        veri['islemler'].append({
                            'tip': 'mint', 'nft_no': yeni['numara'],
                            'gonderen': None, 'alan': st.session_state.kullanici,
                            'fiyat': 0, 'zaman': str(datetime.datetime.now())
                        })
                        if veri_kaydet(veri):
                            st.session_state.dosya_ok = True
                            st.markdown(f"""<div style='background:linear-gradient(135deg,#1abc9c,#27ae60);border-radius:14px;padding:20px;text-align:center'>
<div style='font-size:28px'>🎉</div>
<div style='color:white;font-size:17px;font-weight:700'>NFT Oluşturuldu!</div>
<div style='color:#d5f5e3;font-size:13px;margin-top:4px'>Token #{yeni['numara']} — "{isim}" blockchain'e eklendi</div>
<div style='background:#ffffff33;border-radius:6px;padding:4px 10px;display:inline-block;margin-top:8px;font-size:11px;color:white;font-family:monospace'>{yeni['blok_hash'][:28]}...</div></div>""", unsafe_allow_html=True)
                            st.balloons()
                            sert = sertifika_olustur(yeni)
                            sb = BytesIO()
                            sert.save(sb, 'PNG')
                            sb.seek(0)
                            st.download_button("📥 Sertifika İndir", sb, f"sertifika_{yeni['numara']}.png", "image/png")
                            time.sleep(2)
                            st.session_state.dosya_ok = False
                            st.rerun()
                        else:
                            st.error("Kayıt hatası!")
    elif st.session_state.dosya_ok:
        st.session_state.dosya_ok = False

# KOLEKSİYON
elif sayfa == "Koleksiyonum":
    st.markdown("<h2>🖼️ NFT Koleksiyonum</h2>", unsafe_allow_html=True)
    if not aktif['nftler']:
        st.markdown("<div style='text-align:center;padding:50px;background:#f8f9fa;border-radius:16px;border:2px dashed #dde1e7'><div style='font-size:48px'>🎨</div><div style='font-size:18px;font-weight:600;color:#555;margin-top:8px'>Henüz NFT'n yok</div><div style='color:#888;font-size:14px'>Ana sayfadan ilk eserini ekle!</div></div>", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for idx, nft_no in enumerate(aktif['nftler']):
            b = veri['bloklar'][nft_no]
            with cols[idx % 3]:
                if b.get('resim_veri'):
                    st.image(kirp(base64.b64decode(b['resim_veri'])), use_container_width=True)
                durum_renk = "#27ae60" if b['satista'] else "#3498db"
                durum = "🟢 Satışta" if b['satista'] else "🔒 Koleksiyonda"
                st.markdown(f"""<div style='padding:6px 2px 8px'>
<div style='font-size:15px;font-weight:700;color:#1a1a2e'>{b['isim']}</div>
<div style='display:flex;gap:6px;flex-wrap:wrap;margin-top:4px'>
<span style='background:#f0f4ff;color:#3498db;font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600'>#{b['numara']}</span>
<span style='background:#fff8e7;color:#e67e22;font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600'>💰 {b['fiyat']} TL</span>
<span style='color:{durum_renk};font-size:11px;padding:2px 8px;border-radius:5px;font-weight:600;border:1px solid {durum_renk}'>{durum}</span>
</div></div>""", unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                with bc1:
                    if not b['satista']:
                        if st.button("💰 Sat", key=f"sat_{nft_no}", use_container_width=True):
                            b['satista'] = True
                            veri['pazar'].append(nft_no)
                            veri_kaydet(veri)
                            st.rerun()
                    else:
                        if st.button("❌ İptal", key=f"iptal_{nft_no}", use_container_width=True):
                            b['satista'] = False
                            if nft_no in veri['pazar']:
                                veri['pazar'].remove(nft_no)
                            veri_kaydet(veri)
                            st.rerun()
                with bc2:
                    if st.button("🔄 Transfer", key=f"tr_{nft_no}", use_container_width=True):
                        st.session_state.transfer_nft = nft_no
                        st.rerun()
                st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)
        if st.session_state.transfer_nft is not None:
            st.markdown("---")
            st.markdown("### 🔄 Transfer")
            tb = veri['bloklar'][st.session_state.transfer_nft]
            st.write(f"**Eser:** {tb['isim']}")
            alici = st.text_input("Alıcı kullanıcı adı", key="tr_alici")
            ta, tb2 = st.columns(2)
            with ta:
                if st.button("✅ Transfer Et", use_container_width=True):
                    if not alici:
                        st.error("Boş bırakma!")
                    elif alici not in veri['kullanicilar']:
                        st.error("Kullanıcı bulunamadı!")
                    elif alici == st.session_state.kullanici:
                        st.error("Kendinize transfer edilemez!")
                    else:
                        nft_n = st.session_state.transfer_nft
                        aktif['nftler'].remove(nft_n)
                        veri['kullanicilar'][alici]['nftler'].append(nft_n)
                        veri['bloklar'][nft_n]['sahip'] = alici
                        veri['islemler'].append({
                            'tip': 'transfer', 'nft_no': nft_n,
                            'gonderen': st.session_state.kullanici, 'alan': alici,
                            'fiyat': 0, 'zaman': str(datetime.datetime.now())
                        })
                        veri_kaydet(veri)
                        st.session_state.transfer_nft = None
                        st.success("Transfer tamam!")
                        st.rerun()
            with tb2:
                if st.button("❌ Vazgeç", use_container_width=True):
                    st.session_state.transfer_nft = None
                    st.rerun()

# PAZAR
elif sayfa == "Pazar":
    st.markdown("<h2>🛒 NFT Pazarı</h2>", unsafe_allow_html=True)
    if not veri['pazar']:
        st.markdown("<div style='text-align:center;padding:50px;background:#f8f9fa;border-radius:16px;border:2px dashed #dde1e7'><div style='font-size:48px'>🏪</div><div style='font-size:18px;font-weight:600;color:#555;margin-top:8px'>Pazar boş</div><div style='color:#888;font-size:14px'>Koleksiyonundan NFT satışa çıkar!</div></div>", unsafe_allow_html=True)
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
<div style='font-size:12px;color:#888;margin-top:2px'>{"📌 Senin ilanın" if kendi else f"👤 {b['sahip']}"}</div>
<div style='font-size:22px;font-weight:800;color:#e67e22;margin-top:4px'>💰 {b['fiyat']} TL</div>
{"" if kendi or yeter else "<div style='font-size:11px;color:#e74c3c'>⚠️ Bakiye yetersiz</div>"}</div>""", unsafe_allow_html=True)
                if not kendi:
                    if st.button("🛒 Satın Al", key=f"al_{nft_no}", use_container_width=True):
                        if yeter:
                            satici = b['sahip']
                            aktif['para'] -= b['fiyat']
                            veri['kullanicilar'][satici]['para'] += b['fiyat'] * 0.9
                            veri['kullanicilar'][satici]['nftler'].remove(nft_no)
                            aktif['nftler'].append(nft_no)
                            b['sahip'] = st.session_state.kullanici
                            b['satista'] = False
                            veri['pazar'].remove(nft_no)
                            veri['islemler'].append({
                                'tip': 'satis', 'nft_no': nft_no,
                                'gonderen': satici, 'alan': st.session_state.kullanici,
                                'fiyat': b['fiyat'], 'zaman': str(datetime.datetime.now())
                            })
                            veri_kaydet(veri)
                            st.success("✅ Satın alındı!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Bakiye yetersiz!")
                else:
                    if st.button("❌ İptal", key=f"pazar_iptal_{nft_no}", use_container_width=True):
                        b['satista'] = False
                        veri['pazar'].remove(nft_no)
                        veri_kaydet(veri)
                        st.rerun()
                st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# BLOCKCHAIN KAYITLARI
elif sayfa == "Blockchain":
    st.markdown("<h2>📋 Blockchain Kayıtları</h2>", unsafe_allow_html=True)
    if not veri['bloklar']:
        st.info("Henüz blok yok.")
    else:
        st.caption(f"Toplam {len(veri['bloklar'])} blok | Son hash: `{veri['bloklar'][-1]['blok_hash'][:24]}...`")
        for b in reversed(veri['bloklar']):
            with st.expander(f"Blok #{b['numara']} — {b['isim']}"):
                c1b, c2b = st.columns([1, 2])
                with c1b:
                    if b.get('resim_veri'):
                        st.image(base64.b64decode(b['resim_veri']), width=180)
                with c2b:
                    st.write(f"**Sahip:** {b['sahip']} | **Tarih:** {b['zaman'][:19]} | **Fiyat:** {b['fiyat']} TL")
                    st.code(f"Blok Hash:  {b['blok_hash']}\nÖnceki:     {b['onceki_hash'] or 'Genesis'}\nDosya:      {b['dosya_hash']}", language=None)

# ANALİZ
elif sayfa == "Analiz":
    st.markdown("<h2>📊 Blockchain Analizi</h2>", unsafe_allow_html=True)
    st.markdown("""<div style='background:linear-gradient(135deg,#1f2937,#374151);border-radius:12px;padding:16px 20px;margin-bottom:18px'>
<b style='color:#a78bfa;font-size:15px'>🔗 Blockchain Nasıl Çalışır?</b>
<p style='color:#d1d5db;font-size:13px;margin:6px 0 0'>Her NFT bir blok oluşturur. Blok; sahip, dosya hash'i ve önceki bloğun imzasını içerir. Bu zincir hiç değiştirilemez.</p></div>""", unsafe_allow_html=True)
    fig = blockchain_gorseli(veri['bloklar'])
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=140, bbox_inches='tight')
    buf.seek(0)
    st.image(Image.open(buf), use_container_width=True)
    buf.seek(0)
    st.download_button("📥 Görseli İndir", buf, "blockchain.png", "image/png")
    plt.close(fig)
    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("⛓️ Blok", len(veri['bloklar']))
    k2.metric("📋 İşlem", len(veri['islemler']))
    k3.metric("👥 Kullanıcı", len(veri['kullanicilar']))
    k4.metric("🛒 Pazarda", len(veri['pazar']))
    if veri['bloklar']:
        st.markdown("---")
        if st.button("🔍 Hash Bütünlüğü Doğrula"):
            sorun = False
            for i, b in enumerate(veri['bloklar']):
                if i > 0 and b['onceki_hash'] != veri['bloklar'][i - 1]['blok_hash']:
                    st.error(f"Blok #{b['numara']} uyumsuz!")
                    sorun = True
            if not sorun:
                st.markdown("<div style='background:#eafaf1;border:2px solid #27ae60;border-radius:10px;padding:14px;text-align:center'><b style='color:#1e8449;font-size:16px'>✅ Zincir Sağlam!</b></div>", unsafe_allow_html=True)

# PROFİL
elif sayfa == "Profil":
    st.markdown("<h2>👤 Profil</h2>", unsafe_allow_html=True)
    p1, p2 = st.columns([1, 2])
    with p1:
        st.markdown(f"<div style='background:linear-gradient(135deg,{c1},{c2});border-radius:50%;width:80px;height:80px;display:flex;align-items:center;justify-content:center;font-size:36px;margin:0 auto'>👤</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center'>{st.session_state.kullanici}</h3>", unsafe_allow_html=True)
        st.caption(f"Üye: {aktif['kayit_tarihi'][:10]}")
    with p2:
        st.metric("💰 Bakiye", f"{aktif['para']} TL")
        st.metric("🖼️ NFT", len(aktif['nftler']))
        st.markdown("---")
        ekle = st.number_input("Bakiye Ekle (TL)", min_value=0, value=500, step=50)
        if st.button("💳 Ekle"):
            aktif['para'] += ekle
            veri_kaydet(veri)
            st.success(f"{ekle} TL eklendi!")
            st.rerun()
        st.markdown("---")
        st.markdown("**📋 Son İşlemler**")
        islemler = [i for i in veri['islemler'] if i.get('gonderen') == st.session_state.kullanici or i.get('alan') == st.session_state.kullanici]
        if not islemler:
            st.info("Henüz işlem yok.")
        else:
            for i in reversed(islemler[-8:]):
                ikon = {'mint': '🌱', 'transfer': '🔄', 'satis': '💸'}.get(i['tip'], '📋')
                st.write(f"{ikon} **{i['tip'].upper()}** — NFT #{i['nft_no']} — {i['zaman'][:16]}")

st.markdown("---")
st.caption("ArtGuard AI | TÜBİTAK 4006 Projesi")
