# 🛡️ No-Hype News: AI-Powered Clickbait Remover

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://no-hype-news.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### *An End-to-End Machine Learning Pipeline that reclaims your attention span.*

---

## 🚀 The Problem
Modern news feeds are optimized for **engagement**, not **information**. "Clickbait" headlines manipulate emotions (Fear, FOMO) to drive ad revenue, forcing users to "doomscroll" to find actual facts.

**The result?** Information overload and anxiety.

## 💡 The Solution
I built an automated AI pipeline that treats news as a data engineering problem. It doesn't just "flag" clickbait—it **fixes** it.

The system:
1.  **Scrapes** 1,300+ daily articles from major tech sources (The Verge, Wired, TechCrunch).
2.  **Clusters** duplicate stories using **Vector Embeddings (DBSCAN)** so you don't see the same story 10 times.
3.  **De-Hypes** headlines using an **LLM Agent**. It extracts the core fact and rewrites the title to be neutral and informative.

---

## ⚙️ Architecture Pipeline

```mermaid
graph LR
    A[RSS Feeds] -->|Scraper| B(Raw Data)
    B -->|LLM Processor| C{GPT-4o Agent}
    C -->|Extract Facts| D[Clean Titles]
    D -->|Embeddings| E[Vector Space]
    E -->|DBSCAN| F[Clustered Stories]
    F -->|Streamlit| G[User Dashboard]
