import streamlit as st
from handcalcs.decorator import handcalc
from math import sqrt
import pandas as pd
from datetime import datetime
import json
import forallpeople
forallpeople.environment('structural', top_level=True)

input = {
    'span_type':'Simply supported',
    'exposure': 'Exterior',
    'fc': 25,
    'fy': 400,
    't': 150,
    'clear': 50,
    'span': 3000,
    'Mu':80,
    'Vu':50,
    'transverse': '10M',
    'longitudinal': '15M',
    'long_spacing': 200,
    'trans_spacing': 200,
}

bar_df = pd.DataFrame({
    'bars': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
    'size': [11.3, 16, 19.5, 25.2, 29.9, 35.7, 43.7, 56.4],
    'area': [100, 200, 300, 500, 700, 1000, 1500, 2500],
    'hook dia': [60, 90, 100, 150, 200, 250, 400, 550]
    })

# <!-----Classes-------->
class checks:
    def __init__(self):
        self.code = """<table align="center" border="1" cellpadding="1" cellspacing="1" summary="A summary of checks and Utilization %">
            <thead>
                <tr>
                    <th scope="col">Checks</th>
                    <th scope="col">Util</th>
                </tr>
            </thead>
            <tbody>
        """
        self.completed_code = None

    def add_check(self, title, util):

        if type(util) != str:
            if util > 1:
                color = "#ff3333"
            else:
                color = "#00FF00"
            util = round(util*100,1)
            self.code += (f"""<tr><td>{title}</td><td style="text-align: center;"><span style="background-color:{color};">{util}%</span></td></tr>""")

        else:
            if util.lower().strip().startswith('fail'):
                color = "#ff3333"
            else:
                color = "#00FF00"
            self.code += (f"""<tr><td>{title}</td><td style="text-align: center;"><span style="background-color:{color};">{util}</span></td></tr>""")
        self.completed_code = None

    def html(self):
        if not self.completed_code:
            self.completed_code = self.code + "</tbody></table>"
        return self.completed_code

class section:
    def __init__(self):
        self.code_block = []
    
    def add_markdown(self, text):
        self.code_block.append({"markdown":text})
    
    def add_latex(self, latex, prefix=None, suffix=None):
        self.code_block.append({
            "latex": latex,
            "prefix": prefix,
            "suffix": suffix})           

    def add_section_title(self, title, status=None, status_text=""):
        if status == None:
            self.code_block.append({"title_only": title})
        elif status.lower() == "ok":
            self.code_block.append({
                "title_success": title,
                'status_text': status_text})
        else:
            self.code_block.append({
                "title_error": title,
                'status_text': status_text})

    def write_calcs(self):
        for item in self.code_block:
            if "markdown" in item.keys():
                st.markdown(item['markdown'])
            elif "latex" in item.keys():
                if not item['prefix'] and not item['suffix']:
                    st.latex(item['latex'])
                elif item['prefix'] and not item['suffix']:
                    left, right = st.columns([1,2])
                    left.markdown(item['prefix'])
                    right.latex(item['latex'])
                elif not item['prefix'] and item['suffix']:
                    left, right = st.columns([2,1])
                    right.markdown(item['suffix'])
                    left.latex(item['latex'])
                else:
                    left, center ,right = st.columns([1,3,1])
                    left.markdown(item['prefix'])
                    center.latex(item['latex'])
                    right.markdown(item['suffix'])

            elif "title_only" in item.keys():
                st.markdown(item['title_only'])
            elif "title_success" in item.keys():
                left, right = st.columns([2,1])
                with left:
                    st.markdown(item['title_success'])
                with right:
                    st.success(item['status_text'])
            elif "title_error" in item.keys():
                left, right = st.columns([1,1])
                with left:
                    st.markdown(item['title_error'])
                with right:
                    st.error(item['status_text'])

calc_block = section()
check = checks()
check_list = {}
calc_variables = input.copy()
# <!-----Functions------>
def write_vals_to_session_state(vals):
    for item in vals.keys():
        calc_variables[item] = vals[item]
# <!-----Handcalc functions------>

# <!-----Other functions------>
def update_inputs():
    for key in input.keys():
        st.session_state[key] = input[key]

    checks = checks()
# <!-----Heading------>
st.header("RC One-way slab design")
# <!-----Inputs------>
st.subheader("Inputs")

for key in input.keys():
    if key not in st.session_state:
        st.session_state[key] = input[key]

