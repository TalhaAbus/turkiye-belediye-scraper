# -*- coding: utf-8 -*-
"""Wikipedia 2024 yerel seçim sayfalarından belediye başkanlarını çeker.

Her il için '[İl]'da/de 2024 Türkiye yerel seçimleri' sayfası ana seçim
makalesinden toplanır; İl/Büyükşehir başkanı ile ilçe başkanları (kazanan aday)
ayıklanır. Sonuç (il, ilçe) -> (başkan, parti) sözlüğü olarak döner.
"""

import pickle
import re
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from turkiye_data import PROVINCES, normalize

# Wikipedia il adını (örn. "Hakkâri") kendi veri anahtarımıza eşler ("Hakkari")
_NORM2KEY = {normalize(k): k for k in PROVINCES}


def canonical_il(il):
    return _NORM2KEY.get(normalize(il), il)


# Kendi ilçe adımız -> Wikipedia'daki farklı başlık (il-özel)
ILCE_ALIAS = {
    ("Samsun", "Ondokuzmayıs"): "19 Mayıs",
    ("Zonguldak", "Ereğli"): "Karadeniz Ereğli",
}

MAIN_URL = "https://tr.wikipedia.org/wiki/2024_T%C3%BCrkiye_yerel_se%C3%A7imleri"
CACHE = "baskanlar.pkl"
HDRS = {"User-Agent": "Mozilla/5.0 (compatible; BelediyeScraper/1.0)"}


def _get(url):
    req = urllib.request.Request(url, headers=HDRS)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")


def province_urls():
    """Ana makaleden 81 il seçim sayfasının URL'lerini toplar."""
    soup = BeautifulSoup(_get(MAIN_URL), "html.parser")
    out = {}
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if not h.startswith("/wiki/") or "yerel_se" not in h:
            continue
        title = urllib.parse.unquote(h.split("/wiki/")[1])
        if "'" in title and title.endswith("2024_Türkiye_yerel_seçimleri"):
            il = title.split("'")[0].replace("_", " ")
            out.setdefault(il, "https://tr.wikipedia.org" + h)
    return out


def _winner(table):
    """Bir sonuç tablosundan kazanan adayı (başkan) ve partisini ayıklar."""
    rows = table.find_all("tr")
    hi = None
    for i, tr in enumerate(rows):
        t = tr.get_text(" ", strip=True).lower()
        if "aday" in t and ("oy say" in t or "oy oran" in t):
            hi = i
            break
    if hi is None:
        return None
    for tr in rows[hi + 1:]:
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        cells = [c for c in cells if c]
        vi = next((j for j, c in enumerate(cells)
                   if re.fullmatch(r"\d[\d.]*", c)), None)
        if vi is None or vi < 1:
            continue
        name = cells[vi - 1]
        party = ""
        for c in cells[:vi - 1]:
            if "partisi" in c.lower():        # tam parti adını atla
                continue
            party = c                          # kısaltma (CHP, AK Parti...)
        if not party:
            party = cells[0]
        if re.search(r"[A-Za-zÇĞİÖŞÜçğıöşü]", name) and "parti" not in name.lower():
            return clean(name), clean(party)
    return None


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"\[.*?\]", "", s)).strip()


HARD_STOPS = ("İlçeler", "Kaynakça", "Dış bağlantılar", "Ayrıca bakınız",
              "Merkez beldeleri")


def _winner_after(htag, stop_at_heading=False):
    """Bir başlıktan sonraki ilk sonuç tablosunun kazananını döndürür.

    stop_at_heading=True (ilçe için): bir sonraki h1/h2/h3'te durur (komşu
    ilçeye taşmamak için), ama h4 'beldeleri' alt başlıklarını atlar.
    False (İl/BŞ için): ara alt başlıkları geçer, yalnızca HARD_STOPS'ta durur.
    """
    node = htag
    while True:
        node = node.find_next()
        if node is None:
            return None
        if node.name in ("h1", "h2", "h3", "h4"):
            t = node.get_text().strip()
            if t in HARD_STOPS:
                return None
            if stop_at_heading and node.name in ("h1", "h2", "h3"):
                return None
        if node.name == "table":
            w = _winner(node)
            if w:
                return w


def parse_province(html, il):
    """Tek il sayfasından (il,ilçe)->(başkan,parti) eşlemesi üretir."""
    il = canonical_il(il)            # "Hakkâri" -> "Hakkari"
    soup = BeautifulSoup(html, "html.parser")
    res = {}

    # İl / Büyükşehir başkanı: 'Belediyesi' ile biten ilk başlık (h1/h2/h3)
    for h in soup.find_all(["h1", "h2", "h3"]):
        if h.get_text().strip().endswith("Belediyesi"):
            w = _winner_after(h)
            if w:
                res[(il, "")] = w
            break

    # İlçe başkanları: h3 başlıklarını ilçe adına göre eşle
    h3map = {normalize(h.get_text().strip()): h for h in soup.find_all("h3")}
    for ilce in PROVINCES.get(il, []):
        if ilce == "Merkez":
            continue
        node = h3map.get(normalize(ilce))
        if node is None and (il, ilce) in ILCE_ALIAS:
            node = h3map.get(normalize(ILCE_ALIAS[(il, ilce)]))
        if node:
            w = _winner_after(node, stop_at_heading=True)
            if w:
                res[(il, ilce)] = w
    return res


def build(limit=None, verbose=True):
    urls = province_urls()
    items = list(urls.items())
    if limit:
        items = items[:limit]
    mapping = {}
    for n, (il, url) in enumerate(items, 1):
        try:
            mapping.update(parse_province(_get(url), il))
            if verbose:
                got = sum(1 for k in mapping if k[0] == il)
                print(f"[{n}/{len(items)}] {il}: {got} başkan", flush=True)
        except Exception as e:
            print(f"[{n}/{len(items)}] {il}: HATA {e}", flush=True)
        time.sleep(0.3)
    with open(CACHE, "wb") as f:
        pickle.dump(mapping, f)
    print(f"\nToplam {len(mapping)} başkan -> {CACHE}", flush=True)
    return mapping


def load():
    try:
        with open(CACHE, "rb") as f:
            return pickle.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    import sys
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    build(lim)
