# -----------------------------------------------------------------------------
# CORE CONSTANTS
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = ['timestamp_board_ms', 'timestamp_server_ms', 'seq_id']
L_MAX = 5000.0
OUTAGE_THRESHOLD_MS = 2000
SENSITIVITY_DELTA = 0.10
R_C2_THRESHOLD_PCT = 80.0

# Вагові коефіцієнти (w_A, w_C, w_L, w_I)
WEIGHTS_SAIL_II = (0.35, 0.25, 0.25, 0.15)
WEIGHTS_SAIL_IV = (0.25, 0.30, 0.25, 0.20)

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION (i18n) DICTIONARY
# -----------------------------------------------------------------------------
TRANSLATIONS = {
    "Українська": {
        "language_selector": "🌐 Мова / Language",
        "main_header": "🛸 U-space C2 Readiness Diagnostic Validator",
        "sub_header": "B2B передпольотна експрес-діагностика та аналіз \"вузьких місць\" C2-лінку БАС (за вимогами Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Вхідні параметри та сценарій",
        "file_upload": "📁 Завантажити лог телеметрії (CSV)",
        "network_preset": "⚡ Пресет стандарту зв'язку / Network Preset",
        "scenario_preset": "🛸 Пресет операційного сценарію / Operation Scenario Preset",
        "preset_none": "-- Оберіть пресет --",
        "scenario_title": "1. Сценарій U-space та Геозона",
        "corridor_width": "Ширина коридору OIV (м)",
        "sail_class": "Клас ризику SORA 2.5 (SAIL)",
        "sail_low": "SAIL II (Низький міський ризик)",
        "sail_high": "SAIL IV (Високий міський ризик)",
        "latency_threshold": "Нормативний поріг затримки L_threshold (мс)",
        "uas_specs": "2. Паспортні характеристики БАС",
        "telemetry_freq": "Частота відправки телеметрії f_up (Гц)",
        "gnss_mode": "Режим супутникової навігації",
        "gnss_rtk": "GNSS RTK (Навігація PNT)",
        "gnss_3d": "GNSS 3D Fix (Навігація PNT)",
        "run_button": "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ",
        "log_loaded": "✅ Лог телеметрії успішно завантажено!",
        "demo_log": "ℹ️ Використовується демо-лог польоту у міському каньйоні.",
        "load_error": "🚨 Файл некоректний. Обов'язкові колонки:",
        "welcome_message": "👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику.",
        "integral_indicator": "Інтегральний показник $R_{C2}$",
        "readiness_level": "Рівень готовності C2-лінку",
        "threshold_text": "від порогу (80%)",
        "verdict_header": "Вердикт передпольотного тестування",
        "approved": "✅ APPROVED — C2-лінк готовий до виконання місії у коридорі {:.0f} м",
        "approved_desc": "БАС відповідає вимогам авторизації U-plan. Імовірність втрати відповідності під час польоту не перевищує припустимі норми.",
        "rejected": "🚨 REJECTED — ВИЯВЛЕНО ВУЗЬКЕ МІСЦЕ (BOTTLENECK)",
        "rejected_desc": "C2-лінк у поточній конфігурації має підвищений ризик деградації. Потрібна коригувальна дія до вильоту.",
        "availability": "Доступність (Availability)",
        "continuity": "Безперервність (Continuity)",
        "latency": "Затримка (P95 Latency)",
        "integrity": "Цілісність C2 (Integrity)",
        "packet_loss": "Втрата пакетів (Packet Loss)",
        "p95": "P95:",
        "dropped": "Пропущено:",
        "packets": "пк",
        "availability_target": "Ціль: >98.0%",
        "continuity_target": "Ціль: >99.0%",
        "integrity_target": "Ціль: >99.5%",
        "tab_analysis": "📊 Ботлнек-Аналіз та Графіки",
        "tab_sensitivity": "🔬 Аналіз Чутливості (Sensitivity)",
        "tab_telemetry": "🗺️ Лог та Маршрут Місії",
        "tab_monte_carlo": "🎲 Симуляція Монте-Карло",
        "latency_distribution": "Розподіл затримок мережі (End-to-End Latency)",
        "latency_histogram": "Гістограма затримок у каналі зв'язку",
        "latency_xlabel": "Затримка (мс)",
        "latency_ylabel": "Кількість пакетів",
        "threshold_annotation": "Поріг U-space ({} мс)",
        "radar_title": "Радарна діаграма спроможностей C2",
        "radar_categories": ["Доступність (A)", "Безперервність (C)", "Норм. Затримка (f_L)", "Цілісність (I)"],
        "current_board": "Поточний борт",
        "min_threshold": "Мінімальний поріг U-space",
        "diagnostic_report": "📋 Bottleneck Diagnostic Report",
        "bottleneck_latency": "**🚨 Вузьке місце:** Затримка за квантилем P95 ({:.1f} мс) перевищує нормативний поріг U-space ({} мс).",
        "action_latency": "**🛠️ Рекомендована дія:** Спробуйте використати канал зв'язку з меншою затримкою (наприклад, 5G NR) або перегляньте архітектуру передачі даних.",
        "bottleneck_loss": "**🚨 Вузьке місце:** Рівень втрати пакетів ({:.2f}%) занадто високий для міського середовища.",
        "action_loss": "**🛠️ Рекомендована дія:** Увімкніть дублювання телеметричного каналу (Hybrid Multilink) або перевірте якість антени/модему.",
        "status_ok": "**✅ Стан C2-лінку задовільний:** Параметри затримок, втрат та доступності знаходяться в межах норми для обраного SAIL рівня.",
        "flight_map": "Карта маршруту польоту БАС",
        "raw_log": "Сирий фрагмент логу телеметрії",
        "monte_carlo_title": "Розподіл R_C2 за результатами Монте-Карло (1000 ітерацій)",
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Кількість",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Магістерський дипломний проєкт KSE | Розробник: Студент ОП 'Безпілотні літальні апарати' | Спеціальність G12 (134)"
    },
    "English": {
        "language_selector": "🌐 Language / Мова",
        "main_header": "🛸 U-space C2 Readiness Diagnostic Validator",
        "sub_header": "B2B pre-flight express diagnostics and C2-link bottleneck analysis for UAS (according to Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Input Parameters and Scenario",
        "file_upload": "📁 Upload Telemetry Log (CSV)",
        "network_preset": "⚡ Network Standard Preset",
        "scenario_preset": "🛸 Operation Scenario Preset",
        "preset_none": "-- Select Preset --",
        "scenario_title": "1. U-space Scenario and Geozone",
        "corridor_width": "OIV Corridor Width (m)",
        "sail_class": "SORA 2.5 Risk Class (SAIL)",
        "sail_low": "SAIL II (Low Urban Risk)",
        "sail_high": "SAIL IV (High Urban Risk)",
        "latency_threshold": "Regulatory Latency Threshold L_threshold (ms)",
        "uas_specs": "2. UAS Passport Characteristics",
        "telemetry_freq": "Telemetry Upload Frequency f_up (Hz)",
        "gnss_mode": "Satellite Navigation Mode",
        "gnss_rtk": "GNSS RTK (PNT Navigation)",
        "gnss_3d": "GNSS 3D Fix (PNT Navigation)",
        "run_button": "▶ CALCULATE & SIMULATE",
        "log_loaded": "✅ Telemetry log successfully loaded!",
        "demo_log": "ℹ️ Using demo flight log in urban canyon.",
        "load_error": "🚨 Invalid file. Required columns:",
        "welcome_message": "👈 Configure input parameters or select presets in the sidebar and press the [▶ CALCULATE & SIMULATE] button to start the diagnostics.",
        "integral_indicator": "Integral Indicator $R_{C2}$",
        "readiness_level": "C2-Link Readiness Level",
        "threshold_text": "from threshold (80%)",
        "verdict_header": "Pre-flight Testing Verdict",
        "approved": "✅ APPROVED — C2-link ready for mission in {:.0f} m corridor",
        "approved_desc": "UAS meets U-plan authorization requirements. Probability of compliance loss during flight does not exceed acceptable norms.",
        "rejected": "🚨 REJECTED — BOTTLENECK DETECTED",
        "rejected_desc": "C2-link in current configuration has increased degradation risk. Corrective action required before takeoff.",
        "availability": "Availability",
        "continuity": "Continuity",
        "latency": "P95 Latency",
        "integrity": "C2 Integrity",
        "packet_loss": "Packet Loss",
        "p95": "P95:",
        "dropped": "Dropped:",
        "packets": "pkt",
        "availability_target": "Target: >98.0%",
        "continuity_target": "Target: >99.0%",
        "integrity_target": "Target: >99.5%",
        "tab_analysis": "📊 Bottleneck Analysis & Charts",
        "tab_sensitivity": "🔬 Sensitivity Analysis",
        "tab_telemetry": "MAP Log & Mission Route",
        "tab_monte_carlo": "🎲 Monte Carlo Simulation",
        "latency_distribution": "Network Latency Distribution (End-to-End)",
        "latency_histogram": "Latency Histogram in Communication Channel",
        "latency_xlabel": "Latency (ms)",
        "latency_ylabel": "Packet Count",
        "threshold_annotation": "U-space Threshold ({} ms)",
        "radar_title": "C2 Capabilities Radar Chart",
        "radar_categories": ["Availability (A)", "Continuity (C)", "Norm. Latency (f_L)", "Integrity (I)"],
        "current_board": "Current Board",
        "min_threshold": "Minimum U-space Threshold",
        "diagnostic_report": "📋 Bottleneck Diagnostic Report",
        "bottleneck_latency": "**🚨 Bottleneck:** P95 latency ({:.1f} ms) exceeds U-space regulatory threshold ({} ms).",
        "action_latency": "**🛠️ Recommended Action:** Try using a lower latency communication link (e.g., 5G NR) or review the data transmission architecture.",
        "bottleneck_loss": "**🚨 Bottleneck:** Packet loss rate ({:.2f}%) is too high for an urban environment.",
        "action_loss": "**🛠️ Recommended Action:** Enable telemetry channel redundancy (Hybrid Multilink) or check antenna/modem quality.",
        "status_ok": "**✅ C2-link Status Satisfactory:** Latency, loss, and availability parameters are within norms for the selected SAIL level.",
        "flight_map": "UAS Flight Route Map",
        "raw_log": "Raw Telemetry Log Fragment",
        "monte_carlo_title": "R_C2 Distribution from Monte Carlo Results (1000 iterations)",
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Count",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Master's Thesis Project KSE | Developer: Student of 'Unmanned Aerial Vehicles' Program | Specialty G12 (134)"
    }
}

