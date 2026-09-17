import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import config
import hashlib

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="U-space C2 Readiness Validator",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'lang' not in st.session_state:
    st.session_state.lang = "Українська"

if 'current_df' not in st.session_state:
    st.session_state['current_df'] = None
if 'file_id' not in st.session_state:
    st.session_state['file_id'] = None

if 'has_run' not in st.session_state:
    st.session_state.has_run = False

if 'results' not in st.session_state:
    st.session_state.results = None

if 'last_results' not in st.session_state:
    st.session_state['last_results'] = None

if 'last_file_hash' not in st.session_state:
    st.session_state.last_file_hash = None

if 'selected_network_idx' not in st.session_state:
    st.session_state.selected_network_idx = 0

if 'selected_scenario_idx' not in st.session_state:
    st.session_state.selected_scenario_idx = 0

if 'selected_gnss_idx' not in st.session_state:
    st.session_state.selected_gnss_idx = 0

if 'show_docs' not in st.session_state:
    st.session_state['show_docs'] = False

# -----------------------------------------------------------------------------
# LANGUAGE SELECTOR
# -----------------------------------------------------------------------------
selected_lang_name = st.sidebar.selectbox(
    "🌐 Мова / Language",
    options=["Українська", "English"],
    index=["Українська", "English"].index(st.session_state.lang),
    key="lang_select"
)
st.session_state.lang = selected_lang_name

