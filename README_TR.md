# 🎨 ArtGuard AI - Blockchain + Yapay Zeka ile Dijital Sanat Koruma

TÜBİTAK 4006 Bilim Fuarı Projesi - Blockchain ve Yapay Zeka ile Dijital Sanat Telif Hakkı Koruması

## 🌟 Özellikler

- **Blockchain Teknolojisi:** Değiştirilemez eser kaydı ve sahiplik takibi
- **Yapay Zeka Tespiti:** Görsel benzerlikleri algılayan perceptual hashing (%80+ benzerlik = uyarı)
- **Kopya Tespiti:** SHA256 hash doğrulama ile tekrar kayıt engelleme
- **QR Sertifika:** Her eser için QR kodlu blockchain sertifikası
- **Akıllı Transferler:** %10 telif ücreti simülasyonuyla sahiplik transferi
- **İki Dilli:** Tam Türkçe ve İngilizce destek
- **İstatistik Paneli:** Canlı metrikler ve analizler

## 🚀 Hızlı Başlangıç

### Bilgisayarınızda Çalıştırma

```bash
# Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# Uygulamayı başlat
streamlit run artguard_ai.py
```

Tarayıcıda açılır: `http://localhost:8501`

### Canlı Demo

🌐 **[Buradan deneyin!](https://artguard-ai.streamlit.app)**

## 📦 Gereksinimler

- Python 3.8+
- streamlit
- imagehash
- pillow
- qrcode

## 🎯 Nasıl Çalışır?

1. **Eser Yükle:** Herhangi bir dijital dosya (resim, PDF, MP3, vs.)
2. **Hash Hesaplama:** Sistem SHA256 hash ile tam kopya tespiti yapar
3. **AI Analizi:** Resimler için perceptual hash ile görsel benzerlik tespit eder
4. **Blockchain'e Kaydet:** Eser sahibi bilgisi ve telif beyanıyla kayıt
5. **Sertifika Al:** QR kodlu sahiplik kanıtı olarak sertifika indir
6. **Transfer:** Yeni sahibine otomatik telif takibiyle transfer et

## 🔒 Güvenlik Özellikleri

- Kriptografik hashing (SHA256)
- AI tabanlı benzerlik tespiti için perceptual hashing
- Değiştirilemez blockchain yapısı
- Zaman damgası doğrulama

## 📊 Teknoloji

- **Arayüz:** Streamlit
- **Blockchain:** Basit liste tabanlı zincir (eğitim amaçlı)
- **Yapay Zeka:** Perceptual hashing için ImageHash kütüphanesi
- **Kriptografi:** SHA256 hashing
- **QR Kod:** Python QRCode kütüphanesi

## 🎓 Eğitim Amacı

Bu proje şunları gösterir:
- Blockchain temelleri
- Görsel benzerlik için AI kullanımı
- Telif hakkı koruma mekanizmaları
- Web uygulaması geliştirme

**Not:** Bu TÜBİTAK 4006 için eğitim projesidir. Gerçek üretim ortamında Ethereum veya Solana gibi kurulu blockchain platformları kullanılmalıdır.

## 👨‍🎓 Geliştiriciler

Yağız Günay/Efe Çelik Lise Öğrencisi - TÜBİTAK 4006 Bilim Fuarı Projesi 2026

## 📄 Lisans

Eğitim Projesi - Tüm Hakları Saklıdır

## 🙏 Teşekkürler

- TÜBİTAK 4006 Bilim Fuarı Programı
- Danışman öğretmenime destekleri için

---
## 📞 İletişim

Sorularınız için: +90 530 152 50 21/+90 505 806 14 17
                  yyagizgunay@gmail.com

## 🏆 Nasıl Katkıda Bulunulur?

Bu eğitim projesidir, ancak önerileriniz için İletişim bölümünü kullanabilirsiniz!

## ⚡ Hızlı Linkler

- [https://artguardai.streamlit.app/]
- [Proje Raporu](#) *(ekle)*
