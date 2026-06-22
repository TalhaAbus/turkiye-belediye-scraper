# 🇹🇷 Türkiye Belediye İletişim Scraper

Türkiye'deki **tüm Büyükşehir, İl ve İlçe belediyelerinin** güncel iletişim
bilgilerini (adres, telefon, e-posta) otomatik olarak toplayan bir Playwright
botu. Belediye web sitelerini kademeli bir algoritmayla gezer, iletişim
sayfasını akıllıca bulur ve sonuçları temiz bir Excel tablosuna yazar.

> **Not:** Bu araç yalnızca kamuya açık kurumsal iletişim bilgilerini derler.
> Sunuculara saygılı davranır (istekler arası rastgele gecikme, makul
> eşzamanlılık). Lütfen [Yasal Uyarı](#-yasal-uyarı) bölümünü okuyun.

---

## ✨ Özellikler

- **1003 belediye** başlangıç matrisi: 30 Büyükşehir + 51 İl + 922 İlçe.
- **Belediye başkanı + parti:** 2024 yerel seçim sonuçlarından (Wikipedia) her
  belediyenin güncel başkanı ve partisi otomatik eklenir (1003/1003).
- **Hiçbir belediye atlanmaz:** iletişim sayfasına ulaşılamayan belediyeler bile
  ad + başkan bilgisiyle tabloda yer alır (çıktıda her zaman 1003 satır).
- **Kademeli iletişim sayfası bulma:** önce `/iletisim` türevleri, bulunamazsa
  ana sayfadaki "İletişim / Bize Ulaşın" bağlantısını bulup tıklama (fallback).
- **Akıllı domain çözümü:** Türkçe karakter sadeleştirme, `www`/`belediyesi`
  varyantları, aynı isimli ilçe çakışmaları ve yönlendirme takibi.
- **Etikete duyarlı telefon ayıklama:** "Telefon" etiketli numarayı seçer;
  **Faks / WhatsApp / KEP** numaralarını asla almaz. `444`'lü çağrı merkezi
  numaralarını da destekler.
- **Puanlamalı adres ayıklama:** mahalle + cadde/sokak + no + il/posta kodu
  yapısını puanlayarak gerçek adresi seçer; yazılım firması/ihale ilanı gibi
  çöp metinleri eler.
- **Telefon normalleştirme:** tüm formatları `0XXX XXX XX XX` standardına çevirir.
- **Dayanıklılık:** 8 paralel sekme, her 10 kayıtta otomatik Excel kaydı,
  istekler arası 1.5–3.5 sn rastgele gecikme.
- **Ham metin önbelleği:** ayıklama mantığını değiştirince yeniden tarama
  yapmadan saniyeler içinde tabloyu yeniden üretebilirsiniz (`reextract`).

---

## 🧠 Nasıl Çalışır (Algoritma)

**AŞAMA 1 — Başlangıç Veri Matrisi**
81 il, 30 Büyükşehir ve ~922 ilçe için `[ad].bel.tr` formatında aday alan adları
üretilir (Türkçe karakter sadeleştirme + çakışma/özel domain çözümü).

**AŞAMA 2 — Kademeli İletişim Sayfası Bulma**
1. **Doğrudan link:** `https://[domain]/iletisim`, `/iletisim/`, `/iletisim.html`
   (+ `/iletisim.aspx`, `/bize-ulasin`, `/iletisim-bilgileri`) sırayla denenir.
   Sayfa açılır ve içinde adres/telefon/e-posta varsa veri kazımaya geçilir.
2. **Ana sayfa fallback:** doğrudan linkler çalışmazsa ana sayfaya gidilir,
   metni "İletişim / Bize Ulaşın / Künye" olan `<a>` bağlantısı bulunup tıklanır.
3. Hiçbir yöntem işe yaramazsa o satır **atlanır** (asla uydurma veri yazılmaz).

**AŞAMA 3 — Veri Kazıma**
- **Adres:** temizlenir, çift boşluk/satır sonu kaldırılır, çöp ekler atılır.
- **Telefon:** etikete göre seçilir, `0XXX XXX XX XX` formatına çevrilir.
- **E-posta:** öncelik kurumsal `@...bel.tr` adresinde.

**AŞAMA 4 — Kararlılık**
Her belediye geçişinde rastgele gecikme, her 10 başarılı kayıtta kademeli
Excel güncellemesi.

---

## 🚀 Kurulum

```bash
# 1) Depoyu klonla
git clone https://github.com/TalhaAbus/turkiye-belediye-scraper.git
cd turkiye-belediye-scraper

# 2) Sanal ortam oluştur ve bağımlılıkları kur
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3) Playwright tarayıcısını indir
python -m playwright install chromium
```

---

## 🛠️ Kullanım

```bash
# Tüm 1003 belediyeyi tara (~40-50 dk)
python scrape_belediyeler.py

# Hızlı test: sadece ilk N belediye
python scrape_belediyeler.py 40

# Yeniden ayıklama: tarama yapmadan, önbellekten (raw_pages.pkl) Excel'i
# yeni ayıklama mantığıyla saniyeler içinde yeniden üret
python scrape_belediyeler.py reextract
```

Çıktı: **`sıfırdan_belediyeler_veritabanı.xlsx`** (her çalıştırmada güncellenir).

İlerlemeyi izlemek için botu arka planda çalıştırıp logu takip edebilirsiniz:

```bash
nohup python -u scrape_belediyeler.py > scrape.log 2>&1 &
tail -f scrape.log
```

---

## 📊 Çıktı Formatı

| Sütun | Açıklama |
|---|---|
| İl | Belediyenin bulunduğu il |
| İlçe | İlçe adı (İl/Büyükşehir satırlarında boş) |
| Belediye Türü | `Büyükşehir` / `İl` / `İlçe` |
| Belediye Adı | Örn. "Kadıköy Belediyesi" |
| Belediye Başkanı | 2024 seçimlerinde seçilen başkan |
| Parti | Başkanın partisi (CHP, AK Parti, MHP…) |
| Web Sitesi | Çözümlenen resmi alan adı |
| Adres | Temizlenmiş kurum adresi |
| Telefon | `0XXX XXX XX XX` veya `444`'lü numara |
| E-posta | Öncelikli `@...bel.tr` |
| Kaynak | Verinin çekildiği URL / yöntem |

**Örnek sonuçlar:** 1003 satır (81/81 il); 1003 başkan, 872 telefon, 788 adres,
844 e-posta. İletişim sayfasına ulaşılamayan belediyeler de ad + başkan ile listede.

---

## ⚙️ Yapılandırma

`scrape_belediyeler.py` başındaki sabitlerle ayarlanır:

| Sabit | Varsayılan | Açıklama |
|---|---|---|
| `CONCURRENCY` | `8` | Paralel tarayıcı sekmesi sayısı |
| `DYN_WAIT` | `2.0` | Dinamik içerik için bekleme (sn) |
| `NAV_TIMEOUT` | `18000` | Sayfa yükleme zaman aşımı (ms) |
| `ILETISIM_PATHS` | liste | Denenecek iletişim sayfası yolları |

Tarayıcıyı **görmek** için `chromium.launch(headless=True ...)` satırını
`headless=False` yapın (botun sayfaları gezişini canlı izlersiniz).

---

## 📁 Proje Yapısı

```
turkiye-belediye-scraper/
├── scrape_belediyeler.py     # Ana bot (Playwright + ayıklama mantığı)
├── turkiye_data.py           # 81 il / 922 ilçe veri matrisi + domain üretimi
├── wiki_baskanlar.py         # Wikipedia 2024 seçimlerinden başkan/parti çekme
├── requirements.txt          # Python bağımlılıkları
├── sıfırdan_belediyeler_veritabanı.xlsx  # Üretilen veritabanı (örnek çıktı)
├── raw_pages.pkl             # Ham sayfa metni önbelleği (reextract için)
├── baskanlar.pkl             # Başkan/parti önbelleği
└── README.md
```

> **Başkan verisi:** İlk çalıştırmada `baskanlar.pkl` yoksa bot, başkanları
> otomatik olarak Wikipedia'dan çeker. Dilersen elle de oluşturabilirsin:
> `python wiki_baskanlar.py`

---

## ⚖️ Yasal Uyarı

Bu proje eğitim ve kamu yararı amaçlıdır. Yalnızca belediyelerin web
sitelerinde **kamuya açık** olarak yayımladığı kurumsal iletişim bilgilerini
derler. Bot, sunuculara aşırı yük bindirmemek için istekler arasında rastgele
gecikme kullanır ve makul bir eşzamanlılıkla çalışır. Veriyi kullanırken ilgili
sitelerin kullanım koşullarına ve yürürlükteki mevzuata (ör. KVKK) uymak
kullanıcının sorumluluğundadır. Toplanan bilgiler zamanla değişebilir.

## 📄 Lisans

MIT Lisansı — ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
