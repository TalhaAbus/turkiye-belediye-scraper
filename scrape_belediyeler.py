# -*- coding: utf-8 -*-
"""Kademeli iletişim sayfası bulma + veri kazıma (Playwright, async)."""

import asyncio
import pickle
import random
import re
import sys
import threading
from urllib.parse import urlparse

import pandas as pd
from playwright.async_api import async_playwright

from turkiye_data import build_rows

OUTPUT = "sıfırdan_belediyeler_veritabanı.xlsx"
CONCURRENCY = 8
NAV_TIMEOUT = 18000          # ms
DYN_WAIT = 2.0               # dinamik içerik bekleme (sn)
ILETISIM_PATHS = ["/iletisim", "/iletisim/", "/iletisim.html",
                  "/iletisim.aspx", "/bize-ulasin", "/iletisim-bilgileri"]
LINK_KEYWORDS = ["iletişim bilgileri", "iletişime geç", "bize ulaşın",
                 "iletişim", "künye"]
# ASCII katlanmış (Türkçe büyük-İ sorununu önlemek için JS tarafında kullanılır)
LINK_KEYWORDS_ASCII = ["iletisim bilgileri", "iletisime gec", "bize ulasin",
                       "iletisime", "iletisim", "kunye"]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(?:\+?90[\s\-]?)?\(?0?\d{3}\)?[\s\-./]?\d{3}[\s\-./]?\d{2}[\s\-./]?\d{2}")

# Türkçe karakterleri ASCII'ye katlayıp küçük harfe çevirir (eşleştirme için).
_FOLD = str.maketrans({
    "İ": "i", "I": "i", "ı": "i", "Ş": "s", "ş": "s", "Ğ": "g", "ğ": "g",
    "Ü": "u", "ü": "u", "Ö": "o", "ö": "o", "Ç": "c", "ç": "c"})


def fold(s: str) -> str:
    return s.translate(_FOLD).lower()


# Adres bileşenleri (katlanmış metin üzerinde aranır)
MAH_RE = re.compile(r"\bmah(?:alle(?:si)?|\.)?\b|\bkoyu\b|\bbeldesi\b")
STREET_RE = re.compile(
    r"\b(?:cad(?:de(?:si)?|\.)?|cd\.|sok(?:ak|agi|\.)?|sk\.|"
    r"bulvar[i]?|blv\.?|mevki[i]?|meydan[i]?|kume\s?evler)\b")
NO_RE = re.compile(r"\bno[:.\s]?\s*\d")
POSTAL_RE = re.compile(r"\b\d{5}\b")
# Adresin bittiği yeri işaretleyen anahtar kelimeler (Türkçe varyantlı)
ADDR_STOP_RE = re.compile(
    r"(telefon|tel\.|tel\s*:|\btel\b|faks|fax|santral|pbx|"
    r"çağr[ıi]|cagr[ıi]|e[\-\s]?posta|eposta|e[\-\s]?mail|\bma[iİ]l\b|"
    r"gönder|gonder|harita|google|whatsapp|başkan|baskan|©|copyright|"
    r"her\s+hakk|tıkla|tikla|ulaşın|ulasin)", re.IGNORECASE)
# Belediyeye ait olmayan adresleri (yazılım firması/ihale ilanı vb.) eler
ADDR_NEG_RE = re.compile(
    r"teknokent|teknopark|ar-?ge\b|yazil[ıi]m|bilis[ıi]m|hacettepe|ostim|"
    r"\bltd\b|\ba\.?s\.?\b|san\.?\s*tic|ihale|ilan|parsel|\bada\b", re.I)

