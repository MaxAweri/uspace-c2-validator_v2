# -----------------------------------------------------------------------------
# CORE CONSTANTS
# -----------------------------------------------------------------------------
REQUIRED_COLUMNS = ['timestamp_board_ms', 'timestamp_server_ms', 'seq_id']
L_MAX = 5000.0
OUTAGE_THRESHOLD_MS = 2000
SENSITIVITY_DELTA = 0.10
# -----------------------------------------------------------------------------
# R_C2 PASS THRESHOLDS BY SAIL (differentiated by operational risk)
# Base value 80% is aligned with SESAR U-space CONOPS 4th ed. (2023) baseline
# for C2 Link End-to-End Availability (99.3%) discounted for aggregate index.
# Higher SAIL requires higher margin per SORA 2.5 Annex E OSO#06 assurance level.
# -----------------------------------------------------------------------------
R_C2_THRESHOLDS_BY_SAIL = {
    "SAIL I-II (Low Risk)":      80.0,   # base CONOPS-aligned threshold
    "SAIL III-IV (Medium Risk)": 90.0,   # +10% margin (Medium assurance)
    "SAIL V-VI (High Risk)":     95.0,   # +15% margin (High assurance, 3rd-party validation)
}

# Backwards-compatible fallback (default = SAIL I-II baseline)
R_C2_THRESHOLD_PCT = R_C2_THRESHOLDS_BY_SAIL["SAIL I-II (Low Risk)"]

# Helper for looking up SAIL-specific threshold
def get_r_c2_threshold(sail_level: str) -> float:
    """Return R_C2 pass threshold (%) for the given SAIL level. Falls back to baseline."""
    return R_C2_THRESHOLDS_BY_SAIL.get(sail_level, R_C2_THRESHOLD_PCT)

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# -----------------------------------------------------------------------------
# R_C2_MIN THRESHOLD (min-consensus / RLP-strict verdict)
# Джерело: JARUS RLP Concept (2023), p.20 — "most stringent transaction" principle:
#   "The global value for each parameter is based on the parameter achieving
#    the MOST STRINGENT transaction. For example, the availability is the
#    availability of the least available link element, not the mean."
# https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf
#
# Rationale: weighted arithmetic mean R_C2 може маскувати критично низький
# окремий компонент (aggregate masking). R_C2_min = min(A, C, L, I) відображає
# принцип series reliability (система послідовних елементів = найслабший компонент).
# Threshold 70% — універсальний "unfit for purpose" floor, недиференційований
# по SAIL (це absolute worst-case, не SAIL-specific target).
# SAIL differentiation реалізована через R_C2_THRESHOLDS_BY_SAIL (weighted verdict).
# -----------------------------------------------------------------------------
R_C2_MIN_THRESHOLD_PCT = 70.0

R_C2_MIN_PROVENANCE = {
    "source": "JARUS RLP Concept (2023), p.20",
    "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
    "principle": "Most stringent transaction (min-consensus, series reliability)",
    "formula": "R_C2_min = min(A_norm, C_norm, L_norm, I_norm)",
    "rationale": "Complements weighted arithmetic R_C2 by exposing the worst-performing component. "
                 "Prevents 'aggregate masking' where one critically low metric is hidden by averaging.",
    "threshold_choice": "70% — universal 'unfit for purpose' engineering floor. "
                        "Not differentiated by SAIL (SAIL differentiation is via R_C2_THRESHOLDS_BY_SAIL)."
}

# Metric Target Thresholds
# Джерело: SESAR U-space CONOPS 4th ed. (2023), Appendix G, Table 4 (p.19)
# https://www.sesarju.eu/node/4544
# REQ-DROC2OM-D21-PERF.0010: Availability ≥ 99.3%
# REQ-DROC2OM-D21-PERF.0030: Integrity (Packet Error Rate ≤ 10⁻³) → 99.9%
# CORUS-XUAM-035: UTM position latency ≤ 1000 ms
AVAILABILITY_TARGET = 0.993     # REQ-DROC2OM-D21-PERF.0010 (CONOPS 4.0)
CONTINUITY_TARGET = 0.999       # REQ-DROC2OM-D21-PERF.0030 (PER ≤ 10⁻³)
INTEGRITY_TARGET = 0.999        # REQ-DROC2OM-D21-PERF.0030 (PER ≤ 10⁻³)
COMPLETENESS_TARGET = INTEGRITY_TARGET  # 99.9% цільова повнота телеметрії
LATENCY_TARGET_MS = 1000.0      # CORUS-XUAM-035 (UTM position latency)

# Verdict Status Constants
STATUS_PASS = "PASS (Технічним критеріям відповідає)"
STATUS_CONDITIONAL = "CONDITIONAL (Потребує додаткових даних або усунення завад)"
STATUS_FAIL = "FAIL (Критичні критерії не виконано)"
STATUS_NOT_ASSESSABLE = "NOT ASSESSABLE (Недостатньо даних у логу)"

