# 📦 Inventory & Fire Alarm Management App

**Inventory & Fire Alarm Management App** is a desktop application built with **Flet** that allows users to search fire alarm devices by address, view their maintenance history, and manage inventory of equipment, tools, and materials with real-time movement tracking. It seamlessly integrates with **Firebase** (Realtime Database and Firestore) to provide instant synchronization, structured data storage, and efficient record management for maintenance and operations teams.

---

## 🗂 Main Features

1. **🏠 Home Page**  
   Displays usage instructions and quick-start guidelines for new users.

2. **🚨 Fire Alarm Browser**  
   Search fire alarm devices by their address and instantly view their maintenance history.

3. **📋 Inventory Browser, Management & Activity Log**  
   Search, add, edit, and delete inventory items with real-time updates, and view a detailed log of all inventory movements for better stock control and traceability.

---

## 🖼 Images

<div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px; background-color: #f9f9f9;">
  <img src="src\assets\images\sdaci1.png" alt="Home Page" width="500" style="border-radius: 10px;">
  <img src="src\assets\images\sdaci2.png" alt="Fire Alarm Browser" width="500" style="border-radius: 10px;">
   <img src="src\assets\images\sdaci3.png" alt="Inventory Browser" width="500" style="border-radius: 10px;">
</div>



---

## 🛠 Technologies Used

| Technology        | Purpose |
|-------------------|---------|
| **Python**        | Core programming language for app logic |
| **Flet**          | UI framework for building the desktop interface |
| **Firebase**      | Cloud backend for data storage and real-time sync |
| **Realtime Database** | Instant synchronization of data across clients |
| **Firestore Database** | Structured storage and advanced querying |
| **Git**           | Version control system |
| **GitHub**        | Repository hosting and collaboration |

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/Bescarso/Panel_SDACI-V2.0.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python src\main.py