# 444'lü çağrı merkezi / vanity numaraları (örn. "444 03 01", "444 9 024")
PHONE444_RE = re.compile(r"\b444[\s\-/]?\d[\s\-/]?\d{1,2}[\s\-/]?\d{0,2}\b")
# Numara etiketleri — katlanmış (ASCII) metin üzerinde aranır
TEL_LABEL_RE = re.compile(r"telefon|telephone|\btel\b|tel[.:]|\bphone\b")
FAX_LABEL_RE = re.compile(r"faks|fax|belgegec|whatsapp|\bwp\b|\bkep\b|ihbar")
SOFT_LABEL_RE = re.compile(
    r"santral|power\s*plant|cagri|engelli|barrier|\bmobil\b|\bgsm\b|\bcep\b|"
    r"destek")

_lock = threading.Lock()
_state = {"done": 0, "ok": 0}
results = {}


# ----------------------------- yardımcılar -----------------------------------
def clean_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_phone(raw: str):
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("90") and len(digits) == 12:
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if len(digits) != 10:
        return None
    if digits[0] not in "2345":          # geçerli alan/operatör kodu
        return None
    return f"0{digits[0:3]} {digits[3:6]} {digits[6:8]} {digits[8:10]}"


def normalize_call_center(raw: str):
    """444'lü çağrı merkezi numarasını sade biçimde döndürür (örn. 444 0 301)."""
    digits = re.sub(r"\D", "", raw)
    if not digits.startswith("444") or not (6 <= len(digits) <= 8):
        return None
    return clean_ws(raw.replace("-", " ").replace("/", " "))


def _label_class(context_folded: str) -> str:
    """Numaranın hemen öncesindeki en yakın etikete göre sınıf döndürür."""
    best_pos, cls = -1, "neutral"
    for rx, name in ((TEL_LABEL_RE, "tel"), (FAX_LABEL_RE, "bad"),
                     (SOFT_LABEL_RE, "soft")):
        for m in rx.finditer(context_folded):
            if m.start() > best_pos:    # numaraya en yakın (son) etiket kazanır
                best_pos, cls = m.start(), name
    return cls


def extract_phone(text: str):
    """Numaraları etiketlerine göre seçer: önce 'Telefon', asla Faks/WhatsApp."""
    cands = []   # (pozisyon, normalize, sınıf)
    for m in PHONE_RE.finditer(text):
        norm = normalize_phone(m.group())
        if norm:
            cands.append((m.start(), norm))
    for m in PHONE444_RE.finditer(text):
        prev = text[max(0, m.start() - 4):m.start()]
        if re.search(r"\d\s*$", prev):    # daha uzun bir numaranın parçası
            continue
        norm = normalize_call_center(m.group())
        if norm:
            cands.append((m.start(), norm))
    if not cands:
        return None
    cands.sort()
    classified = [(_label_class(fold(text[max(0, p - 45):p])), n)
                  for p, n in cands]
    # Öncelik: Telefon etiketli > etiketsiz > yumuşak (santral/cep);
    # yalnızca Faks/WhatsApp varsa boş bırak (yanlış numara yazma).
    for target in ("tel", "neutral", "soft"):
        for cls, n in classified:
            if cls == target:
                return n
    return None


def extract_email(text: str, domain: str):
    emails = [e for e in EMAIL_RE.findall(text)
              if not re.search(r"\.(png|jpg|jpeg|gif|svg|webp)$", e, re.I)]
    if not emails:
        return None
    base = domain.replace("www.", "")
    # 1) site domainiyle birebir, 2) bel.tr uzantılı, 3) ilki
    for e in emails:
        if base in e.lower():
            return e.lower()
    for e in emails:
        if "bel.tr" in e.lower():
            return e.lower()
    return emails[0].lower()


def _clean_addr(s: str) -> str:
    """Aday adres metnini temizler: e-posta/telefon/çöp son ekleri atılır."""
    s = clean_ws(s)
    s = EMAIL_RE.sub("", s)
    # baştaki "Adres" etiketini at
    s = re.sub(r"^\s*adres(?:imiz|i)?\s*[:\-]?\s*", "", s, flags=re.IGNORECASE)
    m = ADDR_STOP_RE.search(s)
    if m:
        s = s[:m.start()]
    # sondaki telefon benzeri rakam kümelerini at
    s = re.sub(r"[\(\+]?\d[\d\s\-/()]{8,}$", "", s)
    s = clean_ws(s).strip(" -–—|/•,:;.")
    return s


