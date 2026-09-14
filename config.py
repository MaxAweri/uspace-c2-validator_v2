# config.py

# -----------------------------------------------------------------------------
# CORE CONSTANTS
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = ['timestamp_server_ms', 'timestamp_board_ms', 'seq_id', 'gnss_fix_type', 'lat', 'lon']
L_MAX = 5000.0
OUTAGE_THRESHOLD_MS = 2000
SENSITIVITY_DELTA = 0.10
R_C2_THRESHOLD_PCT = 80.0

# Вагові коефіцієнти (w_A, w_C, w_L, w_I)
WEIGHTS_SAIL_LOW = (0.35, 0.25, 0.25, 0.15)
WEIGHTS_SAIL_HIGH = (0.25, 0.30, 0.25, 0.20)


# -----------------------------------------------------------------------------
# INTERNATIONALIZATION (i18n) DICTIONARY
# -----------------------------------------------------------------------------
TRANSLATIONS = {
    "Українська": {
        "language_selector": "🌐 Мова / Language",
        "main_title": "🛸 U-space C2 Readiness Diagnostic Validator",
        "subtitle": "B2B передпольотна експрес-діагностика та аналіз \"вузьких місць\" C2-лінку БАС (за вимогами Regulation EU 2021/664)",
        "input_params": "⚙️ Вхідні параметри та сценарій",
        "upload_file": "📁 Завантажити лог телеметрії (CSV)",
        "scenario_title": "1. Сценарій U-space та Геозона",
        "corridor_width": "Ширина коридору OIV (м)",
        "sail_class": "Клас ризику SORA 2.5 (SAIL)",
        "sail_low": "SAIL II (Низький міський ризик)",
        "sail_high": "SAIL IV (Високий міський ризик)",
        "latency_threshold": "Нормативний поріг затримки L_threshold (мс)",
        "uas_specs": "2. Паспортні характеристики БАС",
        "telemetry_freq": "Частота відправки телеметрії f_up (Гц)",
        "gnss_mode": "Режим супутникової навігації",
        "gnss_rtk": "GNSS RTK (0.8 - 2.0 м)",
        "gnss_3d": "GNSS 3D Fix (3.0 - 6.0 м)",
        "integral_indicator": "Інтегральний показник $R_{C2}$",
        "readiness_level": "Рівень готовності C2-лінку",
        "verdict_title": "Вердикт передпольотного тестування",
        "approved": "✅ APPROVED — C2-лінк готовий до виконання місії у коридорі {:.0f} м",
        "approved_desc": "БАС відповідає вимогам авторизації U-plan. Імовірність втрати відповідності під час польоту не перевищує припустимі норми.",
        "rejected": "🚨 REJECTED — ВИЯВЛЕНО ВУЗЬКЕ МІСЦЕ (BOTTLENECK)",
        "rejected_desc": "C2-лінк у поточній конфігурації має підвищений ризик деградації. Потрібна коригувальна дія до вильоту.",
        "availability": "Доступність (Availability)",
        "continuity": "Безперервність (Continuity)",
        "latency": "Затримка (Mean Latency)",
        "packet_loss": "Втрата пакетів (Packet Loss)",
        "integrity": "Цілісність (Integrity)",
        "target": "Ціль:",
        "p95": "P95:",
        "dropped": "Пропущено:",
        "packets": "пк",
        "tab_analysis": "📊 Ботлнек-Аналіз та Графіки",
        "tab_sensitivity": "🔬 Аналіз Чутливості (Sensitivity)",
        "tab_telemetry": "🗺️ Лог та Маршрут Місії",
        "tab_monte_carlo": "🎲 Симуляція Монте-Карло",
        "latency_distribution": "Розподіл затримок мережі (End-to-End Latency)",
        "latency_histogram": "Гістограма затримок у каналі зв'язку",
        "latency_ms": "Затримка (мс)",
        "packet_count": "Кількість пакетів",
        "threshold_line": "Поріг U-space (1000 мс)",
        "radar_title": "Радарна діаграма спроможностей C2",
        "current_board": "Поточний борт",
        "min_threshold": "Мінімальний поріг U-space",
        "bottleneck_localization": "Локалізація Parameter Bottlenecks",
        "sensitivity_title": "Коефіцієнти чутливості за варіації параметрів на +10%",
        "latency_param": "Затримка (Latency)",
        "loss_param": "Втрата пакетів (Loss)",
        "continuity_param": "Безперервність (Continuity)",
        "impact_r_c2": "Вплив на R_C2 (% зміни)",
        "diagnostic_report": "📋 Bottleneck Diagnostic Report",
        "bottleneck_latency": "**🚨 Вузьке місце:** Середня затримка мережі ({:.1f} мс) перевищує нормативний поріг U-space ({} мс).",
        "action_latency": "**🛠️ Рекомендована дія:** Спробуйте використати канал зв'язку з меншою затримкою (наприклад, 5G NR) або перегляньте архітектуру передачі даних.",
        "bottleneck_loss": "**🚨 Вузьке місце:** Рівень втрати пакетів ({:.2f}%) занадто високий для міського середовища.",
        "action_loss": "**🛠️ Рекомендована дія:** Увімкніть дублювання телеметричного каналу (Hybrid Multilink) або перевірте якість антени/модему.",
        "status_ok": "**✅ Стан C2-лінку задовільний:** Параметри затримок, втрат та доступності знаходяться в межах норми для обраного SAIL рівня.",
        "flight_map": "Карта маршруту польоту БАС",
        "raw_log": "Сирий фрагмент логу телеметрії",
        "mc_distribution": "Розподіл R_C2 за результатами Монте-Карло (1000 ітерацій)",
        "mc_probability": "Ймовірність P(R_C2 ≥ 80%)",
        "log_loaded": "✅ Лог телеметрії успішно завантажено!",
        "demo_log": "ℹ️ Використовується демо-лог польоту у міському каньйоні.",
        "load_error": "Помилка завантаження тестового файлу логу.",
        "main_header": "🛸 U-space C2 Readiness Diagnostic Validator",
        "sub_header": "B2B передпольотна експрес-діагностика та аналіз \"вузьких місць\" C2-лінку БАС (за вимогами Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Вхідні параметри та сценарій",
        "file_upload": "📁 Завантажити лог телеметрії (CSV)",
        "scenario_header": "1. Сценарій U-space та Геозона",
        "threshold_latency": "Нормативний поріг затримки L_threshold (мс)",
        "file_loaded": "✅ Лог телеметрії успішно завантажено!",
        "file_error": "Помилка завантаження тестового файлу логу.",
        "threshold_text": "від порогу (80%)",
        "verdict_header": "Вердикт передпольотного тестування",
        "availability_target": "Ціль: >98.0%",
        "continuity_target": "Ціль: >99.0%",
        "integrity_target_rtk": "Ціль (RTK): >95%",
        "integrity_target_3d": "Ціль (3D Fix): >99%",
        "latency_xlabel": "Затримка (мс)",
        "latency_ylabel": "Кількість пакетів",
        "threshold_annotation": "Поріг U-space ({} мс)",
        "radar_categories": ["Доступність (A)", "Безперервність (C)", "Норм. Затримка (f_L)", "Цілісність (I)"],
        "sensitivity_params": ["Затримка (Latency)", "Втрата пакетів (Loss)", "Безперервність (Continuity)"],
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Кількість",
        "monte_carlo_title": "Розподіл R_C2 за результатами Монте-Карло (1000 ітерацій)",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Магістерський дипломний проєкт KSE | Розробник: Студент ОП 'Безпілотні літальні апарати' | Спеціальність G12 (134)",
        "network_preset": "⚡ Пресет стандарту зв'язку / Network Preset",
        "operation_preset": "🛸 Пресет операційного сценарію / Operation Scenario Preset",
        "preset_none": "-- Оберіть пресет --",
        "preset_vlos": "VLOS (Visual Line of Sight)",
        "preset_evlos": "EVLOS (Extended Visual Line of Sight)",
        "preset_bvlos_suburban": "BVLOS Suburban (Low Density / Rural)",
        "preset_bvlos_urban": "BVLOS Urban Canyon (Delivery / Dense VLL)",
        "preset_uam": "UAM / eVTOL Passenger Mobility",
        "run_button": "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ",
        "welcome_message": "👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику."
    },
    "English": {
        "language_selector": "🌐 Language / Мова",
        "main_title": "🛸 U-space C2 Readiness Diagnostic Validator",
        "subtitle": "B2B pre-flight express diagnostics and C2-link bottleneck analysis for UAS (according to Regulation EU 2021/664)",
        "input_params": "⚙️ Input Parameters and Scenario",
        "upload_file": "📁 Upload Telemetry Log (CSV)",
        "scenario_title": "1. U-space Scenario and Geozone",
        "corridor_width": "OIV Corridor Width (m)",
        "sail_class": "SORA 2.5 Risk Class (SAIL)",
        "sail_low": "SAIL II (Low Urban Risk)",
        "sail_high": "SAIL IV (High Urban Risk)",
        "latency_threshold": "Regulatory Latency Threshold L_threshold (ms)",
        "uas_specs": "2. UAS Passport Characteristics",
        "telemetry_freq": "Telemetry Upload Frequency f_up (Hz)",
        "gnss_mode": "Satellite Navigation Mode",
        "gnss_rtk": "GNSS RTK (0.8 - 2.0 m)",
        "gnss_3d": "GNSS 3D Fix (3.0 - 6.0 m)",
        "integral_indicator": "Integral Indicator $R_{C2}$",
        "readiness_level": "C2-Link Readiness Level",
        "verdict_title": "Pre-flight Testing Verdict",
        "approved": "✅ APPROVED — C2-link ready for mission in {:.0f} m corridor",
        "approved_desc": "UAS meets U-plan authorization requirements. Probability of compliance loss during flight does not exceed acceptable norms.",
        "rejected": "🚨 REJECTED — BOTTLENECK DETECTED",
        "rejected_desc": "C2-link in current configuration has increased degradation risk. Corrective action required before takeoff.",
        "availability": "Availability",
        "continuity": "Continuity",
        "latency": "Mean Latency",
        "packet_loss": "Packet Loss",
        "integrity": "Integrity",
        "target": "Target:",
        "p95": "P95:",
        "dropped": "Dropped:",
        "packets": "pkt",
        "tab_analysis": "📊 Bottleneck Analysis & Charts",
        "tab_sensitivity": "🔬 Sensitivity Analysis",
        "tab_telemetry": "🗺️ Log & Mission Route",
        "tab_monte_carlo": "🎲 Monte Carlo Simulation",
        "latency_distribution": "Network Latency Distribution (End-to-End)",
        "latency_histogram": "Latency Histogram in Communication Channel",
        "latency_ms": "Latency (ms)",
        "packet_count": "Packet Count",
        "threshold_line": "U-space Threshold (1000 ms)",
        "radar_title": "C2 Capabilities Radar Chart",
        "current_board": "Current Board",
        "min_threshold": "Minimum U-space Threshold",
        "bottleneck_localization": "Parameter Bottleneck Localization",
        "sensitivity_title": "Sensitivity Coefficients for +10% Parameter Variation",
        "latency_param": "Latency",
        "loss_param": "Packet Loss",
        "continuity_param": "Continuity",
        "impact_r_c2": "Impact on R_C2 (% change)",
        "diagnostic_report": "📋 Bottleneck Diagnostic Report",
        "bottleneck_latency": "**🚨 Bottleneck:** Average network latency ({:.1f} ms) exceeds U-space regulatory threshold ({} ms).",
        "action_latency": "**🛠️ Recommended Action:** Try using a lower latency communication link (e.g., 5G NR) or review the data transmission architecture.",
        "bottleneck_loss": "**🚨 Bottleneck:** Packet loss rate ({:.2f}%) is too high for an urban environment.",
        "action_loss": "**🛠️ Recommended Action:** Enable telemetry channel redundancy (Hybrid Multilink) or check antenna/modem quality.",
        "status_ok": "**✅ C2-link Status Satisfactory:** Latency, loss, and availability parameters are within norms for the selected SAIL level.",
        "flight_map": "UAS Flight Route Map",
        "raw_log": "Raw Telemetry Log Fragment",
        "mc_distribution": "R_C2 Distribution from Monte Carlo Results (1000 iterations)",
        "mc_probability": "Probability P(R_C2 ≥ 80%)",
        "log_loaded": "✅ Telemetry log successfully loaded!",
        "demo_log": "ℹ️ Using demo flight log in urban canyon.",
        "load_error": "Error loading test log file.",
        "main_header": "🛸 U-space C2 Readiness Diagnostic Validator",
        "sub_header": "B2B pre-flight express diagnostics and C2-link bottleneck analysis for UAS (according to Regulation EU 2021/664)",
        "sidebar_header": "⚙️ Input Parameters and Scenario",
        "file_upload": "📁 Upload Telemetry Log (CSV)",
        "scenario_header": "1. U-space Scenario and Geozone",
        "threshold_latency": "Regulatory Latency Threshold L_threshold (ms)",
        "file_loaded": "✅ Telemetry log successfully loaded!",
        "file_error": "Error loading test log file.",
        "threshold_text": "from threshold (80%)",
        "verdict_header": "Pre-flight Testing Verdict",
        "availability_target": "Target: >98.0%",
        "continuity_target": "Target: >99.0%",
        "integrity_target_rtk": "Target (RTK): >95%",
        "integrity_target_3d": "Target (3D Fix): >99%",
        "latency_xlabel": "Latency (ms)",
        "latency_ylabel": "Packet Count",
        "threshold_annotation": "U-space Threshold ({} ms)",
        "radar_categories": ["Availability (A)", "Continuity (C)", "Norm. Latency (f_L)", "Integrity (I)"],
        "sensitivity_params": ["Latency", "Packet Loss", "Continuity"],
        "monte_carlo_xlabel": "R_C2 (%)",
        "monte_carlo_ylabel": "Count",
        "monte_carlo_title": "R_C2 Distribution from Monte Carlo Results (1000 iterations)",
        "probability_text": "P(R_C2 ≥ 80%) = {:.1f}%",
        "footer": "Master's Thesis Project KSE | Developer: Student of 'Unmanned Aerial Vehicles' Program | Specialty G12 (134)",
        "network_preset": "⚡ Network Preset / Пресет стандарту зв'язку",
        "operation_preset": "🛸 Operation Scenario Preset / Пресет операційного сценарію",
        "preset_none": "-- Select Preset --",
        "preset_vlos": "VLOS (Visual Line of Sight)",
        "preset_evlos": "EVLOS (Extended Visual Line of Sight)",
        "preset_bvlos_suburban": "BVLOS Suburban (Low Density / Rural)",
        "preset_bvlos_urban": "BVLOS Urban Canyon (Delivery / Dense VLL)",
        "preset_uam": "UAM / eVTOL Passenger Mobility",
        "run_button": "▶ CALCULATE & SIMULATE",
        "welcome_message": "👈 Configure input parameters or select presets in the sidebar and press the [▶ CALCULATE & SIMULATE] button to start the diagnostics."
    }
}

