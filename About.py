#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import os
from util.streamlit_configs import Page_layout

st.set_page_config(
        page_title='Concrete Slab Design',
        page_icon='👨‍🔬',
        initial_sidebar_state="expanded", 
        layout="centered")


app = Page_layout(title='Concrete Slab Check',
                   default_session_key_values={},
                   hide_streamlit_footer=True,
                   custom_footer=None,
                   remove_padding_from_sides=True)
app.set_pagelayout()

with open(os.path.join('util', 'About.md'), 'r') as f:
        page_content = f.read()
st.write(page_content)

st.markdown("#### Change Notes:")
with st.expander("v1.0"):
    st.markdown("""
                * Added one-way slab design per CSA A23.3-19, Includes:
                    * shear check against concrete strength
                    * moment check against slab bot bar strength
                    * crack control parameter check per CSA A23.3,cl -10.6.1""")

st.components.v1.html("""
<h3 style="font-family:courier;">Created by</h3>
<p style="font-family:courier;">
Arun Kishore<br>
Structural EIT,<br>
Associated Engineering,<br>
<a href="mailto:rpakishore@gmail.com">Mail</a> • <a href="https://www.linkedin.com/in/rpakishore/">LinkedIn</a><br>
</p>
""")