# -----------------------------------------------------------------------------
# SAIL WEIGHT PROFILES (Single Source of Truth)
# Weights order: (w_A, w_C, w_L, w_I) — Availability, Continuity, Latency, Integrity
# Rationale: higher SAIL → higher operational risk → higher weight on latency
# and integrity (time-critical failure modes dominate).
# All weight vectors MUST sum to 1.0 (validated at import time).
# -----------------------------------------------------------------------------
SAIL_WEIGHTS = {
    "SAIL I-II (Low Risk)":      (0.25, 0.25, 0.25, 0.25),
    "SAIL III-IV (Medium Risk)": (0.25, 0.25, 0.25, 0.25),
    "SAIL V-VI (High Risk)":     (0.25, 0.25, 0.25, 0.25),
}

SAIL_WEIGHTS_PROVENANCE = {
    "source": "SESAR U-space CONOPS 4th ed. (2023), Appendix G, Table 4",
    "source_url": "https://www.sesarju.eu/node/4544",
    "basis": "CONOPS 4.0 defines four C2 Link performance parameters (Availability, "
             "Continuity/PER, Integrity, Latency) as coequal aspects of link quality. "
             "No weighting differentiation is prescribed between them or across SAIL levels. "
             "REQ-DROC2OM-D21-PERF.0010-0030 (p.19) applies uniformly.",
    "sail_differentiation": "SAIL-based differentiation is implemented via R_C2 PASS thresholds "
                            "(see R_C2_THRESHOLDS_BY_SAIL), NOT via weight coefficients. "
                            "This aligns with SORA 2.5 Annex E OSO#06 (JARUS, 2024): higher SAIL "
                            "requires higher assurance level (Low/Medium/High) rather than "
                            "different metric composition.",
    "deferred_extension": "Opt B (deferred): add complementary R_C2_min = min(A, C, L, I) "
                          "per JARUS RLP Concept p.20 'most stringent transaction' principle.",
    "note": "Equal weights (0.25 each) are the CONOPS-aligned engineering choice. "
            "Sensitivity to weight perturbation is quantified in the Sensitivity Analysis tab."
}

# Legacy short-form aliases for backwards compatibility
SAIL_ALIASES = {
    "SAIL II":  "SAIL I-II (Low Risk)",
    "SAIL IV":  "SAIL III-IV (Medium Risk)",
    "SAIL VI":  "SAIL V-VI (High Risk)",
    "SAIL VII": "SAIL V-VI (High Risk)",
}

# Validation: fail fast at import time if weights are misconfigured
for _key, _w in SAIL_WEIGHTS.items():
    if abs(sum(_w) - 1.0) > 1e-9:
        raise ValueError(
            f"SAIL_WEIGHTS['{_key}'] must sum to 1.0, got {sum(_w)}"
        )

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
        "params": {"corridor_width": 40.0, "l_threshold": 2000, "f_up": 1.0, "sail": "SAIL I-II (Low Risk)"},
        "help": {
            "ua": "Політ у межах прямої видимості. Коридор 40 м, затримка L_threshold ≤ 2000 мс, частота f_up ≥ 1.0 Гц, SAIL I-II (Low Risk).",
            "en": "Visual Line of Sight flight. 40m corridor, latency L_threshold ≤ 2000 ms, frequency f_up ≥ 1.0 Hz, SAIL I-II (Low Risk)."
        }
    },
    "EVLOS (Extended Visual Line of Sight)": {
        "params": {"corridor_width": 30.0, "l_threshold": 1500, "f_up": 1.5, "sail": "SAIL I-II (Low Risk)"},
        "help": {
            "ua": "Розширений політ за участі візуальних спостерігачів. Коридор 30 м, затримка L_threshold ≤ 1500 мс, частота f_up ≥ 1.5 Гц, SAIL I-II (Low Risk).",
            "en": "Extended VLOS with observers. 30m corridor, latency L_threshold ≤ 1500 ms, frequency f_up ≥ 1.5 Hz, SAIL I-II (Low Risk)."
        }
    },
    "BVLOS Suburban (Low Density / Rural)": {
        "params": {"corridor_width": 25.0, "l_threshold": 1000, "f_up": 2.0, "sail": "SAIL I-II (Low Risk)"},
        "help": {
            "ua": "Політ поза межами видимості над передмістям/сільською місцевістю. Коридор 25 м, затримка L_threshold ≤ 1000 мс, частота f_up ≥ 2.0 Гц, SAIL I-II (Low Risk).",
            "en": "BVLOS flight in suburban/rural areas. 25m corridor, latency L_threshold ≤ 1000 ms, frequency f_up ≥ 2.0 Hz, SAIL I-II (Low Risk)."
        }
    },
    "BVLOS Urban Canyon (Delivery / Dense VLL)": {
        "params": {"corridor_width": 15.0, "l_threshold": 500, "f_up": 2.5, "sail": "SAIL III-IV (Medium Risk)"},
        "help": {
            "ua": "Політ у щільній міській забудові (доставка, інспекція). Вузький коридор 15 м, затримка L_threshold ≤ 500 мс, частота f_up ≥ 2.5 Гц, SAIL III-IV (Medium Risk).",
            "en": "Dense urban VLL operations (delivery). Narrow 15m corridor, latency L_threshold ≤ 500 ms, frequency f_up ≥ 2.5 Hz, SAIL III-IV (Medium Risk)."
        }
    },
    "UAM / eVTOL Passenger Mobility": {
        "params": {"corridor_width": 10.0, "l_threshold": 100, "f_up": 5.0, "sail": "SAIL III-IV (Medium Risk)"},
        "help": {
            "ua": "Пасажирські та важкі вантажні UAM/eVTOL перевезення. Вузький коридор 10 м, сувора затримка L_threshold ≤ 100 мс, частота f_up ≥ 5.0 Гц, SAIL III-IV (Medium Risk).",
            "en": "Passenger and cargo UAM/eVTOL transport. Ultra-narrow 10m corridor, latency L_threshold ≤ 100 ms, frequency f_up ≥ 5.0 Hz, SAIL III-IV (Medium Risk)."
        }
    }
}

