import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import config

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

# 3. GNSS Mode Selector
gnss_mode = st.sidebar.selectbox(
    t["gnss_mode"],
    options=["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"],
    index=st.session_state.selected_gnss_idx,
    key="gnss_mode"
)
st.session_state.selected_gnss_idx = ["GNSS RTK (0.8 - 2.0 м)", "GNSS 3D Fix (3.0 - 6.0 м)"].index(gnss_mode)

# Monte Carlo reproducibility controls
st.sidebar.markdown("### Відтворюваність Монте-Карло")
seed = st.sidebar.number_input("Random Seed", value=42, min_value=0, help="Сид для відтворюваності результатів Монте-Карло симуляції")

# Initialize random number generator
rng = np.random.default_rng(seed)

st.sidebar.markdown("---")

# ПРІОРИТЕТНОСТЕЙ: Операційний сценарій (SORA) ВИЗНАЧАЄ поріг безпеки L_threshold та f_up
corridor_width = 20.0
l_threshold_ms = 1000
f_up = 2.5
sail_level = "SAIL II"

if selected_scenario_preset != t["preset_none"]:
    sc_params = config.SCENARIO_PRESETS[selected_scenario_preset]["params"]
    corridor_width = sc_params["corridor_width"]
    l_threshold_ms = sc_params["l_threshold"]
    f_up = sc_params["f_up"]
    sail_level = sc_params["sail"]
elif selected_network_preset != t["preset_none"]:
    net_params = config.NETWORK_PRESETS[selected_network_preset]["params"]
    l_threshold_ms = net_params["l_threshold"]
    f_up = net_params["f_up"]
else:
    sail_level = st.sidebar.selectbox(t["sail_class"], ["SAIL II", "SAIL IV"])
    l_threshold_ms = st.sidebar.number_input(t["latency_threshold"], 100, 2000, 1000, 50)

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

    # 1. Clock Drift Correction & Latency Metrics
    raw_latencies = df['timestamp_server_ms'] - df['timestamp_board_ms']
    clock_offset = np.min(raw_latencies)
    latencies = np.maximum(raw_latencies - clock_offset, 1.0)
    l_p95 = np.percentile(latencies, 95)
    mean_latency = np.mean(latencies)

    # 2. Latency Factor (f_L)
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

    # 6. Weights according to SAIL level
    if sail_level == "SAIL II":
        w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_II
    else:
        w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_IV

    # 7. Final R_C2 Calculation
    R_C2 = w_A * availability + w_C * continuity + w_L * f_L + w_I * c2_data_completeness
    R_C2_pct = R_C2 * 100.0

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

# Determine overall status
status = config.STATUS_PASS if R_C2_pct >= config.R_C2_THRESHOLD_PCT else config.STATUS_FAIL

col_status, col_verdict = st.columns([1, 2])
with col_status:
    st.markdown(f"### {t['integral_indicator']}")
    st.metric(
        label=t["readiness_level"],
        value=f"{R_C2_pct:.1f}%",
        delta=f"{R_C2_pct - config.R_C2_THRESHOLD_PCT:.1f}% {t['threshold_text']}"
    )
with col_verdict:
    st.markdown(f"### {t['verdict_header']}")
    
    # Display status badge
    if status == config.STATUS_PASS:
        st.success(status)
    elif status == config.STATUS_CONDITIONAL:
        st.warning(status)
    elif status == config.STATUS_FAIL:
        st.error(status)
    else:
        st.info(status)

    # Display constraint violations if any
    constraint_violations = []
    if availability < config.AVAILABILITY_TARGET:
        constraint_violations.append(f"Доступність: {availability*100:.1f}% < {config.AVAILABILITY_TARGET*100}%")
    if continuity < config.CONTINUITY_TARGET:
        constraint_violations.append(f"Безперервність: {continuity*100:.1f}% < {config.CONTINUITY_TARGET*100}%")
    if l_p95 > l_threshold_ms:
        constraint_violations.append(f"Затримка P95: {l_p95:.1f}мс > {l_threshold_ms}мс")

    if constraint_violations:
        st.markdown("🚨 Виявлені критичні порушення (Hard Constraints):")
        for violation in constraint_violations:
            st.write(f"• {violation}")

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
tab_summary, tab_sensitivity, tab_monte_carlo, tab_telemetry = st.tabs([
    t["tab_analysis"], t["tab_sensitivity"], t["tab_monte_carlo"], t["tab_telemetry"]
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

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(t["footer"])
