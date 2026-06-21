# -*- coding: utf-8 -*-
"""Türkiye il / ilçe / büyükşehir belediyeleri başlangıç veri matrisi."""

# 30 Büyükşehir belediyesi
BUYUKSEHIR = {
    "Adana", "Ankara", "Antalya", "Aydın", "Balıkesir", "Bursa", "Denizli",
    "Diyarbakır", "Erzurum", "Eskişehir", "Gaziantep", "Hatay", "İstanbul",
    "İzmir", "Kahramanmaraş", "Kayseri", "Kocaeli", "Konya", "Malatya",
    "Manisa", "Mardin", "Mersin", "Muğla", "Ordu", "Sakarya", "Samsun",
    "Şanlıurfa", "Tekirdağ", "Trabzon", "Van",
}

# Her il -> ilçe listesi. Büyükşehir illerinde merkez yoktur (merkez ilçeler
# listede yer alır). Büyükşehir olmayan illerde "Merkez" = İl Belediyesi.
PROVINCES = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu", "Karaisalı",
              "Karataş", "Kozan", "Pozantı", "Saimbeyli", "Sarıçam", "Seyhan",
              "Tufanbeyli", "Yumurtalık", "Yüreğir"],
    "Adıyaman": ["Merkez", "Besni", "Çelikhan", "Gerger", "Gölbaşı", "Kâhta",
                 "Samsat", "Sincik", "Tut"],
    "Afyonkarahisar": ["Merkez", "Başmakçı", "Bayat", "Bolvadin", "Çay",
                       "Çobanlar", "Dazkırı", "Dinar", "Emirdağ", "Evciler",
                       "Hocalar", "İhsaniye", "İscehisar", "Kızılören",
                       "Sandıklı", "Sinanpaşa", "Sultandağı", "Şuhut"],
    "Ağrı": ["Merkez", "Diyadin", "Doğubayazıt", "Eleşkirt", "Hamur", "Patnos",
             "Taşlıçay", "Tutak"],
    "Amasya": ["Merkez", "Göynücek", "Gümüşhacıköy", "Hamamözü", "Merzifon",
               "Suluova", "Taşova"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere",
               "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı",
               "Güdül", "Haymana", "Kahramankazan", "Kalecik", "Keçiören",
               "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar",
               "Sincan", "Şereflikoçhisar", "Yenimahalle"],
    "Antalya": ["Akseki", "Aksu", "Alanya", "Demre", "Döşemealtı", "Elmalı",
                "Finike", "Gazipaşa", "Gündoğmuş", "İbradı", "Kaş", "Kemer",
                "Kepez", "Konyaaltı", "Korkuteli", "Kumluca", "Manavgat",
                "Muratpaşa", "Serik"],
    "Artvin": ["Merkez", "Ardanuç", "Arhavi", "Borçka", "Hopa", "Kemalpaşa",
               "Murgul", "Şavşat", "Yusufeli"],
    "Aydın": ["Bozdoğan", "Buharkent", "Çine", "Didim", "Efeler", "Germencik",
              "İncirliova", "Karacasu", "Karpuzlu", "Koçarlı", "Köşk",
              "Kuşadası", "Kuyucak", "Nazilli", "Söke", "Sultanhisar",
              "Yenipazar"],
    "Balıkesir": ["Altıeylül", "Ayvalık", "Balya", "Bandırma", "Bigadiç",
                  "Burhaniye", "Dursunbey", "Edremit", "Erdek", "Gömeç",
                  "Gönen", "Havran", "İvrindi", "Karesi", "Kepsut", "Manyas",
                  "Marmara", "Savaştepe", "Sındırgı", "Susurluk"],
    "Bilecik": ["Merkez", "Bozüyük", "Gölpazarı", "İnhisar", "Osmaneli",
                "Pazaryeri", "Söğüt", "Yenipazar"],
    "Bingöl": ["Merkez", "Adaklı", "Genç", "Karlıova", "Kiğı", "Solhan",
               "Yayladere", "Yedisu"],
    "Bitlis": ["Merkez", "Adilcevaz", "Ahlat", "Güroymak", "Hizan", "Mutki",
               "Tatvan"],
    "Bolu": ["Merkez", "Dörtdivan", "Gerede", "Göynük", "Kıbrıscık", "Mengen",
             "Mudurnu", "Seben", "Yeniçağa"],
    "Burdur": ["Merkez", "Ağlasun", "Altınyayla", "Bucak", "Çavdır", "Çeltikçi",
               "Gölhisar", "Karamanlı", "Kemer", "Tefenni", "Yeşilova"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik",
              "Karacabey", "Keles", "Kestel", "Mudanya", "Mustafakemalpaşa",
              "Nilüfer", "Orhaneli", "Orhangazi", "Osmangazi", "Yenişehir",
              "Yıldırım"],
    "Çanakkale": ["Merkez", "Ayvacık", "Bayramiç", "Biga", "Bozcaada", "Çan",
                  "Eceabat", "Ezine", "Gelibolu", "Gökçeada", "Lapseki",
                  "Yenice"],
    "Çankırı": ["Merkez", "Atkaracalar", "Bayramören", "Çerkeş", "Eldivan",
                "Ilgaz", "Kızılırmak", "Korgun", "Kurşunlu", "Orta",
                "Şabanözü", "Yapraklı"],
    "Çorum": ["Merkez", "Alaca", "Bayat", "Boğazkale", "Dodurga", "İskilip",
              "Kargı", "Laçin", "Mecitözü", "Oğuzlar", "Ortaköy", "Osmancık",
              "Sungurlu", "Uğurludağ"],
    "Denizli": ["Acıpayam", "Babadağ", "Baklan", "Bekilli", "Beyağaç",
                "Bozkurt", "Buldan", "Çal", "Çameli", "Çardak", "Çivril",
                "Güney", "Honaz", "Kale", "Merkezefendi", "Pamukkale",
                "Sarayköy", "Serinhisar", "Tavas"],
    "Diyarbakır": ["Bağlar", "Bismil", "Çermik", "Çınar", "Çüngüş", "Dicle",
                   "Eğil", "Ergani", "Hani", "Hazro", "Kayapınar", "Kocaköy",
                   "Kulp", "Lice", "Silvan", "Sur", "Yenişehir"],
    "Edirne": ["Merkez", "Enez", "Havsa", "İpsala", "Keşan", "Lalapaşa",
               "Meriç", "Süloğlu", "Uzunköprü"],
    "Elazığ": ["Merkez", "Ağın", "Alacakaya", "Arıcak", "Baskil", "Karakoçan",
               "Keban", "Kovancılar", "Maden", "Palu", "Sivrice"],
    "Erzincan": ["Merkez", "Çayırlı", "İliç", "Kemah", "Kemaliye", "Otlukbeli",
                 "Refahiye", "Tercan", "Üzümlü"],
    "Erzurum": ["Aşkale", "Aziziye", "Çat", "Hınıs", "Horasan", "İspir",
                "Karaçoban", "Karayazı", "Köprüköy", "Narman", "Oltu", "Olur",
                "Palandöken", "Pasinler", "Pazaryolu", "Şenkaya", "Tekman",
                "Tortum", "Uzundere", "Yakutiye"],
    "Eskişehir": ["Alpu", "Beylikova", "Çifteler", "Günyüzü", "Han", "İnönü",
                  "Mahmudiye", "Mihalgazi", "Mihalıççık", "Odunpazarı",
                  "Sarıcakaya", "Seyitgazi", "Sivrihisar", "Tepebaşı"],
    "Gaziantep": ["Araban", "İslahiye", "Karkamış", "Nizip", "Nurdağı",
                  "Oğuzeli", "Şahinbey", "Şehitkamil", "Yavuzeli"],
    "Giresun": ["Merkez", "Alucra", "Bulancak", "Çamoluk", "Çanakçı", "Dereli",
                "Doğankent", "Espiye", "Eynesil", "Görele", "Güce", "Keşap",
                "Piraziz", "Şebinkarahisar", "Tirebolu", "Yağlıdere"],
    "Gümüşhane": ["Merkez", "Kelkit", "Köse", "Kürtün", "Şiran", "Torul"],
    "Hakkari": ["Merkez", "Çukurca", "Derecik", "Şemdinli", "Yüksekova"],
    "Hatay": ["Altınözü", "Antakya", "Arsuz", "Belen", "Defne", "Dörtyol",
              "Erzin", "Hassa", "İskenderun", "Kırıkhan", "Kumlu", "Payas",
              "Reyhanlı", "Samandağ", "Yayladağı"],
    "Isparta": ["Merkez", "Aksu", "Atabey", "Eğirdir", "Gelendost", "Gönen",
                "Keçiborlu", "Senirkent", "Sütçüler", "Şarkikaraağaç",
                "Uluborlu", "Yalvaç", "Yenişarbademli"],
    "Mersin": ["Akdeniz", "Anamur", "Aydıncık", "Bozyazı", "Çamlıyayla",
               "Erdemli", "Gülnar", "Mezitli", "Mut", "Silifke", "Tarsus",
               "Toroslar", "Yenişehir"],
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar",
                 "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa",
                 "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece",
                 "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan",
                 "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane",
                 "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe",
                 "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile",
                 "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ",
              "Bornova", "Buca", "Çeşme", "Çiğli", "Dikili", "Foça", "Gaziemir",
              "Güzelbahçe", "Karabağlar", "Karaburun", "Karşıyaka",
              "Kemalpaşa", "Kınık", "Kiraz", "Konak", "Menderes", "Menemen",
              "Narlıdere", "Ödemiş", "Seferihisar", "Selçuk", "Tire",
              "Torbalı", "Urla"],
    "Kars": ["Merkez", "Akyaka", "Arpaçay", "Digor", "Kağızman", "Sarıkamış",
             "Selim", "Susuz"],
    "Kastamonu": ["Merkez", "Abana", "Ağlı", "Araç", "Azdavay", "Bozkurt",
                  "Cide", "Çatalzeytin", "Daday", "Devrekani", "Doğanyurt",
                  "Hanönü", "İhsangazi", "İnebolu", "Küre", "Pınarbaşı",
                  "Seydiler", "Şenpazar", "Taşköprü", "Tosya"],
    "Kayseri": ["Akkışla", "Bünyan", "Develi", "Felahiye", "Hacılar", "İncesu",
                "Kocasinan", "Melikgazi", "Özvatan", "Pınarbaşı", "Sarıoğlan",
                "Sarız", "Talas", "Tomarza", "Yahyalı", "Yeşilhisar"],
    "Kırklareli": ["Merkez", "Babaeski", "Demirköy", "Kofçaz", "Lüleburgaz",
                   "Pehlivanköy", "Pınarhisar", "Vize"],
    "Kırşehir": ["Merkez", "Akçakent", "Akpınar", "Boztepe", "Çiçekdağı",
                 "Kaman", "Mucur"],
    "Kocaeli": ["Başiskele", "Çayırova", "Darıca", "Derince", "Dilovası",
                "Gebze", "Gölcük", "İzmit", "Kandıra", "Karamürsel",
                "Kartepe", "Körfez"],
    "Konya": ["Ahırlı", "Akören", "Akşehir", "Altınekin", "Beyşehir", "Bozkır",
              "Cihanbeyli", "Çeltik", "Çumra", "Derbent", "Derebucak",
              "Doğanhisar", "Emirgazi", "Ereğli", "Güneysınır", "Hadim",
              "Halkapınar", "Hüyük", "Ilgın", "Kadınhanı", "Karapınar",
              "Karatay", "Kulu", "Meram", "Sarayönü", "Selçuklu", "Seydişehir",
              "Taşkent", "Tuzlukçu", "Yalıhüyük", "Yunak"],
    "Kütahya": ["Merkez", "Altıntaş", "Aslanapa", "Çavdarhisar", "Domaniç",
                "Dumlupınar", "Emet", "Gediz", "Hisarcık", "Pazarlar",
                "Simav", "Şaphane", "Tavşanlı"],
    "Malatya": ["Akçadağ", "Arapgir", "Arguvan", "Battalgazi", "Darende",
                "Doğanşehir", "Doğanyol", "Hekimhan", "Kale", "Kuluncak",
                "Pütürge", "Yazıhan", "Yeşilyurt"],
    "Manisa": ["Ahmetli", "Akhisar", "Alaşehir", "Demirci", "Gölmarmara",
               "Gördes", "Kırkağaç", "Köprübaşı", "Kula", "Salihli", "Sarıgöl",
               "Saruhanlı", "Selendi", "Soma", "Şehzadeler", "Turgutlu",
               "Yunusemre"],
    "Kahramanmaraş": ["Afşin", "Andırın", "Çağlayancerit", "Dulkadiroğlu",
                      "Ekinözü", "Elbistan", "Göksun", "Nurhak", "Onikişubat",
                      "Pazarcık", "Türkoğlu"],
    "Mardin": ["Artuklu", "Dargeçit", "Derik", "Kızıltepe", "Mazıdağı",
               "Midyat", "Nusaybin", "Ömerli", "Savur", "Yeşilli"],
    "Muğla": ["Bodrum", "Dalaman", "Datça", "Fethiye", "Kavaklıdere",
              "Köyceğiz", "Marmaris", "Menteşe", "Milas", "Ortaca",
              "Seydikemer", "Ula", "Yatağan"],
    "Muş": ["Merkez", "Bulanık", "Hasköy", "Korkut", "Malazgirt", "Varto"],
    "Nevşehir": ["Merkez", "Acıgöl", "Avanos", "Derinkuyu", "Gülşehir",
                 "Hacıbektaş", "Kozaklı", "Ürgüp"],
    "Niğde": ["Merkez", "Altunhisar", "Bor", "Çamardı", "Çiftlik", "Ulukışla"],
    "Ordu": ["Akkuş", "Altınordu", "Aybastı", "Çamaş", "Çatalpınar", "Çaybaşı",
             "Fatsa", "Gölköy", "Gülyalı", "Gürgentepe", "İkizce", "Kabadüz",
             "Kabataş", "Korgan", "Kumru", "Mesudiye", "Perşembe", "Ulubey",
             "Ünye"],
    "Rize": ["Merkez", "Ardeşen", "Çamlıhemşin", "Çayeli", "Derepazarı",
             "Fındıklı", "Güneysu", "Hemşin", "İkizdere", "İyidere",
             "Kalkandere", "Pazar"],
    "Sakarya": ["Adapazarı", "Akyazı", "Arifiye", "Erenler", "Ferizli",
                "Geyve", "Hendek", "Karapürçek", "Karasu", "Kaynarca",
                "Kocaali", "Pamukova", "Sapanca", "Serdivan", "Söğütlü",
                "Taraklı"],
    "Samsun": ["Alaçam", "Asarcık", "Atakum", "Ayvacık", "Bafra", "Canik",
               "Çarşamba", "Havza", "İlkadım", "Kavak", "Ladik", "Ondokuzmayıs",
               "Salıpazarı", "Tekkeköy", "Terme", "Vezirköprü", "Yakakent"],
    "Siirt": ["Merkez", "Baykan", "Eruh", "Kurtalan", "Pervari", "Şirvan",
              "Tillo"],
    "Sinop": ["Merkez", "Ayancık", "Boyabat", "Dikmen", "Durağan", "Erfelek",
              "Gerze", "Saraydüzü", "Türkeli"],
    "Sivas": ["Merkez", "Akıncılar", "Altınyayla", "Divriği", "Doğanşar",
              "Gemerek", "Gölova", "Gürün", "Hafik", "İmranlı", "Kangal",
              "Koyulhisar", "Suşehri", "Şarkışla", "Ulaş", "Yıldızeli", "Zara"],
    "Tekirdağ": ["Çerkezköy", "Çorlu", "Ergene", "Hayrabolu", "Kapaklı",
                 "Malkara", "Marmaraereğlisi", "Muratlı", "Saray",
                 "Süleymanpaşa", "Şarköy"],
    "Tokat": ["Merkez", "Almus", "Artova", "Başçiftlik", "Erbaa", "Niksar",
              "Pazar", "Reşadiye", "Sulusaray", "Turhal", "Yeşilyurt", "Zile"],
    "Trabzon": ["Akçaabat", "Araklı", "Arsin", "Beşikdüzü", "Çarşıbaşı",
                "Çaykara", "Dernekpazarı", "Düzköy", "Hayrat", "Köprübaşı",
                "Maçka", "Of", "Ortahisar", "Sürmene", "Şalpazarı", "Tonya",
                "Vakfıkebir", "Yomra"],
    "Tunceli": ["Merkez", "Çemişgezek", "Hozat", "Mazgirt", "Nazımiye",
                "Ovacık", "Pertek", "Pülümür"],
    "Şanlıurfa": ["Akçakale", "Birecik", "Bozova", "Ceylanpınar", "Eyyübiye",
                  "Halfeti", "Haliliye", "Harran", "Hilvan", "Karaköprü",
                  "Siverek", "Suruç", "Viranşehir"],
    "Uşak": ["Merkez", "Banaz", "Eşme", "Karahallı", "Sivaslı", "Ulubey"],
    "Van": ["Bahçesaray", "Başkale", "Çaldıran", "Çatak", "Edremit", "Erciş",
            "Gevaş", "Gürpınar", "İpekyolu", "Muradiye", "Özalp", "Saray",
            "Tuşba"],
    "Yozgat": ["Merkez", "Akdağmadeni", "Aydıncık", "Boğazlıyan", "Çandır",
               "Çayıralan", "Çekerek", "Kadışehri", "Saraykent", "Sarıkaya",
               "Sorgun", "Şefaatli", "Yenifakılı", "Yerköy"],
    "Zonguldak": ["Merkez", "Alaplı", "Çaycuma", "Devrek", "Ereğli",
                  "Gökçebey", "Kilimli", "Kozlu"],
    "Aksaray": ["Merkez", "Ağaçören", "Eskil", "Gülağaç", "Güzelyurt",
                "Ortaköy", "Sarıyahşi", "Sultanhanı"],
    "Bayburt": ["Merkez", "Aydıntepe", "Demirözü"],
    "Karaman": ["Merkez", "Ayrancı", "Başyayla", "Ermenek", "Kazımkarabekir",
                "Sarıveliler"],
    "Kırıkkale": ["Merkez", "Bahşılı", "Balışeyh", "Çelebi", "Delice",
                  "Karakeçili", "Keskin", "Sulakyurt", "Yahşihan"],
    "Batman": ["Merkez", "Beşiri", "Gercüş", "Hasankeyf", "Kozluk", "Sason"],
    "Şırnak": ["Merkez", "Beytüşşebap", "Cizre", "Güçlükonak", "İdil", "Silopi",
               "Uludere"],
    "Bartın": ["Merkez", "Amasra", "Kurucaşile", "Ulus"],
    "Ardahan": ["Merkez", "Çıldır", "Damal", "Göle", "Hanak", "Posof"],
    "Iğdır": ["Merkez", "Aralık", "Karakoyunlu", "Tuzluca"],
    "Yalova": ["Merkez", "Altınova", "Armutlu", "Çınarcık", "Çiftlikköy",
               "Termal"],
    "Karabük": ["Merkez", "Eflani", "Eskipazar", "Ovacık", "Safranbolu",
                "Yenice"],
    "Kilis": ["Merkez", "Elbeyli", "Musabeyli", "Polateli"],
    "Osmaniye": ["Merkez", "Bahçe", "Düziçi", "Hasanbeyli", "Kadirli",
                 "Sumbas", "Toprakkale"],
    "Düzce": ["Merkez", "Akçakoca", "Cumayeri", "Çilimli", "Gölyaka",
              "Gümüşova", "Kaynaşlı", "Yığılca"],
}