t = config.TRANSLATIONS.get(st.session_state.lang, config.TRANSLATIONS["Українська"])
lang_code = "ua" if st.session_state.lang == "Українська" else "en"

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(f'<p class="main-header">{t["main_header"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t["sub_header"]}</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: INPUT PARAMETERS, PRESETS & FILE UPLOAD
# -----------------------------------------------------------------------------
st.sidebar.header(t["sidebar_header"])
uploaded_file = st.sidebar.file_uploader(t["file_upload"], type=["csv"], key="csv_uploader")
st.sidebar.markdown("---")

# Initialize SAIL index in session state
if 'selected_sail_idx' not in st.session_state:
    st.session_state.selected_sail_idx = 1

# 1. Network Preset Selector
network_preset_options = [t["preset_none"]] + list(config.NETWORK_PRESETS.keys())
selected_network_preset = st.sidebar.selectbox(
    t["network_preset"],
    options=network_preset_options,
    index=st.session_state.selected_network_idx,
    key="network_preset"
)
st.session_state.selected_network_idx = network_preset_options.index(selected_network_preset)

if selected_network_preset != t["preset_none"]:
    preset_details = config.NETWORK_PRESETS[selected_network_preset]
    st.sidebar.caption(f"💡 {preset_details['help'][lang_code]}")

# 2. Operation Scenario Preset Selector
scenario_preset_options = [t["preset_none"]] + list(config.SCENARIO_PRESETS.keys())
selected_scenario_preset = st.sidebar.selectbox(
    t["scenario_preset"],
    options=scenario_preset_options,
    index=st.session_state.selected_scenario_idx,
    key="scenario_preset"
)
st.session_state.selected_scenario_idx = scenario_preset_options.index(selected_scenario_preset)

if selected_scenario_preset != t["preset_none"]:
    preset_details = config.SCENARIO_PRESETS[selected_scenario_preset]
    st.sidebar.caption(f"💡 {preset_details['help'][lang_code]}")

if selected_scenario_preset in getattr(config, 'PRESET_EXPLANATIONS_SHORT', {}):
    with st.sidebar.popover("📖 Коротке обґрунтування пресета"):
        info_short = config.PRESET_EXPLANATIONS_SHORT[selected_scenario_preset]
        st.markdown(f"#### {info_short['title']}")
        for item in info_short['qa_list']:
            st.markdown(f"**{item['q']}**")
            st.caption(item['a'])
            st.markdown("---")
        if st.button("📚 Відкрити повний нормативний довідник", key="btn_open_docs", use_container_width=True):
            st.session_state['show_docs'] = True
            st.rerun()

# -----------------------------------------------------------------------------
# L_THRESHOLD & f_up DISPLAY — прив'язані до активного пресета
# ПРІОРИТЕТ джерела: Operation Scenario > Network Preset > Manual override
# -----------------------------------------------------------------------------
corridor_width = 20.0
l_threshold_default = 1000
f_up = 2.5
sail_level_from_preset = None
l_threshold_source = None
l_threshold_locked = False

if selected_scenario_preset != t["preset_none"]:
    sc_params = config.SCENARIO_PRESETS[selected_scenario_preset]["params"]
    corridor_width = sc_params["corridor_width"]
    l_threshold_default = sc_params["l_threshold"]
    f_up = sc_params["f_up"]
    sail_level_from_preset = sc_params["sail"]
    l_threshold_source = f"🛸 Operation Scenario: {selected_scenario_preset}"
    l_threshold_locked = True
elif selected_network_preset != t["preset_none"]:
    net_params = config.NETWORK_PRESETS[selected_network_preset]["params"]
    l_threshold_default = net_params["l_threshold"]
    f_up = net_params["f_up"]
    l_threshold_source = f"⚡ Network Preset: {selected_network_preset}"
    l_threshold_locked = True
else:
    l_threshold_source = "✋ Manual override (no preset active)"
    l_threshold_locked = False

l_threshold_ms = st.sidebar.slider(
    label=t["latency_threshold"],
    min_value=50,
    max_value=2500,
    value=int(l_threshold_default),
    step=50,
    disabled=l_threshold_locked,
    help=f"Джерело значення: {l_threshold_source}. "
         f"Щоб рухати повзунок вручну, скиньте обидва пресети на '-- Оберіть пресет --'."
)

if l_threshold_locked:
    st.sidebar.caption(f"🔒 {l_threshold_source}")
else:
   st.sidebar.caption(f"🎚️ {l_threshold_source}")

st.sidebar.metric(
    label="Мінімальна частота f_up (Гц)",
    value=f"{f_up:.2f} Hz",
    help="Тягнеться з активного пресету. Порівнюється з фактичною частотою логу (CHK-005)."
)

st.sidebar.markdown("---")

# 3. GNSS Mode Selector
gnss_mode = st.sidebar.selectbox(
    t["gnss_mode"],
    options=["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"],
    index=st.session_state.selected_gnss_idx,
    key="gnss_mode"
)
st.session_state.selected_gnss_idx = ["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"].index(gnss_mode)

# 4. SAIL Risk Profile Selector (only used when no preset is selected)
sail_select = st.sidebar.selectbox(
    t["sail_class"],
    options=["SAIL I-II (Low Risk)", "SAIL III-IV (Medium Risk)", "SAIL V-VI (High Risk)"],
    index=st.session_state.get('selected_sail_idx', 1),
    key="sail_select",
    help="Сценарний профіль вимог для дослідження. Визначає суворість порогів затримки та вагові коефіцієнти."
)
st.session_state.selected_sail_idx = ["SAIL I-II (Low Risk)", "SAIL III-IV (Medium Risk)", "SAIL V-VI (High Risk)"].index(sail_select)

# Пресет сценарію ПЕРЕЗАПИСУЄ SAIL з селектора (нормативна консистентність)
if sail_level_from_preset is not None:
    sail_level = sail_level_from_preset
    _sail_options = ["SAIL I-II (Low Risk)", "SAIL III-IV (Medium Risk)", "SAIL V-VI (High Risk)"]
    if sail_level in _sail_options:
        st.session_state.selected_sail_idx = _sail_options.index(sail_level)
else:
    sail_level = sail_select

# Monte Carlo reproducibility controls
st.sidebar.markdown("### Відтворюваність Монте-Карло")
seed = st.sidebar.number_input("Random Seed", value=42, min_value=0, help="Сид для відтворюваності результатів Монте-Карло симуляції")

# Initialize random number generator
rng = np.random.default_rng(seed)

st.sidebar.markdown("---")


# Add these lines after line 22 (SESSION STATE INITIALIZATION section)
if 'current_df' not in st.session_state:
    st.session_state['current_df'] = None
if 'last_uploaded_filename' not in st.session_state:
    st.session_state['last_uploaded_filename'] = None

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(file_path_or_buffer):
    return pd.read_csv(file_path_or_buffer)

if uploaded_file is not None:
    current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    if current_file_id != st.session_state['file_id']:
        # Це новий файл
        st.session_state['file_id'] = current_file_id
        st.session_state['current_df'] = load_data(uploaded_file)
        st.session_state['last_results'] = None # Скидаємо старі результати
        st.sidebar.success(t["log_loaded"])
    df = st.session_state['current_df']
else:
    if st.session_state['current_df'] is None:
        try:
            df = load_data("flight_telemetry_log.csv")
            st.session_state['current_df'] = df
            st.sidebar.info(t["demo_log"])
        except Exception:
            st.error("Будь ласка, завантажте CSV-файл телеметрії.")
            st.stop()
    df = st.session_state['current_df']

# -----------------------------------------------------------------------------
# DATA VALIDATION
# -----------------------------------------------------------------------------
def validate_telemetry_log(df, l_threshold_ms):
    """Comprehensive data quality validation for telemetry logs."""
    errors = []
    warnings = []

    # 1. Check required columns
    missing_columns = [col for col in config.REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Відсутні обов'язкові колонки: {missing_columns}")

    # 2. Check numeric columns
    numeric_columns = ['timestamp_board_ms', 'timestamp_server_ms', 'seq_id']
    for col in numeric_columns:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Колонка '{col}' має нечисловий тип даних")
            elif df[col].isna().any():
                errors.append(f"Колонка '{col}' містить відсутні значення (NaN)")
            elif np.isinf(df[col]).any():
                errors.append(f"Колонка '{col}' містить нескінченні значення")

    # 3. Check timestamp monotonicity
    if 'timestamp_board_ms' in df.columns:
        if not df['timestamp_board_ms'].is_monotonic_increasing:
            warnings.append("Мітки часу 'timestamp_board_ms' не є монотонно зростаючими")

    # 4. Check seq_id duplicates
    if 'seq_id' in df.columns:
        duplicate_seq = df['seq_id'].duplicated().sum()
        if duplicate_seq > 0:
            warnings.append(f"Знайдено {duplicate_seq} дублікатів у колонці 'seq_id'")

    # 5. Check latency threshold validation
    if l_threshold_ms >= config.L_MAX:
        errors.append(
            f"L_threshold ({l_threshold_ms} мс) не може бути більшим або рівним "
            f"L_MAX ({config.L_MAX} мс)"
        )

    return errors, warnings


errors, warnings = validate_telemetry_log(df, l_threshold_ms)

if errors:
    st.error("🚨 ВИЯВЛЕНО КРИТИЧНІ ПОМИЛКИ В ЛОЗІ ТЕЛЕМЕТРІЇ:")
    for error in errors:
        st.error(f"• {error}")

    st.markdown("---")
    st.subheader("📊 Звіт про якість даних (Data Quality Report)")
    quality_data = []
    for error in errors:
        quality_data.append({"Тип": "ПОМИЛКА", "Опис": error, "Статус": "❌ КРИТИЧНО"})
    for warning in warnings:
        quality_data.append({"Тип": "ПОПЕРЕДЖЕННЯ", "Опис": warning, "Статус": "⚠️ УВАГА"})

    if quality_data:
        st.dataframe(pd.DataFrame(quality_data))

    st.stop()

if warnings:
    st.warning("⚠️ ВИЯВЛЕНО ПОПЕРЕДЖЕННЯ В ЛОЗІ ТЕЛЕМЕТРІЇ:")
    for warning in warnings:
        st.warning(f"• {warning}")

# -----------------------------------------------------------------------------
# METRIC COMPUTATION
# -----------------------------------------------------------------------------
def compute_metrics(df, l_threshold_ms, f_up, sail_level, gnss_mode):
    """Compute all C2 readiness metrics."""
    # Edge case protection: check log duration and row count
    if len(df) < 2:
        return None

    delta_time = df['timestamp_board_ms'].iloc[-1] - df['timestamp_board_ms'].iloc[0]
    if delta_time <= 0:
        return None

    # 1. Log metadata: SHA-256 Hash and time window
    # 1. SHA-256 Hash файлу/лог-даних
    log_bytes = df.to_csv(index=False).encode('utf-8')
    dataset_hash = hashlib.sha256(log_bytes).hexdigest()[:16]

    # 2. Обсяг та часове вікно
    sample_count = len(df)
    t_start_ms = df['timestamp_board_ms'].min()
    t_end_ms = df['timestamp_board_ms'].max()
    duration_s = (t_end_ms - t_start_ms) / 1000.0
    time_window_str = f"Duration: {duration_s:.1f}s (Board TS: {t_start_ms}ms - {t_end_ms}ms)"

    # 2. Clock Drift Correction & Latency Metrics
    raw_latencies = df['timestamp_server_ms'] - df['timestamp_board_ms']
    clock_offset = np.min(raw_latencies)
    latencies = np.maximum(raw_latencies - clock_offset, 1.0)
    l_p95 = np.percentile(latencies, 95)
    mean_latency = np.mean(latencies)

    # 3. Latency Factor (f_L)
    denominator = config.L_MAX - l_threshold_ms
    if denominator <= 0:
        raise ValueError(
            f"L_threshold ({l_threshold_ms} мс) має бути меншим за L_MAX "
            f"({config.L_MAX} мс), інакше формула f_L призводить до ділення на нуль."
        )
    f_L = max(0.0, min(1.0, (config.L_MAX - l_p95) / denominator))

    # 3. C2 Availability
    n_valid = df['seq_id'].nunique()
    total_time_s = (df['timestamp_board_ms'].iloc[-1] - df['timestamp_board_ms'].iloc[0]) / 1000.0
    n_expected = int(np.floor(total_time_s * f_up)) + 1
    availability = min(1.0, max(0.0, n_valid / max(n_expected, 1)))
    if n_valid > n_expected:
        warnings.append("Кількість отриманих пакетів перевищує очікувану (перевірте дублікати або f_up)")

    # 4. Temporal Continuity
    t_gaps = np.diff(df['timestamp_board_ms']) / 1000.0
    outage_gaps = t_gaps[t_gaps > config.MIN_OUTAGE_GAP_S]
    total_outage_time_s = np.sum(outage_gaps)
    total_time_s = (df['timestamp_board_ms'].iloc[-1] - df['timestamp_board_ms'].iloc[0]) / 1000.0
    continuity = max(0.0, min(1.0, 1.0 - (total_outage_time_s / max(total_time_s, 1.0))))
    max_outage_duration_s = float(np.max(outage_gaps)) if len(outage_gaps) > 0 else 0.0
    outage_events_count = int(len(outage_gaps))

    # 5. C2 Data Completeness
    seq_range = df['seq_id'].max() - df['seq_id'].min() + 1
    c2_data_completeness = max(0.0, min(1.0, df['seq_id'].nunique() / max(seq_range, 1)))

    # 6. GNSS Fix Compliance
    if 'gnss_fix_type' in df.columns:
        if gnss_mode == "GNSS RTK (0.8 - 2.0 м)":
            f_gnss = float((df['gnss_fix_type'] == 4).mean())
        else:
            f_gnss = float((df['gnss_fix_type'] >= 3).mean())
    else:
        f_gnss = 1.0

    # 6. Weights per SAIL profile — single source of truth in config.SAIL_WEIGHTS
    sail_level_normalized = config.SAIL_ALIASES.get(sail_level, sail_level)
    if sail_level_normalized not in config.SAIL_WEIGHTS:
        raise ValueError(
            f"Unknown SAIL profile '{sail_level}'. "
            f"Expected one of: {list(config.SAIL_WEIGHTS.keys())}"
        )
    w_A, w_C, w_L, w_I = config.SAIL_WEIGHTS[sail_level_normalized]

    # 7. Control Checks (CHK-001 ... CHK-005)
    sanity_results = []

    # CHK-001: Monotonicity
    is_monotonic = df['timestamp_board_ms'].is_monotonic_increasing
    sanity_results.append({
        "id": "CHK-001", "name": "Monotonicity Check",
        "passed": bool(is_monotonic),
        "details": "Timestamp board ms зростає монотонно" if is_monotonic else "Виявлено порушення хронології часу"
    })

    # CHK-002: Sequence Integrity & Duplicates
    has_seq = 'seq_id' in df.columns
    seq_duplicates = df['seq_id'].duplicated().sum() if has_seq else 0
    seq_passed = bool(has_seq and seq_duplicates == 0)
    sanity_results.append({
        "id": "CHK-002", "name": "Sequence Integrity Check",
        "passed": seq_passed,
        "details": "Послідовність seq_id коректна, дублікатів немає" if seq_passed else f"Виявлено {seq_duplicates} дублікатів у seq_id"
    })

    # CHK-003: Duration Sufficiency
    dur_passed = bool(duration_s >= 10.0)
    sanity_results.append({
        "id": "CHK-003", "name": "Duration Sufficiency",
        "passed": dur_passed,
        "details": f"Тривалість {duration_s:.1f}s (≥ 10s)" if dur_passed else f"Занадто короткий лог ({duration_s:.1f}s < 10s)"
    })

    # CHK-004: Zero/Negative Delay
    raw_lat = df['timestamp_server_ms'] - df['timestamp_board_ms']
    neg_lat_count = (raw_lat < 0).sum()
    delay_passed = bool(neg_lat_count == 0)
    sanity_results.append({
        "id": "CHK-004", "name": "Clock Relation Check",
        "passed": delay_passed,
        "details": "Часові позначки сервера та борту узгоджени" if delay_passed else f"Виявлено {neg_lat_count} від'ємних затримок"
    })

    # CHK-005: Sampling Rate Alignment
    actual_f_up = sample_count / duration_s if duration_s > 0 else 0.0
    freq_diff = abs(actual_f_up - f_up) / f_up if f_up > 0 else 1.0
    freq_passed = bool(freq_diff <= 0.5)  # Допуск 50%
    sanity_results.append({
        "id": "CHK-005", "name": "Sampling Rate Alignment",
        "passed": freq_passed,
        "details": f"Фактична частота {actual_f_up:.1f} Гц узгоджена з f_up ({f_up} Гц)" if freq_passed else f"Фактична частота {actual_f_up:.1f} Гц суттєво відрізняється від {f_up} Гц"
    })

    # 8. Aggregation Models (R_linear, R_geom, R_min)
    # Нормалізовані показники (0..1)
    f_L = max(0.0, min(1.0, (config.L_MAX - l_p95) / (config.L_MAX - l_threshold_ms))) if config.L_MAX > l_threshold_ms else 0.0

    # Model 1: Linear Weighted Sum
    r_linear = w_A * availability + w_C * continuity + w_L * f_L + w_I * c2_data_completeness

    # Model 2: Geometric Mean
    r_geom = (availability**w_A) * (continuity**w_C) * (f_L**w_L) * (c2_data_completeness**w_I)

    # Model 3: Minimum Criterion (Weakest Link)
    r_min = min(availability, continuity, f_L, c2_data_completeness)

    # 9. Final R_C2 Calculation
    R_C2 = w_A * availability + w_C * continuity + w_L * f_L + w_I * c2_data_completeness
    R_C2_pct = R_C2 * 100.0

    # 10. Store results in session state
    if st.session_state.get('last_results') is None:
        st.session_state['last_results'] = {}
    st.session_state['last_results'].update({
        "dataset_hash": dataset_hash,
        "sample_count": sample_count,
        "duration_s": duration_s,
        "time_window_str": time_window_str,
        "sanity_results": sanity_results,
        "r_linear": r_linear * 100.0,
        "r_geom": r_geom * 100.0,
        "r_min": r_min * 100.0,
        "f_L_norm": f_L
    })

    return {
        'availability': availability,
        'continuity': continuity,
        'f_L': f_L,
        'c2_data_completeness': c2_data_completeness,
        'f_gnss': f_gnss,
        'R_C2': R_C2,
        'R_C2_pct': R_C2_pct,
        'l_p95': l_p95,
        'mean_latency': mean_latency,
        'w_A': w_A,
        'w_C': w_C,
        'w_L': w_L,
        'w_I': w_I,
        'latencies': latencies,
        'l_threshold_ms': l_threshold_ms,
        'f_up': f_up,
        'sail_level': sail_level
    }


# -----------------------------------------------------------------------------
# RUN BUTTON: CALCULATION IS PERFORMED ONLY ON EXPLICIT USER ACTION
# -----------------------------------------------------------------------------
run_btn = st.sidebar.button(
    "▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ / CALCULATE & SIMULATE",
    type="primary",
    width='stretch'
)

if run_btn:
    try:
        results = compute_metrics(df, l_threshold_ms, f_up, sail_level, gnss_mode)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    if results is not None:
        st.session_state.results = results
        st.session_state.has_run = True
        st.session_state.last_file_hash = hash(uploaded_file.getvalue()) if uploaded_file else hash(str(df))
        st.session_state['last_results'] = results
    else:
        st.error("Неможливо розрахувати метрики. Перевірте вхідні дані.")
        st.stop()

# -----------------------------------------------------------------------------
# DOCS OVERVIEW: Display full U-space documentation if requested (outside Execution Guard)
# -----------------------------------------------------------------------------
if st.session_state.get('show_docs', False):
    if selected_scenario_preset in getattr(config, 'PRESET_EXPLANATIONS_FULL', {}):
        full_info = config.PRESET_EXPLANATIONS_FULL[selected_scenario_preset]
        st.subheader(full_info['title'])
        st.write(full_info['intro'])
        st.markdown("---")
        for sec in full_info['sections']:
            st.markdown(f"### {sec['question']}")
            st.write(sec['answer'])
            st.caption(f"📑 **Нормативне джерело**: {sec['normative']}")
            st.markdown("---")
    st.button("❌ Закрити довідник", on_click=lambda: st.session_state.update(show_docs=False), key="close_docs_btn")

# -----------------------------------------------------------------------------
# EXECUTION GUARD: RESULTS ARE SHOWN ONLY AFTER THE BUTTON IS CLICKED
# -----------------------------------------------------------------------------
if st.session_state.get('last_results') is not None:
    results = st.session_state['last_results']
elif not st.session_state.get('has_run', False):
    st.info(
        "👈 Налаштуйте вхідні параметри або оберіть пресети у бічній панелі та "
        "натисніть кнопку [▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ], щоб розпочати діагностику."
    )
    st.stop()

# Only show log change warning if there are actual calculation results
if st.session_state.get('last_results') is not None and st.session_state.get('last_file_hash') != (
    hash(uploaded_file.getvalue()) if uploaded_file else hash(str(df))
):
    st.warning(
        "⚠️ Лог телеметрії змінився. Натисніть кнопку "
        "[▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ] для перерахунку метрик."
    )
    st.stop()

results = st.session_state.get('results')
if results is None:
    st.error(
        "Результати обчислень відсутні. Натисніть кнопку "
        "[▶ РОЗРАХУВАТИ ТА СИМУЛЮВАТИ] для розрахунку."
    )
    st.stop()

# -----------------------------------------------------------------------------
# MAIN DASHBOARD LAYOUT
# -----------------------------------------------------------------------------
availability = results['availability']
continuity = results['continuity']
f_L = results['f_L']
c2_data_completeness = results['c2_data_completeness']
f_gnss = results['f_gnss']
R_C2 = results['R_C2']
R_C2_pct = results['R_C2_pct']
l_p95 = results['l_p95']
mean_latency = results['mean_latency']
w_A, w_C, w_L, w_I = results['w_A'], results['w_C'], results['w_L'], results['w_I']
latencies = results['latencies']
l_threshold_ms = results['l_threshold_ms']
f_up = results['f_up']
sail_level = results['sail_level']

# Determine constraint violations
constraint_violations = []
if availability < config.AVAILABILITY_TARGET:
    constraint_violations.append(f"Доступність: {availability*100:.1f}% < {config.AVAILABILITY_TARGET*100}%")
if continuity < config.CONTINUITY_TARGET:
    constraint_violations.append(f"Безперервність: {continuity*100:.1f}% < {config.CONTINUITY_TARGET*100}%")
if l_p95 > l_threshold_ms:
    constraint_violations.append(f"Затримка P95: {l_p95:.1f}мс > {l_threshold_ms}мс")

# SAIL-specific R_C2 pass threshold (differentiated per SORA 2.5 Annex E OSO#06 assurance level)
r_c2_threshold = config.get_r_c2_threshold(sail_level)

# Determine overall status
if constraint_violations:
    status = config.STATUS_FAIL
else:
    if R_C2_pct >= r_c2_threshold:
        status = config.STATUS_PASS
    else:
        status = config.STATUS_CONDITIONAL

col_status, col_verdict = st.columns([1, 2])
with col_status:
    st.markdown(f"### {t['integral_indicator']}")
    st.metric(
        label=t["readiness_level"],
        value=f"{R_C2_pct:.1f}%",
     delta=f"{R_C2_pct - r_c2_threshold:.1f}% від порогу {r_c2_threshold:.0f}% (SAIL: {sail_level})"
    )
with col_verdict:
    st.markdown(f"### {t['verdict_header']}")
    
    # Display status badge and constraint violations
    if status == config.STATUS_PASS:
        st.success(status)
    elif status == config.STATUS_CONDITIONAL:
        st.warning(status)
    elif status == config.STATUS_FAIL:
        if constraint_violations:
            # Display red FAIL block with the list of detected violations
            error_msg = f"**{status}**\n\n🚨 **Виявлені критичні порушення (Hard Constraints):**\n"
            for violation in constraint_violations:
                error_msg += f"- {violation}\n"
            st.error(error_msg)
        else:
            st.error(status)
    else:
        st.info(status)

st.markdown("---")

# Key Indicators KPI Row
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

# Dynamic threshold highlighting with green/red badges
availability_delta = (
    f"{config.AVAILABILITY_TARGET*100:.1f}%"
    if availability >= config.AVAILABILITY_TARGET
    else f"↓ {config.AVAILABILITY_TARGET*100:.1f}%"
)
availability_color = "normal" if availability >= config.AVAILABILITY_TARGET else "inverse"

continuity_delta = (
    f"{config.CONTINUITY_TARGET*100:.1f}%"
    if continuity >= config.CONTINUITY_TARGET
    else f"↓ {config.CONTINUITY_TARGET*100:.1f}%"
)
continuity_color = "normal" if continuity >= config.CONTINUITY_TARGET else "inverse"

completeness_delta = (
    f"{config.COMPLETENESS_TARGET*100:.1f}%"
    if c2_data_completeness >= config.COMPLETENESS_TARGET
    else f"↓ {config.COMPLETENESS_TARGET*100:.1f}%"
)
completeness_color = "normal" if c2_data_completeness >= config.COMPLETENESS_TARGET else "inverse"

latency_delta = f"{l_threshold_ms} ms" if l_p95 <= l_threshold_ms else f"↓ {l_threshold_ms} ms"
latency_color = "normal" if l_p95 <= l_threshold_ms else "inverse"

gnss_delta = "100%" if f_gnss >= 1.0 else f"↓ 100%"
gnss_color = "normal" if f_gnss >= 1.0 else "inverse"

kpi1.metric(t["availability"], f"{availability*100:.2f}%", availability_delta, delta_color=availability_color, help=t["availability_help"])
kpi2.metric(t["continuity"], f"{continuity*100:.2f}%", continuity_delta, delta_color=continuity_color, help=t["continuity_help"])
kpi3.metric("C2 Data Completeness", f"{c2_data_completeness*100:.2f}%", completeness_delta, delta_color=completeness_color, help="Частка отриманих пакетів відносно очікуваних")
kpi4.metric(t["latency"], f"{l_p95:.1f} ms", latency_delta, delta_color=latency_color, help=t["latency_help"])
kpi5.metric("PNT GNSS Fix Compliance", f"{f_gnss*100:.2f}%", gnss_delta, delta_color=gnss_color, help="Відсоток RTK/3D фіксів")

# Add captions with normative sources
st.caption("Engineering Target / SORA 2.5")

st.markdown("---")

# -----------------------------------------------------------------------------
# CHARTS & DIAGNOSTICS SECTION
# -----------------------------------------------------------------------------
tab_summary, tab_sensitivity, tab_monte_carlo, tab_telemetry, tab_matrix, tab_docs = st.tabs([
    t["tab_analysis"],
    t["tab_sensitivity"],
    t["tab_monte_carlo"],
    t["tab_telemetry"],
    "📋 Requirement Traceability & Evidence",
    "📚 Довідник U-space"
])

with tab_summary:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader(t["latency_distribution"])
        fig_lat = px.histogram(x=latencies, nbins=50, labels={'x': t["latency_xlabel"], 'y': t["latency_ylabel"]})
        fig_lat.add_vline(x=l_threshold_ms, line_dash="dash", line_color="red", annotation_text=t["threshold_annotation"].format(l_threshold_ms))
        st.plotly_chart(fig_lat, width='stretch')

    with col_chart2:
        st.subheader(t["radar_title"])
        categories = t["radar_categories"]
        values = [availability * 100, continuity * 100, f_L * 100, c2_data_completeness * 100]
        fig_radar = go.Figure()
        # Add current performance trace
        fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', name=t["current_board"]))

        # Add regulatory requirements contour
        regulatory_values = [
            config.AVAILABILITY_TARGET * 100,
            config.CONTINUITY_TARGET * 100,
            config.LATENCY_TARGET_MS / l_threshold_ms * 100,
            config.INTEGRITY_TARGET * 100
        ]
        fig_radar.add_trace(go.Scatterpolar(
            r=regulatory_values + [regulatory_values[0]],
            theta=categories + [categories[0]],
            name="Нормативні сценарні вимоги (Engineering Targets)",
            mode='lines+markers',
            line=dict(color='red', dash='dash', width=2),
            marker=dict(color='red', size=6)
        ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True
        )
        st.plotly_chart(fig_radar, width='stretch')

with tab_sensitivity:
    st.subheader("🔬 Sensitivity Analysis (Аналіз чутливості вагових коефіцієнтів)")
    delta = config.SENSITIVITY_DELTA
    base_weights = np.array([w_A, w_C, w_L, w_I])
    metrics = np.array([availability, continuity, f_L, c2_data_completeness])

    factors = [t["availability"], t["continuity"], t["latency"], t["integrity"]]
    sens_data = []

    for i, factor_name in enumerate(factors):
        # 1. Додаємо delta до i-ї ваги
        w_temp = base_weights.copy()
        w_temp[i] += delta

        # 2. Нормуємо вектор, щоб сума ваг строго дорівнювала 1.0
        w_norm = w_temp / np.sum(w_temp)

        # 3. Обчислюємо коректне значення R_C2 (не перевищує 1.0)
        r_c2_sens = np.sum(w_norm * metrics)

        sens_data.append({
            "Factor": f"{factor_name} (+{int(delta*100)}%)",
            "R_C2 (%)": r_c2_sens * 100.0,
            "Delta (%)": (r_c2_sens - R_C2) * 100.0
        })

    df_sens = pd.DataFrame(sens_data)
    fig_sens = px.bar(
        df_sens,
        x="Factor",
        y="R_C2 (%)",
        text_auto='.2f',
        color="Delta (%)",
        color_continuous_scale="Viridis"
    )
    fig_sens.add_hline(y=config.R_C2_THRESHOLD_PCT, line_dash="dash", line_color="red")
    fig_sens.update_layout(yaxis_range=[0, 105])
    st.plotly_chart(fig_sens, width='stretch')

with tab_monte_carlo:
    st.subheader(t["monte_carlo_title"])
    n_simulations = 1000
    mu = np.log(max(mean_latency, 1.0)) - 0.5 * (0.4 ** 2)
    simulated_latencies = rng.lognormal(mean=mu, sigma=0.4, size=n_simulations)

    # Vectorized calculation of sim_f_L using np.clip
    sim_f_L = np.clip((config.L_MAX - simulated_latencies) / (config.L_MAX - l_threshold_ms), 0.0, 1.0)

    sim_availability = rng.beta(a=max(availability * 100, 1), b=max((1 - availability) * 100, 1), size=n_simulations)
    sim_continuity = rng.beta(a=max(continuity * 100, 1), b=max((1 - continuity) * 100, 1), size=n_simulations)
    sim_completeness = rng.beta(a=max(c2_data_completeness * 100, 1), b=max((1 - c2_data_completeness) * 100, 1), size=n_simulations)

    sim_R_C2 = w_A * sim_availability + w_C * sim_continuity + w_L * sim_f_L + w_I * sim_completeness
    sim_R_C2_pct = sim_R_C2 * 100.0

    # Calculate 95% confidence interval
    ci_lower = np.percentile(sim_R_C2_pct, 2.5)
    ci_upper = np.percentile(sim_R_C2_pct, 97.5)

    fig_mc = px.histogram(x=sim_R_C2_pct, nbins=50, labels={'x': t["monte_carlo_xlabel"], 'y': t["monte_carlo_ylabel"]})
    fig_mc.add_vline(x=config.R_C2_THRESHOLD_PCT, line_dash="dash", line_color="red", annotation_text="80% Threshold")
    st.plotly_chart(fig_mc, width='stretch')

    prob_success = np.mean(sim_R_C2_pct >= config.R_C2_THRESHOLD_PCT) * 100.0
    st.metric(label=t["probability_text"].split("=")[0], value=f"{prob_success:.1f}%", delta=f"Mean R_C2: {np.mean(sim_R_C2_pct):.1f}%")
    st.write(f"95% довірчий інтервал: [{ci_lower:.1f}%, {ci_upper:.1f}%]")

with tab_telemetry:
    if 'lat' in df.columns and 'lon' in df.columns:
        st.subheader(t["flight_map"])
        st.map(df[['lat', 'lon']])
    st.subheader(t["raw_log"])
    st.dataframe(df.head(20))

with tab_matrix:
    st.header("📋 Матриця простежуваності вимог та доказів (Requirement Traceability & Evidence Record)")
    st.caption("Рівень B: Автоматична верифікація відповідності телеметрії нормативним вимогам Regulation (EU) 2021/664, ASTM F3548-21 та SORA 2.5 із фіксацією провінансу (Provenance) та формуванням доказового звіту.")
    
    res = st.session_state['last_results']
    
    # ---------------------------------------------------------------------
    # БЛОК 1: EVIDENCE METADATA & DATA SANITY REPORT
    # ---------------------------------------------------------------------
    st.subheader("1. Метадані доказової бази та перевірка якості логу (Data Sanity)")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("SHA-256 Dataset Hash", res.get("dataset_hash", "N/A"))
    m_col2.metric("Обсяг кадрів (N_samples)", f"{res.get('sample_count', 0):,} пакетів")
    m_col3.metric("Тривалість логу", f"{res.get('duration_s', 0.0):.1f} сек")
    m_col4.metric("Монте-Карло Seed", seed)
    
    st.caption(f"🗓️ **Часове вікно**: {res.get('time_window_str', 'N/A')}")
    
    # Таблиця Control Checks
    sanity_list = res.get("sanity_results", [])
    if sanity_list:
        sanity_df = pd.DataFrame(sanity_list)
        sanity_df['Статус'] = sanity_df['passed'].apply(lambda x: "🟢 PASSED" if x else "🔴 FAILED")
        sanity_df_display = sanity_df[['id', 'name', 'Статус', 'details']].rename(columns={
            'id': 'ID перевірки', 'name': 'Назва Control Check', 'details': 'Результат та деталі'
        })
        st.dataframe(sanity_df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # БЛОК 2: REQUIREMENT TRACEABILITY MATRIX
    # ---------------------------------------------------------------------
    st.subheader("2. Матриця простежуваності нормативних вимог (Traceability Matrix)")
    
    matrix_rows = []
    for req in config.REQUIREMENT_REGISTER:
        val = res.get(req["metric_key"], 0.0)
        
        # Визначення статусів і порогів
        if req["id"] == "C2-LAT-001":
            target_limit = res["l_threshold_ms"]
            passed = (val <= target_limit)
            val_str = f"{val:.1f} мс"
            target_str = f"≤ {target_limit:.0f} мс"
        elif req["id"] == "NAV-FIX-001" and 'gnss_fix_type' not in df.columns:
            passed = None
            val_str = "N/A"
            target_str = req["target_text"]
        else:
            target_limit = req["target_val"]
            passed = (val >= target_limit)
            val_str = f"{val*100:.2f}%"
            target_str = req["target_text"]
        
        if passed is True:
            verdict = "🟢 PASS"
        elif passed is False:
            verdict = "🔴 FAIL"
        else:
            verdict = "⚪ NOT ASSESSABLE"
            
        matrix_rows.append({
            "Req ID": req["id"],
            "Назва вимоги": req["title"],
            "Джерело & Статус норми (Provenance)": f"{req['source']} — {req['provenance']}",
            "Поле CSV": req["parameter"],
            "Нормативний поріг": target_str,
            "Фактичне значення": val_str,
            "Вердикт": verdict
        })
    
    st.table(pd.DataFrame(matrix_rows))
    
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # БЛОК 3: AGGREGATION MODEL COMPARISON
    # ---------------------------------------------------------------------
    st.subheader("3. Академічне порівняння моделей агрегації (Baseline Aggregation Comparison)")
    st.caption("Порівняння 3-х математичних підходів до формування підсумкового індексу готовності C2 для Розділу 2/3 диплома:")
    
    a_col1, a_col2, a_col3 = st.columns(3)
    a_col1.metric(
        "Лінійна зважена сума (R_linear)",
        f"{res.get('r_linear', 0.0):.1f}%",
        help=config.AGGREGATION_MODELS["linear"]["description"]
    )
    a_col2.metric(
        "Геометричне середнє (R_geom)",
        f"{res.get('r_geom', 0.0):.1f}%",
        help=config.AGGREGATION_MODELS["geometric"]["description"]
    )
    a_col3.metric(
        "Найслабша ланка (R_min)",
        f"{res.get('r_min', 0.0):.1f}%",
        help=config.AGGREGATION_MODELS["minimum"]["description"]
    )
    
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # БЛОК 4: BOTTLENECK DIAGNOSTICS & CORRECTIVE ACTIONS
    # ---------------------------------------------------------------------
    st.subheader("4. Діагностика 'вузьких місць' та план усунення (Corrective Actions Plan)")
    
    detected_bottlenecks = []
    if res.get("l_p95", 0.0) > res.get("l_threshold_ms", 1000):
        detected_bottlenecks.append("l_p95")
    if res.get("availability", 0.0) < config.AVAILABILITY_TARGET:
        detected_bottlenecks.append("availability")
    if res.get("continuity", 0.0) < config.CONTINUITY_TARGET:
        detected_bottlenecks.append("continuity")
    if res.get("c2_data_completeness", 0.0) < config.COMPLETENESS_TARGET:
        detected_bottlenecks.append("c2_data_completeness")
        
    if detected_bottlenecks:
        st.warning("🚨 **Виявлено деградацію показників C2-лінку! Рекомендовано наступні корегувальні дії:**")
        for key_b in detected_bottlenecks:
            act_info = config.CORRECTIVE_ACTIONS_LOOKUP.get(key_b, {})
            with st.expander(f"🔴 Проблема: {act_info.get('issue', key_b)} ({act_info.get('severity', '')})", expanded=True):
                st.write(f"**Рекомендована інженерна дія**: {act_info.get('action', 'N/A')}")
                st.caption(f"👤 **Відповідальна сторона**: {act_info.get('owner', 'N/A')}")
    else:
        st.success("✅ **'Вузьких місць' не виявлено.** Усі показники C2-лінку знаходяться в межах встановлених сценарних норм!")
        
    st.markdown("---")
    
    # ---------------------------------------------------------------------
    # БЛОК 5: HUMAN REVIEWER SIGN-OFF & EXPORT
    # ---------------------------------------------------------------------
    st.subheader("5. Картка інженерного затвердження та експорт звіту (Technical Sign-Off)")
    
    rev_col1, rev_col2 = st.columns(2)
    with rev_col1:
        reviewer_name = st.text_input("ПІБ відповідального інженера / рецензента USSP:", value="Оператор БАС / Інженер C2")
        review_notes = st.text_area("Інженерні коментарі та особливі умови:", value="Попередній скринінг виконано успішно. Лог підтверджує відсутність критичних завад.")
    with rev_col2:
        st.markdown("**Прийняті припущення (Accepted Assumptions):**")
        st.checkbox("Звірено з нормативною базою EU Regulation 2021/664 Art. 13", value=True)
        st.checkbox("Підтверджено придатність часового вікна та SHA-256 хешу логу", value=True)
        st.checkbox("Монте-Карло симуляція виконана з фіксованим Random Seed", value=True)
        
        # Формування підписаного JSON-звіту для завантаження
        export_report = {
            "tool_version": "2.0",
            "reviewer": reviewer_name,
            "review_notes": review_notes,
            "dataset_hash": res.get("dataset_hash"),
            "time_window": res.get("time_window_str"),
            "metrics": {
                "availability": res.get("availability"),
                "continuity": res.get("continuity"),
                "l_p95_ms": res.get("l_p95"),
                "c2_completeness": res.get("c2_data_completeness"),
                "R_linear_pct": res.get("r_linear"),
                "R_geom_pct": res.get("r_geom"),
                "R_min_pct": res.get("r_min")
            },
            "control_checks": res.get("sanity_results")
        }
        
        import json
        report_json_bytes = json.dumps(export_report, ensure_ascii=False, indent=2).encode('utf-8')
        
        st.download_button(
            label="📥 Завантажити технічний звіт доказів (JSON)",
            data=report_json_bytes,
            file_name=f"c2_evidence_report_{res.get('dataset_hash', 'log')}.json",
            mime="application/json",
            width="stretch"
        )

with tab_docs:
    st.header("📚 Інженерно-нормативний довідник U-space")
    if selected_scenario_preset in getattr(config, 'PRESET_EXPLANATIONS_FULL', {}):
        full_info = config.PRESET_EXPLANATIONS_FULL[selected_scenario_preset]
        st.subheader(full_info['title'])
        st.write(full_info['intro'])
        st.markdown("---")
        for sec in full_info['sections']:
            st.markdown(f"### {sec['question']}")
            st.write(sec['answer'])
            st.caption(f"📑 **Нормативне джерело**: {sec['normative']}")
            st.markdown("---")
    else:
        st.info("Оберіть операційний сценарій у бічній панелі для перегляду розгорнутого нормативного аналізу.")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(t["footer"])
