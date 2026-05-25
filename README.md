# Budget App

A robust Python budget management system that enables categorical spending tracking, inter-category transfers, and visual expenditure analysis. This project emphasizes clean object-oriented design and precise text-based data visualization.

## 🚀 Key Features
- **Categorical Ledger:** Maintains individual transaction histories for distinct budget categories (e.g., Food, Clothing).
- **Safe Transfers:** Implements internal logic to prevent overdrafts during inter-category transfers.
- **Visual Analytics:** Generates a dynamic, ASCII-based bar chart to illustrate spending distribution across all categories.
- **Precision Formatting:** Custom string representation (`__str__`) for ledger printing with strict alignment constraints.

## 🛠️ Technical Stack
- **Language:** Python 3
- **Concepts:** Object-Oriented Programming (OOP), String Formatting, Algorithmic Visualization, State Management

## 🧩 Architecture Overview
The system relies on the `Category` class to act as a self-contained controller for its own balance and ledger history. The `create_spend_chart` function acts as an external reporter, aggregating data from multiple instances.



```mermaid
graph TD
    A[Category Object] -->|deposit/withdraw| B[Ledger List]
    B --> C[get_balance]
    A -->|transfer| D[Target Category]
    subgraph Visualization
    E[create_spend_chart] --> F[Calculate Percentages]
    F --> G[Build ASCII Grid]
    end