def _addr_score(cand: str, il: str, ilce: str) -> int:
    f = fold(cand)
    score = 0
    if MAH_RE.search(f):
        score += 2
    if STREET_RE.search(f):
        score += 2
    if NO_RE.search(f):
        score += 2
    if POSTAL_RE.search(f):
        score += 1
    if il and fold(il) in f:
        score += 2
    if ilce and fold(ilce) in f:
        score += 1
    if "@" in cand or "http" in f or "©" in cand:
        score -= 4
    if ADDR_NEG_RE.search(cand):        # yazılım firması / ihale ilanı vb.
        score -= 5
    return score


def extract_address(text: str, il: str = "", ilce: str = ""):
    """Adres yapısını puanlayarak en olası adres satırını seçer."""
    raw_lines = [clean_ws(l) for l in text.splitlines()]
    raw_lines = [l for l in raw_lines if l]

    candidates = []
    # 1) "Adres[imiz/i]:" etiketini izleyen metin
    for m in re.finditer(r"adres(?:imiz|i)?\s*[:\-]\s*", text, re.IGNORECASE):
        candidates.append(text[m.end():m.end() + 200])
    # 2) tek tek satırlar
    for l in raw_lines:
        if 12 <= len(l) <= 200:
            candidates.append(l)
    # 3) ardışık satır çiftleri (adres iki satıra bölünmüşse)
    for i in range(len(raw_lines) - 1):
        joined = raw_lines[i] + " " + raw_lines[i + 1]
        if 18 <= len(joined) <= 200 and MAH_RE.search(fold(raw_lines[i])):
            candidates.append(joined)

    best, best_score = None, 0
    for cand in candidates:
        cleaned = _clean_addr(cand)
        if not (12 <= len(cleaned) <= 180):
            continue
        sc = _addr_score(cleaned, il, ilce)
        if sc > best_score:
            best, best_score = cleaned, sc
    # Gerçek adres için en az: (mahalle/sokak) + (no/posta/il) ~ skor>=4
    if best and best_score >= 4:
        return best
    return None


def has_contact(text: str, domain: str, il: str = "", ilce: str = ""):
    return bool(extract_phone(text) or extract_email(text, domain)
                or extract_address(text, il, ilce))


# ----------------------------- tarayıcı işleri -------------------------------
async def page_text(page):
    try:
        return await page.inner_text("body")
    except Exception:
        try:
            return await page.evaluate("() => document.body.innerText")
        except Exception:
            return ""


async def try_goto(page, url):
    try:
        resp = await page.goto(url, wait_until="domcontentloaded",
                               timeout=NAV_TIMEOUT)
        await asyncio.sleep(DYN_WAIT)
        return resp
    except Exception:
        return None


async def resolve_live(page, candidates):
    """İlk açılabilen domaini bulur; yönlenmelerden sonraki nihai origin'i
    (örn. www. ekli / https) ve ana sayfa metnini döndürür."""
    for cand in candidates:
        for host in (cand, "www." + cand):
            for scheme in ("https", "http"):
                resp = await try_goto(page, f"{scheme}://{host}/")
                if resp is None:
                    continue
                if resp.status < 400:
                    txt = await page_text(page)
                    if len(txt) > 40:
                        u = urlparse(page.url)
                        origin = f"{u.scheme}://{u.netloc}"
                        return origin, txt
    return None, None