left_column, right_column = st.columns(2)
with left_column:
    options = ('Simply supported', 'One end continuous', 'Both ends continuous')
    calc_variables['span_type'] = st.selectbox(label='Slab span type',
                                options=options,
                                key='span_type')
    if type(calc_variables['span_type']) == int:
        calc_variables['span_type'] = options[calc_variables['span_type']]

    options = ('Interior', 'Exterior')
    calc_variables['exposure'] = st.selectbox(label='Exposure type',
                                options=options,
                                key='exposure')
    if type(calc_variables['exposure']) == int:
        calc_variables['exposure'] = options[calc_variables['exposure']]

    st.markdown("-----")
    st.markdown("**Material Characteristics**")
    calc_variables['fc'] = st.slider(
        label="Concrete compressive Strength (f'c)", 
        min_value=5, 
        max_value=60, 
        step=5, 
        help="Clause 12.1.2 limits the max. concrete strength to 64MPa",
        key='fc')
    calc_variables['fc'] = calc_variables['fc']*MPa

    calc_variables['fy'] = st.slider(
        label="Steel tensile Strength (fy)", 
        min_value=300, 
        max_value=500, 
        step=50, 
        key='fy')
    calc_variables['fy'] = calc_variables['fy'] * MPa

with right_column:    
    #st.markdown("**Geometry**")
    calc_variables['t'] = st.number_input(
        label="Slab thickness (t | mm)",
        min_value=0,
        key='t')
    calc_variables['t'] = calc_variables['t']*mm

    calc_variables['clear'] = st.number_input(
        label="Clear cover (clr | mm)",
        min_value=10,
        key='clear')
    calc_variables['clear'] = calc_variables['clear']*mm

    calc_variables['span'] = st.number_input(
        label="Clear shorter span of slab (span | mm)",
        min_value=100,
        key='span')
    calc_variables['span'] = calc_variables['span']*mm

    st.markdown("**Moment and Shear**")
    calc_variables['Mu'] = st.number_input(
        label="Factored positive moment at section in slab (Mup | kNm/m)",
        min_value=0.00,
        key='Mu')
    calc_variables['Mu'] = calc_variables['Mu'] * kN*m/m

    calc_variables['Vu'] = st.number_input(
        label="Factored shear force at section in slab (Vu | kN/m)",
        key='Vu')
    calc_variables['Vu'] = calc_variables['Vu'] * kN/m

st.markdown("##### Bar Selection")
left, right = st.columns(2)
left.markdown("**Longitudinal Steel**")
right.markdown("**Transverse Steel**")
col1, col2, col3, col4 = st.columns(4)
options = tuple(bar_df['bars'])

calc_variables['longitudinal'] = col1.selectbox(label='bar size',
                            options=options,
                            key='longitudinal')
if type(calc_variables['longitudinal']) == int:
    calc_variables['longitudinal'] = options[calc_variables['longitudinal']]
d_longitudinal = bar_df[bar_df['bars']==calc_variables['longitudinal']]['size'].iloc[0] * mm
As_longitudinal = bar_df[bar_df['bars']==calc_variables['longitudinal']]['area'].iloc[0] * mm**2

calc_variables['long_spacing'] = col2.number_input(
    label="spacing (mm)",
    min_value=10,
    key='long_spacing')
calc_variables['long_spacing'] = calc_variables['long_spacing'] * mm

calc_variables['transverse'] = col3.selectbox(label='bar size',
                            options=options,
                            key='transverse')
if type(calc_variables['transverse']) == int:
    calc_variables['transverse'] = options[calc_variables['transverse']]
d_transverse = bar_df[bar_df['bars']==calc_variables['transverse']]['size'].iloc[0] * mm
As_transverse = bar_df[bar_df['bars']==calc_variables['transverse']]['area'].iloc[0] * mm**2

calc_variables['trans_spacing'] = col4.number_input(
    label="spacing (mm)",
    min_value=10,
    key='trans_spacing')
calc_variables['trans_spacing'] = calc_variables['trans_spacing'] * mm
# <!-----Calculations------>

## Span/Depth

if st.session_state.span/st.session_state.t <= 20:
    @handcalc(precision=1)
    def span_t_less(span,t):
        ratio = span/t
        return locals()
    latex, vals = span_t_less(calc_variables["span"],calc_variables["t"])
    latex = latex + '\leq\ 20\ (CSA\ A23.3,\ Cl.\ 9.8.2.1,\ Table 9.2)'
else:
    @handcalc(precision=1)
    def span_t_more(span,t):
        ratio = span/t
        return locals()
    latex, vals = span_t_more(calc_variables["span"],calc_variables["t"])
    latex = latex + '>\ 20\ (CSA\ A23.3,\ Cl.\ 9.8.2.1,\ Table 9.2)'