OPERATION_PRESETS = SCENARIO_PRESETS



# -----------------------------------------------------------------------------
# PRESET EXPLANATIONS (TWO-LEVEL REFERENCE SYSTEM)
# -----------------------------------------------------------------------------
PRESET_EXPLANATIONS_SHORT = {
    "BVLOS Urban Canyon (Delivery / Dense VLL)": {
        "title": "⚡ Швидкий інженерний розбір: BVLOS Urban Canyon",
        "qa_list": [
            {
                "q": "❓ Чому затримка L_threshold = 500 мс?",
                "a": "Сумарний часовий бюджет U-space (End-to-End) становить 1.0 с (Art. 13 EU 2021/664). 500 мс виділяється на C2-канал, а інші 500 мс — на серверну обробку та генерацію alerts."
            },
            {
                "q": "❓ Чому частота телеметрії f_up = 2.5 Гц?",
                "a": "При швидкості БАС 10–15 м/с частота 1 Гц створює «сліпий проміжок» у 15 м. Частота 2.5 Гц (пакет кожні 400 мс) — математичний мінімум для запобігання хибним тривогам."
            },
            {
                "q": "❓ Чому ширина коридору W_corridor = 15.0 м?",
                "a": "Визначається габаритами міських вулиць та щільністю забудови (EUROCAE ED-269 / Operational Intent Volume)."
            },
            {
                "q": "❓ Чому клас ризику SAIL III-IV (Medium Risk)?",
                "a": "Польоти над містом належать до Medium Risk за SORA 2.5, що вимагає підвищених ваг для затримки та цілісності (OSO#06)."
            }
        ]
    },
    "VLOS (Visual Line of Sight)": {
        "title": "⚡ Швидкий інженерний розбір: VLOS",
        "qa_list": [
            {
                "q": "❓ Чому затримка L_threshold = 2000 мс?",
                "a": "При польоті у межах прямої видимості пілот здійснює безпосереднє візуальне спостереження за БАС. Поріг 2000 мс допустимий, оскільки загрози усуваються ручним втручанням пілота."
            },
            {
                "q": "❓ Чому частота телеметрії f_up = 1.0 Гц?",
                "a": "Передача кадру телеметрії 1 раз на секунду є базовим стандартом для візуального моніторингу траєкторії на сервері USSP у нещільних геозонах."
            },
            {
                "q": "❓ Чому ширина коридору W_corridor = 40.0 м?",
                "a": "Враховує геометричну похибку візуальної орієнтації дистанційного пілота на відстані до 500 м без використання автоматичного трекінгу."
            },
            {
                "q": "❓ Чому клас ризику SAIL I-II (Low Risk)?",
                "a": "За SORA 2.5 польоти VLOS на малих висотах мають найнижчі класи наземного (GRC) та повітряного (ARC) ризиків."
            }
        ]
    },
    "EVLOS (Extended Visual Line of Sight)": {
        "title": "⚡ Швидкий інженерний розбір: EVLOS",
        "qa_list": [
            {
                "q": "❓ Чому затримка L_threshold = 1500 мс?",
                "a": "У сценарії EVLOS за БАС спостерігають візуальні спостерігачі (VO). Поріг 1500 мс враховує часову затримку голосового зв'язку між спостерігачем та пілотом."
            },
            {
                "q": "❓ Чому частота телеметрії f_up = 1.5 Гц?",
                "a": "Частота 1.5 Гц (пакет кожні 660 мс) гарантує кращу дискретизацію треку на межах зони видимості спостерігачів при збільшенні радіуса польоту."
            },
            {
                "q": "❓ Чому ширина коридору W_corridor = 30.0 м?",
                "a": "Звуження коридору з 40 м до 30 м обґрунтовано наявністю додаткових точок спостереження (Visual Observers), що знижує кутову похибку позиції."
            },
            {
                "q": "❓ Чому клас ризику SAIL I-II (Low Risk)?",
                "a": "Залучення візуальних спостерігачів єофіційним заходом зниження ризику (Mitigation M1) за SORA 2.5."
            }
        ]
    },
    "BVLOS Suburban (Low Density / Rural)": {
        "title": "⚡ Швидкий інженерний розбір: BVLOS Suburban",
        "qa_list": [
            {
                "q": "❓ Чому затримка L_threshold = 1000 мс?",
                "a": "У передмісті з низькою щільністю забудови допустима затримка до 1.0 с (базовий норматив EASA), оскільки щільність людського трафіку та висотних перешкод є низькою."
            },
            {
                "q": "❓ Чому частота телеметрії f_up = 2.0 Гц?",
                "a": "Відправка даних кожні 500 мс гарантує стабільний моніторинг траєкторії на швидкостях 15–20 м/с поза межами зони видимості."
            },
            {
                "q": "❓ Чому ширина коридору W_corridor = 25.0 м?",
                "a": "Враховує сумарну похибку супутникової навігації (GNSS 3D Fix) та можливий вітровий дрейф на відкритій місцевості."
            },
            {
                "q": "❓ Чому клас ризику SAIL I-II (Low Risk)?",
                "a": "Сільська місцевість має низький клас наземного ризику (Ground Risk Class 2-3), що зберігає місію в категорії Low Risk."
            }
        ]
    },
    "UAM / eVTOL Passenger Mobility": {
        "title": "⚡ Швидкий інженерний розбір: UAM / eVTOL",
        "qa_list": [
            {
                "q": "❓ Чому затримка L_threshold = 100 мс?",
                "a": "Пасажирські та важкі eVTOL вимагають реакції рівня Real-Time / URLLC. Затримка понад 100 мс неприпустима через загрозу критичних авіаподій."
            },
            {
                "q": "❓ Чому частота телеметрії f_up = 5.0 Гц?",
                "a": "Передача кадру кожні 200 мс (5 Гц) є найсуворішою вимогою для міської аеромобільності (Dense UAM) для миттєвого розведення бортового трафіку."
            },
            {
                "q": "❓ Чому ширина коридору W_corridor = 10.0 м?",
                "a": "Ультравузький польотний коридор (Vertiport Airway), який вимагає обов'язкового використання високоточної навігації GNSS RTK."
            },
            {
                "q": "❓ Чому клас ризику SAIL III-IV (Medium/High Risk)?",
                "a": "Пасажирські перевезення над містом мають найвищі вимоги до надійності C2-каналу та резервування (Dual-SIM 5G / SatCom)."
            }
        ]
    }
}

