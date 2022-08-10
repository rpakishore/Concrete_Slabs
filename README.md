<!--- Heading --->
<div align="center">
  <img src="assets/logo.jpg" alt="logo" width="200" height="auto" /><br>
  <a style="font-size:50%;" href="https://www.freepik.com/vectors/steel-rod">Steel rod vector created by upklyak - www.freepik.com</a>
  
  <h1>Development length Calculator</h1>
  <p>
    Rebar development length calculator is a web application that calculates the necessary tension and compression development lengths required in accordance with CSA A23.3-19.
  </p>
<h4>
    <a href="assets\output.gif">View Demo</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Stru-Development-length/blob/main/README.md">Documentation</a>
  <span> · </span>
    <a href="mailto:rpakishore@gmail.com?subject=[BUG_Development-length]">Report Bug</a>
  <span> · </span>
    <a href="mailto:rpakishore@gmail.com?subject=[REQ_Development-length]">Request Feature</a>
  </h4>
</div>
<br />

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Screenshots](#11-screenshots)
  - [1.2. Features](#12-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Dependencies](#22-dependencies)
- [3. Usage](#3-usage)
- [4. Other Functions](#4-other-functions)
  - [4.1. update_requirements.py](#41-update_requirementspy)
- [5. Roadmap](#5-roadmap)
- [6. FAQ](#6-faq)
- [7. License](#7-license)
- [8. Contact](#8-contact)
- [9. Acknowledgements](#9-acknowledgements)

<!-- About the Project -->
## 1. About the Project
<!-- Screenshots -->
### 1.1. Screenshots

<div align="center"> 
  <img src="assets\output.gif" alt="screenshot" />
</div>

<!-- Features -->
### 1.2. Features

- Hooked tension development length
- Compression development length
- Tension development length


<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites
Python 3.7 or above

### 2.2. Dependencies
Create the virutual environment and install dependencies

```bash
python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt
```

<!-- Usage -->
## 3. Usage

Use this space to tell a little more about your project and how it can be used. Show additional screenshots, code samples, demos or link to other resources.


```powershell
python -m streamlit run About.py
```

Alternatively, You can checkout the script hosted on streamlit.io [here](https://rpakishore-stru-development-length-about-vpt3t6.streamlitapp.com/).
## 4. Other Functions
### 4.1. update_requirements.py
```bash
python update_requirements.py
```
! Be sure to run this command outside of the virtual environment

The way this script works is as follows:
- deletes the existing virtual environment
- Opens all `.py` files and checks for pip requirements
- If found, compiles the pip commands together
- Creates a new virtual env in the same directory and runs all the compiled pip commands

Inorder to ensure that all the `pip` commands are found. ensure that every time a non standard library is imported, add a line with the following in code
> #pip import XXXX


<!-- Roadmap -->
## 5. Roadmap

* [x] Hooked development length
* [x] Tension development length
* [x] Compression development length

<!-- FAQ -->
## 6. FAQ
- Can I save this to PDF
  + Yes! Simply hide the sidebar and use `Ctrl + P` to print the document to PDF.
<!-- License -->
## 7. License
Distributed under the no License. See LICENSE.txt for more information.

<!-- Contact -->
## 8. Contact

Arun Kishore - [@rpakishore](mailto:rpakishore@gmail.com)

Project Link: [https://github.com/rpakishore/Stru-Development-length](https://github.com/rpakishore/Stru-Development-length)


<!-- Acknowledgments -->
## 9. Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)