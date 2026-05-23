"""
Nomenclature — the naming system for the constraint instrument.

Every word on this instrument means something. Not parameter_3 — SAUDADE.
Not consensus_score — CHORUS. The names teach.

Three layers:
  1. API names (English, snake_case) — what developers type
  2. Panel names (multilingual) — what musicians see
  3. Descriptions — etymology, feeling, story

Usage:
    from constraint_instrument.nomenclature import display_name, full_description

    display_name("funnel")         # → "SAUDADE"
    display_name("miles")          # → "WANDERLUST"
    full_description("holonomy")   # → "GEIST (German) — ..."
"""

from typing import Dict, Optional


# ── The Master Registry ───────────────────────────────────────────────
# Every internal name → its display identity.

_Entry = dict  # {"panel": str, "origin": str, "meaning": str, "lang_variants": dict}

_REGISTRY: Dict[str, _Entry] = {
    # ── The Five Primitives ───────────────────────────────────────────
    "lattice_snap": {
        "panel": "MOORING",
        "origin": "English (nautical)",
        "meaning": (
            "Where you tie up. The anchor point that keeps you tethered to "
            "the constraint surface. Like a boat at mooring — you can drift, "
            "but you know where home is."
        ),
        "lang_variants": {
            "de": "ANKERPLATZ",
            "es": "AMARRE",
            "pt": "AMARRAÇÃO",
            "ja": "係留",
            "zh": "锚泊",
            "it": "ORMEGGIO",
            "ar": "رسو",
            "hi": "लंगरगाह",
        },
    },
    "funnel": {
        "panel": "SAUDADE",
        "origin": "Portuguese",
        "meaning": (
            "A longing for something not yet reached. The gravitational pull "
            "toward certain pitches — not a rule, but a yearning. The funnel "
            "doesn't force; it aches."
        ),
        "lang_variants": {
            "de": "SEHNSUCHT",
            "es": "AÑORANZA",
            "pt": "SAUDADE",
            "ja": "憧れ",
            "zh": "乡愁",
            "it": "MALINCONIA",
            "ar": "حنين",
            "hi": "उदासी",
        },
    },
    "is_laman": {
        "panel": "RIGGING",
        "origin": "English (nautical)",
        "meaning": (
            "Is the structure holding? Are the lines taut? Laman's theorem "
            "says the lattice is rigid — RIGGING asks: are the constraint "
            "lines properly rigged, or are some slack?"
        ),
        "lang_variants": {
            "de": "TAKELAGE",
            "es": "APAREJO",
            "pt": "ENXÁRCIA",
            "ja": "索具",
            "zh": "索具",
            "it": "SARTIAME",
            "ar": "أشرعة",
            "hi": "रिगिंग",
        },
    },
    "consensus": {
        "panel": "CHORUS",
        "origin": "Greek χορός (khorós)",
        "meaning": (
            "The dance together. When multiple constraint voices agree, they "
            "form a chorus — not unison, but consensus. The word literally "
            "means 'circular dance.'"
        ),
        "lang_variants": {
            "de": "CHOR",
            "es": "CORO",
            "pt": "CORO",
            "ja": "合唱",
            "zh": "合唱",
            "it": "CORO",
            "ar": "جوقة",
            "hi": "समूहगान",
        },
    },
    "holonomy": {
        "panel": "GEIST",
        "origin": "German",
        "meaning": (
            "The spirit of the loop. Holonomy measures how much you've changed "
            "after completing a cycle. Geist — spirit, ghost, mind — captures "
            "the uncanny return: you're back where you started, but transformed."
        ),
        "lang_variants": {
            "de": "GEIST",
            "es": "ESPÍRITU",
            "pt": "ESPÍRITO",
            "ja": "霊",
            "zh": "精神",
            "it": "SPIRITO",
            "ar": "روح",
            "hi": "प्रेतात्मा",
        },
    },

    # ── The Seven Modes ───────────────────────────────────────────────
    "parker": {
        "panel": "SITZFLEISCH",
        "origin": "German",
        "meaning": (
            "'Sitting flesh' — the stamina of practice. Parker internalized "
            "every change so deeply that the constraints disappeared. This mode "
            "is about building that muscle memory through relentless, focused repetition."
        ),
        "lang_variants": {
            "de": "SITZFLEISCH",
            "es": "AGUANTE",
            "pt": "PERSISTÊNCIA",
            "ja": "根気",
            "zh": "坐功",
            "it": "COSTANZA",
            "ar": "مثابرة",
            "hi": "धैर्य",
        },
    },
    "miles": {
        "panel": "WANDERLUST",
        "origin": "German",
        "meaning": (
            "The compulsion to explore, always seeking new territory. Miles Davis "
            "never repeated himself; every performance went somewhere it hadn't been. "
            "This mode pushes toward the frontier."
        ),
        "lang_variants": {
            "de": "WANDERLUST",
            "es": "INQUIETUD",
            "pt": "INQUIETUDE",
            "ja": " wanderlust",
            "zh": "漫游欲",
            "it": "VAGABONDAGGIO",
            "ar": "شغف الرحيل",
            "hi": "भटकना",
        },
    },
    "ellington": {
        "panel": "ARCHITETTURA",
        "origin": "Italian",
        "meaning": (
            "The architecture — building structures for others to inhabit. "
            "Ellington composed for his band, his soloists, his audience. This mode "
            "creates frameworks; it builds houses, not just rooms."
        ),
        "lang_variants": {
            "de": "ARCHITEKTUR",
            "es": "ARQUITECTURA",
            "pt": "ARQUITETURA",
            "ja": "建築",
            "zh": "建筑",
            "it": "ARCHITETTURA",
            "ar": "عمارة",
            "hi": "वास्तुकला",
        },
    },
    "basie": {
        "panel": "SAISON",
        "origin": "French",
        "meaning": (
            "The season — finding rhythm together as it emerges. Basie's band "
            "swung as one organism. This mode doesn't impose a groove; it discovers "
            "the shared pulse through listening."
        ),
        "lang_variants": {
            "de": "SAISON",
            "es": "ESTACIÓN",
            "pt": "ESTAÇÃO",
            "ja": "季節",
            "zh": "季节",
            "it": "STAGIONE",
            "ar": "موسم",
            "hi": "ऋतु",
        },
    },
    "goodman": {
        "panel": "DIAGNOSTICO",
        "origin": "Italian",
        "meaning": (
            "Clinical precision — knowing exactly what's missing. Goodman was a "
            "perfectionist who could diagnose a band's weakness in one bar. This mode "
            "doesn't play; it listens and tells you what's absent."
        ),
        "lang_variants": {
            "de": "DIAGNOSE",
            "es": "DIAGNÓSTICO",
            "pt": "DIAGNÓSTICO",
            "ja": "診断",
            "zh": "诊断",
            "it": "DIAGNOSTICO",
            "ar": "تشخيص",
            "hi": "निदान",
        },
    },
    "armstrong": {
        "panel": "LIBERTAD",
        "origin": "Spanish",
        "meaning": (
            "Liberation through constraint removal. Armstrong stripped away everything "
            "that didn't serve the music. This mode starts loaded with constraints and "
            "frees you by removing them one by one."
        ),
        "lang_variants": {
            "de": "FREIHEIT",
            "es": "LIBERTAD",
            "pt": "LIBERDADE",
            "ja": "自由",
            "zh": "自由",
            "it": "LIBERTÀ",
            "ar": "حرية",
            "hi": "स्वतंत्रता",
        },
    },
    "ella": {
        "panel": "DUENDE",
        "origin": "Spanish (Andalusian)",
        "meaning": (
            "The dark fire — when the tool disappears and only music remains. "
            "Federico García Lorca described duende as the mysterious force that makes "
            "great art. Ella's scat singing had it: pure flow, no thinking, just music."
        ),
        "lang_variants": {
            "de": "DÄMON",
            "es": "DUENDE",
            "pt": "DUENDE",
            "ja": "魔性",
            "zh": "魔力",
            "it": "DUENDE",
            "ar": "شيطانة",
            "hi": "दुएंदे",
        },
    },

    # ── Monitor States ────────────────────────────────────────────────
    "flow_state": {
        "panel": "DUENDE LEVEL",
        "origin": "Spanish",
        "meaning": (
            "How much dark fire is present. 0% = mechanical, 100% = the "
            "instrument has vanished."
        ),
        "lang_variants": {
            "de": "DÄMON-PEGEL",
            "es": "NIVEL DE DUENDE",
            "pt": "NÍVEL DE DUENDE",
            "ja": "魔性レベル",
            "zh": "魔力等级",
            "it": "LIVELLO DUENDE",
            "ar": "مستوى الروح",
            "hi": "दुएंदे स्तर",
        },
    },
    "error_rate": {
        "panel": "STRAY",
        "origin": "English",
        "meaning": (
            "How far from home. Not 'wrong' — just stray. A stray dog isn't "
            "broken, it's just wandered."
        ),
        "lang_variants": {
            "de": "ABSCHWEIFUNG",
            "es": "DESVÍO",
            "pt": "DESVIO",
            "ja": "逸脱",
            "zh": "偏离",
            "it": "DEVIAZIONE",
            "ar": "شرد",
            "hi": "भटकाव",
        },
    },
    "consistency": {
        "panel": "GROOVE DEPTH",
        "origin": "English",
        "meaning": (
            "How deep the pocket. Consistency isn't boring — it's the depth of "
            "the groove, how locked-in the rhythm is."
        ),
        "lang_variants": {
            "de": "GROOVTIEFE",
            "es": "PROFUNDIDAD DEL GROOVE",
            "pt": "PROFUNDIDADE DO GROOVE",
            "ja": "グルーヴの深さ",
            "zh": "律动深度",
            "it": "PROFONDITÀ DEL GROOVE",
            "ar": "عمق الأزيز",
            "hi": "ग्रूव गहराई",
        },
    },
    "exploration_velocity": {
        "panel": "HORIZON",
        "origin": "English",
        "meaning": (
            "How far you can see. Exploration isn't randomness — it's extending "
            "the horizon of what's possible."
        ),
        "lang_variants": {
            "de": "HORIZONT",
            "es": "HORIZONTE",
            "pt": "HORIZONTE",
            "ja": "地平線",
            "zh": "地平线",
            "it": "ORIZZONTE",
            "ar": "أفق",
            "hi": "क्षितिज",
        },
    },
    "energy": {
        "panel": "FIRE",
        "origin": "English",
        "meaning": "Raw intensity — average velocity, how hard you're pushing.",
        "lang_variants": {
            "de": "FEUER",
            "es": "FUEGO",
            "pt": "FOGO",
            "ja": "炎",
            "zh": "烈火",
            "it": "FUOCO",
            "ar": "نار",
            "hi": "आग",
        },
    },
    "energy_trajectory": {
        "panel": "EMBER",
        "origin": "English",
        "meaning": "Is the fire growing or fading? The trajectory of energy over time.",
        "lang_variants": {
            "de": "GLUT",
            "es": "BRASA",
            "pt": "BRASA",
            "ja": "燃えさし",
            "zh": "余烬",
            "it": "BRACE",
            "ar": "جمر",
            "hi": "अंगार",
        },
    },
    "is_vanished": {
        "panel": "MA",
        "origin": "Japanese 間",
        "meaning": (
            "The space where the tool doesn't exist. Ma (間) is the Japanese concept "
            "of 'negative space' — when the monitor detects full internalization and "
            "vanishes into silence."
        ),
        "lang_variants": {
            "de": "MA",
            "es": "MA",
            "pt": "MA",
            "ja": "間",
            "zh": "间",
            "it": "MA",
            "ar": "ما",
            "hi": "मा",
        },
    },

    # ── Terrain Properties ────────────────────────────────────────────
    "scale_degrees": {
        "panel": "SEEDS",
        "origin": "English",
        "meaning": (
            "What can grow here. Scale degrees aren't rules — they're seeds. "
            "Some grow strong (high weight), some struggle (low weight), some "
            "are the wild blue notes that grow between the cracks."
        ),
        "lang_variants": {
            "de": "SAMEN",
            "es": "SEMILLAS",
            "pt": "SEMENTES",
            "ja": "種",
            "zh": "种子",
            "it": "SEMI",
            "ar": "بذور",
            "hi": "बीज",
        },
    },
    "funnel_targets": {
        "panel": "GRAVITY WELLS",
        "origin": "Physics",
        "meaning": (
            "Where things fall toward. The gravitational centers of the terrain — "
            "pitches that pull you in, whether you intend to land on them or not."
        ),
        "lang_variants": {
            "de": "GRAVITATIONSBRUNNEN",
            "es": "POZOS DE GRAVEDAD",
            "pt": "POÇOS DE GRAVIDADE",
            "ja": "重力井戸",
            "zh": "重力井",
            "it": "POZZI GRAVITAZIONALI",
            "ar": "آبار جاذبية",
            "hi": "गुरुत्व कूप",
        },
    },
    "register_tendency": {
        "panel": "TERRAIN",
        "origin": "French (terre)",
        "meaning": (
            "The ground you walk on. Register tendency defines the physical space — "
            "low valleys, high ridges — where this music naturally lives."
        ),
        "lang_variants": {
            "de": "GELÄNDE",
            "es": "TERRENO",
            "pt": "TERRENO",
            "ja": "地形",
            "zh": "地形",
            "it": "TERRENO",
            "ar": "تضاريس",
            "hi": "भूभाग",
        },
    },
    "chromatic_density": {
        "panel": "SPICE",
        "origin": "English",
        "meaning": (
            "How much chromatic flavor. 0% = pure diatonic water, 100% = everything "
            "is available, total chromatic saturation."
        ),
        "lang_variants": {
            "de": "WÜRZE",
            "es": "ESPECIA",
            "pt": "TEMPERO",
            "ja": "スパイス",
            "zh": "香料",
            "it": "SPEZIA",
            "ar": "توابل",
            "hi": "मसाला",
        },
    },
    "typical_tempo": {
        "panel": "PULSE",
        "origin": "English",
        "meaning": (
            "The heartbeat. Not a metronome — a pulse. Every terrain has a natural "
            "resting heart rate."
        ),
        "lang_variants": {
            "de": "PULS",
            "es": "PULSO",
            "pt": "PULSO",
            "ja": "脈動",
            "zh": "脉动",
            "it": "PULSO",
            "ar": "نبض",
            "hi": "स्पंदन",
        },
    },
    "characteristic_intervals": {
        "panel": "FINGERPRINTS",
        "origin": "English",
        "meaning": (
            "The intervals that define this terrain's sonic identity. Like a "
            "fingerprint — unique, recognizable, inescapable."
        ),
        "lang_variants": {
            "de": "FINGERABDRÜCKE",
            "es": "HUELLAS",
            "pt": "IMPRESSÕES",
            "ja": "指紋",
            "zh": "指纹",
            "it": "IMPRONTE",
            "ar": "بصمات",
            "hi": "फिंगरप्रिंट",
        },
    },
    "rhythmic_skeletons": {
        "panel": "BONES",
        "origin": "English",
        "meaning": (
            "The rhythmic skeleton underneath the flesh of the music. "
            "The bones that hold it up."
        ),
        "lang_variants": {
            "de": "KNOCHEN",
            "es": "HUESOS",
            "pt": "OSSOS",
            "ja": "骨格",
            "zh": "骨架",
            "it": "OSSA",
            "ar": "عظام",
            "hi": "हड्डियाँ",
        },
    },
    "rigidity": {
        "panel": "ICE",
        "origin": "English",
        "meaning": (
            "How frozen are the rules. 0% = liquid, anything flows. "
            "100% = rigid, no escape from the lattice."
        ),
        "lang_variants": {
            "de": "EIS",
            "es": "HIELO",
            "pt": "GELO",
            "ja": "氷",
            "zh": "冰",
            "it": "GHIACCIO",
            "ar": "جليد",
            "hi": "बर्फ़",
        },
    },
    "blues_note": {
        "panel": "CRACKS",
        "origin": "English",
        "meaning": (
            "The places where the lattice doesn't quite hold. Blue notes don't "
            "sit on the grid — they live in the cracks between scale degrees."
        ),
        "lang_variants": {
            "de": "RISSE",
            "es": "GRIETAS",
            "pt": "FRESCURAS",
            "ja": "裂け目",
            "zh": "裂缝",
            "it": "CREPE",
            "ar": "شقوق",
            "hi": "दरारें",
        },
    },

    # ── The Terrains ──────────────────────────────────────────────────
    "delta_blues": {
        "panel": "BLUES DELTA",
        "origin": "Spanish word order",
        "meaning": (
            "'The delta of sorrows.' The Spanish inversion (noun then qualifier) "
            "mirrors how delta blues builds: the feeling first, the form second."
        ),
        "lang_variants": {
            "de": "BLUES DELTA",
            "es": "BLUES DELTA",
            "pt": "BLUES DELTA",
            "ja": "ブルース・デルタ",
            "zh": "三角洲蓝调",
            "it": "BLUES DELTA",
            "ar": "دلتا البلوز",
            "hi": "ब्लूज़ डेल्टा",
        },
    },
    "bebop": {
        "panel": "BEBOP",
        "origin": "Onomatopoeia",
        "meaning": (
            "The sound itself. Bebop is named for the scat syllables — "
            "it doesn't translate, it IS. The word is the music."
        ),
        "lang_variants": {
            "de": "BEBOP",
            "es": "BEBOP",
            "pt": "BEBOP",
            "ja": "ビバップ",
            "zh": "比波普",
            "it": "BEBOP",
            "ar": "بيبوب",
            "hi": "बीबॉप",
        },
    },
    "bebop_rich": {
        "panel": "BEBOP",
        "origin": "Onomatopoeia",
        "meaning": "The full bathymetric chart of bebop. Same name, deeper map.",
        "lang_variants": {
            "de": "BEBOP",
            "es": "BEBOP",
            "pt": "BEBOP",
            "ja": "ビバップ",
            "zh": "比波普",
            "it": "BEBOP",
            "ar": "بيبوب",
            "hi": "बीबॉप",
        },
    },
    "modal_jazz": {
        "panel": "RAGA",
        "origin": "Sanskrit राग (rāga)",
        "meaning": (
            "Color, mood, passion. Modal jazz's closest ancestor. A raga isn't a "
            "scale — it's a complete melodic framework with rules for ascent, descent, "
            "emphasis, and time of day. Modal jazz is its American cousin."
        ),
        "lang_variants": {
            "de": "RAGA",
            "es": "RAGA",
            "pt": "RAGA",
            "ja": "ラーガ",
            "zh": "拉格",
            "it": "RAGA",
            "ar": "راغا",
            "hi": "राग",
        },
    },
    "classical_counterpoint": {
        "panel": "KONTRAPUNKT",
        "origin": "German",
        "meaning": (
            "The original term. Counterpoint entered English from the Latin punctus "
            "contra punctum (note against note), but the German preserves the "
            "discipline's architectural weight."
        ),
        "lang_variants": {
            "de": "KONTRAPUNKT",
            "es": "CONTRAPUNTO",
            "pt": "CONTRAPONTO",
            "ja": "対位法",
            "zh": "对位法",
            "it": "CONTRAPPUNTO",
            "ar": "طباق",
            "hi": "प्रतिबंध",
        },
    },
    "bluegrass": {
        "panel": "HIGHLONESOME",
        "origin": "Appalachian English",
        "meaning": (
            "The feeling, not the genre. 'High lonesome sound' is what Bill Monroe "
            "called it — that keening, mountain-top ache. Bluegrass is named for "
            "the grass; HIGHLONESOME is named for what it feels like."
        ),
        "lang_variants": {
            "de": "HOHEINSAMKEIT",
            "es": "ALTA SOLEDAD",
            "pt": "ALTA SOLIDÃO",
            "ja": "ハイロンサム",
            "zh": "高山孤音",
            "it": "ALTA SOLITUDINE",
            "ar": "الوحدة العالية",
            "hi": "हाईलोनसम",
        },
    },
    "hip_hop_trap": {
        "panel": "808",
        "origin": "English (tech)",
        "meaning": (
            "The Roland TR-808 drum machine that IS the genre. The 808 kick is so "
            "fundamental to trap that naming this terrain anything else would be dishonest."
        ),
        "lang_variants": {
            "de": "808",
            "es": "808",
            "pt": "808",
            "ja": "808",
            "zh": "808",
            "it": "808",
            "ar": "808",
            "hi": "808",
        },
    },
    "afro_cuban": {
        "panel": "CLAVE",
        "origin": "Spanish",
        "meaning": (
            "The key — literally. La clave is both the instrument (two wooden sticks) "
            "and the rhythmic pattern that unlocks all Afro-Cuban music. Everything "
            "else is commentary."
        ),
        "lang_variants": {
            "de": "CLAVE",
            "es": "CLAVE",
            "pt": "CLAVE",
            "ja": "クラーベ",
            "zh": "克拉韦",
            "it": "CLAVE",
            "ar": "كلافي",
            "hi": "क्लावे",
        },
    },
    "indian_raga": {
        "panel": "SRUTI",
        "origin": "Sanskrit स्रुति",
        "meaning": (
            "The 22 microtones of the Indian musical system. Where Western music "
            "has 12 pitches, Indian music recognizes 22 places between them. SRUTI "
            "is the resolution that hears what Western ears can't."
        ),
        "lang_variants": {
            "de": "SRUTI",
            "es": "SRUTI",
            "pt": "SRUTI",
            "ja": "シュルティ",
            "zh": "什鲁提",
            "it": "SRUTI",
            "ar": "شروتي",
            "hi": "श्रुति",
        },
    },
    "chinese_silk_bamboo": {
        "panel": "SĪZHU",
        "origin": "Mandarin 絲竹",
        "meaning": (
            "Silk and bamboo — the instruments. 絲 (silk = strings) and 竹 (bamboo = "
            "winds). The name IS the ensemble."
        ),
        "lang_variants": {
            "de": "SĪZHU",
            "es": "SĪZHU",
            "pt": "SĪZHU",
            "ja": "糸竹",
            "zh": "丝竹",
            "it": "SĪZHU",
            "ar": "سِتْشُو",
            "hi": "सीझू",
        },
    },
    "electronic_techno": {
        "panel": "KICK",
        "origin": "English",
        "meaning": (
            "The heartbeat of techno. Not a bass drum — THE kick. The four-on-the-floor "
            "pulse that defines an entire culture of music."
        ),
        "lang_variants": {
            "de": "KICK",
            "es": "KICK",
            "pt": "KICK",
            "ja": "キック",
            "zh": "底鼓",
            "it": "KICK",
            "ar": "كيك",
            "hi": "किक",
        },
    },
    "gospel": {
        "panel": "TESTIFY",
        "origin": "English",
        "meaning": (
            "The act, not the genre. Gospel music isn't a style — it's testimony. "
            "'Testifying' is what happens when the music crosses from performance "
            "into witness."
        ),
        "lang_variants": {
            "de": "ZEUGNIS",
            "es": "TESTIFICAR",
            "pt": "TESTEMUNHAR",
            "ja": "証言",
            "zh": "见证",
            "it": "TESTIMONIANZA",
            "ar": "شهادة",
            "hi": "गवाही",
        },
    },
    "free_improvisation": {
        "panel": "MA",
        "origin": "Japanese 間",
        "meaning": (
            "The space where anything can happen. Ma (間) — the same concept as the "
            "monitor's vanished state — but here it's the terrain itself. Free "
            "improvisation is the music of ma: the space between notes IS the music."
        ),
        "lang_variants": {
            "de": "MA",
            "es": "MA",
            "pt": "MA",
            "ja": "間",
            "zh": "间",
            "it": "MA",
            "ar": "ما",
            "hi": "मा",
        },
    },

    # ── Legacy Terrains ───────────────────────────────────────────────
    "blues": {
        "panel": "BLUES DELTA",
        "origin": "English",
        "meaning": "Legacy terrain — see delta_blues for the full bathymetric chart.",
        "lang_variants": {},
    },
    "modal": {
        "panel": "RAGA",
        "origin": "English",
        "meaning": "Legacy terrain — see modal_jazz for the full bathymetric chart.",
        "lang_variants": {},
    },
    "classical": {
        "panel": "KONTRAPUNKT",
        "origin": "English",
        "meaning": "Legacy terrain — see classical_counterpoint for the full chart.",
        "lang_variants": {},
    },
    "free_jazz": {
        "panel": "MA",
        "origin": "English",
        "meaning": "Legacy terrain — see free_improvisation for the full chart.",
        "lang_variants": {},
    },

    # ── Voices ────────────────────────────────────────────────────────
    "piano": {
        "panel": "IVORY",
        "origin": "English",
        "meaning": "The keys — classical, jazz, everything in between.",
        "lang_variants": {},
    },
    "sax": {
        "panel": "BRASS",
        "origin": "English",
        "meaning": "The reed's voice — breath made metal.",
        "lang_variants": {},
    },
    "drums": {
        "panel": "SKIN",
        "origin": "English",
        "meaning": "The drumhead — rhythm's body.",
        "lang_variants": {},
    },
    "voice": {
        "panel": "THROAT",
        "origin": "English",
        "meaning": "The original instrument.",
        "lang_variants": {},
    },
    "guitar": {
        "panel": "WIRE",
        "origin": "English",
        "meaning": "The strings — steel or nylon.",
        "lang_variants": {},
    },
    "orchestra": {
        "panel": "CITY",
        "origin": "English",
        "meaning": "The orchestra — a city of instruments.",
        "lang_variants": {},
    },
    "bass": {
        "panel": "ROOT",
        "origin": "English",
        "meaning": "The foundation — where everything grows from.",
        "lang_variants": {},
    },
    "trumpet": {
        "panel": "BRAZEN",
        "origin": "English",
        "meaning": "The bell — bold, bright, brass.",
        "lang_variants": {},
    },

    # ── Morph Paths ───────────────────────────────────────────────────
    "blues_to_bebop": {
        "panel": "DELTA → SPEED",
        "origin": "English",
        "meaning": "From the muddy water to the angular city.",
        "lang_variants": {},
    },
    "classical_to_free": {
        "panel": "ORDER → MA",
        "origin": "English / Japanese",
        "meaning": "From architecture to empty space.",
        "lang_variants": {},
    },
    "techno_to_raga": {
        "panel": "KICK → SRUTI",
        "origin": "English / Sanskrit",
        "meaning": "From the machine pulse to the microtonal drone.",
        "lang_variants": {},
    },
    "jazz_to_silk": {
        "panel": "RAGA → SĪZHU",
        "origin": "Sanskrit / Mandarin",
        "meaning": "From American modal to Chinese classical.",
        "lang_variants": {},
    },

    # ── Morph Concepts ────────────────────────────────────────────────
    "blend": {
        "panel": "CROSSFADE",
        "origin": "English (audio engineering)",
        "meaning": "Smooth transition between two terrains at the constraint level.",
        "lang_variants": {},
    },
    "snap": {
        "panel": "MOORING SNAP",
        "origin": "English",
        "meaning": "The act of snapping a note to the nearest point on the constraint lattice.",
        "lang_variants": {},
    },
    "sensitivity": {
        "panel": "EAR",
        "origin": "English",
        "meaning": "How quickly the monitor reacts. The monitor's ear — 0=deaf, 1=omniscient.",
        "lang_variants": {},
    },
    "intervention": {
        "panel": "NUDGE",
        "origin": "English",
        "meaning": "The gentlest possible correction — not a rule, a suggestion.",
        "lang_variants": {},
    },
}


