# 🚚 CourierTrack

**CourierTrack** is an **AI agent courier tracking assistant** that enables customers and recipients to interact with their shipments using **natural language**.  
It combines **FastAPI, LangChain, and React** with an **orchestrator agent** and a **SQL agent**, working together to provide real-time tracking updates and intelligent customer service in a conversational interface.

---

## 🎯 Use Case 

- **For Customers (authenticated users):**  
  Get full access to your shipment history, statuses, delivery times, and updates with secure account-based queries.

- **For Recipients (anonymous users):**  
  Track a package with just the tracking number and ask questions like *“When will it arrive?”* or *“Where is it right now?”*.

This system is designed for courier and shipping companies that want to provide **personalized, instant, and AI-driven customer support**.

---

## 🎥 Demo

https://github.com/user-attachments/assets/cc70025f-3886-46a0-a679-091f95172ac8


---

## ✨ Features

- 🔐 **Authenticated Chat:** Secure shipment history and customer support.  
- 📦 **Anonymous Tracking:** Track shipments by tracking number without login.  
- 💬 **Natural Language Queries:** Ask in plain English, no need for complex forms.  
- ⚡ **AI Orchestration:** Smart agent decides when to query the database vs. answer directly.  
- 🗄️ **SQL Agent:** Generates SQL queries dynamically for real-time shipment info.  
- 📜 **Conversation History:** Keeps track of past interactions for smoother dialogue.  
- 🎨 **Modern UI:** React + Tailwind with Aramex-inspired red theme.  

---

## ⚙️ How It Works

1. **User enters a question** (e.g., *“Show my recent shipments”*).  
2. **Orchestrator Agent** checks if it can answer directly or if it needs a DB lookup.  
3. If DB data is needed → the **SQL Agent** generates and executes a query on PostgreSQL.  
4. Results are translated into a natural response by the LLM.  
5. **Frontend React chat interface** displays the AI’s response in real-time.  

---

## 🛠 Tech Stack

- **Backend:** FastAPI, LangChain, ChatGroq LLM, SQLAlchemy, PostgreSQL  
- **Frontend:** React, TailwindCSS, React Router  
- **AI Orchestration:** ConversationBufferMemory, Orchestrator Agent, SQL Agent  
- **Database:** PostgreSQL (shipments, users, tracking updates)  

---

## 💡 Examples

- *“Where is my package with tracking TN0001?”*  
- *“Show me my recent deliveries”*  
- *“When will my package arrive?”*  
- *“How long does shipping usually take?”*  

---
