# FeedbackLens AI

### AI-Powered Feedback Sentiment Analysis & Insights

FeedbackLens AI is a Python-based web application that analyzes learner and training feedback using sentiment analysis. The application classifies feedback as **Positive, Neutral, or Negative**, visualizes sentiment patterns, identifies common descriptive terms, and generates insights and recommendations based on the results.

<img width="1199" height="517" alt="feedbacklens AI 1" src="https://github.com/user-attachments/assets/b607305b-a87a-4793-86fd-45c8d7f5c6c5" />


---

## Project Overview

Organizations and training programmes collect large amounts of feedback, but manually reviewing every response can be time-consuming.

FeedbackLens AI provides a simple way to turn feedback data into meaningful information.

Users can upload a CSV file containing feedback, and the application automatically:

- Analyzes the sentiment of each feedback response
- Classifies responses as Positive, Neutral, or Negative
- Calculates sentiment percentages
- Visualizes the sentiment distribution
- Identifies common descriptive terms
- Generates key insights
- Provides recommendations for improvement
- Displays the analyzed feedback
- Allows users to download the analysis as a CSV file

---

## Key Features

### CSV Feedback Upload

Users can upload their own feedback dataset in CSV format.

The CSV file should contain a column named:

```text
feedback
```

Example:

```csv
id,feedback
1,"The training was excellent and informative."
2,"The instructions were confusing."
3,"The course was okay."
```

---

### Sentiment Analysis

FeedbackLens uses **VADER Sentiment Analysis** to calculate sentiment scores for each feedback response.

Each response is classified into one of three categories:

| Sentiment | Description |
|---|---|
| Positive | Indicates favourable or positive feedback |
| Neutral | Indicates a mixed or moderate response |
| Negative | Indicates dissatisfaction or concerns |

The application also stores the sentiment compound score for each response.

---

### Sentiment Dashboard

The dashboard provides an overview of the dataset, including:

- Total feedback responses
- Positive feedback percentage
- Negative feedback percentage
- Neutral feedback percentage
- Sentiment distribution chart
  
<img width="1159" height="608" alt="feedbacklens AI 2" src="https://github.com/user-attachments/assets/0ae6e452-fd98-44e9-8431-aeb2b347ceeb" />


---

### Data Insights

FeedbackLens goes beyond simply displaying sentiment percentages.

The application identifies descriptive terms within feedback to help highlight areas that learners frequently mention.

For example:

**Positive terms**

- excellent
- helpful
- useful
- clear
- practical
- engaging

**Negative terms**

- confusing
- boring
- difficult
- frustrating
- long
- technical

---

### Recommendations

The application generates recommendations based on patterns found in the feedback.

For example:

> Increase learner engagement by adding more interactive activities and practical exercises.

> Review difficult or confusing topics and provide clearer instructions, explanations, and examples.

This helps turn the analysis into practical actions rather than simply presenting numbers.

<img width="1009" height="446" alt="feedbacklens AI 3" src="https://github.com/user-attachments/assets/d71c68f9-f1bd-4784-8024-224358d690f7" />

---

### Custom Themes

FeedbackLens includes selectable interface themes.

Available themes include:

- Standard Streamlit
- Pastel Bloom
- Lavender
- Soft Cream
- Pastel Blue

The **Standard Streamlit** theme is used by default, while the pastel themes allow users to personalize the dashboard appearance.

---

### Download Results

Users can download the analyzed feedback as a CSV file containing:

- Feedback
- Sentiment
- Sentiment Score

This allows the analysis to be reused or reviewed outside the application.

<img width="1177" height="525" alt="feedbacklens AI 4" src="https://github.com/user-attachments/assets/a3113e6d-01d2-4467-9707-eee7b4956894" />
---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application and dashboard |
| Pandas | Data loading and processing |
| VADER | Sentiment analysis |
| Matplotlib | Data visualization |
| CSV | Feedback data storage |
| GitHub | Version control and project documentation |

---

## Project Structure

