import streamlit as st
import json
from datetime import datetime
from util import html_css as ht

class app_value:
    def __init__(self, units:dict, default_inputs:dict):
        self.units = units
        self.default_inputs = default_inputs

    def getval(self, var:str):
        if type(st.session_state[var]) == str:
            return st.session_state[var]
        unit = self.units.get(var)
        if not unit:
            unit = 1
        return st.session_state[var] * unit
    
    def __str__(self):
        return 'App Values - Default Inputs\n' + '\n'.join([f"{key}: {value}" for key, value in self.default_inputs.items()])
    
    def __repr__(self):
        return f"app_value(units={self.units}, default_inputs={self.default_inputs})"
    
    def run_handcalc_function(self, function, *vars):
        self.latex, self.value = function(*vars)
        self.update_sessionstate(self.value)
        return self.latex, self.value
    
    def update_sessionstate(self, values:dict):
        for key, value in values.items():
            if type(value) != str:
                unit = self.units.get(key)
                if not unit:
                    unit = 1
                st.session_state[key] / unit
            else:
                st.session_state[key] = value
                
class Page_layout:
    def __init__(self, 
                 title: str, 
                 default_session_key_values:dict ={}, 
                 hide_streamlit_footer:bool = False, 
                 custom_footer: str = None, 
                 remove_padding_from_sides: bool = False):
        """Sets the Page title and default session state values

        Args:
            title (str): Page Title
            default_session_key_values (dict, optional): Dict of startup sessionstate keys and values, Defaults to {}
        """
        self.hide_streamlit_footer = hide_streamlit_footer
        self.custom_footer = custom_footer
        self.remove_padding_from_sides = remove_padding_from_sides

        self.default_session_key_values = default_session_key_values
        self.title = title
    
    def set_pagelayout(self):
        st.header(self.title)
        self.set_default_sessionstate_keys(self.default_session_key_values)
        if self.hide_streamlit_footer:
            hide_streamlit_footer()
        if self.custom_footer:
            add_footer(self.custom_footer)
        if self.remove_padding_from_sides:
            remove_padding_from_sides()
    
    def __repr__(self):
        return f"Page_Layout(title={self.title}, default_session_key_values={self.default_session_key_values},hide_streamlit_footer = {self.hide_streamlit_footer}, custom_footer = {self.custom_footer}, remove_padding_from_sides={self.remove_padding_from_sides})"
           
    @staticmethod
    def set_default_sessionstate_keys(default_session_key_values):
        for key, value in default_session_key_values.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
    def setup_calc_outline(self, inputs:bool =True, results: bool=True, calculations:bool=True, checks_and_summary_within_results:bool =True):
        """Sets up the initial outline of the document with `Inputs`, `Results` and `Calculations` and relevant containers for same.

        Returns:
            list[st.container]: A list of `Inputs`, `Results`, `Results-Summary`, `Results-Checks` and `Calculations` container
        """
        return_containers = []

        if inputs:
            st.subheader('Inputs')
            self.inputs_container = st.container()
            return_containers.append(self.inputs_container)
            st.markdown('----')
        else:
            return_containers.append(None)
            self.inputs_container = None
        
        if results:
            st.subheader('Results')
            self.results_container = st.container()
            return_containers.append(self.results_container)
            if checks_and_summary_within_results:
                with self.results_container:
                    self.summary_container, self.checks_container = st.columns(2)
                return_containers.extend([self.summary_container, self.checks_container])
            else:
                return_containers.extend([None, None])
                self.summary_container, self.checks_container = None, None
            self.checks_html = ""
            self.summary_html = ""
            st.markdown('----')
        else:
            return_containers.extend([None, None, None])
            self.results_container, self.summary_container, self.checks_container = None, None, None
        
        if calculations: 
            st.subheader('Calculations')
            self.calc_container = st.container()
            st.markdown('----')
        else:
            return_containers.append(None)
            self.calc_container = None
        return return_containers

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
            self.checks_html = ht.checks_table_html_header
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
    
    def final_cleanup(self):
        #Display the checks table
        if self.checks_container and self.checks_html != "":
            self.checks_html += "</tbody></table>"
            self.checks_container.write(self.checks_html, unsafe_allow_html=True)
        #Display summary_table
        if self.summary_container and self.summary_html != "":
            self.summary_html += "</tbody></table>"
            self.summary_container.write(self.summary_html, unsafe_allow_html=True)

            

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
    


    @staticmethod
    def add_inputs_export_import_to_sidebar(title: str) -> None:
        st.sidebar.markdown("------")
        st.sidebar.download_button(
            label="Export Variables",
            help=f"Export the variables for {title}",
            file_name=f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            data=json.dumps(st.session_state, indent=4))
        st.sidebar.markdown("------")
        
        uploaded_file = st.sidebar.file_uploader(label="Upload inputs",
                                                type = "json",
                                                help="Import previously used inputs",
                                                accept_multiple_files=False)
        if uploaded_file is not None:
            #bytes_data = uploaded_file.getvalue()
            input = json.load(uploaded_file)
            
            def _update_inputs():
                for key, value in input.items():
                    st.session_state[key] = value
                return

            st.sidebar.button(label="Update",
                            on_click=_update_inputs,
                            key="update_button")
            
            
def hide_streamlit_footer():
    """
    Hides default streamlit footer and main menu (on top right)
    """
    st.markdown(ht.hide_streamlit_footer,unsafe_allow_html = True) 
    

def remove_padding_from_sides():
    #Remove Extra Padding from all sides of the page and top/bottom of sidebar
    st.markdown(ht.remove_padding_from_sides, unsafe_allow_html=True)
    

    

def add_footer(html):
    """Adds passed html as page footer

    Args:
        html (str): Footer in HTML format
    """

    st.markdown(ht.add_footer_begin + html + ht.add_footer_end ,unsafe_allow_html=True)

    
