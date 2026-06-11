
# Life Sciences Commercial Analytics Knowledge Graph Explorer

## Overview

The Life Sciences Commercial Analytics Knowledge Graph Explorer is an interactive analytics application developed using Python, Streamlit, NetworkX, Matplotlib, and NumPy. The project models commercial analytics data as a knowledge graph, enabling users to explore entities, analyze relationships, perform graph-based queries, discover business insights, and visualize complex commercial networks.

The application demonstrates how Knowledge Graphs can be used in Life Sciences Commercial Analytics to improve business intelligence, customer understanding, market segmentation analysis, and product influence assessment.

-------------------------------------------------------------------------------------------------------------------------

## Live Application

**Application URL:**
[Knowledge Graph Explorer Live App] https://knowledge-graph-for-customer-analytics-in-life-sciences.streamlit.app/

-------------------------------------------------------------------------------------------------------------------------

## GitHub Repository

**Repository URL:**
(Add your GitHub repository link here)

-----------------------------------------------------------------------------------------------------------------------------

## Project Objective

The objective of this project is to build a Knowledge Graph-based Commercial Analytics platform that:

* Models commercial entities and their relationships.
* Enables knowledge discovery through graph analytics.
* Provides relationship exploration and path finding.
* Generates actionable business insights.
* Supports interactive visualization and reporting.

----------------------------------------------------------------------------------------------------------------------------

## Domain

**Commercial Analytics – Life Sciences**

---------------------------------------------------------------------------------------------------------------------------

## Technology Stack

* Python
* Streamlit
* NetworkX
* Matplotlib
* NumPy
* JSON
* Logging Module

---------------------------------------------------------------------------------------------------------------------------

## Key Features

### 1. Entity Exploration

* View all available entities.
* Search entities by name or type.
* Explore entity information.

### 2. Relationship Exploration

* Analyze connections between entities.
* View relationship distributions.
* Explore business networks.

### 3. Knowledge Queries

* Retrieve products by segment.
* Retrieve customers by region.
* Analyze distributor coverage.
* Explore sales representative assignments.

### 4. Graph Insights

* Most connected entity.
* Most purchased product.
* Most active sales representative.
* Most targeted market segment.
* Region with maximum customers.
* Graph density metrics.

### 5. Custom Discovery Rule

* High Influence Product Score.
* Product influence classification.
* Commercial impact assessment.

### 6. Relationship Path Finder

* Discover shortest paths between entities.
* Analyze indirect relationships.
* Visualize connection chains.

### 7. Knowledge Graph Visualization

* Interactive graph visualization.
* Network structure analysis.
* Relationship mapping.

### 8. Report Generation

* Entity statistics.
* Relationship statistics.
* Business insights.
* Discovery rule results.
* Recommendations.

----------------------------------------------------------------------------------------------------------------------------

## Ontology Structure

### Entity Types

* Products
* Customers
* Sales Representatives
* Distributors
* Regions
* Market Segments

### Relationship Types

* TARGETS
* PURCHASES
* SOLD_IN
* MANAGES
* PROMOTES
* DISTRIBUTES
* OPERATES_IN
* LOCATED_IN
* COVERS

---------------------------------------------------------------------------------------------------------------------------

## Dataset Summary

| Component          |                Count |
| ------------------ | -------------------: |
| Entities           |                   60 |
| Relationship Types |             Multiple |
| Domain             | Commercial Analytics |
| Graph Type         |      Knowledge Graph |

---------------------------------------------------------------------------------------------------------------------------

## High Influence Product Discovery Rule

The project implements a custom business discovery rule:

**Influence Score =**
(Customer Reach × 2) +
(Regional Reach × 3) +
(Segment Breadth × 4)

Products are classified as:

* HIGH Influence
* MEDIUM Influence
* LOW Influence

This enables identification of commercially impactful products.

---------------------------------------------------------------------------------------------------------------------------

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Knowledge-Graph-for-Customer-Analytics-in-Life-Sciences
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run knowledge_graph_explorer.py
```

---

## Requirements

```text
streamlit
networkx
matplotlib
numpy
```

---------------------------------------------------------------------------------------------------------------------------

## Deployment

The application is deployed using Streamlit Community Cloud.

### Deployment Steps

1. Upload project to GitHub.
2. Create a Streamlit Cloud account.
3. Connect the GitHub repository.
4. Select the main branch.
5. Configure the application entry file.
6. Deploy the application.
7. Verify successful deployment.

---------------------------------------------------------------------------------------------------------------------------

## Project Workflow

1. Import libraries and configure logging.
2. Create Entity and Relationship classes.
3. Load Commercial Analytics entities.
4. Load relationship datasets.
5. Build the knowledge graph.
6. Explore entities and relationships.
7. Execute knowledge queries.
8. Generate graph insights.
9. Apply custom discovery rules.
10. Visualize the graph.
11. Perform path finding.
12. Generate reports.
13. Launch Streamlit application.

----------------------------------------------------------------------------------------------------------------------------

## Future Enhancements

* Real-time data integration.
* Interactive graph filtering.
* Advanced graph analytics.
* Machine learning integration.
* Predictive commercial intelligence.
* Automated recommendation engine.

----------------------------------------------------------------------------------------------------------------------------

## Author
Merina Roy
