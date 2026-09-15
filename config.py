# -----------------------------------------------------------------------------
# CORE CONSTANTS
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = ['timestamp_board_ms', 'timestamp_server_ms', 'seq_id']
L_MAX = 5000.0
OUTAGE_THRESHOLD_MS = 2000
SENSITIVITY_DELTA = 0.10
R_C2_THRESHOLD_PCT = 80.0

# Metric Target Thresholds
AVAILABILITY_TARGET = 0.98  # Research/Engineering target
CONTINUITY_TARGET = 0.99    # Research/Engineering target
INTEGRITY_TARGET = 0.995    # Research/Engineering target
COMPLETENESS_TARGET = INTEGRITY_TARGET  # 0.995 (99.5% цільова повнота телеметрії)
LATENCY_TARGET_MS = 500.0   # 500 ms

# Verdict Status Constants
STATUS_PASS = "PASS (Технічним критеріям відповідає)"
STATUS_CONDITIONAL = "CONDITIONAL (Потребує додаткових даних або усунення завад)"
STATUS_FAIL = "FAIL (Критичні критерії не виконано)"
STATUS_NOT_ASSESSABLE = "NOT ASSESSABLE (Недостатньо даних у логу)"

WEIGHTS_SAIL_II = (0.35, 0.25, 0.25, 0.15)
WEIGHTS_SAIL_IV = (0.25, 0.30, 0.25, 0.20)

# Configuration Validation Constants
MIN_OUTAGE_GAP_S = 2.0

