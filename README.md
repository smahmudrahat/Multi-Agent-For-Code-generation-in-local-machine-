# Code Query Agent

## Project Description

This repository contains a Python-based agent designed to query and process code documentation and files using various tools and models. The agent leverages the capabilities of LlamaParse, Ollama, and other modules to provide an interactive experience for querying and generating code documentation.

## Features

- **Document Parsing:** Uses LlamaParse to parse documents and extract relevant information.
- **Query Engine:** Utilizes VectorStoreIndex and QueryEngineTool to handle queries.
- **Multiple Models:** Integrates multiple language models including "mistral" and "codellama".
- **Code Generation:** Generates code snippets based on prompts and saves them to files.
- **Retry Mechanism:** Implements a retry mechanism to handle query failures gracefully.

## Models Used

- **Mistral AI Model:** Used for conversation and interactive prompts.
- **Local Ollama:** Used for various local processing tasks.
- **Codellama (Ollama):** Used specifically for code generation tasks.

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and Activate Virtual Environment:**
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Requirements:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory and add your environment variables:
     ```
     LLAMA_CLOUD_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Script:**
   ```sh
   python main.py
   ```

2. **Interactive Prompt:**
   - Enter prompts to query the agent. Type "q" to quit.
   - The agent will process the query and generate code snippets based on the input.

3. **Generated Code:**
   - The generated code will be displayed and saved to a file in the `output` directory.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
