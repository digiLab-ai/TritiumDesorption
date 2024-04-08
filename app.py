import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import twinlab as tl

def get_emulators(api_key):
    if api_key:
        tl.set_api_key(api_key)
    return tl.list_emulators()

def load_data(emulator, e1, e2, e3, n1, n2):
    df_mean, df_std = emulator.predict(pd.DataFrame([[e1, e2, e3, n1, n2]], columns=['E1', 'E2', 'E3', 'n1', 'n2']))
    return df_mean, df_std

# API Key Input at the top of the sidebar
api_key = st.sidebar.text_input("API Key (if not stored locally):", "")

# Load emulators when the button is pressed and cache the list in the session state
if st.sidebar.button('Load Emulators') or 'emulators' not in st.session_state:
    st.session_state.emulators = get_emulators(api_key)

# Dropdown menu to select an emulator from the loaded list
if 'emulators' in st.session_state and st.session_state.emulators:
    # Find the index of 'tritium-desorption' in the list to set it as the default value
    default_index = st.session_state.emulators.index('tritium_desorption') if 'tritium_desorption' in st.session_state.emulators else 0
    
    selected_emulator = st.sidebar.selectbox(
        'Select an Emulator:', 
        st.session_state.emulators, 
        index=default_index  # Set the default index
    )
    
    # Load emulator button to trigger data loading and plotting
    if st.sidebar.button('Load Emulator'):
        st.session_state.selected_emulator_loaded = True
        st.session_state.emulator_obj = tl.Emulator(selected_emulator)  # Store the emulator object in session state for reuse
else:
    st.sidebar.write("Please load emulators first.")
    st.session_state.selected_emulator_loaded = False

# Display waiting message or the interactive components based on emulator load state
if not st.session_state.get('selected_emulator_loaded', False):
    st.write("Waiting for emulator to load")
else:
    # Interactive parameter sliders
    e1 = st.sidebar.slider('E$_1$', 0.7, 1.0, 0.8, format="%.4f")
    e2 = st.sidebar.slider('E$_2$', 0.9, 1.3, 1.0, format="%.4f")
    e3 = st.sidebar.slider('E$_3$', 1.1, 1.75, 1.2, format="%.4f")
    n1 = st.sidebar.slider('n$_1$', 0.0005, 0.005, value=0.001, step=0.0001, format="%.4f")
    n2 = st.sidebar.slider('n$_2$', 0.0001, 0.001, value=0.0005, step=0.00001, format="%.4f")

    # Load and plot data using the selected emulator and parameters
    if 'emulator_obj' in st.session_state:
        df_mean, df_std = load_data(st.session_state.emulator_obj, e1, e2, e3, n1, n2)
        fig, ax = plt.subplots()
        wavelength = np.linspace(300, 800, len(df_mean.values[0]))  # Adjust based on your data's actual range
        ax.plot(wavelength, df_mean.values[0], '-')
        ax.fill_between(wavelength, df_mean.values[0] - 2*df_std.values[0], df_mean.values[0] + 2*df_std.values[0], alpha=0.4)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Absorbance')
        st.write(fig)
