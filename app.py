import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import config

# -----------------------------------------------------------------------------\
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="U-space C2 Readiness Validator",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------\
# INTERNATIONALIZATION (i18n) DICTIONARY
# -----------------------------------------------------------------------------

# Custom CSS styling
st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------\
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'has_run' not in st.session_state:
    st.session_state['has_run'] = False
if 'preset_applied' not in st.session_state:
    st.session_state.preset_applied = False
    st.session_state.corridor_width = 20.0
    st.session_state.l_threshold = 1000
    st.session_state.telemetry_freq = 2.5
    st.session_state.sail_index = 0

# -----------------------------------------------------------------------------\
# LANGUAGE SELECTOR
# -----------------------------------------------------------------------------
lang_map = {"Українська": "ua", "English": "en"}
selected_lang_name = st.sidebar.selectbox("🌐 Мова / Language", ["Українська", "English"])
lang_code = lang_map[selected_lang_name]
t = config.TRANSLATIONS[selected_lang_name]

# -----------------------------------------------------------------------------\
# HEADER
# -----------------------------------------------------------------------------
st.markdown(f'<p class="main-header">{t["main_header"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t["sub_header"]}</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------\
# SIDEBAR: INPUT PARAMETERS & FILE UPLOAD
# -----------------------------------------------------------------------------
st.sidebar.header(t["sidebar_header"])
uploaded_file = st.sidebar.file_uploader(t["file_upload"], type=["csv"])
st.sidebar.markdown("---")

# Network Preset Selector
network_preset_options = [t["preset_none"]] + list(config.NETWORK_PRESETS.keys())
selected_network_preset = st.sidebar.selectbox(
    t["network_preset"],
    options=network_preset_options,
    index=0
)

# Apply Network Preset and show help
if selected_network_preset != t["preset_none"]:
    preset_config = config.NETWORK_PRESETS[selected_network_preset]
    st.session_state.l_threshold = preset_config["params"]["l_threshold"]
    st.session_state.telemetry_freq = preset_config["params"]["telemetry_freq"]
    st.sidebar.info(preset_config["help"][lang_code])
    
# Operation Scenario Preset Selector
operation_preset_options = [t["preset_none"]] + list(config.OPERATION_PRESETS.keys())

selected_operation_preset = st.sidebar.selectbox(
    t["operation_preset"],
    options=operation_preset_options,
    index=0
)

# Apply Operation Scenario Preset and show help info box
if selected_operation_preset != t["preset_none"]:
    preset_data = config.OPERATION_PRESETS[selected_operation_preset]
    preset_config = preset_data["params"]
    
    st.session_state.corridor_width = preset_config["corridor_width"]
    st.session_state.l_threshold = preset_config["l_threshold"]
    st.session_state.telemetry_freq = preset_config["telemetry_freq"]
    st.session_state.sail_index = preset_config["sail_level"]
    
    # Виведення підказки у синьому блоці під списком
    st.sidebar.info(preset_data["help"][lang_code])

st.sidebar.markdown("---")

# Manual Input Controls
st.sidebar.subheader(t["scenario_title"])
corridor_width_m = st.sidebar.slider(t["corridor_width"], 10.0, 50.0, st.session_state.corridor_width, 5.0, key='corridor_slider')
sail_level = st.sidebar.selectbox(t["sail_class"], [t["sail_low"], t["sail_high"]], index=st.session_state.sail_index, key='sail_selector')
l_threshold_ms = st.sidebar.number_input(t["latency_threshold"], 100, 2000, st.session_state.l_threshold, 50, key='l_threshold_input')

st.sidebar.subheader(t["uas_specs"])
telemetry_freq_hz = st.sidebar.slider(t["telemetry_freq"], 0.5, 10.0, st.session_state.telemetry_freq, 0.5, key='telemetry_freq_slider')
gnss_type = st.sidebar.selectbox(t["gnss_mode"], [t["gnss_rtk"], t["gnss_3d"]], index=0)

# Update session state with current control values
st.session_state.corridor_width = corridor_width_m
st.session_state.l_threshold = l_threshold_ms
st.session_state.telemetry_freq = telemetry_freq_hz
st.session_state.sail_index = 0 if t["sail_low"] in sail_level else 1

# Add Run Button
st.sidebar.markdown("---")
run_btn = st.sidebar.button(t["run_button"], type="primary", use_container_width=True)

if run_btn:
    st.session_state['has_run'] = True

# -----------------------------------------------------------------------------\
# DATA LOADING & WELCOME MESSAGE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer)
    df['latency_ms'] = df['timestamp_server_ms'] - df['timestamp_board_ms']
    return df

try:
    if uploaded_file is not None:
        df_telemetry = load_data(uploaded_file)
        st.sidebar.success(t["log_loaded"])
    else:
        df_telemetry = load_data('flight_telemetry_log.csv')
        st.sidebar.info(t["demo_log"])
except Exception as e:
    st.error(t["load_error"] + f": {e}")
    st.stop()

# -----------------------------------------------------------------------------\
# MAIN LOGIC: RUN ON BUTTON CLICK
# -----------------------------------------------------------------------------
if not st.session_state['has_run']:
    st.info(t['welcome_message'])
    st.stop()

# --- All calculations below this line are executed only after the button is pressed ---

# Weights according to SAIL level
if t["sail_low"] in sail_level:
    w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_LOW
else:  # SAIL IV
    w_A, w_C, w_L, w_I = config.WEIGHTS_SAIL_HIGH

# CORE C2 METRICS CALCULATION
total_packets = len(df_telemetry)
min_seq, max_seq = df_telemetry['seq_id'].min(), df_telemetry['seq_id'].max()
expected_packets = max_seq - min_seq + 1
dropped_packets = expected_packets - total_packets
packet_loss_rate = (dropped_packets / expected_packets) if expected_packets > 0 else 0.0

mean_latency = df_telemetry['latency_ms'].mean()
p95_latency = df_telemetry['latency_ms'].quantile(0.95)

f_L = max(0.0, min(1.0, (config.L_MAX - mean_latency) / (config.L_MAX - l_threshold_ms)))
availability = max(0.0, 1.0 - packet_loss_rate)

time_diffs_ms = df_telemetry['timestamp_server_ms'].diff().dropna()
outages = (time_diffs_ms > config.OUTAGE_THRESHOLD_MS).sum()
continuity = max(0.0, 1.0 - (outages / len(time_diffs_ms))) if len(time_diffs_ms) > 0 else 1.0

# Integrity (I) calculation based on GNSS mode
if gnss_type == t["gnss_rtk"]:
    integrity = (df_telemetry['gnss_fix_type'] == 4).mean()
    integrity_target = t["integrity_target_rtk"]
else:  # GNSS 3D Fix
    integrity = (df_telemetry['gnss_fix_type'] >= 3).mean()
    integrity_target = t["integrity_target_3d"]

R_C2 = w_A * availability + w_C * continuity + w_L * f_L + w_I * integrity
R_C2_pct = R_C2 * 100.0

# -----------------------------------------------------------------------------\
# MAIN DASHBOARD LAYOUT
# -----------------------------------------------------------------------------
col_status, col_verdict = st.columns([1, 2])
with col_status:
    st.markdown(f"### {t['integral_indicator']}")
    st.metric(label=t["readiness_level"], value=f"{R_C2_pct:.1f}%", delta=f"{R_C2_pct - config.R_C2_THRESHOLD_PCT:.1f}% {t['threshold_text']}")
with col_verdict:
    st.markdown(f"### {t['verdict_header']}")
    if R_C2_pct >= config.R_C2_THRESHOLD_PCT:
        st.markdown(f'<div class="status-approved">{t["approved"].format(corridor_width_m)}</div>', unsafe_allow_html=True)
        st.write(t["approved_desc"])
    else:
        st.markdown(f'<div class="status-rejected">{t["rejected"]}</div>', unsafe_allow_html=True)
        st.write(t["rejected_desc"])

st.markdown("---")

# Key Indicators KPI Row
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric(t["availability"], f"{availability*100:.2f}%", t["availability_target"])
kpi2.metric(t["continuity"], f"{continuity*100:.2f}%", t["continuity_target"])
kpi3.metric(t["integrity"], f"{integrity*100:.2f}%", integrity_target)
kpi4.metric(t["latency"], f"{mean_latency:.1f} ms", f"{t['p95']} {p95_latency:.1f} ms")
kpi5.metric(t["packet_loss"], f"{packet_loss_rate*100:.2f}%", f"{t['dropped']} {dropped_packets} {t['packets']}")

st.markdown("---")

# -----------------------------------------------------------------------------\
# CHARTS & DIAGNOSTICS SECTION
# -----------------------------------------------------------------------------
tab_summary, tab_sensitivity, tab_telemetry, tab_monte_carlo = st.tabs([
    t["tab_analysis"], t["tab_sensitivity"], t["tab_telemetry"], t["tab_monte_carlo"]
])

with tab_summary:
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader(t["latency_distribution"])
        fig_lat = px.histogram(df_telemetry, x="latency_ms", nbins=40, color_discrete_sequence=['#0F2C59'],
                               labels={'latency_ms': t["latency_xlabel"], 'count': t["latency_ylabel"]},
                               title=t["latency_histogram"])
        fig_lat.add_vline(x=l_threshold_ms, line_dash="dash", line_color="red", annotation_text=t["threshold_annotation"].format(l_threshold_ms))
        st.plotly_chart(fig_lat, use_container_width=True)

    with col_chart2:
        st.subheader(t["radar_title"])
        categories = t["radar_categories"]
        values = [availability * 100, continuity * 100, f_L * 100, integrity * 100]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', name=t["current_board"], line_color='#0F2C59'))
        fig_radar.add_trace(go.Scatterpolar(r=[80, 80, 80, 80, 80], theta=categories + [categories[0]], name=t["min_threshold"], line_color='red', line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    st.markdown("---")
    st.markdown(f"### {t['diagnostic_report']}")
    if mean_latency > l_threshold_ms:
        st.warning(t["bottleneck_latency"].format(mean_latency, l_threshold_ms) + "\n\n" + t["action_latency"])
    elif packet_loss_rate > 0.03:
        st.warning(t["bottleneck_loss"].format(packet_loss_rate*100) + "\n\n" + t["action_loss"])
    else:
        st.info(t["status_ok"])

with tab_sensitivity:
    st.subheader(t["bottleneck_localization"])
    delta = config.SENSITIVITY_DELTA
    f_L_perturbed = max(0.0, min(1.0, (config.L_MAX - mean_latency*(1 + delta)) / (config.L_MAX - l_threshold_ms)))
    R_C2_lat_change = (w_A*availability + w_C*continuity + w_L*f_L_perturbed + w_I*integrity) - R_C2
    avail_perturbed = max(0.0, 1.0 - packet_loss_rate*(1 + delta))
    R_C2_loss_change = (w_A*avail_perturbed + w_C*continuity + w_L*f_L + w_I*integrity) - R_C2
    cont_perturbed = continuity * (1 - delta)
    R_C2_cont_change = (w_A*availability + w_C*cont_perturbed + w_L*f_L + w_I*integrity) - R_C2
    
    sens_df = pd.DataFrame({
        'Parameter': t["sensitivity_params"],
        t["impact_r_c2"]: [R_C2_lat_change*100, R_C2_loss_change*100, R_C2_cont_change*100]
    })
    
    fig_sens = px.bar(sens_df, x='Parameter', y=t["impact_r_c2"], color=t["impact_r_c2"],
                      color_continuous_scale='Reds_r', title=t["sensitivity_title"])
    st.plotly_chart(fig_sens, use_container_width=True)

with tab_telemetry:
    st.subheader(t["flight_map"])
    st.map(df_telemetry[['lat', 'lon']].rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
    st.subheader(t["raw_log"])
    st.dataframe(df_telemetry.head(20))

with tab_monte_carlo:
    st.subheader(t["tab_monte_carlo"])
    n_simulations = 1000
    r_c2_results = []
    
    progress_bar = st.progress(0, text=f"Running {n_simulations} simulations...")
    
    for i in range(n_simulations):
        sim_latency = np.random.lognormal(mean=np.log(mean_latency), sigma=0.4)
        sim_packet_loss = np.random.beta(a=2, b=50) * (packet_loss_rate + 0.05)
        sim_continuity = np.random.beta(a=95, b=5)
        
        sim_f_L = max(0.0, min(1.0, (config.L_MAX - sim_latency) / (config.L_MAX - l_threshold_ms)))
        sim_availability = max(0.0, 1.0 - sim_packet_loss)
        sim_integrity = integrity # Assume integrity is stable from test data
        
        sim_R_C2 = w_A*sim_availability + w_C*sim_continuity + w_L*sim_f_L + w_I*sim_integrity
        r_c2_results.append(sim_R_C2 * 100.0)
        progress_bar.progress((i + 1) / n_simulations, text=f"Running {n_simulations} simulations... ({i+1}/{n_simulations})")

    r_c2_array = np.array(r_c2_results)
    prob_success = np.mean(r_c2_array >= 80.0) * 100.0
    
    fig_mc = px.histogram(x=r_c2_array, nbins=50, color_discrete_sequence=['#0F2C59'],
                        labels={'x': t["monte_carlo_xlabel"], 'count': t["monte_carlo_ylabel"]},
                        title=t["monte_carlo_title"])
    fig_mc.add_vline(x=80.0, line_dash="dash", line_color="red", annotation_text="80% Threshold")
    st.plotly_chart(fig_mc, use_container_width=True)
    
    st.metric(label="Simulation Result", value=t["probability_text"].format(prob_success),
              delta=f"Mean R_C2: {np.mean(r_c2_array):.1f}%")

# -----------------------------------------------------------------------------\
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(t["footer"])