check_list["Span/Depth check"]= calc_variables["span"]/calc_variables["t"]/20
write_vals_to_session_state(vals)

### Add to checklist table
check.add_check("Span/Depth check", check_list["Span/Depth check"])

### Write to calc block
calc_block.add_section_title(
    title="#### Span/Depth check",
    status="FAIL" if check_list["Span/Depth check"] > 1 else "OK",
    status_text= "Span/Depth exceeds max allowed" if check_list["Span/Depth check"] > 1 else "OK"
)
calc_block.add_latex(latex)

calc_block.add_section_title("#### Check Slab in bending - SAGGING")
## Check slab in bending
@handcalc(precision=2)
def formula(fc):
    alpha_1 = max(0.67, 0.85 - 0.0015*fc/MPa)
    return locals()
latex, vals = formula(calc_variables['fc'])
calc_variables['phi_s'] = 0.85
write_vals_to_session_state(vals)
calc_block.add_latex(latex, suffix="Cl. 10.1.7.c")

@handcalc(precision=2)
def formula(fc):
    beta_1 = max(0.67, 0.97 - 0.0025*fc/MPa)
    return locals()
latex, vals = formula(calc_variables['fc'])
write_vals_to_session_state(vals)
calc_block.add_latex(latex, suffix="Cl. 10.1.7.c")

## Steel Calculation
@handcalc(precision=1)
def formula(t, LongAs_prov, Longs_prov, TransAs_prov, Transs_prov):
    As_min = 0.002 * t * 1000*mm
    As_max = 0.004 * t * 1000*mm
    As_prov_long = LongAs_prov 
    As_prov_trans = TransAs_prov 
    s_max = min(5*t, 500*mm)
    s_prov_long = Longs_prov
    s_prov_rans = Transs_prov 
    return locals()

latex, vals = formula(
    t=calc_variables['t'], 
    TransAs_prov=As_transverse*1000/calc_variables['trans_spacing']*mm, 
    Transs_prov=calc_variables['trans_spacing'], 
    LongAs_prov=As_longitudinal*1000/calc_variables['long_spacing']*mm, 
    Longs_prov=calc_variables['long_spacing'])
write_vals_to_session_state(vals)
if vals['Transs_prov'] > vals['s_max']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Transverse provided spacing exceeds max spacing"
    )
elif vals['TransAs_prov'] < vals['As_min']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Transverse provided reinforcing is less than code minimum"
    )

elif vals['As_max'] < vals['TransAs_prov']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Transverse provided reinforcing is more than code maximum"
    )
elif vals['Longs_prov'] > vals['s_max']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Longitudinal provided spacing exceeds max spacing"
    )
elif vals['LongAs_prov'] < vals['As_min']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Longitudinal provided reinforcing is less than code minimum"
    )

elif vals['As_max'] < vals['LongAs_prov']:
    check.add_check("Minimum Steel","Fail")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="not ok",
        status_text="Longitudinal provided reinforcing is more than code maximum"
    )
else:
    check.add_check("Minimum Steel","Pass")
    calc_block.add_section_title(
        title="#### Minimum steel calculation - SAGGING (CSA A23.3, cl - 7.8)",
        status="ok",
        status_text="Steel meets code min./max req"
    )
calc_block.add_latex(latex)

## Check for Moment
@handcalc(precision=1)
def formula(t, clr, d_b):
    d_act = t - clr - d_b / 2
    return locals()
latex1, vals = formula(calc_variables['t'], calc_variables['clear'], d_longitudinal)
write_vals_to_session_state(vals)


@handcalc(precision=2)
def formula(phi_s, As_prov, f_y, d_act, alpha_1, phi_c, f_prime_c):
    Mu_prov = phi_s*As_prov*f_y*(d_act - (phi_s* As_prov*f_y)/(alpha_1*phi_c*f_prime_c*m))
    return locals()

latex2, vals = formula(
    phi_s = 0.85, 
    As_prov=As_longitudinal*1000/calc_variables['long_spacing']*mm, 
    f_y=calc_variables['fy'], 
    d_act=calc_variables['d_act'], 
    alpha_1=calc_variables['alpha_1'], 
    phi_c=0.65, 
    f_prime_c=calc_variables['fc'])
write_vals_to_session_state(vals)
check.add_check("Moment Capacity",calc_variables['Mu']*m /vals['Mu_prov'])
if vals['Mu_prov'] >= calc_variables['Mu']*m:
    calc_block.add_section_title(
        title = "#### Check for moment per meter of slab",
        status="ok",
        status_text="OK"
    )
    
