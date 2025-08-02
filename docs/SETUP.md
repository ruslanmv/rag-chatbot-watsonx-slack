# Project Setup and Execution Guide

This guide provides step-by-step instructions to set up and run the RAG Chatbot project from scratch.

## Prerequisites

Before you begin, ensure you have the following:

-   A **watsonx Orchestrate** account or trial access.
-   Access to **watsonx.ai**.
-   A **Slack workspace** with admin permissions to create and install apps.
-   A **Box** account with a folder containing your knowledge base documents.
-   **Python 3.11+** installed on your system.
-   **Docker** and **Docker Compose** installed and running.

---

## Step 1: Clone and Configure the Environment

1.  **Clone the Repository**
    -   Get the project code onto your local machine.

2.  **Set Up Environment Variables**
    -   Navigate into the project directory: `cd rag-chatbot-watsonx-slack`
    -   Copy the example environment file: `cp .env.example .env`
    -   Open the `.env` file and fill in all the required credentials for watsonx, Box, and Slack.

3.  **Install Dependencies**
    -   It is highly recommended to use a Python virtual environment.
    -   Run the following command to install all required libraries:
        ```bash
        pip install -r requirements.txt
        ```
    -   Alternatively, if you have `make` installed, you can simply run:
        ```bash
        make setup
        ```

---

## Step 2: Set Up External Services

1.  **Configure Box**
    -   Create a folder in your Box account (e.g., `RAG_Knowledge_Base`).
    -   Upload the documents you want to use for your knowledge base.
    -   Go to the [Box Developer Console](https://app.box.com/developers/console) to create a Custom App and generate a **Developer Token**.
    -   Add the **Folder ID** and **Developer Token** to your `.env` file.

2.  **Configure Slack**
    -   Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app.
    -   Enable **Socket Mode**.
    -   Add the required **Bot Token Scopes** (`app_mentions:read`, `chat:write`, etc.) under **OAuth & Permissions**.
    -   Generate an **App-Level Token** with the `connections:write` scope.
    -   Install the app to your workspace.
    -   Add the **Bot User OAuth Token** (`xoxb-...`) and **App-Level Token** (`xapp-...`) to your `.env` file.

---

## Step 3: Run the Application

1.  **Start the watsonx Orchestrate Developer Edition**
    -   This command starts the local server using your credentials.
        ```bash
        orchestrate server start -e .env
        ```

2.  **Activate the Local Environment**
    -   This command points the CLI to your local server.
        ```bash
        orchestrate env activate local
        ```

3.  **Sync Documents and Import the Knowledge Base**
    -   This command runs the `sync_and_import.py` script, which downloads your files from Box and then imports them into watsonx Orchestrate as a knowledge base.
        ```bash
        make import-kb
        ```
    -   *Alternatively, you can run the steps manually:*
        ```bash
        python sync_and_import.py
        orchestrate knowledge-bases import -f knowledge_base_box.yaml
        ```

4.  **Import the Agents and Tools**
    -   Import the initial RAG agent:
        ```bash
        orchestrate agents import -f rag_agent.yaml
        ```
    -   Create the Slack connection and import the tools:
        ```bash
        orchestrate connections add -a slack_connection
        orchestrate connections configure -a slack_connection --env draft -k key_value -t team
        orchestrate connections set-credentials -a slack_connection --env draft -e "bot_token=$SLACK_BOT_TOKEN" -e "app_token=$SLACK_APP_TOKEN"
        orchestrate tools import -k python -f advanced_slack_bot.py --app-id slack_connection
        ```
    -   Import the final agent that uses the Slack tools:
        ```bash
        orchestrate agents import -f enhanced_rag_agent.yaml
        ```

5.  **Start the Chat and Test**
    -   Start the local chat interface:
        ```bash
        orchestrate chat start
        ```
    -   In the chat, start the Slack bot by typing: `Start the advanced Slack bot`
    -   Go to your Slack workspace, invite the bot to a channel, and start asking it questions by mentioning it (e.g., `@YourBot what are the company policies?`).