# ── Supported Languages ───────────────────────────────────────────────

SUPPORTED_LANGUAGES = ("en", "de", "es", "pt", "ja", "zh", "it", "ar", "hi")


# ── Public API ────────────────────────────────────────────────────────

def display_name(internal_name: str, lang: str = "en") -> str:
    """Get the panel display name for an internal API name.

    Args:
        internal_name: The snake_case API name (e.g. "funnel", "miles", "delta_blues").
        lang: Language code for localized display. Default "en" uses the
              multilingual panel name. Supported: en, de, es, pt, ja, zh, it, ar, hi.

    Returns:
        The display name, or the internal_name unchanged if not found.
    """
    entry = _REGISTRY.get(internal_name)
    if not entry:
        return internal_name

    if lang == "en":
        return entry["panel"]

    variant = entry.get("lang_variants", {}).get(lang)
    return variant if variant else entry["panel"]


def full_description(internal_name: str) -> str:
    """Get the full etymological description for an internal API name.

    Returns:
        A string like "PANEL_NAME (Origin) — Meaning..."
        or the internal_name if not found.
    """
    entry = _REGISTRY.get(internal_name)
    if not entry:
        return internal_name

    return f'{entry["panel"]} ({entry["origin"]}) — {entry["meaning"]}'


def origin(internal_name: str) -> str:
    """Get just the origin/etymology for an internal name."""
    entry = _REGISTRY.get(internal_name)
    return entry["origin"] if entry else internal_name