# -----------------------------------------------------------------------------
# PRESET CONFIGURATIONS
# -----------------------------------------------------------------------------
NETWORK_PRESETS = {
    "4G LTE (Cat. 4/6)": {
        "params": {"l_threshold": 1000, "f_up": 2.5},
        "help": {
            "ua": "Стандартний стільниковий зв'язок для BVLOS. Широке покриття, але можливі затримки (jitter) при handover між сотами.",
            "en": "Standard cellular communication for BVLOS. Wide coverage, but potential for jitter during handover between cells."
        }
    },
    "5G NR (URLLC Slice)": {
        "params": {"l_threshold": 500, "f_up": 5.0},
        "help": {
            "ua": "Виділений мережевий 'слайс' 5G з пріоритетом URLLC для критичних місій, UAM. Гарантована низька затримка.",
            "en": "Dedicated 5G network 'slice' with URLLC priority for critical missions, UAM. Guaranteed low latency."
        }
    },
    "SDR (ISM Band)": {
        "params": {"l_threshold": 200, "f_up": 2.0},
        "help": {
            "ua": "Програмно-визначене радіо в неліцензованому діапазоні (2.4/5.8 ГГц). Низька затримка, але обмежена дальність і високий ризик завад у місті.",
            "en": "Software-Defined Radio in the unlicensed ISM band (2.4/5.8 GHz). Low latency, but limited range and high risk of interference in urban areas."
        }
    },
    "SatCom (L-Band)": {
        "params": {"l_threshold": 1500, "f_up": 1.0},
        "help": {
            "ua": "Супутниковий зв'язок L-діапазону для місій поза зоною покриття стільникових мереж (BRLOS). Глобальне покриття, але значна затримка.",
            "en": "L-band satellite communication for missions beyond cellular coverage (BRLOS). Global coverage, but significant latency."
        }
    }
}

