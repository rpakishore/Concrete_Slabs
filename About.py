#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from util.custom_streamlit_configs import hide_streamlit_footer, remove_padding_from_sides
st.set_page_config(
        page_title='Concrete Slab Design',
        page_icon='👨‍🔬',
        initial_sidebar_state="collapsed", 
        layout="auto")

hide_streamlit_footer()
remove_padding_from_sides()
st.write("# Concrete Slab Checks")
st.write("""
### Purpose
- These calculations check solid slabs supported by beams or walls.

### Disclaimer
Although this calculator has been formally checked for technical correctness, it is not a substitute for engineering judgement, and does not relieve users of their duty to conduct required checking and quality control procedures.

### Features
- [x] One-way slab design
    - [x] Checks shear requirements against concrete shear capacity
    - [x] Checks moment requirements against capacity
    - [x] Accounts for crack control parameter, per CSA A23.3,cl -10.6.1
    - [x] Simply supported condition
    - [ ] One end continuous condition
    - [ ] Both end continuous condition
    - [ ] Deflection checks
    - [ ] Export/Import calculation parameters
- [ ] Punching shear checks
    - [ ] Export/Import calculation parameters

### References
| S. No. | Reference | Year|
|--------|-----------|-----|
| 1. | CSA A23.3 | 2019 |

### Color reference
| Color             | Legend                                                                |
| ----------------- | ------------------------------------------------------------------ |
| ![ee0e00](https://via.placeholder.com/25/ee0e00?text=+) #Red | Error|
| ![ebbd14](https://via.placeholder.com/25/ebbd14?text=+) #Yellow | Warning message |
| ![CEEED8](https://via.placeholder.com/25/BDDA98?text=+) #Green | OK |
| ![002080](https://via.placeholder.com/25/002080?text=+) #Blue | Author's notes  |

### Assumptions and Limitations
* The effect of compression steel is ignored
* Contribution of steel is ignored in the shear checks. 


### Instructions for use
1. Review all information on the cover sheet
2. From the side bar, choose one of the pages available
3. Proceed to calculations by filing in all the values
4. Review entire workbook after completion
5. You may collapse the side bar and print the page using `Ctrl+P` to save the calculation as PDF.

### Version Notes and releases

|Version|v1.0|
|---|---|
|Version Notes| web-release|
|Version Date| 2022 - August - 13|


***
""")

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