def meaning(internal_name: str) -> str:
    """Get just the meaning for an internal name."""
    entry = _REGISTRY.get(internal_name)
    return entry["meaning"] if entry else internal_name


def all_names() -> dict:
    """Return a snapshot of the full registry (read-only copy)."""
    import copy
    return copy.deepcopy(_REGISTRY)


def registered_names() -> list:
    """Return all registered internal names."""
    return sorted(_REGISTRY.keys())


def categories() -> dict:
    """Return internal names grouped by category."""
    return {
        "primitives": ["lattice_snap", "funnel", "is_laman", "consensus", "holonomy"],
        "modes": ["parker", "miles", "ellington", "basie", "goodman", "armstrong", "ella"],
        "monitor_states": [
            "flow_state", "error_rate", "consistency",
            "exploration_velocity", "energy", "energy_trajectory", "is_vanished",
        ],
        "terrain_properties": [
            "scale_degrees", "funnel_targets", "register_tendency",
            "chromatic_density", "typical_tempo", "characteristic_intervals",
            "rhythmic_skeletons", "rigidity", "blues_note",
        ],
        "terrains": [
            "delta_blues", "bebop", "bebop_rich", "modal_jazz",
            "classical_counterpoint", "bluegrass", "hip_hop_trap",
            "afro_cuban", "indian_raga", "chinese_silk_bamboo",
            "electronic_techno", "gospel", "free_improvisation",
            "blues", "modal", "classical", "free_jazz",
        ],
        "voices": ["piano", "sax", "drums", "voice", "guitar", "orchestra", "bass", "trumpet"],
        "morph_paths": [
            "blues_to_bebop", "classical_to_free",
            "techno_to_raga", "jazz_to_silk",
        ],
    }
