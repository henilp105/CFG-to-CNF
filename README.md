# CFG to CNF Converter

This Python script converts Context-Free Grammars (CFGs) into Chomsky Normal Form (CNF) using Streamlit, a web application framework.

## Table of Contents
- [Overview](#overview)
- [Instructions](#instructions)
- [Functionality](#functionality)
- [Vulnerabilities](#vulnerabilities)
- [Contributing](#contributing)
- [License](#license)

## Overview
The provided script allows users to input production rules for a CFG via a web interface. Upon conversion, the script applies various transformations to bring the CFG into CNF and displays the resulting CNF grammar.

## Instructions
### Running Locally
1. **Install Dependencies**: Ensure you have Python installed on your system. Install the required dependencies using:
pip install streamlit

2. **Clone the Repository**: Clone this repository to your local machine:

3. **Navigate to Directory**: Navigate to the directory where the script is located:
streamlit run cfg_to_cnf_converter.py


5. **Access the Web Interface**: Open your web browser and go to the URL provided in the terminal (usually `http://localhost:8501`). You should see the CFG to CNF converter interface.

## Functionality
- Users can input production rules for a CFG using text inputs in the web interface.
- Upon clicking the "Convert" button, the script converts the provided CFG into CNF.
- The resulting CNF grammar is displayed on the web interface.

## Vulnerabilities
1. **Input Validation**: The script lacks robust input validation on user-provided production rules, which could lead to unexpected behavior or errors if the input is malformed or contains invalid characters.
2. **Security**: As with any web application, there may be security vulnerabilities related to user input, such as XSS or CSRF, that need to be addressed depending on deployment and usage scenarios.
3. **Error Handling**: The script lacks comprehensive error handling, which could make it difficult to diagnose and fix issues that arise during execution.
4. **Efficiency**: The efficiency of the conversion algorithms could be improved, especially for large CFGs, as some operations may have high time complexity.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to contribute to the project.

## License
This project is licensed under the [MIT License](LICENSE).