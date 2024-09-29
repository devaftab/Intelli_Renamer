# Image, Pdf file Processing and Renaming Tool

This Python project automates the extraction of details from invoices and bills, renaming image files accordingly. It utilizes the Google Generative AI API (Gemini) to read text from images and extract relevant information like the date, company name, bill number, and amount. The renamed files are organized into designated folders.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Overview](#code-overview)
- [Contact](#contact)

## Features

- Extracts date, company name, bill number, and amount from invoice images (according to given prompt).
- Renames files based on extracted details.
- Moves files without valid details to a separate folder.
- Supports multiple image formats: JPEG, PNG, PDF, and JFIF.

## Requirements

- Python 3.x
- `google-generativeai` library
- `Pillow` library
- `google-api-core` library
- `os`, `re`, and `shutil` (standard libraries)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/devaftab/Intelli_Renamer.git
   cd Intelli_Renamer
   ```

2. Install the required packages:

   ```bash
   pip install google-generativeai Pillow google-api-core
   ```

3. Obtain your Gemini API key from Google and replace the placeholder `GEMINI_API_KEY` in the code.

## Usage

1. Place your files in the designated input folder:

   ```plaintext
   <folder_name>
   ```

2. Update the `folder_name` variable in the script to match your input folder.

3. Run the script:

   ```bash
   python intelli_renamer.py
   ```

4. The renamed files will be saved in the output folder:

   ```plaintext
   renamed_files/<folder_name>/
   ```

5. Files that could not be processed will be moved to:
   ```plaintext
   skipped_files/<folder_name>/
   ```

## Code Overview

### Main Components

- **intelli_renamer**: Main function that have below sub functions.
- **extract_bill_details**: Extracts the date, company name, bill number, and amount using regular expressions.
- **prep_image**: Prepares the image for processing.
- **rename_image_file**: Renames the image file based on extracted details.
- **move_file_to_folder**: Moves files to a specified folder.
- **extract_text_from_image**: Uses the Google Gemini model to extract text from images based on a given prompt.
- **process_images_in_folder**: Processes each image in the input folder, extracting details and renaming files accordingly.

### Prompt

Update the prompt used in the `extract_text_from_image` function to match the specific format of your invoices.

## Contact

If you have any questions or would like to collaborate, feel free to reach out to me:<br/><br/>
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:web.dev.aftab@gamil.com)<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/devaftab/) <br/>

[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/devaftab/)