async def find_contact_via_home(page, base_url):
    """Ana sayfadaki İletişim/Bize Ulaşın linkini bulup ona yönlenir.
    Türkçe büyük harf (İ) sorununu önlemek için ASCII katlama yapar."""
    try:
        await page.mouse.wheel(0, 4000)   # tembel yüklenen footer'ı tetikle
        await asyncio.sleep(0.8)
    except Exception:
        pass
    href = await page.evaluate(
        """(keywords) => {
            const fold = (s) => s
                .replace(/[İIı]/g,'i').replace(/[Şş]/g,'s').replace(/[Ğğ]/g,'g')
                .replace(/[Üü]/g,'u').replace(/[Öö]/g,'o').replace(/[Çç]/g,'c')
                .toLowerCase();
            const els = Array.from(document.querySelectorAll('a'));
            for (const kw of keywords) {
                for (const el of els) {
                    const t = fold((el.textContent || '').trim());
                    const title = fold(el.getAttribute('title') || '');
                    if (el.href && ((t && t.length < 40 && t.includes(kw))
                                    || title.includes(kw))) {
                        return el.href;
                    }
                }
            }
            // href'inde iletisim geçen linkler
            for (const el of els) {
                if (el.href && /iletisim|bize-?ulas|iletisim-bilgileri/i
                        .test(fold(el.href))) return el.href;
            }
            return null;
        }""", LINK_KEYWORDS_ASCII)
    if href:
        resp = await try_goto(page, href)
        if resp and resp.status < 400:
            return await page_text(page)
    return None


def _completeness(rec):
    """Adres en değerli alan; sonra telefon ve e-posta."""
    if rec is None:
        return -1
    return (2 if rec["Adres"] else 0) + (1 if rec["Telefon"] else 0) \
        + (1 if rec["E-posta"] else 0)


async def scrape_one(page, row):
    candidates = row["domain_candidates"]
    base, home_txt = await resolve_live(page, candidates)
    if not base:
        return None
    live = urlparse(base).netloc.replace("www.", "")
    best = None

    def consider(text, source):
        nonlocal best
        if not text or not has_contact(text, live, row["il"], row["ilce"]):
            return
        rec = build_record(row, text, live, source)
        if _completeness(rec) > _completeness(best):
            best = rec

    # AŞAMA 2 - 1. Adım: doğrudan iletişim linkleri
    for path in ILETISIM_PATHS:
        resp = await try_goto(page, base + path)
        if resp and resp.status < 400:
            consider(await page_text(page), base + path)
            if best and best["Adres"]:        # tam adres bulundu, yeter
                return best

    # AŞAMA 2 - 2. Adım: ana sayfadan İletişim butonuna tıklama (fallback)
    await try_goto(page, base + "/")
    consider(await find_contact_via_home(page, base), base + " (buton)")
    if best and best["Adres"]:
        return best

    # Son çare: ana sayfa footer'ındaki iletişim verisi
    consider(home_txt, base + " (anasayfa)")
    return best


def build_record(row, text, domain, source):
    rec = {
        "İl": row["il"],
        "İlçe": row["ilce"],
        "Belediye Türü": row["tur"],
        "Belediye Adı": (row["il"] + " Büyükşehir Belediyesi") if row["tur"] == "Büyükşehir"
                        else (row["il"] + " Belediyesi") if row["tur"] == "İl"
                        else (row["ilce"] + " Belediyesi"),
        "Web Sitesi": "https://" + domain,
        "Adres": extract_address(text, row["il"], row["ilce"]) or "",
        "Telefon": extract_phone(text) or "",
        "E-posta": extract_email(text, domain) or "",
        "Kaynak": source,
    }
    rec["_raw"] = text          # ham metin önbelleği (yeniden ayıklama için)
    return rec


COLUMNS = ["İl", "İlçe", "Belediye Türü", "Belediye Adı", "Web Sitesi",
           "Adres", "Telefon", "E-posta", "Kaynak"]
RAW_CACHE = "raw_pages.pkl"