else:
    calc_block.add_section_title(
        title = "#### Check for moment per meter of slab",
        status="Fail",
        status_text="Section capacity is lower than required"
    )

calc_block.add_latex(latex1,prefix="Actual depth of tension steel provided")
calc_block.add_latex(latex2)

if vals['Mu_prov'] >= calc_variables['Mu']*m:
    calc_block.add_latex("M_{u.prov} ("+ str(round(vals['Mu_prov']/kN,1))+"kNm) \geq M_{up} ("+ str(round(calc_variables['Mu']/kN,1)) + "kNm)")
else:
    calc_block.add_latex("M_{u.prov} ("+ str(round(vals['Mu_prov']/kN,1))+"kNm) < M_{up} ("+ str(round(calc_variables['Mu']/kN,1)) + "kNm)")

## Check for shear
@handcalc(precision=1)
def formula(d_act, t, phi_c, f_prime_c):
    d_v = max(d_act, 0.72*t)
    beta = 230*mm/(1000*mm+d_v)
    V_c = beta*phi_c*sqrt(f_prime_c*1*MPa)*MPa*d_v*1*m
    return locals()
latex, vals = formula(
    t=calc_variables['t'], 
    d_act=calc_variables['d_act'],
    phi_c = calc_variables['phi_c'],
    f_prime_c= calc_variables['fc'])
write_vals_to_session_state(vals)

check.add_check("Shear Capacity",calc_variables['Vu']*m /vals['V_c'])
if vals['V_c'] >= calc_variables['Vu']*m:
    calc_block.add_section_title(
        title = "#### Check for One-way Shear per meter of slab",
        status="OK",
        status_text="Section has adequate capacity"
    )
else:
    calc_block.add_section_title(
        title = "#### Check for One-way Shear per meter of slab",
        status="Fail",
        status_text="Section capacity is lower than required"
    )
calc_block.add_latex(latex)

if vals['V_c'] >= calc_variables['Vu']*m:
    calc_block.add_latex("V_{c} ("+ str(round(vals['V_c']/kN,1))+"kN) \geq V_{u} ("+ str(round(calc_variables['Vu']*m/kN,1)) + "kN)")
else:
    calc_block.add_latex("V_{c} ("+ str(round(vals['V_c']/kN,1))+"kN) < V_{u} ("+ str(round(calc_variables['Vu']*m/kN,1)) + "kN)")

## Crack control parameter
@handcalc(precision=1)
def formula(clr, d_b, s, f_y, z_allow):
    d_c = min(clr, 50*mm) + d_b / 2
    A = 2*d_c*s
    z_act = 0.6*f_y*(d_c*A)**(1/3)
    z_allow =z_allow
    return locals()

latex, vals = formula(
    clr=calc_variables['clear'], 
    d_b=d_longitudinal, 
    s=calc_variables['long_spacing'], 
    f_y= calc_variables['fy'],
    z_allow=25000*N/mm if calc_variables['exposure']== "Exterior" else 30000*N/mm)
write_vals_to_session_state(vals)

calc_block.add_section_title(
    title="#### Check for crack control parameter (CSA A23.3,cl -10.6.1)",
    status="ok" if vals['z_act'] <= vals['z_allow'] else "fail",
    status_text="OK" if vals['z_act'] <= vals['z_allow'] else "Z value exceeded",
)
calc_block.add_latex(latex)
check.add_check("Crack control parameter",vals['z_act'] / vals['z_allow'])

# <!-----Results tab------>
st.subheader("Results")
left, right = st.columns(2)      
right.write(check.html(), unsafe_allow_html=True)
result = f"""<table align="center" border="1" cellpadding="1" cellspacing="1"><tbody>
            <tr><td scope="col">Slab thickness</td><td scope="col">{calc_variables['t']} mm</td></tr>
            <tr><td scope="col">Slab span</td><td scope="col">{calc_variables['span']} mm</td></tr>
            <tr><td scope="col">Longitudinal Reinforcing</td><td scope="col">{calc_variables['longitudinal']} @ {int(calc_variables['long_spacing'])}mm</td></tr>
            <tr><td scope="col">Transverse Reinforcing</td><td scope="col">{calc_variables['transverse']} @ {int(calc_variables['trans_spacing'])}mm</td></tr>
            </tbody></table>"""
left.write(result, unsafe_allow_html=True)
# <!-----Calculations tab------>
st.subheader("Calculation")
calc_block.write_calcs()


# ---- HIDE STREAMLIT STYLE ----

hide_st_style = """
                <style>
                #MainMenu{visibility: hidden;}
                footer{visibility: hidden;}
                header{visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html = True)  
