# FeedbackLens AI 2.0

### AI-Powered Feedback Sentiment Analysis & Insights

FeedbackLens AI is a Python-based web application that helps organisations and training programmes understand learner feedback through sentiment analysis, data visualisation and AI-assisted insights.

The application classifies feedback as **Positive, Neutral or Negative**, identifies recurring descriptive terms, highlights patterns and generates recommendations to support informed decision-making.

It also includes **Feedy**, an AI-powered assistant that allows users to ask questions about their analysed feedback dataset.

**Live Demo:** https://feedbacklensgit-cwtjn3mhachcsczytlhme2.streamlit.app/

---

## Project Overview

Organisations and training programmes collect large amounts of feedback, but manually reviewing every response can be time-consuming.

FeedbackLens AI provides an interactive way to transform unstructured feedback into meaningful information.

Users can upload a feedback dataset, and the application automatically:

- Analyses individual feedback responses.
- Classifies responses as Positive, Neutral or Negative.
- Calculates sentiment scores and percentages.
- Displays sentiment patterns through visualisations.
- Identifies common descriptive terms.
- Generates key insights.
- Provides recommendations for improvement.
- Allows users to explore individual feedback responses.
- Offers an AI assistant for questions about the dataset.
- Supports downloadable analysis results.

---

## Key Features

### 1. Sentiment Analysis

FeedbackLens uses **VADER Sentiment Analysis** to calculate sentiment scores for individual feedback responses.

Each response is classified into one of three categories:

| Sentiment | Description |
|---|---|
| Positive | Indicates favourable or positive feedback |
| Neutral | Indicates a moderate or mixed response |
| Negative | Indicates dissatisfaction or concerns |

The application also retains the compound sentiment score for each response.

<img width="1517" height="747" alt="1" src="https://github.com/user-attachments/assets/fae49ad5-c117-45dc-bd38-bc67439ae297" />


---

### 2. Sentiment Dashboard

The dashboard provides an overview of the analysed feedback dataset, including:

- Total feedback responses.
- Positive feedback percentage.
- Negative feedback percentage.
- Neutral feedback percentage.
- Sentiment distribution visualisations.

<img width="1514" height="756" alt="Sentiment Dashboard" src="https://github.com/user-attachments/assets/cb5de24c-639a-4447-b83b-3620bbe9df99" />

---

### 3. Data Insights

FeedbackLens goes beyond displaying sentiment percentages by identifying descriptive terms that appear in feedback responses.

Examples include:

**Positive terms**
- Excellent
- Helpful
- Useful
- Clear
- Practical
- Engaging

**Negative terms**
- Confusing
- Boring
- Difficult
- Frustrating
- Long
- Technical

These terms help highlight recurring experiences and areas that may require attention.

<img width="1260" height="623" alt="Data Insights" src="https://github.com/user-attachments/assets/9727a191-52f5-4a9a-ba47-06c4b6d3e623" />

---

### 4. Recommendations

The application generates recommendations based on patterns identified in the feedback.

For example:

> Increase learner engagement by introducing more interactive activities and practical exercises.

> Review difficult or confusing topics and provide clearer instructions, explanations and examples.

The purpose is to turn the analysis into practical suggestions rather than simply presenting statistics.

<img width="1494" height="658" alt="Recommendations" src="https://github.com/user-attachments/assets/14e0d1aa-932e-468f-b1b2-7742d6c8d04f" />

---

### 5. Feedy AI Assistant

FeedbackLens includes **Feedy**, an AI-powered assistant that allows users to interact with their analysed feedback dataset.

Users can ask questions about their results and receive responses based on the available feedback and sentiment analysis.

Examples include:

- What should we improve first?
- What are people unhappy about?
- What are people praising?
- What patterns can you identify in the feedback?

Feedy uses Google's Gemini API to generate responses, making it easier to explore feedback without manually reviewing every response.

<img width="1515" height="540" alt="8" src="https://github.com/user-attachments/assets/550a94d1-683f-462e-9e3f-2bd8bc437015" />

---

### 6. Customisable Themes

FeedbackLens includes selectable interface themes designed to provide a more personalised dashboard experience.

Available themes include:

- **Standard Streamlit:** The default Streamlit appearance.
- **Pastel Bloom:** Soft blush and warm pastel colours.
- **Lavender:** A combination of lavender, lilac and cream.
- **Soft Cream:** Warm ivory, butter and neutral tones.
- **Pastel Blue:** Soft blue, cream and complementary pastel accents.

The custom themes coordinate the application's sidebar, header, cards, navigation and visual elements.

---

### 7. Feedback Explorer and Downloads

