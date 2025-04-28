# Agentic-AI-Multiagentic-with-Autogen

This project implements a multi-agent system using the `pyautogen` library to generate AI-driven architecture solutions. The system leverages multiple agents, each with a specific role, to collaboratively design solutions for business problems. The application is built using Streamlit for an interactive user interface.

---

## Business Use Case

### Problem Statement
Organizations often face challenges in designing robust, scalable, and cost-effective architecture solutions for their business requirements. These solutions may involve cloud services, open-source software, or a combination of both. Additionally, evaluating and comparing these solutions requires expertise and time.

### Solution
This project provides an **AI-driven multi-agent system** that automates the process of designing and evaluating architecture solutions. The system uses three specialized agents:
1. **Cloud Architect Agent**: Designs solutions using cloud platforms like Azure, AWS, and GCP.
2. **Open-Source Architect Agent**: Focuses on solutions using open-source software, avoiding cloud dependencies.
3. **Lead Architect Agent**: Reviews and evaluates the solutions provided by the other agents, highlighting pros and cons and selecting the best approach.

The user provides a business problem or requirement, and the system generates architecture designs, comparisons, and recommendations.

---

## Workflow Diagram

Below is the high-level workflow of the system:

Multi-Agent System
The application uses the following components from the autogen library:

AssistantAgent: Represents an AI agent that performs specific tasks.
UserProxyAgent: Acts as a proxy for user interactions.
GroupChat and GroupChatManager: Manage communication and collaboration between agents.
Workflow
User Input: The user enters a business problem or requirement through the Streamlit UI.
Agent Initialization: The application initializes the agents (Cloud Architect, Open-Source Architect, and Lead Architect) using the autogen library.
Task Execution: Each agent generates solutions based on its expertise.
Evaluation: The Lead Architect Agent evaluates the solutions and provides a recommendation.
Output Display: The final output is displayed in the Streamlit UI.