# Parameter Metadata with Sources and Provenance
PARAMETER_METADATA = {
    "AVAILABILITY_TARGET": {
        "value": 0.98,
        "source": "Research/Engineering target",
        "provenance": "Derived from U-space operational requirements analysis"
    },
    "CONTINUITY_TARGET": {
        "value": 0.99,
        "source": "Research/Engineering target",
        "provenance": "Based on SORA 2.5 continuity requirements for SAIL II-IV operations"
    },
    "INTEGRITY_TARGET": {
        "value": 0.995,
        "source": "Research/Engineering target",
        "provenance": "Derived from U-space packet delivery integrity requirements"
    },
    "L_MAX": {
        "value": 5000.0,
        "source": "Upper degradation bound",
        "provenance": "Engineering assumption for latency normalization function"
    },
    "LATENCY_TARGET_MS": {
        "value": 500.0,
        "source": "U-space regulatory threshold",
        "provenance": "EU Regulation 2021/664 U-space performance requirements"
    }
}

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION (i18n) DICTIONARY
# -----------------------------------------------------------------------------
TRANSLATIONS = {
    "Українська": {
        "language_selector": "🌐 Мова / Language",
        "main_header": "🛸 U-space C2 Technical Readiness Screening Tool",
        "sub_header": "B2B передпольотна експрес-діагностика та аналіз \"вузьких місць\" C2-лінку БАС (за вимогами Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Вхідні параметри та сценарій",
        "file_upload": "📁 Завантажити лог телеметрії (CSV)",
        "network_preset": "⚡ Пресет стандарту зв'язку / Network Preset",
        "scenario_preset": "🛸 Пресет операційного сценарію / Operation Scenario Preset",
        "gnss_mode": "🛰️ Режим супутникової навігації (GNSS)",
        "preset_none": "-- Оберіть пресет --",
        "sail_class": "Клас ризику SORA 2.5 (SAIL)",
        "latency_threshold": "Нормативний поріг затримки L_threshold (мс)",
        "run_button": "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ / CALCULATE & SIMULATE",
        "log_loaded": "✅ Лог телеметрії успішно завантажено!",
        "demo_log": "ℹ️ Використовується демо-лог польоту.",
        "load_error": "🚨 Файл некоректний. Обов'язкові колонки:",
        "welcome_message": "👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику.",
        "integral_indicator": "Інтегральний показник $R_{C2}$",
        "readiness_level": "Рівень готовності C2-лінку",
        "threshold_text": "від порогу (80%)",
        "verdict_header": "Вердикт передпольотного тестування",
        "approved": "✅ PASS — C2-лінк готовий до виконання місії у коридорі {:.0f} м",
        "rejected": "🚨 FAIL — ВИЯВЛЕНО ВУЗЬКЕ МІСЦЕ (BOTTLENECK)",
        "availability": "Доступність (Availability)",
        "continuity": "Безперервність (Continuity)",
        "latency": "Затримка (P95 Latency)",
        "integrity": "Цілісність C2 (Integrity)",
        "availability_target": "Ціль: >98.0%",
        "continuity_target": "Ціль: >99.0%",
        "integrity_target": "Ціль: >99.5%",
        "availability_help": "Відсоток часу, протягом якого C2-канал підключений та готовий до передачі даних.",
        "continuity_help": "Ймовірність збереження з'єднання без незапланованих розривів чи збоїв хендоверу під час місії.",
        "integrity_help": "Частка пакетів, доставлених вчасно (затримка ≤ L_max), без втрат та спотворень.",
        "latency_help": "95-й перцентиль затримки. 95% пакетів доставлені швидше за вказаний час.",
        "tab_analysis": "📊 Ботлнек-Аналіз та Графіки",
        "tab_sensitivity": "🔬 Аналіз Чутливості (Sensitivity)",
        "tab_telemetry": "🗺️ Лог та Маршрут Місії",
        "tab_monte_carlo": "🎲 Симуляція Монте-Карло",
        "latency_distribution": "Розподіл затримок мережі (End-to-End Latency)",
        "latency_xlabel": "Затримка (мс)",
        "latency_ylabel": "Кількість пакетів",
        "threshold_annotation": "Поріг U-space ({} мс)",
        "radar_title": "Радарна діаграма спроможностей C2",
        "radar_categories": ["Доступність (A)", "Безперервність (C)", "Норм. Затримка (f_L)", "Цілісність (I)"],
        "current_board": "Поточний борт",
        "min_threshold": "Мінімальний поріг U-space",
        "flight_map": "Карта маршруту польоту БАС",
        "raw_log": "Сирий фрагмент логу телеметрії",
        "monte_carlo_title": "Розподіл R_C2 за результатами Монте-Карло (1000 ітерацій)",
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Кількість",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Магістерський дипломний проєкт KSE | ОП 'Безпілотні літальні апарати' | Спеціальність G12 (134)"
    },
    "English": {
        "language_selector": "🌐 Language / Мова",
        "main_header": "🛸 U-space C2 Technical Readiness Screening Tool",
        "sub_header": "B2B pre-flight express diagnostics and C2-link bottleneck analysis for UAS (Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Input Parameters and Scenario",
        "file_upload": "📁 Upload Telemetry Log (CSV)",
        "network_preset": "⚡ Network Standard Preset",
        "scenario_preset": "🛸 Operation Scenario Preset",
        "gnss_mode": "🛰️ Satellite Navigation Mode (GNSS)",
        "preset_none": "-- Select Preset --",
        "sail_class": "SORA 2.5 Risk Class (SAIL)",
        "latency_threshold": "Regulatory Latency Threshold L_threshold (ms)",
        "run_button": "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ / CALCULATE & SIMULATE",
        "log_loaded": "✅ Telemetry log successfully loaded!",
        "demo_log": "ℹ️ Using demo flight log.",
        "load_error": "🚨 Invalid file. Required columns:",
        "welcome_message": "👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику.",
        "integral_indicator": "Integral Indicator $R_{C2}$",
        "readiness_level": "C2-Link Readiness Level",
        "threshold_text": "from threshold (80%)",
        "verdict_header": "Pre-flight Testing Verdict",
        "approved": "✅ PASS — C2-link ready for mission in {:.0f} m corridor",
        "rejected": "🚨 FAIL — BOTTLENECK DETECTED",
        "availability": "Availability",
        "continuity": "Continuity",
        "latency": "P95 Latency",
        "integrity": "C2 Integrity",
        "availability_target": "Target: >98.0%",
        "continuity_target": "Target: >99.0%",
        "integrity_target": "Target: >99.5%",
        "availability_help": "Percentage of operational time during which the C2 link is connected and ready for data transmission.",
        "continuity_help": "Probability of maintaining the link without unintended terminations or handover failures during the mission.",
        "integrity_help": "Ratio of packets delivered within deadline (latency ≤ L_max), without loss or corruption.",
        "latency_help": "95th percentile latency. 95% of packets were delivered faster than this duration.",
        "tab_analysis": "📊 Bottleneck Analysis & Charts",
        "tab_sensitivity": "🔬 Sensitivity Analysis",
        "tab_telemetry": "🗺️ MAP Log & Mission Route",
        "tab_monte_carlo": "🎲 Monte Carlo Simulation",
        "latency_distribution": "Network Latency Distribution (End-to-End)",
        "latency_xlabel": "Latency (ms)",
        "latency_ylabel": "Packet Count",
        "threshold_annotation": "U-space Threshold ({} ms)",
        "radar_title": "C2 Capabilities Radar Chart",
        "radar_categories": ["Availability (A)", "Continuity (C)", "Norm. Latency (f_L)", "Integrity (I)"],
        "current_board": "Current Board",
        "min_threshold": "Minimum U-space Threshold",
        "flight_map": "UAS Flight Route Map",
        "raw_log": "Raw Telemetry Log Fragment",
        "monte_carlo_title": "R_C2 Distribution from Monte Carlo Results (1000 iterations)",
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Count",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Master's Thesis Project KSE | Unmanned Aerial Vehicles Program"
    }
}

