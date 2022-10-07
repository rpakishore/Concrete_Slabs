import streamlit as st
import pandas as pd
import json


    
def add_footer(html):
    """Adds passed html as page footer

    Args:
        html (str): Footer in HTML format
    """
    footer="""
    <style>
        a:link , a:visited\{
            color: blue;
            background-color: transparent;
            text-decoration: underline;
            }

        a:hover,  a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
            }

        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            color: black;
            text-align: center;
            }
    </style>
    <div class="footer">
        <hr>
            <p style="font-family:Source Sans Pro;">
    """
    st.markdown(footer + html + '</p></div>',unsafe_allow_html=True)
    
class Page_layout:
    def __init__(self, title, default_session_key_values={}):
        """Sets the Page title and default session state values

        Args:
            title (str): Page Title
            default_session_key_values (dict, optional): Dict of startup sessionstate keys and values, Defaults to {}
        """
        self.title = title
        self.calc_vars={}
        self.set_default_sessionstate_keys(default_session_key_values)
        self.setup_calc_outline()
    
    def update_calc_vars(self, variable_values):
        """Updates the `.calc_vars` attribute with the updated values passed to function

        Args:
            variable_values (dict): Dict of variable name and value
        """
        for key, value in variable_values.items():
            self.calc_vars[key] = value
            
    @staticmethod
    def set_default_sessionstate_keys(default_session_key_values):
        for key, value in default_session_key_values.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
    def setup_calc_outline(self):
        """Sets up the initial outline of the document with `Inputs`, `Results` and `Calculations` and relevant containers for same.
        """
        st.header(self.title)
        
        st.subheader('Inputs')
        self.inputs_container = st.container()
        st.markdown('----')
        
        st.subheader('Results')
        self.results_container = st.container()
        with self.results_container:
            self.summary_container, self.checks_container = st.columns(2)
            self.checks_html = ""
            self.summary_html = ""
        st.markdown('----')
            
        st.subheader('Calculations')
        self.calc_container = st.container()
        st.markdown('----')
        return

    @staticmethod
    def add_sub_container_w_status(head_container, title):
        """Creates a sub-container under the passed head container, Adds title and creates space for defining status of the following checks

        Args:
            head_container (streamlit container): container under which the sub-container is to be created
            title (str): Title in markdown format

        Returns:
            subcontainer, status_col: The created sub container and the column taking in status
        """
        sub_container = head_container.container()
        title_col, status_col = sub_container.columns(2)
        title_col.markdown(title)
        return sub_container, status_col

    @staticmethod
    def update_status(status_col, 
                      status="Pass", 
                      failure_note="Check Failed", 
                      success_note="Check Passed",
                      warn_note="Some Issue encontered"):
        """Updated the status column (created under `self.add_sub_container_w_status) with the passed value

        Args:
            status_col (streamlit column): streamlit column/container
            status (str, optional): Can be one of ["Pass","Fail","Warn"]. Defaults to "Pass".
            failure_note (str, optional): Note to show on "Fail". Defaults to "Check Failed".
            success_note (str, optional): Note to show on "Pass". Defaults to "Check Passed".
            warn_note (str, optional): Note to show on "Warn". Defaults to "Some Issue encontered".
        """
        assert status.strip().lower() in ['pass', 'fail', 'warn'], f"`{status}` is not a recognized option. Check Docstring"
        
        if status.lower().strip() == 'pass':
            status_col.success(success_note)
        elif status.lower().strip() == 'fail':
            status_col.error(failure_note)
        elif status.lower().strip() == 'warn':
            status_col.warning(warn_note)

    def add_to_checks_container(self, title,utilization):
        """Takes the Check title and the utilization (can be float, int or "Fail") and adds it to the `.checks_html` attribute, initializes html on first run

        Args:
            title (str): Check title
            utilization (float, int, "Fail"): Utilization to display on the table

        Returns:
            None: None
        """
        
        if self.checks_html == "":
            self.checks_html = """
            <style>
                .pass {
                    background-color: #e8f9ed;
                    color: #297d43;
                    }
                .fail {
                    background-color: #ffecec;
                    color: #96585c;
                    }
                .warn {
                    background-color: #fffce6;
                    color: #a4832a;
                    }
            </style>
            <table align="center" border="1" cellpadding="1" cellspacing="1" summary="A summary of checks and Utilization %">
            <thead>
                <tr>
                    <th scope="col">Checks</th>
                    <th scope="col">Util</th>
                </tr>
            </thead>
            <tbody>
            """
        if type(utilization) != str:
            if utilization > 1:
                tag_class = "fail"
            elif utilization < 1:
                tag_class = "pass"
            else:
                tag_class = "warn"
            utilization = round(utilization*100,1)
            self.checks_html += (f'<tr><td>{title}</td><td style="text-align: center;" class="{tag_class}">{utilization}%</td></tr>')

        else:
            tag_class = utilization.lower().strip()
            self.checks_html += (f'<tr><td>{title}</td><td style="text-align: center;" class="{tag_class}">{utilization}</td></tr>')
        
        return None

    def add_to_summary_container(self, title,value):
        """Takes the Summary Title and value and adds it to the `.summary_html` attribute, initializes html on first run

        Args:
            title (str): left column
            value (str): right column

        Returns:
            None: None
        """
        
        if self.summary_html == "":
            self.summary_html = """
            <table align="center" border="1" cellpadding="1" cellspacing="1"><tbody>
            """

        self.summary_html += (f'<tr><td scope="col">{title}</td><td scope="col">{value}</td></tr>')
        return None
    
    @staticmethod
    def hide_streamlit_footer():
        """
        Hides default streamlit footer and main menu (on top right)
        """
        hide_st_style = """
                        <style>
                        #MainMenu{visibility: hidden;}
                        footer{visibility: hidden;}
                        header{visibility: hidden;}
                        </style>
                        """

        st.markdown(hide_st_style,unsafe_allow_html = True) 
    
    def final_cleanup(self, hide_default_footer=False):
        #Display the checks table
        if self.checks_html != "":
            self.checks_html += "</tbody></table>"
            self.checks_container.write(self.checks_html, unsafe_allow_html=True)
        #Display summary_table
        if self.summary_html != "":
            self.summary_html += "</tbody></table>"
            self.summary_container.write(self.summary_html, unsafe_allow_html=True)
            
        #Remove Extra Padding from all sides of the page and top/bottom of sidebar
        st.markdown("""
                    <style>
                        .css-12oz5g7 {
                            padding-top: 0rem;
                            padding-bottom: 0rem;
                            padding-left: 0rem;
                            padding-right: 0rem;
                        }
                        .css-uc76bn{
                            padding-top: 2rem;
                            padding-bottom: 2rem;
                        }
                    </style>""", unsafe_allow_html=True)
        
        #Hide default streamlit footer and menu
        if hide_default_footer:
            self.hide_streamlit_footer()

    @staticmethod
    def write_formula_to_container(container, latex, prefix=None, suffix = None):
        """ Writes calculation latex along with any prefix(calc explanation) or suffix (calc reference) to the passed container
            If no prefix or suffix passed, latex is centered on page; 
            If both prefix else suffix passed, columns are split in the 1:3:1 ratio
            If only one of prefix or suffix passed, columns split into 1:4 (or 4:1) ratio

        Args:
            container (streamlit container): streamlit container to write the items to
            latex (str): Latex string/formula to write
            prefix (str, optional): string to write to prefix. Defaults to None.
            suffix (str, optional): string to write to suffix. Defaults to None.
        """
        if prefix != None and suffix != None:
            prefix_col, formula_col, suffix_col = container.columns([1,3,1])
        elif prefix != None or suffix != None:
            if prefix:
                prefix_col, formula_col = container.columns([1,4])
            else:
                formula_col, suffix_col = container.columns([4,1])
        else:
            formula_col = container
        
        if prefix:
            prefix_col.write(prefix)
        if suffix:
            suffix_col.write(suffix)
        
        formula_col.latex(latex)
    
    def run_handcalc_function(self, function, *vars):
        self.latex, self.value = function(*vars)
        self.update_calc_vars(self.value)

            
bar_df = pd.DataFrame({
    'bars': ['10M', '15M', '20M', '25M', '30M', '35M', '45M', '55M'],
    'size': [11.3, 16, 19.5, 25.2, 29.9, 35.7, 43.7, 56.4],
    'area': [100, 200, 300, 500, 700, 1000, 1500, 2500],
    'hook dia': [60, 90, 100, 150, 200, 250, 400, 550]
    })
