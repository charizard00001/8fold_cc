# AI Powered Resume Screening

**Team**: Capsule Corporation

## Introduction

The goal of this project is to develop a comprehensive HR candidate screening system that evaluates candidate profiles based on factors such as fraud detection, network strength, experience, and skill synergy. By utilizing advanced natural language processing (NLP) techniques and graph-based network analysis, this system provides a holistic evaluation of candidates, identifies potential risks, and supports data-driven HR decision-making.

**The system is divided into three main components:**

- **Fraud Detection System (Risk Score Calculation)**
- **Network Connection Analysis (Network Connection Score)**
- **HR Decision Support Dashboard**

The final output is an HR dashboard that provides a side-by-side comparison of candidates, highlights red flags, ranks candidates, and visually represents the network strength of each individual.

## Methodology and Models

### 1. Using RAG LLM with Google Gemini for Our Project

In this project, we implemented a Retrieval-Augmented Generation (RAG) approach using Google Gemini to extract structured data from unstructured resumes. RAG combines information retrieval with generative AI, allowing us to process domain-specific data effectively.

#### Approach Overview:

- **Retrieval Layer**: We used `pdfplumber` to extract resume text from PDFs, serving as input for the generative model.

  ```python
  import pdfplumber

  def extract_text_from_pdf(pdf_path):
      text = ""
      with pdfplumber.open(pdf_path) as pdf:
          for page in pdf.pages:
              text += page.extract_text()
      return text
