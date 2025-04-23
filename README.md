# Leveraging Large Language Models for Automated Completion of Public Service Forms
## Project Overview
This project is created as part of a graduation thesis at the University of Science, Ho Chi Minh City (HCMUS) focusing on Natural Language Processing (NLP) research and its application in automating the completion of public service forms. The goal is to leverage large language models (LLMs) to automatically fill out information in forms using a pre-defined set of tagnames, improving the efficiency of form completion and reducing human error.


## Project Goal
The primary objective of this project is to automate the completion of public service forms using large language models like Gemini or GPT-4o-mini. Post-processing steps are applied to refine and adjust the generated data according to the specific needs of the form.

## How It Works
The system processes form templates and generates tag names for each field that needs to be filled. The LLM (either Gemini or GPT-4o-mini) is employed to identify and fill out the placeholders in the form based on the context and available data. A post-processing algorithm ensures that the tagnames are correctly adjusted to match the expected format and context.

## Usage
Prerequisites
Ensure you have the required dependencies installed by running:
```
pip install -r requirements.txt
```
## Running the Script
To run the project, use the following commands:
**1. To generate tag names for a single file:**
```
python main.py 1 --file your_file_dir
```
**2. To generate tag names for all text files in a folder:**
```
python main.py 2 --folder your_folder_dir
```
All the results will be saved in a Results/ subdirectory.

## Post-Processing
After the LLM generates the initial tag names, a post-processing algorithm is applied to ensure that the generated data matches the required format and context. This includes adjusting tagnames based on rules defined for various form fields.

# Participants
## Students:
- 21120291: Nguyễn Đức Nam
- 21120463: Lê Hữu Hưng
## Instructors:
- TS. Nguyễn Tiến Huy
- TS. Lê Thanh Tùng