```text
FeedbackLens/
│
├── app.py
├── analysis.py
├── sentiment.py
├── data_loader.py
├── visualizations.py
├── insights.py
├── report_analysis.py
├── theme.py
│
├── data/
│   └── feedback.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

### File Responsibilities

**`app.py`**

Controls the Streamlit interface and brings the different components of the application together.

**`data_loader.py`**

Loads feedback data from the default CSV file or an uploaded CSV file.

**`sentiment.py`**

Performs sentiment analysis using VADER.

**`analysis.py`**

Processes the feedback and calculates sentiment statistics.

**`visualizations.py`**

Creates the sentiment distribution chart.

**`insights.py`**

Generates basic insights from the sentiment summary.

**`report_analysis.py`**

Performs additional feedback analysis and generates insights, descriptive terms, and recommendations.

**`theme.py`**

Contains the colour definitions used by the application's customizable themes.

---

## How It Works

The application follows this basic workflow:

```text
CSV Feedback
     ↓
Data Loading
     ↓
Sentiment Analysis
     ↓
Positive / Neutral / Negative Classification
     ↓
Sentiment Statistics
     ↓
Data Visualization
     ↓
Descriptive Term Analysis
     ↓
Insights
     ↓
Recommendations
     ↓
Downloadable Results
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Palesa2323/FeedbackLens.git
```

### 2. Open the project folder

```bash
cd FeedbackLens
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
[streamlit run app.py](https://feedbacklensgit-cwtjn3mhachcsczytlhme2.streamlit.app/) 
```

The application will open in your web browser.

---

## Dataset Requirements

FeedbackLens expects a CSV file containing a column named:

```text
feedback
```

Additional columns can be included, but the `feedback` column is required for sentiment analysis.

Example:

```csv
id,feedback
1,"The training was excellent and very informative."
2,"The instructor explained everything clearly."
3,"The instructions were confusing."
```

---

## Technical Approach

FeedbackLens uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to calculate sentiment scores.

The compound sentiment score is used to classify each response:

```text
Score >= 0.05
    → Positive

Score <= -0.05
    → Negative

Between -0.05 and 0.05
    → Neutral
```

The sentiment results are then processed using Pandas to calculate the distribution of sentiment across the dataset.

Matplotlib is used to visualize the results, while Streamlit provides the interactive dashboard.

---

## What I Learned

This project helped me develop practical experience with:

- Sentiment analysis
- Text classification
- Data processing with Pandas
- Data visualization
- Building interactive Streamlit applications
- Working with CSV datasets
- Designing modular Python applications
- Generating insights from data
- AI-assisted analysis
- Creating recommendations from identified patterns
- Structuring and documenting an individual software project

The project also strengthened my understanding of how AI can be combined with traditional data analysis techniques to turn unstructured text into useful information.

---

## Limitations

FeedbackLens is designed as a learning and portfolio project.

Some limitations include:

- VADER is a lexicon-based sentiment analysis tool and may not understand every context or nuance.
- The descriptive term analysis currently uses a predefined vocabulary rather than advanced linguistic or POS-tagging techniques.
- Recommendations are based on predefined rules and identified feedback patterns.
- The application does not currently store historical datasets or user accounts.

These limitations provide opportunities for future improvements.

---

## Future Improvements

Possible future improvements include:

- Add more advanced NLP models
- Add keyword frequency visualizations
- Add sentiment trends across dates
- Add filtering by category or feedback type
- Add exportable PDF reports
- Add AI-generated summaries using an LLM
- Add more advanced recommendation logic
- Add historical dataset comparison
- Add database storage
- Improve text classification using machine learning
- Deploy the application online

---

## Project Outcome

FeedbackLens AI demonstrates how sentiment analysis and data visualization can be combined into a practical application for understanding learner feedback.

Rather than only showing whether feedback is positive or negative, the application attempts to identify **what users are saying, what areas may require attention, and what actions could improve the experience**.

---

## Author

**Palesa Gaetsewe**

Computer and Information Sciences Graduate  
Aspiring Software Developer  
AI Engineer Intern

---

## Project Status

**Status:** In Development

The core sentiment analysis, dashboard, insights, recommendations, CSV upload, downloadable results, and theme functionality have been implemented. Further improvements will be added as the project develops.
