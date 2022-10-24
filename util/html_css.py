add_footer_begin = """
<style>
    a:link , a:visited {
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
add_footer_end = """
        </p></div>
"""

remove_padding_from_sides="""
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
</style>
"""

hide_streamlit_footer="""
<style>
    #MainMenu{visibility: hidden;}
    footer{visibility: hidden;}
    header{visibility: hidden;}
</style>
"""

checks_table_html_header="""
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