from typing import Any, Callable, Dict, Union, cast
import streamlit as st

#-------------
# Page Config
#-------------
st.set_page_config(page_title="Advanced Unit Converter", layout="centered", page_icon="⚡")

#------------
# Custom CSS
#------------
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0e1117;
}

.st-emotion-cache-1v0mbdj {
    display: block;
    margin: 0 auto;
}

header {
    padding: 2rem 0 !important;
    border-bottom: 1px solid #0e1117 !important;
}

.st-emotion-cache-1avcm0n {
    background: #ffffff !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border-right: 1px solid #e9ecef !important;
}

.stSelectbox > div > div {
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

.stSelectbox:focus-within > div > div {
    border-color: #4a90e2 !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

.stNumberInput input {
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

.stNumberInput:focus-within input {
    border-color: #4a90e2 !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}

.stButton button {
    width: 100%;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    background: #4a90e2 !important;
    color: white !important;
    transition: transform 0.2s ease, background 0.2s ease !important;
    border: none !important;
}

.stButton button:hover {
    background: #357abd !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(74, 144, 226, 0.2) !important;
}

.stButton button:active {
    transform: translateY(0);
}

.result {
    font-size: 1.5rem;
    font-weight: 500;
    color: #2e7d32;
    text-align: center;
    padding: 1.5rem;
    background: #edf7ed;
    border-radius: 8px;
    margin: 2rem 0;
    animation: fadeIn 0.3s ease;
}

.error {
    font-size: 1.5rem;
    font-weight: 500;
    color: #d32f2f;
    text-align: center;
    padding: 1.5rem;
    background: #fce8e6;
    border-radius: 8px;
    margin: 2rem 0;
    animation: shake 0.4s ease;
}

footer {
    text-align: center;
    color: #6c757d;
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid #e9ecef;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-8px); }
    50% { transform: translateX(8px); }
    75% { transform: translateX(-4px); }
    100% { transform: translateX(0); }
}

.st-emotion-cache-10trblm {
    text-align: center !important;
    width: 100% !important;
    margin: 1rem 0 2rem 0 !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>⚡ Advanced Unit Converter</h1>", unsafe_allow_html=True)

#----------------------------------------
# Temperature Conversion at Module Level
#----------------------------------------
def celsius_to_base(x: float) -> float:
    return x

def celsius_from_base(x: float) -> float:
    return x

def fahrenheit_to_base(x: float) -> float:
    return (x - 32) * 5 / 9

def fahrenheit_from_base(x: float) -> float:
    return (x * 9 / 5) + 32

def kelvin_to_base(x: float) -> float:
    return x - 273.15

def kelvin_from_base(x: float) -> float:
    return x + 273.15

#------------------------------
# Types for Conversion Factors
#------------------------------
ConversionUnit = Union[float, Dict[str, Callable[[float], float]]]
ConversionCategory = Dict[str, ConversionUnit]
ConversionFactors = Dict[str, ConversionCategory]

conversion_factors: ConversionFactors = {
    "Plane Angle": {
        "Degree": 1.0,
        "Arcsecond": 1 / 3600,
        "Gradian": 0.9,
        "Milliradian": 0.0572958,
        "Minute of arc": 1 / 60,
        "Radian": 57.2958
    },
    "Length": {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Micrometer": 1e-6,
        "Nanometer": 1e-9,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254,
        "Nautical Mile": 1852.0
    },
    "Mass": {
        "Tonne": 1000.0,
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 1e-6,
        "Microgram": 1e-9,
        "Pound": 0.453592,
        "Ounce": 0.0283495,
        "Stone": 6.35029,
        "Ton (metric)": 1000.0,
        "Imperial ton": 1016.04691
    },
    "Temperature": {
        "Celsius": {"to_base": celsius_to_base, "from_base": celsius_from_base},
        "Fahrenheit": {"to_base": fahrenheit_to_base, "from_base": fahrenheit_from_base},
        "Kelvin": {"to_base": kelvin_to_base, "from_base": kelvin_from_base}
    },
    "Speed": {
        "Meters per second": 1.0,
        "Kilometers per hour": 0.277778,
        "Miles per hour": 0.44704,
        "Knots": 0.514444,
        "Feet per second": 0.3048
    },
    "Time": {
        "Nanosecond": 1e-9,
        "Microsecond": 1e-6,
        "Millisecond": 0.001,
        "Second": 1.0,
        "Minute": 60.0,
        "Hour": 3600.0,
        "Day": 86400.0,
        "Week": 604800.0,
        "Month": 2629746.0,
        "Year": 31556952.0,
        "Decade": 315569520.0,
        "Century": 3155695200.0
    },
    "Volume": {
        "US liquid gallon": 3.78541,
        "US liquid quart": 0.946353,
        "US liquid pint": 0.473176,
        "US fluid ounce": 0.0295735,
        "US tablespoon": 0.0147868,
        "US teaspoon": 0.00492892,
        "Imperial gallon": 4.54609,
        "Imperial quart": 1.13652,
        "Imperial pint": 0.568261,
        "Imperial cup": 0.284131,
        "Imperial fluid ounce": 0.0284131,
        "Imperial tablespoon": 0.0177582,
        "Imperial teaspoon": 0.00591939,
        "Cubic foot": 28.3168,
        "Cubic inch": 0.0163871,
        "Liter": 1.0,
        "Milliliter": 0.001,
        "Cubic meter": 1000.0,
        "Cubic centimeter": 0.001
    },
    "Pressure": {
        "Pascal": 1.0,
        "Kilopascal": 1000.0,
        "Bar": 100000.0,
        "Atmosphere": 101325.0,
        "PSI": 6894.76,
        "Torr": 133.322
    },
    "Energy": {
        "Joule": 1.0,
        "Kilojoule": 1000.0,
        "Calorie": 4.184,
        "Kilocalorie": 4184.0,
        "Watt-hour": 3600.0,
        "Kilowatt-hour": 3.6e6,
        "Electronvolt": 1.60218e-19,
        "British thermal unit": 1055.06
    },
    "Power": {
        "Watt": 1.0,
        "Kilowatt": 1000.0,
        "Megawatt": 1000000.0,
        "Horsepower": 745.7
    },
    "Fuel Economy": {
        "Miles per gallon (US)": 1.0,
        "Miles per gallon (UK)": 1.20095,
        "Kilometers per liter": 0.425144,
        "Liters per 100km": 235.215,
        "Kilometre per gallon (US)": 0.425144 * 3.78541,
        "Litres per 1000km": 23.5215
    },
    "Data Transfer Rate": {
        "Bits per second": 1.0,
        "Kilobits per second": 1e3,
        "Megabits per second": 1e6,
        "Gigabits per second": 1e9,
        "Terabits per second": 1e12,
        "Kilobytes per second": 8e3,
        "Megabytes per second": 8e6,
        "Gigabytes per second": 8e9,
        "Terabytes per second": 8e12
    },
    "Digital Storage": {
        "Bit": 1.0,
        "Byte": 8.0,
        "Kilobit": 1e3,
        "Megabit": 1e6,
        "Gigabit": 1e9,
        "Terabit": 1e12,
        "Petabit": 1e15,
        "Kilobyte": 8e3,
        "Megabyte": 8e6,
        "Gigabyte": 8e9,
        "Terabyte": 8e12,
        "Petabyte": 8e15
    },
    "Area": {
        "Square kilometre": 1e6,
        "Square metre": 1.0,
        "Square mile": 2.58999e6,
        "Square yard": 0.836127,
        "Square foot": 0.092903,
        "Square inch": 0.00064516,
        "Hectare": 10000,
        "Acre": 4046.85642
    },
    "Frequency": {
        "Hertz": 1.0,
        "Kilohertz": 1e3,
        "Megahertz": 1e6,
        "Gigahertz": 1e9
    }
}

#--------------------------
# Cache Conversion Factors
#--------------------------
@st.cache_data
def get_conversion_factors() -> ConversionFactors:
    return conversion_factors

def convert_units(value: float, from_unit: str, to_unit: str, category: str) -> float:
    factors = cast(ConversionFactors, get_conversion_factors())
    cat_factors = factors[category]
    
    if category == "Temperature":
        base_value = cat_factors[from_unit]["to_base"](value)  # type: ignore
        return cat_factors[to_unit]["from_base"](base_value)    # type: ignore
    else:
        return (value * cat_factors[from_unit]) / cat_factors[to_unit]  # type: ignore

#---------------------------------
# Sidebar for Conversion Category
#---------------------------------
conversion_type = st.sidebar.selectbox("Select Conversion Category", list(conversion_factors.keys()))

#---------------------------
# Main Conversion Interface
#---------------------------
units = list(conversion_factors[conversion_type].keys())
col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", units, key="from_unit")
with col2:
    to_unit = st.selectbox("To Unit", units, key="to_unit")

value_input = st.number_input("Enter Value", value=1.0, step=0.1, format="%.4f")

if st.button("Convert"):
    try:
        result = convert_units(value_input, from_unit, to_unit, conversion_type)
        st.markdown(f"<div class='result'>Result: {result:.4f}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"<div class='error'>Error: {e}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""<footer>Developed with ❤️ by Muhammad Salman Hussain</footer>""", unsafe_allow_html=True)