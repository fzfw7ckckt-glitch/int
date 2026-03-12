"""
OSINT Tools Catalog - 150 інструментів за категоріями розвідки (Золотий стандарт 2026 для MiniMax Space)
"""

TOOLS_CATALOG = {
    # GEOINT / IMINT - 20 інструментів
    "GEOINT": {
        "name": "Геолокація та Космічна розвідка (GEOINT)",
        "count": 20,
        "tools": [
            {"id": "deepstatemap", "name": "DeepStateMap", "description": "Інтерактивна карта фронту в Україні з OSINT-даними", "category": "GEOINT", "type": "Військова карта", "api": "✓"},
            {"id": "liveuamap", "name": "Liveuamap", "description": "Інтерактивна карта конфліктів у реальному часі", "category": "GEOINT", "type": "Війською карта", "api": "✓"},
            {"id": "conflictly", "name": "Conflictly", "description": "Мапінг інцидентів у зонах конфліктів (удари, авіація)", "category": "GEOINT", "type": "Війська карта", "api": "✓"},
            {"id": "geospy", "name": "GeoSpy.ai", "description": "LGM-модель для геолокації за пікселями зображення (Graylark)", "category": "GEOINT", "type": "AI Геолокація", "api": "✓"},
            {"id": "picarta", "name": "Picarta", "description": "AI-геолокація фотографій за архітектурою", "category": "GEOINT", "type": "AI Аналіз", "api": "✓"},
            {"id": "google_earth_pro", "name": "Google Earth Pro", "description": "Історичні супутникові знімки та 3D-моделі", "category": "GEOINT", "type": "Супутникові дані", "api": "✗"},
            {"id": "zoom_earth", "name": "Zoom Earth", "description": "Супутникові знімки в реальному часі", "category": "GEOINT", "type": "Супутникові дані", "api": "✓"},
            {"id": "copernicus_browser", "name": "Copernicus Browser", "description": "Наступник Sentinel Hub для аналізу супутникових даних ESA", "category": "GEOINT", "type": "Супутникові дані", "api": "✓"},
            {"id": "planet_insights", "name": "Planet Insights Platform", "description": "Професійний моніторинг змін земної поверхні", "category": "GEOINT", "type": "Супутникові дані", "api": "✓"},
            {"id": "soar", "name": "SOAR", "description": "Архів супутникових даних NASA", "category": "GEOINT", "type": "Супутникові дані", "api": "✓"},
            {"id": "eosda_landviewer", "name": "EOSDA LandViewer", "description": "Обробка супутникових знімків високої роздільної здатності", "category": "GEOINT", "type": "Супутникові дані", "api": "✓"},
            {"id": "suncalc", "name": "SunCalc", "description": "Аналіз тіней та позиції сонця", "category": "GEOINT", "type": "Тіньовий аналіз", "api": "✓"},
            {"id": "overpass_turbo", "name": "Overpass Turbo", "description": "Запити до OpenStreetMap геоданих", "category": "GEOINT", "type": "Геоданні", "api": "✓"},
            {"id": "wikimapia", "name": "Wikimapia", "description": "Спільна географічна база даних місцевостей", "category": "GEOINT", "type": "Геовіки", "api": "✓"},
            {"id": "mw_geofind", "name": "MW Geofind", "description": "Пошук геотегованих відео YouTube за координатами", "category": "GEOINT", "type": "Відео-геопошук", "api": "✓"},
            {"id": "mapillary", "name": "Mapillary", "description": "Вуличні панорами (краудсорсинг)", "category": "GEOINT", "type": "Вуличні знімки", "api": "✓"},
            {"id": "kartaview", "name": "KartaView", "description": "Відкриті вуличні знімки", "category": "GEOINT", "type": "Вуличні знімки", "api": "✓"},
            {"id": "yandex_maps", "name": "Yandex Maps", "description": "Детальні карти та панорами СНД", "category": "GEOINT", "type": "Карти СНД", "api": "✓"},
            {"id": "2gis", "name": "2GIS", "description": "Довідники та детальні карти міст СНД", "category": "GEOINT", "type": "Карти СНД", "api": "✓"},
            {"id": "exiftool_online", "name": "ExifTool Online", "description": "Витяг метаданих з файлів для геолокації", "category": "GEOINT", "type": "Метадані", "api": "✓"}
        ]
    },

    # SIGINT / Технічна розвідка - 19 інструментів
    "SIGINT": {
        "name": "Сигналізація та Технічна розвідка (SIGINT)",
        "count": 19,
        "tools": [
            {"id": "shodan", "name": "Shodan", "description": "Пошук IoT пристроїв та мережевої інфраструктури", "category": "SIGINT", "type": "Мережа", "api": "✓"},
            {"id": "censys", "name": "Censys", "description": "TLS сертифікати, хости та мережева інфраструктура", "category": "SIGINT", "type": "Мережа", "api": "✓"},
            {"id": "fofa", "name": "FOFA", "description": "Пошук мережевих активів (китайський сегмент)", "category": "SIGINT", "type": "Мережа", "api": "✓"},
            {"id": "websdr", "name": "WebSDR", "description": "Онлайн-приймачі HF-радіо для моніторингу частот", "category": "SIGINT", "type": "Радіорозвідка", "api": "✗"},
            {"id": "hfgcs", "name": "HFGCS", "description": "Моніторинг Global Communications System США", "category": "SIGINT", "type": "Радіорозвідка", "api": "✗"},
            {"id": "reveng_ai", "name": "RevEng.AI", "description": "BinNet AI для аналізу бінарного коду та шкідливого ПЗ", "category": "SIGINT", "type": "CYBINT", "api": "✓"},
            {"id": "amass_v5", "name": "Amass v5", "description": "Глибинне мапування поверхні атаки (OWASP)", "category": "SIGINT", "type": "Мережа", "api": "✓"},
            {"id": "securitytrails", "name": "SecurityTrails", "description": "Історичні DNS записи та WHOIS дані", "category": "SIGINT", "type": "DNS/WHOIS", "api": "✓"},
            {"id": "dnsdumpster", "name": "DNSDumpster", "description": "DNS-рекогносцировка для інфраструктури", "category": "SIGINT", "type": "DNS", "api": "✓"},
            {"id": "virustotal", "name": "VirusTotal", "description": "Аналіз файлів, URL та хешів", "category": "SIGINT", "type": "Малвер-аналіз", "api": "✓"},
            {"id": "spiderfoot", "name": "SpiderFoot", "description": "Автоматизований збір OSINT (200+ модулів)", "category": "SIGINT", "type": "Автоматизація", "api": "✓"},
            {"id": "recon_ng", "name": "Recon-ng", "description": "Фреймворк для техрекогносцировки", "category": "SIGINT", "type": "Фреймворк", "api": "✗"},
            {"id": "theharvester", "name": "theHarvester", "description": "Збір email/subdomains з відкритих джерел", "category": "SIGINT", "type": "Збір даних", "api": "✗"},
            {"id": "viewdns", "name": "ViewDNS.info", "description": "Комплекс DNS-інструментів", "category": "SIGINT", "type": "DNS", "api": "✓"},
            {"id": "mxtoolbox", "name": "MXToolbox", "description": "Діагностика пошти та DNS", "category": "SIGINT", "type": "DNS/Email", "api": "✓"},
            {"id": "bgp_looking_glass", "name": "BGP Looking Glass", "description": "Аналіз BGP маршрутизації", "category": "SIGINT", "type": "BGP", "api": "✓"},
            {"id": "nmap", "name": "Nmap", "description": "Сканування портів та ОС", "category": "SIGINT", "type": "Мережа", "api": "✗"},
            {"id": "apify_biz_osint", "name": "Apify Small Business OSINT", "description": "Досьє компаній з 15 джерел за один виклик", "category": "SIGINT", "type": "Business OSINT", "api": "✓"},
            {"id": "recorded_future", "name": "Recorded Future", "description": "Найбільша у світі платформа аналізу кіберзагроз та OSINT", "category": "SIGINT", "type": "Threat Intel", "api": "✓"}
        ]
    },

    # SOCMINT / HUMINT - 16 інструментів
    "SOCMINT": {
        "name": "Соціальна та Людська розвідка (SOCMINT/HUMINT)",
        "count": 16,
        "tools": [
            {"id": "osavul_nebula", "name": "Osavul Nebula", "description": "ШІ-моніторинг Telegram-каналів та наративів", "category": "SOCMINT", "type": "Telegram/AI", "api": "✓"},
            {"id": "maigret_v3", "name": "Maigret v3.0", "description": "Пошук нікнейму на 2500+ сайтах (оновлення 2026)", "category": "SOCMINT", "type": "Нікнейм", "api": "✗"},
            {"id": "whatsmyname_json", "name": "WhatsMyName (JSON)", "description": "Прямий парсинг еталонної бази wmn-dat.json", "category": "SOCMINT", "type": "Нікнейм", "api": "✓"},
            {"id": "user_scanner", "name": "User-Scanner", "description": "Сучасна альтернатива Holehe для перевірки реєстрацій", "category": "SOCMINT", "type": "Енумерація", "api": "✓"},
            {"id": "tgstat", "name": "TGStat", "description": "Глибока аналітика Telegram каналів", "category": "SOCMINT", "type": "Telegram", "api": "✓"},
            {"id": "telemetrio", "name": "Telemetr.io", "description": "Статистика та пошук у Telegram", "category": "SOCMINT", "type": "Telegram", "api": "✓"},
            {"id": "vk_osint", "name": "VK OSINT", "description": "Аналіз профілів та зв'язків у VK", "category": "SOCMINT", "type": "Соцмережі СНД", "api": "✗"},
            {"id": "think_pol", "name": "Think-Pol", "description": "ШІ-пошук по Reddit для HUMINT", "category": "SOCMINT", "type": "Reddit/AI", "api": "✓"},
            {"id": "social_links", "name": "Social Links", "description": "Комерційна платформа для соціальної розвідки", "category": "SOCMINT", "type": "Платформа", "api": "✓"},
            {"id": "osint_industries", "name": "OSINT Industries", "description": "Професійний пошук з гарантією відсутності false positives", "category": "SOCMINT", "type": "Платформа", "api": "✓"},
            {"id": "hunchly", "name": "Hunchly", "description": "Збереження доказів OSINT під час розслідування", "category": "SOCMINT", "type": "Інструмент", "api": "✗"},
            {"id": "telegago", "name": "Telegago", "description": "Пошук повідомлень у Telegram каналах", "category": "SOCMINT", "type": "Telegram", "api": "✓"},
            {"id": "reddit_search", "name": "Reddit Search", "description": "Пошук постів на Reddit", "category": "SOCMINT", "type": "Reddit", "api": "✓"},
            {"id": "youtube_search", "name": "YouTube Search", "description": "Пошук відео та каналів на YouTube", "category": "SOCMINT", "type": "YouTube", "api": "✓"},
            {"id": "siliconbag_profiler", "name": "SiliconBag Profiler", "description": "LLM-пайплайн для нормалізації та профілювання користувачів", "category": "SOCMINT", "type": "Профілювання", "api": "✓"},
            {"id": "sherlock", "name": "Sherlock", "description": "Швидкий пошук нікнейму", "category": "SOCMINT", "type": "Нікнейм", "api": "✗"}
        ]
    },

    # Dark Web / Leaks - 12 інструментів
    "DARKWEB": {
        "name": "Dark Web та Витоки (DARKWEB)",
        "count": 12,
        "tools": [
            {"id": "ahmia", "name": "Ahmia", "description": "Пошуковик для .onion сайтів", "category": "DARKWEB", "type": "Tor Search", "api": "✓"},
            {"id": "onionland", "name": "OnionLand", "description": "Індекс та пошук Tor мережі", "category": "DARKWEB", "type": "Tor Search", "api": "✓"},
            {"id": "hudson_rock", "name": "Hudson Rock", "description": "Витоки облікових даних від взлому", "category": "DARKWEB", "type": "Leaks", "api": "✓"},
            {"id": "intelligence_x", "name": "Intelligence X", "description": "Архів deep/dark web та витоків", "category": "DARKWEB", "type": "Archive", "api": "✓"},
            {"id": "dehashed", "name": "Dehashed", "description": "База даних скомпрометованих даних", "category": "DARKWEB", "type": "Leaks", "api": "✓"},
            {"id": "haveibeenpwned", "name": "Have I Been Pwned", "description": "Перевірка email на витоки", "category": "DARKWEB", "type": "Leaks", "api": "✓"},
            {"id": "spycloud", "name": "SpyCloud", "description": "Пост-інфекційна розвідка та витоки", "category": "DARKWEB", "type": "Leaks", "api": "✓"},
            {"id": "socradar", "name": "SOCRadar", "description": "Кіберрозвідка з дашбордами конфліктів", "category": "DARKWEB", "type": "Threat Intel", "api": "✓"},
            {"id": "darksearch", "name": "DarkSearch.io", "description": "Пошук у dark web paste сайтах", "category": "DARKWEB", "type": "Paste Search", "api": "✓"},
            {"id": "pastebin_search", "name": "Pastebin Search", "description": "Пошук утікань на Pastebin", "category": "DARKWEB", "type": "Paste", "api": "✓"},
            {"id": "wastebin", "name": "WasteBin", "description": "Пошук paste сайтів", "category": "DARKWEB", "type": "Paste", "api": "✓"},
            {"id": "fotoforensics", "name": "FotoForensics", "description": "Аналіз ELA зображень на маніпуляції", "category": "DARKWEB", "type": "Верифікація", "api": "✗"}
        ]
    },

    # TRANSPORT / Трекування - 12 інструментів
    "TRANSPORT": {
        "name": "Транспорт та Трекування (TRANSPORT)",
        "count": 12,
        "tools": [
            {"id": "adsb_exchange", "name": "ADS-B Exchange", "description": "Трекер військової авіації без фільтрів (Enterprise API)", "category": "TRANSPORT", "type": "Авіація", "api": "✓"},
            {"id": "radarbox", "name": "RadarBox", "description": "Авіаційний трекер у реальному часі", "category": "TRANSPORT", "type": "Авіація", "api": "✓"},
            {"id": "planefinder", "name": "Plane Finder", "description": "Трекер польотів", "category": "TRANSPORT", "type": "Авіація", "api": "✓"},
            {"id": "flightaware", "name": "FlightAware", "description": "Історія рейсів та трекування", "category": "TRANSPORT", "type": "Авіація", "api": "✓"},
            {"id": "airnow", "name": "AirNow", "description": "Трекер авіації з картами (доповнює ADS-B)", "category": "TRANSPORT", "type": "Авіація", "api": "✓"},
            {"id": "marinetraffic_v2", "name": "MarineTraffic v2", "description": "AIS трекування з прогнозуванням умов та AR-ідентифікацією", "category": "TRANSPORT", "type": "Морський", "api": "✓"},
            {"id": "vesselfinder", "name": "VesselFinder", "description": "Альтернативний трекер суден", "category": "TRANSPORT", "type": "Морський", "api": "✓"},
            {"id": "fleetmon", "name": "FleetMon", "description": "AIS з фото суден", "category": "TRANSPORT", "type": "Морський", "api": "✓"},
            {"id": "openrailway_etcs", "name": "OpenRailwayMap", "description": "Мапування залізничної інфраструктури (ETCS/Логістика)", "category": "TRANSPORT", "type": "Залізниця", "api": "✓"},
            {"id": "windy", "name": "Windy", "description": "Погода з авіа-шарами", "category": "TRANSPORT", "type": "Погода/Авіа", "api": "✓"},
            {"id": "broadcastify", "name": "Broadcastify", "description": "Потоки радіосканерів служб", "category": "TRANSPORT", "type": "Радіо", "api": "✗"},
            {"id": "pizzint_watch", "name": "Pizzint Watch", "description": "Моніторинг замовлень піци біля Пентагону (індикатор криз)", "category": "TRANSPORT", "type": "Індикатор", "api": "✗"}
        ]
    },

    # MILITARY / OSINT Платформи - 14 інструментів
    "MILITARY": {
        "name": "Військова розвідка та Платформи (MILITARY)",
        "count": 14,
        "tools": [
            {"id": "warspy", "name": "WarSpy", "description": "Військова телеметрія та розвідка", "category": "MILITARY", "type": "Військова", "api": "✓"},
            {"id": "odin_weg", "name": "ODIN WEG", "description": "Каталог світової військової техніки (TRADOC)", "category": "MILITARY", "type": "Техніка", "api": "✗"},
            {"id": "patria_crawlr", "name": "Patria CRAWLR", "description": "OSINT-платформа для військових з ML-аналізом", "category": "MILITARY", "type": "Платформа", "api": "✓"},
            {"id": "knowlesys_kis", "name": "Knowlesys KIS", "description": "Багатомовна OSINT проти дезінформації", "category": "MILITARY", "type": "Платформа", "api": "✓"},
            {"id": "maltego_v4", "name": "Maltego v4.11", "description": "Візуальний аналіз зв'язків та хмарні графи", "category": "MILITARY", "type": "Граф-аналіз", "api": "✓"},
            {"id": "ce_poshuk_bot", "name": "CE Poshuk Bot", "description": "Telegram бот для українських реєстрів", "category": "MILITARY", "type": "Українське", "api": "✓"},
            {"id": "nazk_sanctions", "name": "НАЗК War & Sanctions", "description": "Санкційний портал України", "category": "MILITARY", "type": "Санкції", "api": "✓"},
            {"id": "invid", "name": "InVID", "description": "Верифікація відео/зображень онлайн", "category": "MILITARY", "type": "Верифікація", "api": "✓"},
            {"id": "amnesty_yt", "name": "Amnesty YouTube DataViewer", "description": "Витяг метаданих YouTube-відео", "category": "MILITARY", "type": "Верифікація", "api": "✓"},
            {"id": "minimax_m2_5", "name": "MiniMax-M2.5", "description": "Агентний оркестратор (197k контекст)", "category": "MILITARY", "type": "AI Агент", "api": "✓"},
            {"id": "blacksmith_ai", "name": "BlacksmithAI", "description": "Багатоагентна розвідка", "category": "MILITARY", "type": "AI Агент", "api": "✓"},
            {"id": "perplexity_osint", "name": "Perplexity Computer", "description": "AI координатор для OSINT завдань", "category": "MILITARY", "type": "AI Агент", "api": "✓"},
            {"id": "minimax_m2_1", "name": "MiniMax-M2.1", "description": "Sparse MoE модель (230B) для глибокого аналізу", "category": "MILITARY", "type": "AI Агент", "api": "✓"},
            {"id": "deepface", "name": "DeepFace", "description": "Розпізнавання та порівняння облич", "category": "MILITARY", "type": "CV", "api": "✗"}
        ]
    },

    # FININT / CONTACT - 13 інструментів
    "FININT": {
        "name": "Фінансова та Контактна розвідка (FININT/CONTACT)",
        "count": 13,
        "tools": [
            {"id": "castellum_ai_arbiter", "name": "Castellum.AI Arbiter", "description": "AI-агенти для KYC/AML та санкційного комплаєнсу (94% менше false positives)", "category": "FININT", "type": "AML/KYC", "api": "✓"},
            {"id": "opensanctions_v2026", "name": "OpenSanctions (2026)", "description": "Консолідована база (2.1M+ сутностей) з оновленим UK Sanctions List", "category": "FININT", "type": "Санкції", "api": "✓"},
            {"id": "youcontrol", "name": "YouControl", "description": "Українські компанії, зв'язки, PEP та санкції", "category": "FININT", "type": "Українське", "api": "✓"},
            {"id": "rupep", "name": "RuPEP", "description": "База PEP Російської Федерації та Білорусі", "category": "FININT", "type": "PEP", "api": "✓"},
            {"id": "hunter_io", "name": "Hunter.io", "description": "Пошук email адрес за доменом", "category": "FININT", "type": "Email", "api": "✓"},
            {"id": "phoneinfoga", "name": "PhoneInfoga", "description": "Розвідка за номером телефону", "category": "FININT", "type": "Телефон", "api": "✓"},
            {"id": "pipl", "name": "Pipl", "description": "Пошук людей за багатьма параметрами", "category": "FININT", "type": "Люди", "api": "✓"},
            {"id": "kharon", "name": "Kharon", "description": "Розкриття корпоративних мереж", "category": "FININT", "type": "Корпоративне", "api": "✓"},
            {"id": "occrp_aleph", "name": "OCCRP Aleph", "description": "Глобальні витоки та корупція", "category": "FININT", "type": "Витоки", "api": "✓"},
            {"id": "dun_bradstreet", "name": "Dun & Bradstreet", "description": "Комерційні дані про компанії", "category": "FININT", "type": "Бізнес", "api": "✓"},
            {"id": "forbes_list", "name": "Forbes Billionaires", "description": "База активів найбагатших людей", "category": "FININT", "type": "Бізнес", "api": "✓"},
            {"id": "reverse_phone", "name": "ReversePhoneLookup", "description": "Зворотний пошук за номером", "category": "FININT", "type": "Телефон", "api": "✓"},
            {"id": "uk_sanctions_new", "name": "UK Sanctions List (New)", "description": "Новий консолідований список Великобританії (XML/CSV)", "category": "FININT", "type": "Санкції", "api": "✓"}
        ]
    },

    # IMINT / Аналіз зображень - 11 інструментів
    "IMINT": {
        "name": "Аналіз зображень та Фото-OSINT (IMINT)",
        "count": 11,
        "tools": [
            {"id": "pimeyes", "name": "Pimeyes", "description": "Найпотужніший пошук облич по всьому інтернету", "category": "IMINT", "type": "Розпізнавання облич", "api": "✓"},
            {"id": "facecheck_id", "name": "FaceCheck.ID", "description": "Пошук облич по базах соцмереж та кримінальних реєстрах", "category": "IMINT", "type": "Розпізнавання облич", "api": "✓"},
            {"id": "search4faces", "name": "Search4Faces", "description": "Спеціалізований пошук облич (VK, OK, TikTok, СНД)", "category": "IMINT", "type": "Розпізнавання облич", "api": "✓"},
            {"id": "forensically", "name": "Forensically", "description": "Веб-інструмент для форензики зображень (ELA, аналіз шуму)", "category": "IMINT", "type": "Верифікація", "api": "✗"},
            {"id": "sherloq_toolkit", "name": "Sherloq", "description": "Професійний набір інструментів для аналізу автентичності фото", "category": "IMINT", "type": "Верифікація", "api": "✗"},
            {"id": "yandex_images", "name": "Yandex Images", "description": "Кращий зворотний пошук для ідентифікації об'єктів та локацій", "category": "IMINT", "type": "Зворотний пошук", "api": "✓"},
            {"id": "tineye", "name": "TinEye", "description": "Пошук оригінальних джерел зображення та його модифікацій", "category": "IMINT", "type": "Зворотний пошук", "api": "✓"},
            {"id": "google_lens", "name": "Google Lens", "description": "Розпізнавання об'єктів, тексту та переклад на фото в реальному часі", "category": "IMINT", "type": "Візуальний аналіз", "api": "✓"},
            {"id": "bing_visual_search", "name": "Bing Visual Search", "description": "Альтернативний ШІ-пошук по зображеннях від Microsoft", "category": "IMINT", "type": "Візуальний аналіз", "api": "✓"},
            {"id": "metadata2go", "name": "Metadata2Go", "description": "Глибокий аналіз прихованих метаданих (EXIF, XMP, IPTC)", "category": "IMINT", "type": "Метадані", "api": "✓"},
            {"id": "clearview_ai", "name": "Clearview AI", "description": "Найбільш розширена база розпізнавання облич для правоохоронних органів", "category": "IMINT", "type": "Facial Recognition", "api": "✓"}
        ]
    },

    # CRYPTOINT / Блокчейн розвідка - 8 інструментів
    "CRYPTOINT": {
        "name": "Блокчейн розвідка та Крипто-OSINT (CRYPTOINT)",
        "count": 8,
        "tools": [
            {"id": "breadcrumbs", "name": "Breadcrumbs.app", "description": "Візуальний аналіз транзакцій та трекування гаманців", "category": "CRYPTOINT", "type": "Аналіз", "api": "✓"},
            {"id": "etherscan", "name": "Etherscan", "description": "Експлорер блокчейну Ethereum та смарт-контрактів", "category": "CRYPTOINT", "type": "Explorer", "api": "✓"},
            {"id": "tronscan", "name": "TronScan", "description": "Аналіз транзакцій у мережі TRON (USDT)", "category": "CRYPTOINT", "type": "Explorer", "api": "✓"},
            {"id": "blockchain_com", "name": "Blockchain.com", "description": "Класичний експлорер для Bitcoin та Ethereum", "category": "CRYPTOINT", "type": "Explorer", "api": "✓"},
            {"id": "walletexplorer", "name": "WalletExplorer", "description": "Кластеризація Bitcoin-адрес та ідентифікація бірж", "category": "CRYPTOINT", "type": "Кластеризація", "api": "✓"},
            {"id": "crystal_blockchain", "name": "Crystal Blockchain", "description": "Професійна платформа для AML/KYT крипто-розслідувань", "category": "CRYPTOINT", "type": "Compliance", "api": "✓"},
            {"id": "chainalysis_eye", "name": "Chainalysis Storyline", "description": "Візуалізація складних крос-чейн транзакцій", "category": "CRYPTOINT", "type": "Аналіз", "api": "✓"},
            {"id": "whale_alert", "name": "Whale Alert", "description": "Моніторинг великих переміщень криптовалют", "category": "CRYPTOINT", "type": "Моніторинг", "api": "✓"}
        ]
    },

    # WIRELESS / IoT розвідка - 5 інструментів
    "WIRELESS": {
        "name": "Бездротові мережі та IoT (WIRELESS)",
        "count": 5,
        "tools": [
            {"id": "wigle_net", "name": "Wigle.net", "description": "Глобальна база даних Wi-Fi мереж та веж зв'язку", "category": "WIRELESS", "type": "Гео-пошук", "api": "✓"},
            {"id": "skyhook", "name": "Skyhook", "description": "Визначення локації за Wi-Fi та стільниковими даними", "category": "WIRELESS", "type": "Гео-пошук", "api": "✓"},
            {"id": "bluetooth_le_scanner", "name": "BLE Scanner", "description": "Пошук та ідентифікація Bluetooth-пристроїв", "category": "WIRELESS", "type": "IoT", "api": "✗"},
            {"id": "shodan_iot", "name": "Shodan IoT Monitor", "description": "Спеціалізований моніторинг вразливих IoT пристроїв", "category": "WIRELESS", "type": "IoT", "api": "✓"},
            {"id": "mwigle", "name": "WiGLE Mobile", "description": "Мобільний збір даних про бездротові мережі", "category": "WIRELESS", "type": "Збір даних", "api": "✗"}
        ]
    },

    # CODE OSINT / Розвідка коду - 6 інструментів
    "CODEINT": {
        "name": "Розвідка коду та Секретів (CODEINT)",
        "count": 6,
        "tools": [
            {"id": "trufflehog", "name": "TruffleHog", "description": "Пошук секретів, API-ключів та токенів у комітах", "category": "CODEINT", "type": "Секрети", "api": "✓"},
            {"id": "gitleaks", "name": "Gitleaks", "description": "Аудит репозиторіїв на предмет витоку конфіденційних даних", "category": "CODEINT", "type": "Секрети", "api": "✓"},
            {"id": "github_advanced_search", "name": "GitHub Advanced Search", "description": "Пошук коду та витоків за складними фільтрами", "category": "CODEINT", "type": "Пошук", "api": "✓"},
            {"id": "greptile", "name": "Greptile", "description": "AI-пошук та розуміння великих кодових баз", "category": "CODEINT", "type": "AI Аналіз", "api": "✓"},
            {"id": "sourcegraph", "name": "Sourcegraph", "description": "Глобальний пошук коду по мільйонах репозиторіїв", "category": "CODEINT", "type": "Пошук", "api": "✓"},
            {"id": "leakix", "name": "LeakIX", "description": "Пошук публічно відкритих конфігурацій та витоків", "category": "CODEINT", "type": "Витоки", "api": "✓"}
        ]
    },

    # DEEPFAKE / AI Верифікація - 6 інструментів
    "DEEPFAKE": {
        "name": "Верифікація AI-контенту (DEEPFAKE)",
        "count": 6,
        "tools": [
            {"id": "sentinel_ai_detector", "name": "Sentinel AI", "description": "Професійна платформа для виявлення діпфейків", "category": "DEEPFAKE", "type": "AI Detector", "api": "✓"},
            {"id": "reality_defender", "name": "Reality Defender", "description": "Захист від медіа-маніпуляцій та AI-генерацій", "category": "DEEPFAKE", "type": "AI Detector", "api": "✓"},
            {"id": "deepfake_o_meter", "name": "Deepfake-o-meter", "description": "Відкрита платформа для тестування зображень/відео", "category": "DEEPFAKE", "type": "AI Detector", "api": "✗"},
            {"id": "hive_moderation", "name": "Hive Moderation", "description": "Виявлення AI-генерованого контенту та дипфейків", "category": "DEEPFAKE", "type": "AI Detector", "api": "✓"},
            {"id": "weverify", "name": "WeVerify", "description": "Інструменти для верифікації дезінформації та фото/відео", "category": "DEEPFAKE", "type": "Верифікація", "api": "✗"},
            {"id": "illuminarty", "name": "Illuminarty", "description": "Аналіз ймовірності використання AI у зображеннях", "category": "DEEPFAKE", "type": "AI Detector", "api": "✓"}
        ]
    },

    # WEB ARCHIVE / Історія вебу - 4 інструменти
    "ARCHIVE": {
        "name": "Архівування та Історія вебу (ARCHIVE)",
        "count": 4,
        "tools": [
            {"id": "wayback_machine", "name": "Wayback Machine", "description": "Найбільший архів інтернету (Internet Archive)", "category": "ARCHIVE", "type": "Архів", "api": "✓"},
            {"id": "archive_today", "name": "Archive.today", "description": "Снапшоти веб-сторінок з обходом paywall", "category": "ARCHIVE", "type": "Архів", "api": "✓"},
            {"id": "cachedview", "name": "CachedView", "description": "Доступ до кешованих копій Google, Bing та Yandex", "category": "ARCHIVE", "type": "Кеш", "api": "✓"},
            {"id": "common_crawl", "name": "Common Crawl", "description": "Відкритий репозиторій даних веб-кроулінгу", "category": "ARCHIVE", "type": "Big Data", "api": "✓"}
        ]
    },

    # AI AGENT OSINT / Розвідка ШІ-агентів - 4 інструменти
    "AI_OSINT": {
        "name": "Розвідка ШІ-агентів та LLM (AI_OSINT)",
        "count": 4,
        "tools": [
            {"id": "llm_fingerprint", "name": "LLM Fingerprinting", "description": "Ідентифікація моделі ШІ за патернами відповідей", "category": "AI_OSINT", "type": "Ідентифікація", "api": "✓"},
            {"id": "prompt_injection_test", "name": "Prompt Injection Scanner", "description": "Тестування стійкості ШІ-агентів до маніпуляцій", "category": "AI_OSINT", "type": "Безпека", "api": "✓"},
            {"id": "ai_watermark_check", "name": "AI Watermark Checker", "description": "Пошук цифрових водяних знаків LLM у текстах", "category": "AI_OSINT", "type": "Верифікація", "api": "✓"},
            {"id": "agent_discovery", "name": "Agent Discovery", "description": "Пошук публічних API та ендпоінтів ШІ-агентів", "category": "AI_OSINT", "type": "Пошук", "api": "✓"}
        ]
    }
}

# Загальна статистика
TOTAL_TOOLS = 150
TOTAL_CATEGORIES = len(TOOLS_CATALOG)


# Лист всіх інструментів для швидкого пошуку
ALL_TOOLS_LIST = []
for category_key, category_data in TOOLS_CATALOG.items():
    for tool in category_data["tools"]:
        ALL_TOOLS_LIST.append(tool)