SCENARIO_PRESETS = {
    "BVLOS Urban (SAIL IV)": {
        "params": {"corridor_width": 15.0, "l_threshold": 500, "f_up": 2.5, "sail": "SAIL IV"},
        "help": {
            "ua": "Політ у щільній міській забудові (доставка, інспекція). Вузький коридор (15 м), високі вимоги до надійності, SAIL IV.",
            "en": "Flight in dense urban environments (delivery, inspection). Narrow corridor (15 m), high reliability requirements, SAIL IV."
        }
    },
    "BVLOS Rural (SAIL II)": {
        "params": {"corridor_width": 25.0, "l_threshold": 1000, "f_up": 2.0, "sail": "SAIL II"},
        "help": {
            "ua": "Політ над сільською місцевістю з низькою щільністю населення. Ширший коридор (25 м), стандартні вимоги, SAIL II.",
            "en": "Flight over rural areas with low population density. Wider corridor (25 m), standard requirements, SAIL II."
        }
    },
    "VLOS (SAIL II)": {
        "params": {"corridor_width": 40.0, "l_threshold": 2000, "f_up": 1.0, "sail": "SAIL II"},
        "help": {
            "ua": "Політ у межах прямої видимості. Низький ризик, широкий коридор (40 м), менш суворі вимоги до затримки, SAIL II.",
            "en": "Flight within visual line of sight. Low risk, wide corridor (40 m), less strict latency requirements, SAIL II."
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