Users can explore analysed feedback and review individual responses alongside their sentiment classifications.

The application also supports downloading analysed feedback as a CSV file containing:

- Feedback
- Sentiment
- Sentiment Score

This allows users to review and reuse their results outside the application.

<img width="1549" height="693" alt="Download Results" src="https://github.com/user-attachments/assets/2a196f1a-a771-44e5-a502-9f20080bea72" />

---

## Application Pages

| Page | Purpose |
|---|---|
| Overview | Displays a summary of the analysed feedback |
| Sentiment Analysis | Uploads and analyses feedback data |
| Insights & Recommendations | Presents findings and suggested improvements |
| Feedback Explorer | Allows users to explore individual responses |
| Ask Feedy | Provides an AI assistant for questions about the dataset |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application and interactive dashboard |
| Pandas | Data loading and processing |
| VADER | Sentiment analysis |
| Matplotlib | Data visualisation |
| Google Gemini API | AI-assisted responses through Feedy |
| HTML & CSS | Custom interface styling |
| CSV | Feedback data input and result export |
| GitHub | Version control and project documentation |
| Streamlit Community Cloud | Application deployment |

---

## How It Works

The application follows this general workflow:

```text
Feedback Dataset
       ↓
Data Loading
       ↓
Sentiment Analysis
       ↓
Positive / Neutral / Negative Classification
       ↓
Sentiment Statistics
       ↓
Data Visualisation
       ↓
Descriptive Term Analysis
       ↓
Insights
       ↓
Recommendations
       ↓
Feedback Exploration & Downloads
       ↓
AI-Assisted Questions with Feedy
```

---

## Technical Approach

### Sentiment Classification

FeedbackLens uses VADER to calculate sentiment scores.

The compound score determines the sentiment category:

```text
Compound Score >= 0.05
    → Positive

Compound Score <= -0.05
    → Negative

Between -0.05 and 0.05
    → Neutral
```

The sentiment results are processed using Pandas to calculate the distribution of feedback across the three categories.

### AI-Assisted Responses

Feedy uses the Google Gemini API to generate responses to user questions about the analysed feedback.

The assistant receives relevant dataset context and sentiment information to help generate useful, feedback-related responses.

---

## What I Learned

This project provided practical experience with:

- Sentiment analysis and text classification.
- Data processing using Pandas.
- Data visualisation.
- Building interactive Streamlit applications.
- Working with CSV datasets.
- Integrating generative AI through an API.
- Prompt engineering and generating context-aware AI responses.
- Generating insights and recommendations from data.
- Designing modular Python applications.
- Managing API keys and application secrets.
- Deploying applications using Streamlit Community Cloud.
- Improving user experience through custom themes and interface styling.

The project strengthened my understanding of how traditional data analysis techniques can be combined with generative AI to turn unstructured text into useful information.

---

## Limitations

FeedbackLens AI is a learning and portfolio project. Some limitations include:

- VADER is a lexicon-based sentiment analysis tool and may not understand every context, sarcasm or linguistic nuance.
- Descriptive term analysis currently uses a predefined vocabulary rather than advanced linguistic or POS-tagging techniques.
- Recommendations are based on predefined rules and identified feedback patterns.
- Feedy's responses depend on the quality of the supplied dataset and the Gemini API.
- The application does not currently provide persistent user accounts or historical dataset storage.

These limitations provide opportunities for future improvements.

---

## Future Improvements

Potential future enhancements include:

- Introduce more advanced NLP models.
- Add keyword frequency visualisations.
- Add sentiment trends across dates.
- Support filtering by category or feedback type.
- Expand downloadable PDF reporting.
- Improve AI-generated summaries and recommendations.
- Introduce more advanced recommendation logic.
- Add historical dataset comparisons.
- Implement database storage.
- Improve classification using machine learning.
- Expand Feedy's ability to compare datasets.

---

## Project Outcome

FeedbackLens AI demonstrates how sentiment analysis, data visualisation and generative AI can be combined into a practical application for understanding learner and training feedback.

Rather than simply identifying whether feedback is positive or negative, the application aims to help users understand **what people are saying, which areas require attention and what actions could improve the overall experience.**

---

## Author

**Palesa Gaetsewe**

Computer and Information Sciences Graduate  
Aspiring Software Developer  
AI Engineer Intern

---

## Project Status

**Status: In Development**

The application currently includes sentiment analysis, feedback uploads, dashboard visualisations, insights, recommendations, feedback exploration, CSV downloads, selectable themes and the Feedy AI assistant.

Further improvements and refinements are planned as the project continues to develop.
