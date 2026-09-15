# -----------------------------------------------------------------------------
# PRESET CONFIGURATIONS
# -----------------------------------------------------------------------------
NETWORK_PRESETS = { ... }  # ваш код пресетів мережі

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

# Аліас для зворотної сумісності (якщо десь у коді залишилася стара назва)
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