PRESET_EXPLANATIONS_FULL = {
    "BVLOS Urban Canyon (Delivery / Dense VLL)": {
        "title": "📚 Інженерно-нормативний розбір: BVLOS Urban Canyon (Delivery / Dense VLL)",
        "intro": "Сценарій описує польоти БАС поза межами прямої видимості в умовах щільної міської забудови на малих висотах (Very Low Level airspace). Додаток оцінює відповідність телеметрії нормативним рамкам EASA та ASTM.",
        "sections": [
            {
                "question": "❓ Чому порогова затримка C2-каналу встановлена саме L_threshold = 500 мс?",
                "answer": "Згідно зі ст. 13 Імплементаційного регламенту Комісії (EU) 2021/664 та розділу 6.2 стандарту ASTM F3548-21, сервіс моніторингу відповідності (Conformance Monitoring Service, CMS) повинен виявляти відхилення БАС від виділеного 4D-об'єму. Загальний допустимий часовий бюджет системи (End-to-End Latency) від борту до пульту USSP становить 1.0 с. Половинний поріг у 500 мс закладається на C2-канал зв'язку (Transmission Latency), щоб залишити 500 мс запасу на серверну екстраполяцію, розрахунок конфліктів та розсилку попереджень іншим учасникам руху.",
                "normative": "Regulation (EU) 2021/664 (Art. 13), ASTM F3548-21 (Section 6.2), CORUS CONOPS Ed. 4"
            },
            {
                "question": "❓ Чому мінімальна частота оновлення телеметрії повинна бути f_up = 2.5 Гц?",
                "answer": "У науковому дослідженні MDPI 'Analysis of UTM Tracking Performance for Conformance Monitoring' доведено, що при швидкості польоту БАС 10–15 м/с (36–54 км/год) у вузьких міських вулицях частота відправки телеметрії 1.0 Гц створює дискретний 'сліпий проміжок' у 10–15 метрів між сусідніми пакетами. Частота 2.5 Гц (передача кадру кожні 400 мс) є експериментально та математично доведеним мінімумом, який гарантує, що похибка запізнення позиції не перевищить допустиму геометрію міського коридору.",
                "normative": "MDPI Aerospace 'Analysis of UTM Tracking Performance' (2023)"
            },
            {
                "question": "❓ Чому ширина польотного коридору становить W_corridor = 15.0 м?",
                "answer": "Ширина визначає геометрію об'єму польотного наміру (Operational Intent Volume, OIV) згідно зі стандартом EUROCAE ED-269. У міських каньйонах ширина коридору обмежена фізичною відстанню між будівлями та висотністю забудови, що вимагає високої точності витримування траєкторії автопілотом (Flight Technical Error, FTE).",
                "normative": "EUROCAE ED-269 / EASA Easy Access Rules for U-space"
            },
            {
                "question": "❓ Чому застосовується клас ризику SORA 2.5 SAIL III-IV (Medium Risk)?",
                "answer": "За методологією оцінки ризиків JARUS SORA 2.5, польоти BVLOS над густозаселеними міськими районами автоматично класифікуються як Medium Risk (SAIL IV). Відповідно до вимоги OSO#06 (C2 Link Performance), це передбачає збільшення вагових коефіцієнтів затримки (w_L=0.25) та цілісності телеметрії (w_I=0.25) при формуванні підсумкового балу R_C2.",
                "normative": "JARUS SORA 2.5 (OSO#06 Command & Control Link Performance)"
            },
            {
                "question": "🎯 Чому це критично для передпольотного тестування (що бачить оператор)?",
                "answer": "Інструмент перевіряє завантажений лог телеметрії на відповідність вказаним Hard Constraints. Якщо фактичний лог має затримку P95 = 800 мс (> 500 мс) або частоту запису 1.5 Гц (< 2.5 Гц), система миттєво видає вердикт FAIL і вказує на точне 'вузьке місце' (Bottleneck Diagnostic). Це сигналізує операторові про необхідність збільшити частоту відправки телеметрії на борту або змінити 4G-модуль на 5G NR до вильоту.",
                "normative": "U-space C2 Technical Readiness Screening Methodology (KSE Thesis)"
            }
        ]
    },
    "VLOS (Visual Line of Sight)": {
        "title": "📚 Інженерно-нормативний розбір: VLOS (Visual Line of Sight)",
        "intro": "Сценарій VLOS передбачає польоти, під час яких дистанційний пілот постійно утримує БАС у невооруженому візуальному контакті для контролю траєкторії та уникнення зіткнень.",
        "sections": [
            {
                "question": "❓ Чому порогова затримка C2-каналу встановлена L_threshold = 2000 мс?",
                "answer": "Згідно з EASA Easy Access Rules for UAS (AMC1 Article 13 Regulation EU 2021/664), при візуальному політі основну функцію виявлення та запобігання зіткненням (See-and-Avoid) виконує безпосередньо пілот. Затримка C2-каналу до 2.0 секунд є припустимою, оскільки сервіс U-space виконує лише фонову інформаційну функцію.",
                "normative": "Regulation (EU) 2021/664 (Art. 13), EASA Easy Access Rules for UAS"
            },
            {
                "question": "❓ Чому мінімальна частота оновлення телеметрії повинна бути f_up = 1.0 Гц?",
                "answer": "При швидкостях VLOS-польотів (до 8–10 м/с) та візуальному контролі частота відправлення телеметрії 1.0 Гц забезпечує достатню дискретизацію для відображення позиції БАС на моніторі USSP без перевантаження радіоефіру ISM-діапазонів (2.4/5.8 ГГц).",
                "normative": "JARUS RLP Concept / EUROCAE ED-269"
            },
            {
                "question": "❓ Чому ширина польотного коридору становить W_corridor = 40.0 м?",
                "answer": "Ширина коридору у 40 метрів враховує сумарну похибку оцінки віддалі людським оком (Visual Perception Error) та фізичну глибину орієнтації БАС у просторі на відстані 300–500 метрів від пілота.",
                "normative": "EASA SORA 2.5 Ground Risk Assessment Guidelines"
            },
            {
                "question": "❓ Чому застосовується клас ризику SORA 2.5 SAIL I-II (Low Risk)?",
                "answer": "Операції у межах прямої видимості зазвичай мають низьку щільність повітряного руху (ARC-A/ARC-B). За методикою SORA 2.5 це відповідає рівню SAIL II, де вимоги до надійності C2-лінку (OSO#06) є мінімальними.",
                "normative": "JARUS SORA 2.5 (OSO#06 Command & Control Link Performance)"
            }
        ]
    },
    "EVLOS (Extended Visual Line of Sight)": {
        "title": "📚 Інженерно-нормативний розбір: EVLOS (Extended Visual Line of Sight)",
        "intro": "Сценарій EVLOS дозволяє розширити радіус польоту БАС за рахунок залучення додаткових навчених візуальних спостерігачів (Visual Observers, VO).",
        "sections": [
            {
                "question": "❓ Чому порогова затримка C2-каналу встановлена L_threshold = 1500 мс?",
                "answer": "При EVLOS інформація про перешкоди передається пілоту через спостерігача. Поріг затримки телеметрії 1500 мс закладає 500 мс запасу на затримку голосової команди від спостерігача до пілота (Human Communication Latency).",
                "normative": "EASA Easy Access Rules for UAS (GM1 to Specific Category)"
            },
            {
                "question": "❓ Чому мінімальна частота оновлення телеметрії повинна бути f_up = 1.5 Гц?",
                "answer": "При збільшенні віддалення БАС до 1.5–2.0 км частота 1.5 Гц (пакет кожні 660 мс) є математично достатньою для підтримання синхронізації між візуальним спостереженням та даними на сервері USSP.",
                "normative": "MDPI Aerospace 'UAS Tracking Performance' (2023)"
            },
            {
                "question": "❓ Чому ширина польотного коридору становить W_corridor = 30.0 м?",
                "answer": "Наявність точок перехресного спостереження (Cross-Observer Positioning) зменшує невизначеність координатного положення БАС порівняно з VLOS, що дозволяє звузити коридор до 30 метрів.",
                "normative": "EUROCAE ED-269 / EASA AMC1 Article 13"
            },
            {
                "question": "❓ Чому застосовується клас ризику SORA 2.5 SAIL I-II (Low Risk)?",
                "answer": "Використання процедури передачі контролю між спостерігачами є визнаним заходом зниження ризику (Mitigation M1) за SORA 2.5, що утримує операцію в категорії Low Risk (SAIL II).",
                "normative": "JARUS SORA 2.5 (Annex Glossary & M1 Mitigations)"
            }
        ]
    },
    "BVLOS Suburban (Low Density / Rural)": {
        "title": "📚 Інженерно-нормативний розбір: BVLOS Suburban (Low Density / Rural)",
        "intro": "Сценарій описує польоти поза межами прямої видимості над передмістям чи сільською місцевістю з низькою щільністю населення.",
        "sections": [
            {
                "question": "❓ Чому порогова затримка C2-каналу встановлена L_threshold = 1000 мс?",
                "answer": "Відповідно до EASA Easy Access Rules for U-space (Art. 13 EU 2021/664), затримка 1000 мс є класичним часовим лімітом для автоматизованого моніторингу відповідності у зонах низького ризику.",
                "normative": "Regulation (EU) 2021/664 / ASTM F3548-21"
            },
            {
                "question": "❓ Чому мінімальна частота оновлення телеметрії повинна бути f_up = 2.0 Гц?",
                "answer": "При швидкостях польоту 15–20 м/с частота 2.0 Гц забезпечує інтервал між точками у 7.5–10 метрів, що задовольняє вимоги геометричного ешелонування BUBBLES у нещільних геозонах.",
                "normative": "SESAR BUBBLES CONOPS / EUROCAE ED-269"
            },
            {
                "question": "❓ Чому ширина польотного коридору становить W_corridor = 25.0 м?",
                "answer": "Враховує сумарну похибку системи (Total System Error, TSE), яка поєднує похибку GNSS позиціонування та вітрові збурення автопілота на відкритому просторі.",
                "normative": "EASA Special Condition for Light UAS"
            },
            {
                "question": "❓ Чому застосовується клас ризику SORA 2.5 SAIL I-II (Low Risk)?",
                "answer": "Мала щільність населення на землі забезпечує низький початковий клас наземного ризику (Intrinsic GRC), що дозволяє проводити операцію в категорії Low Risk.",
                "normative": "JARUS SORA 2.5 Main Body"
            }
        ]
    },
    "UAM / eVTOL Passenger Mobility": {
        "title": "📚 Інженерно-нормативний розбір: UAM / eVTOL Passenger Mobility",
        "intro": "Сценарій описує польоти пасажирських та важких вантажних безпілотних повітряних суден (eVTOL / Urban Air Mobility) у міських вертіпортах.",
        "sections": [
            {
                "question": "❓ Чому порогова затримка C2-каналу встановлена L_threshold = 100 мс?",
                "answer": "Для пасажирських eVTOL згідно з EASA SC-VTOL та вимогами 3GPP URLLC, затримка C2-каналу понад 100 мс створює загрозу для динамічної стабілізації та автоматичного розведення БАС у критичних фазах посадки на вертіпорт.",
                "normative": "EASA Special Condition VTOL / 3GPP TS 22.125 (UAV URLLC)"
            },
            {
                "question": "❓ Чому мінімальна частота оновлення телеметрії повинна бути f_up = 5.0 Гц?",
                "answer": "Частота 5.0 Гц (передача пакету кожні 200 мс) є стандартом аеромобільності UAM для забезпечення цільового рівня безпеки (Target Level of Safety 10^-9 авіаподій на годину).",
                "normative": "CORUS-XUAM Concept of Operations / ASTM F3548-21"
            },
            {
                "question": "❓ Чому ширина польотного коридору становить W_corridor = 10.0 м?",
                "answer": "Ультравузькі міські вертісмуги вимагають найвищої навігаційної точності (RNP 0.01 / GNSS RTK) для утримання важкого апарата всередині повітряного трафіку.",
                "normative": "EASA PTS-VCA (Physical Characteristics for Vertiports)"
            },
            {
                "question": "❓ Чому застосовується клас ризику SORA 2.5 SAIL III-IV (Medium Risk)?",
                "answer": "Перевезення пасажирів над містом належить до категорії підвищеного ризику, що вимагає залучення резервованих каналів зв'язку (Dual 5G + SatCom) та підвищених вагових коефіцієнтів C2.",
                "normative": "JARUS SORA 2.5 / EASA Easy Access Rules for U-space"
            }
        ]
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


# -----------------------------------------------------------------------------
# REQUIREMENT REGISTER & PROVENANCE METADATA
# -----------------------------------------------------------------------------
REQUIREMENT_REGISTER = [
    {
        "id": "C2-AVA-001",
        "title": "Доступність каналу C2 (End-to-end Availability)",
        "source": "SESAR U-space CONOPS 4th ed. (2023), Appendix G, Table 4, REQ-DROC2OM-D21-PERF.0010, p.19",
        "source_url": "https://www.sesarju.eu/node/4544",
        "provenance": "Прескриптивна вимога SESAR CORUS-XUAM (U-space enabling framework)",
        "parameter": "timestamp_board_ms, seq_id",
        "metric_key": "availability",
        "target_text": "A ≥ 99.3%",
        "target_val": 0.993,
        "type": "min",
        "unit": "%"
    },
    {
        "id": "C2-LAT-001",
        "title": "Порогова затримка C2 (UTM Position Update Latency)",
        "source": "SESAR U-space CONOPS 4th ed. (2023), CORUS-XUAM-035, p.281",
        "source_url": "https://www.sesarju.eu/node/4544",
        "provenance": "Прескриптивна вимога SESAR CORUS-XUAM для передачі позиції/треків/алертів",
        "parameter": "timestamp_board_ms, timestamp_server_ms",
        "metric_key": "l_p95",
        "target_text": "P95 ≤ 1000 мс (базовий U-space поріг) АБО L_threshold сценарію",
        "target_val": 1000.0,  # Може перевизначатися динамічно через scenario/network preset
        "type": "max",
        "unit": "мс"
    },
    {
        "id": "C2-LAT-002",
        "title": "Затримка релею голосу ATC через C2 (Voice Relay Latency)",
        "source": "SESAR U-space CONOPS 4th ed. (2023), CORUS-XUAM-050, p.285",
        "source_url": "https://www.sesarju.eu/node/4544",
        "provenance": "Прескриптивна вимога для операцій у контрольованому повітряному просторі (SAIL III-IV+)",
        "parameter": "timestamp_board_ms, timestamp_server_ms (у режимі voice relay)",
        "metric_key": "l_p95_voice",
        "target_text": "Voice latency ≤ 400 мс, Availability ≥ 99.998%",
        "target_val": 400.0,
        "type": "max",
        "unit": "мс",
        "applies_to": "SAIL III-IV (Medium Risk), SAIL V-VI (High Risk)"
    },
    {
        "id": "C2-CON-001",
        "title": "Часова безперервність (Continuity / Loss Probability)",
        "source": "JARUS RLP Concept (2023), p.20, 'most stringent transaction' principle; "
                  "аналог з SESAR U-space CONOPS CORUS-XUAM-009 (Tactical Geofencing) для SAIL III+",
        "source_url": "https://jarus-rpas.org/wp-content/uploads/2023/06/jar_05_doc_rlp_concept_upgraded.pdf",
        "provenance": "Інженерна вимога (SORA 2.5 Annex E OSO#06 не задає прямо для C2)",
        "parameter": "timestamp_board_ms (t_gaps > 2.0s)",
        "metric_key": "continuity",
        "target_text": "C ≥ 99.0% (Low Risk), C ≥ 99.999% (High Risk, аналог tactical geofencing)",
        "target_val": 0.99,
        "type": "min",
        "unit": "%"
    },
    {
        "id": "C2-INT-001",
        "title": "Цілісність каналу C2 (Integrity via Packet Error Rate)",
        "source": "SESAR U-space CONOPS 4th ed. (2023), Appendix G, Table 4, REQ-DROC2OM-D21-PERF.0030, p.19",
        "source_url": "https://www.sesarju.eu/node/4544",
        "provenance": "Прескриптивна вимога SESAR CORUS-XUAM (PER ≤ 10⁻³ на інтерфейсі network/logical link)",
        "parameter": "seq_id (proxy для PER через втрачені пакети)",
        "metric_key": "c2_data_completeness",
        "target_text": "I_data ≥ 99.9% (PER ≤ 10⁻³)",
        "target_val": 0.999,
        "type": "min",
        "unit": "%"
    },
    {
        "id": "NAV-FIX-001",
        "title": "Придатність супутникового фіксу (GNSS Fix Quality)",
        "source": "EASA Easy Access Rules for UAS (Consolidated version, ongoing updates); "
                  "EUROCAE ED-269 для геофенсинга з GNSS",
        "source_url": "https://www.easa.europa.eu/en/document-library/easy-access-rules",
        "provenance": "Допоміжний навігаційний індикатор (не C2-показник; впливає на geo-caging quality)",
        "parameter": "gnss_fix_type",
        "metric_key": "i_gnss",
        "target_text": "F_GNSS ≥ 95.0% (fix_type ≥ 3 = 3D fix)",
        "target_val": 0.95,
        "type": "min",
        "unit": "%"
    }
]

# -----------------------------------------------------------------------------
# DATA SANITY & QUALITY CHECKS DEFINITIONS
# -----------------------------------------------------------------------------
DATA_SANITY_CHECKS = [
    {
        "check_id": "CHK-001",
        "name": "Monotonicity Check",
        "desc": "Перевірка монотонності зростання бортового часу (timestamp_board_ms)."
    },
    {
        "check_id": "CHK-002",
        "name": "Sequence Integrity Check",
        "desc": "Перевірка відсутності дублікатів і некоректних значень seq_id."
    },
    {
        "check_id": "CHK-003",
        "name": "Duration Sufficiency",
        "desc": "Перевірка достатності тривалості логу (не менше 10 секунд)."
    },
    {
        "check_id": "CHK-004",
        "name": "Zero/Negative Delay Check",
        "desc": "Перевірка некоректних або від'ємних часових затримок."
    },
    {
        "check_id": "CHK-005",
        "name": "Sampling Rate Alignment",
        "desc": "Перевірка відповідності фактичної частоти запису до заявленої f_up."
    }
]

# -----------------------------------------------------------------------------
# BASELINE AGGREGATION MODELS
# -----------------------------------------------------------------------------
AGGREGATION_MODELS = {
    "linear": {
        "name": "Лінійна зважена сума (Weighted Arithmetic Mean)",
        "formula": "R_linear = w_A*A + w_C*C + w_L*f_L + w_I*I",
        "description": "Класична базова модель. Дозволяє взаємну компенсацію показників."
    },
    "geometric": {
        "name": "Геометричне середнє (Weighted Geometric Mean)",
        "formula": "R_geom = A^w_A * C^w_C * f_L^w_L * I^w_I",
        "description": "Суворіша модель. Значно карає підсумковий бал за деградацію навіть одного параметра."
    },
    "minimum": {
        "name": "Принцип найслабшої ланки (Minimum Criterion / Weakest Link)",
        "formula": "R_min = min(A, C, f_L, I)",
        "description": "Найсуворіший орієнтир для safety-critical місій. Базується на найгіршому показнику."
    }
}

# -----------------------------------------------------------------------------
# MONTE CARLO CORRELATION MATRIX (P1-2)
# Джерело: Sklar (1959) copula theory; Nelsen (2006), "An Introduction to Copulas"
# Аналог з телеком-інженерії: series reliability of C2 network components
# Order: (Availability, Continuity, Latency, Completeness)
# -----------------------------------------------------------------------------
MC_CORRELATION_MATRIX = [
    [ 1.00,  0.75, -0.60,  0.55],  # Availability
    [ 0.75,  1.00, -0.50,  0.50],  # Continuity
    [-0.60, -0.50,  1.00, -0.40],  # Latency
    [ 0.55,  0.50, -0.40,  1.00],  # Completeness
]

MC_CORRELATION_PROVENANCE = {
    "source": "Sklar (1959) copula theory; Nelsen (2006) 'An Introduction to Copulas'",
    "method": "Simplified Gaussian copula: correlated standard normals -> uniforms via CDF -> target marginals via inverse CDF",
    "rationale": "Uncorrelated Monte Carlo underestimates uncertainty width. C2 link parameters degrade "
                 "synchronously under network failures (Availability drops -> Continuity drops -> Latency rises -> "
                 "Completeness suffers). Empirical correlations based on telecom series-reliability heuristics.",
    "impact": "Correlated MC produces wider CI95 (more realistic), higher P(fail) under stress, "
              "and better reflects worst-case scenarios for BVLOS operations."
}

# -----------------------------------------------------------------------------
# BOTTLENECK DIAGNOSTICS & CORRECTIVE ACTIONS
# -----------------------------------------------------------------------------
CORRECTIVE_ACTIONS_LOOKUP = {
    "l_p95": {
        "issue": "Затримка P95 перевищує сценарний поріг L_threshold.",
        "severity": "High (Ризик виникнення Non-Conformance Alerts у U-space)",
        "action": "Збільшити пріоритет C2-каналу (перехід на 5G URLLC Slice), збільшити частоту f_up або звузити польотний коридор.",
        "owner": "Оператор БАС / Провайдер стільникового зв'язку"
    },
    "availability": {
        "issue": "Доступність каналу C2 нижче цільового значення 98.0%.",
        "severity": "Critical (Ризик втрати зв'язку та переходу в режим Lost Link)",
        "action": "Провести радіочастотний аудит покриття вздовж маршруту або переключитися на дубльований модуль (Dual-SIM / SatCom).",
        "owner": "Інженер з телекомунікацій / Оператор БАС"
    },
    "continuity": {
        "issue": "Виявлено тривалі розриви зв'язку (Outages > 2.0 с).",
        "severity": "High (Переривання безперервності передачі телеметрії)",
        "action": "Оптимізувати параметри хендоверу (Handover) між базовими станціями або підключити буферну чергу пакетів.",
        "owner": "Провайдер мережі зв'язку (MNO)"
    },
    "c2_data_completeness": {
        "issue": "Повнота послідовності пакетів нижче 99.5%.",
        "severity": "Medium (Втрата окремих телеметричних кадрів)",
        "action": "Перевірити бортовий модуль зв'язку на наявність переповнення буфера або електромагнітних завад.",
        "owner": "Бортовий інженер БАС"
    }
}