def checkpoint():
    rows = [results[i] for i in sorted(results)]
    if not rows:
        return
    df = pd.DataFrame(rows)[COLUMNS]
    df.to_excel(OUTPUT, index=False)
    # ham metinleri ayrı sakla (yeniden ayıklama için; xlsx'e yazılmaz)
    raw = {i: {"il": results[i]["İl"], "ilce": results[i]["İlçe"],
               "tur": results[i]["Belediye Türü"],
               "domain": results[i]["Web Sitesi"].replace("https://", ""),
               "source": results[i]["Kaynak"], "text": results[i].get("_raw", "")}
           for i in results}
    try:
        with open(RAW_CACHE, "wb") as f:
            pickle.dump(raw, f)
    except Exception:
        pass


def reextract():
    """Ham önbellekten (raw_pages.pkl) xlsx'i yeniden üretir — tarama yok."""
    with open(RAW_CACHE, "rb") as f:
        raw = pickle.load(f)
    rows = []
    for i in sorted(raw):
        d = raw[i]
        text, domain = d["text"], d["domain"]
        tur = d["tur"]
        ad = (d["il"] + " Büyükşehir Belediyesi") if tur == "Büyükşehir" \
            else (d["il"] + " Belediyesi") if tur == "İl" \
            else (d["ilce"] + " Belediyesi")
        rows.append({
            "İl": d["il"], "İlçe": d["ilce"], "Belediye Türü": tur,
            "Belediye Adı": ad, "Web Sitesi": "https://" + domain,
            "Adres": extract_address(text, d["il"], d["ilce"]) or "",
            "Telefon": extract_phone(text) or "",
            "E-posta": extract_email(text, domain) or "",
            "Kaynak": d["source"]})
    pd.DataFrame(rows)[COLUMNS].to_excel(OUTPUT, index=False)
    full = sum(1 for r in rows if r["Adres"])
    print(f"Yeniden ayıklandı: {len(rows)} kayıt, {full} adres dolu -> {OUTPUT}")


# ----------------------------- iş kuyruğu ------------------------------------
async def worker(context, queue, total):
    page = await context.new_page()
    await page.set_extra_http_headers({"Accept-Language": "tr-TR,tr;q=0.9"})
    while True:
        try:
            idx, row = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        rec = None
        try:
            rec = await asyncio.wait_for(scrape_one(page, row), timeout=120)
        except Exception:
            rec = None
        with _lock:
            _state["done"] += 1
            if rec:
                _state["ok"] += 1
                results[idx] = rec
                if _state["ok"] % 10 == 0:
                    checkpoint()
            d, ok = _state["done"], _state["ok"]
        label = row["ilce"] or row["il"]
        print(f"[{d}/{total}] ok={ok} {row['il']}/{label} "
              f"-> {'✓' if rec else '—'}", flush=True)
        await asyncio.sleep(random.uniform(1.5, 3.5))
    await page.close()


async def main():
    rows = build_rows()
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        rows = rows[:limit]
    total = len(rows)
    print(f"Başlıyor: {total} belediye, eşzamanlılık={CONCURRENCY}", flush=True)

    queue = asyncio.Queue()
    for i, r in enumerate(rows):
        queue.put_nowait((i, r))

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage",
                  "--disable-blink-features=AutomationControlled"])
        contexts = []
        for _ in range(CONCURRENCY):
            ctx = await browser.new_context(
                user_agent=UA, ignore_https_errors=True,
                viewport={"width": 1366, "height": 768})
            ctx.set_default_navigation_timeout(NAV_TIMEOUT)
            contexts.append(ctx)
        await asyncio.gather(*[worker(c, queue, total) for c in contexts])
        for c in contexts:
            await c.close()
        await browser.close()

    checkpoint()
    print(f"\nTAMAMLANDI. Toplam {_state['done']} denendi, "
          f"{_state['ok']} kayıt yazıldı -> {OUTPUT}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "reextract":
        reextract()
    else:
        asyncio.run(main())