# -----------------------------------------------------------------------------
# NETWORK PRESETS (ТЕХНОЛОГІЧНІ ХАРАКТЕРИСТИКИ КАНАЛУ)
# -----------------------------------------------------------------------------
NETWORK_PRESETS = {
    "ISM RF 2.4/5.8 GHz (Direct RLOS | <3km | 10-30ms)": {
        "params": {"l_threshold": 200, "f_up": 2.0},
        "help": {
            "ua": "Прямий радіоканал для VLOS. Низька затримка, але обмежена дальність і ризик завад у місті.",
            "en": "Direct radio link for VLOS. Low latency, but limited range and risk of urban interference."
        }
    },
    "4G LTE Cellular (Public Band 3/7/20 | 80-200ms)": {
        "params": {"l_threshold": 1000, "f_up": 2.5},
        "help": {
            "ua": "Публічна стільникова мережа для BVLOS. Широке покриття, наявність джиттеру при handover.",
            "en": "Public cellular network for BVLOS. Broad coverage, jitter during handover."
        }
    },
    "5G NR + QoS Slicing (Sub-6GHz Band n78 | 15-50ms)": {
        "params": {"l_threshold": 300, "f_up": 5.0},
        "help": {
            "ua": "Виділений мережевий слайс із пріоритетом URLLC для критичних міських місій та UAM.",
            "en": "Dedicated network slice with URLLC priority for critical urban missions and UAM."
        }
    },
    "SatCom L-Band (Iridium/Inmarsat | BRLOS | 400-1200ms)": {
        "params": {"l_threshold": 1500, "f_up": 1.0},
        "help": {
            "ua": "Супутниковий канал для віддалених місій. Глобальне покриття, але значна затримка.",
            "en": "Satellite channel for remote missions. Global coverage, but significant latency."
        }
    },
    "Hybrid Multilink (Dual-SIM 4G/5G + SatCom | Redundant)": {
        "params": {"l_threshold": 500, "f_up": 4.0},
        "help": {
            "ua": "Дубльований агрегований канал із динамічним перемиканням при деградації.",
            "en": "Redundant aggregated channel with dynamic failover upon degradation."
        }
    }
}