# -----------------------------------------------------------------------------
# PRESET CONFIGURATIONS
# -----------------------------------------------------------------------------
# Network Presets with help text
NETWORK_PRESETS = {
    "ISM RF 2.4/5.8 GHz (Direct RLOS | <3km | 10-30ms)": {
        "params": {"l_threshold": 200, "telemetry_freq": 2.0},
        "help": {
            "ua": "Прямий радіоканал для VLOS. Низька затримка, але обмежена дальність і ризик завад у місті.",
            "en": "Direct radio link for VLOS. Low latency, but limited range and risk of interference in the city."
        }
    },
    "4G LTE Cellular (Public Band 3/7/20 | 80-200ms)": {
        "params": {"l_threshold": 1000, "telemetry_freq": 2.5},
        "help": {
            "ua": "Публічна стільникова мережа для BVLOS. Широке покриття, наявність джиттеру при handover.",
            "en": "Public cellular network for BVLOS. Wide coverage, jitter presence during handover."
        }
    },
    "5G NR + QoS Slicing (Sub-6GHz Band n78 | 15-50ms)": {
        "params": {"l_threshold": 500, "telemetry_freq": 5.0},
        "help":
        {
            "ua": "Виділений мережевий слайс із пріоритетом URLLC для критичних міських місій та UAM.",
            "en": "Dedicated network slice with URLLC priority for critical urban missions and UAM."
        }
    },
    "SatCom L-Band (Iridium/Inmarsat | BRLOS | 400-1200ms)": {
        "params": {"l_threshold": 1500, "telemetry_freq": 1.0},
        "help": {
            "ua": "Супутниковий канал для віддалених місій. Глобальне покриття, але значна затримка.",
            "en": "Satellite channel for remote missions. Global coverage, but significant latency."
        }
    },
    "Hybrid Multilink (Dual-SIM 4G/5G + SatCom | Redundant)": {
        "params": {"l_threshold": 800, "telemetry_freq": 3.0},
        "help": {
            "ua": "Дубльований агрегований канал із динамічним перемиканням при деградації.",
            "en": "Redundant aggregated channel with dynamic switching on degradation."
        }
    }
}