# Bilinen özel / istisnai domainler (pattern dışındakiler). İlk denenecek aday.
SPECIAL_DOMAINS = {
    ("İstanbul", "", "Büyükşehir"): ["ibb.istanbul", "istanbul.bel.tr"],
    ("Ankara", "", "Büyükşehir"): ["ankara.bel.tr"],
    ("İzmir", "", "Büyükşehir"): ["izmir.bel.tr"],
    ("Bursa", "", "Büyükşehir"): ["bursa.bel.tr"],
    ("Antalya", "", "Büyükşehir"): ["antalya.bel.tr"],
    ("Konya", "", "Büyükşehir"): ["konya.bel.tr"],
    ("Gaziantep", "", "Büyükşehir"): ["gaziantep.bel.tr"],
    ("Mersin", "", "Büyükşehir"): ["mersin.bel.tr"],
}


def normalize(name: str) -> str:
    """Türkçe karakterleri sadeleştirip domain-uyumlu küçük harfe çevirir."""
    table = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
        "â": "a", "Â": "a", "î": "i", "Î": "i", "û": "u", "Û": "u",
    })
    s = name.translate(table).lower()
    for ch in (" ", "'", "’", "-", ".", "/"):
        s = s.replace(ch, "")
    return s


def build_rows():
    """Tüm belediyeleri (Büyükşehir + İl + İlçe) liste olarak üretir.

    Her satır: dict(il, ilce, tur, domain_candidates)
    """
    # Çakışan ilçe adlarını tespit et (birden fazla ilde geçen).
    name_count = {}
    for il, ilceler in PROVINCES.items():
        for ilce in ilceler:
            if ilce == "Merkez":
                continue
            name_count[ilce] = name_count.get(ilce, 0) + 1
    collision = {n for n, c in name_count.items() if c > 1}

    rows = []
    for il, ilceler in PROVINCES.items():
        is_bs = il in BUYUKSEHIR
        nil = normalize(il)

        # İl / Büyükşehir belediyesi
        tur = "Büyükşehir" if is_bs else "İl"
        cands = list(SPECIAL_DOMAINS.get((il, "", tur), [f"{nil}.bel.tr"]))
        for extra in (f"{nil}.bel.tr", f"{nil}belediyesi.bel.tr",
                      f"{nil}bld.bel.tr"):
            if extra not in cands:
                cands.append(extra)
        rows.append({"il": il, "ilce": "", "tur": tur,
                     "domain_candidates": cands})

        # İlçe belediyeleri
        for ilce in ilceler:
            if ilce == "Merkez":
                # Merkez ilçe = İl Belediyesi (zaten eklendi)
                continue
            nilce = normalize(ilce)
            cands = [f"{nilce}.bel.tr"]
            # Çakışma varsa il ekli aday da dene
            if ilce in collision:
                cands.append(f"{nilce}{nil}.bel.tr")
                cands.append(f"{nil}{nilce}.bel.tr")
            cands.append(f"{nilce}belediyesi.bel.tr")
            cands.append(f"{nilce}bld.bel.tr")
            rows.append({"il": il, "ilce": ilce, "tur": "İlçe",
                         "domain_candidates": cands})
    return rows


if __name__ == "__main__":
    rows = build_rows()
    bs = sum(1 for r in rows if r["tur"] == "Büyükşehir")
    il = sum(1 for r in rows if r["tur"] == "İl")
    ilce = sum(1 for r in rows if r["tur"] == "İlçe")
    print(f"Toplam: {len(rows)} | Büyükşehir: {bs} | İl: {il} | İlçe: {ilce}")