# -----------------------------------------------------------------------------
# OPERATION SCENARIO PRESETS (НОРМАТИВНІ ВИМОГИ МІСІЇ SORA / SAIL)
# -----------------------------------------------------------------------------
SCENARIO_PRESETS = {
    "VLOS (Visual Line of Sight)": {
        "params": {"corridor_width": 40.0, "l_threshold": 2000, "f_up": 1.0, "sail": "SAIL II"},
        "help": {
            "ua": "Політ у межах прямої видимості. Широкий коридор (40 м), затримка до 2000 мс, SAIL II.",
            "en": "Visual Line of Sight flight. Wide 40m corridor, up to 2000 ms latency, SAIL II."
        }
    },
    "EVLOS (Extended Visual Line of Sight)": {
        "params": {"corridor_width": 30.0, "l_threshold": 1500, "f_up": 1.5, "sail": "SAIL II"},
        "help": {
            "ua": "Розширений політ за участі візуальних спостерігачів. Коридор 30 м, затримка до 1500 мс, SAIL II.",
            "en": "Extended VLOS with observers. 30m corridor, up to 1500 ms latency, SAIL II."
        }
    },
    "BVLOS Suburban (Low Density / Rural)": {
        "params": {"corridor_width": 25.0, "l_threshold": 1000, "f_up": 2.0, "sail": "SAIL II"},
        "help": {
            "ua": "Політ поза межами видимості над передмістям чи сільською місцевістю. Коридор 25 м, затримка 1000 мс, SAIL II.",
            "en": "BVLOS flight in suburban or rural low-density areas. 25m corridor, 1000 ms latency, SAIL II."
        }
    },
    "BVLOS Urban Canyon (Delivery / Dense VLL)": {
        "params": {"corridor_width": 15.0, "l_threshold": 500, "f_up": 2.5, "sail": "SAIL IV"},
        "help": {
            "ua": "Політ у щільній міській забудові (доставка, інспекція). Вузький коридор (15 м), затримка 500 мс, SAIL IV.",
            "en": "Dense urban VLL operations (delivery, inspection). Narrow 15m corridor, 500 ms latency, SAIL IV."
        }
    },
    "UAM / eVTOL Passenger Mobility": {
        "params": {"corridor_width": 10.0, "l_threshold": 100, "f_up": 5.0, "sail": "SAIL IV"},
        "help": {
            "ua": "Пасажирські та важкі вантажні UAM/eVTOL перевезення. Вузький коридор (10 м), сувора затримка (100 мс), SAIL IV.",
            "en": "Passenger and cargo UAM/eVTOL transport. Ultra-narrow 10m corridor, 100 ms latency limit, SAIL IV."
        }
    }
}

OPERATION_PRESETS = SCENARIO_PRESETS

# -----------------------------------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------------------------------
CUSTOM_CSS = '''
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #0F2C59; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #4F709C; margin-bottom: 25px; }
    .metric-card { background-color: #F8F9FA; border-radius: 10px; padding: 15px; border-left: 5px solid #0F2C59; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .status-approved { background-color: #E8F5E9; color: #2E7D32; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 1.2rem; border: 1px solid #A5D6A7; }
    .status-rejected { background-color: #FFEBEE; color: #C62828; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 1.2rem; border: 1px solid #EF9A9A; }
</style>
'''

# -----------------------------------------------------------------------------
# CONFIGURATION VALIDATION FUNCTIONS
# -----------------------------------------------------------------------------
def validate_configuration():
    """Validate configuration parameters for scientific consistency."""
    # Ensure L_MAX > LATENCY_TARGET_MS for proper normalization
    if L_MAX <= LATENCY_TARGET_MS:
        raise ValueError(f"L_MAX ({L_MAX}) must be greater than LATENCY_TARGET_MS ({LATENCY_TARGET_MS}) for proper latency normalization")
    
    # Validate MIN_OUTAGE_GAP_S is positive
    if MIN_OUTAGE_GAP_S <= 0:
        raise ValueError(f"MIN_OUTAGE_GAP_S ({MIN_OUTAGE_GAP_S}) must be positive")
    
    # Validate target thresholds are within valid range (0-1)
    for param_name in ["AVAILABILITY_TARGET", "CONTINUITY_TARGET", "INTEGRITY_TARGET"]:
        value = globals()[param_name]
        if not 0 <= value <= 1:
            raise ValueError(f"{param_name} ({value}) must be between 0 and 1")
    
    return True