# Operation Scenario Presets
OPERATION_PRESETS = {
    "VLOS (Visual Line of Sight)": {
        "params": {"corridor_width": 40.0, "l_threshold": 2000, "telemetry_freq": 1.0, "sail_level": 0},
        "help": {
            "ua": "Політ у межах прямої видимості пілота (до 500 м). Низький ризик (SAIL II), широкий коридор OIV (40 м), поріг затримки L_threshold = 2000 мс.",
            "en": "Flight within the pilot's direct line of sight (up to 500 m). Low risk (SAIL II), wide OIV corridor (40 m), latency threshold L_threshold = 2000 ms."
        }
    },
    "EVLOS (Extended Visual Line of Sight)": {
        "params": {"corridor_width": 30.0, "l_threshold": 1500, "telemetry_freq": 1.5, "sail_level": 0},
        "help": {
            "ua": "Політ поза безпосередньою видимістю пілота, але за участю візуальних спостерігачів (VO). Коридор 30 м, поріг затримки L_threshold = 1500 мс, SAIL II.",
            "en": "Flight beyond the pilot's direct visibility, but with the involvement of visual observers (VO). Corridor 30 m, latency threshold L_threshold = 1500 ms, SAIL II."
        }
    },
    "BVLOS Suburban (Low Density / Rural)": {
        "params": {"corridor_width": 25.0, "l_threshold": 1000, "telemetry_freq": 2.0, "sail_level": 0},
        "help": {
            "ua": "Політ поза межами видимості над передмістям або сільською місцевістю з низькою щільністю населення. Коридор 25 м, L_threshold = 1000 мс, SAIL II.",
            "en": "Flight beyond line of sight over suburbs or rural areas with low population density. Corridor 25 m, L_threshold = 1000 ms, SAIL II."
        }
    },
    "BVLOS Urban Canyon (Delivery / Dense VLL)": {
        "params": {"corridor_width": 15.0, "l_threshold": 500, "telemetry_freq": 2.5, "sail_level": 1},
        "help": {
            "ua": "Політ у щільній міській забудові (експрес-доставка). Вузький коридор (15 м), підвищені вимоги до затримки L_threshold = 500 мс, SAIL IV.",
            "en": "Flight in dense urban development (express delivery). Narrow corridor (15 m), increased requirements for latency L_threshold = 500 ms, SAIL IV."
        }
    },
    "UAM / eVTOL Passenger Mobility": {
        "params": {"corridor_width": 10.0, "l_threshold": 100, "telemetry_freq": 5.0, "sail_level": 1},
        "help": {
            "ua": "Пасажирська та критична міська аеромобільність (eVTOL). Гранично вузький коридор (10 м), високі вимоги до затримки L_threshold = 100 мс, f_up = 5.0 Гц, SAIL IV.",
            "en": "Passenger and critical urban air mobility (eVTOL). Extremely narrow corridor (10 m), high requirements for latency L_threshold = 100 ms, f_up = 5.0 Hz, SAIL IV."
        }
    }
}


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
