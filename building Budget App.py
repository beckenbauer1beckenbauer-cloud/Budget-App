class Category:
    """
    A class to represent a budget category, managing deposits, withdrawals,
    and transfers, and providing a formatted ledger view.
    """
    def __init__(self, name):
        """Initializes a Category with a name and an empty ledger."""
        self.name = name
        self.ledger = []

    def __str__(self):
        """Returns a string representation of the budget category ledger."""
        
        # 1. Title Line
        title = self.name.center(30, '*')
        
        # 2. Ledger Items
        items = []
        for item in self.ledger:
            # Format description (max 23 chars)
            description = item['description'][:23].ljust(23)
            
            # Format amount (right-aligned, 2 decimal places, max 7 chars)
            # The format specifier '7.2f' ensures 7 characters total (including '.', and negative sign)
            amount = format(item['amount'], '.2f').rjust(7)
            
            items.append(f"{description}{amount}")
            
        ledger_output = '\n'.join(items)
        
        # 3. Total Line
        total = self.get_balance()
        total_line = f"Total: {format(total, '.2f')}"
        
        return f"{title}\n{ledger_output}\n{total_line}"

    def deposit(self, amount, description=""):
        """
        Adds a deposit to the ledger.
        """
        self.ledger.append({"amount": amount, "description": description})

    def check_funds(self, amount):
        """
        Returns True if the amount is less than or equal to the current balance, False otherwise.
        """
        return amount <= self.get_balance()

    def withdraw(self, amount, description=""):
        """
        Adds a withdrawal to the ledger if sufficient funds exist. 
        Returns True if withdrawal took place, False otherwise.
        """
        if self.check_funds(amount):
            # Amount stored as a negative number
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """
        Returns the current balance of the budget category.
        """
        total = sum(item['amount'] for item in self.ledger)
        return total

    def transfer(self, amount, category):
        """
        Transfers funds to another budget category. 
        Returns True if the transfer took place, False otherwise.
        """
        if self.check_funds(amount):
            # Withdrawal from source category
            self.withdraw(amount, f"Transfer to {category.name}")
            
            # Deposit to destination category
            category.deposit(amount, f"Transfer from {self.name}")
            
            return True
        return False

# --- Function for creating the spend chart ---

def create_spend_chart(categories):
    """
    Creates a bar chart showing the percentage spent (withdrawals only) 
    in each category relative to the total spent across all categories.
    """
    
    # 1. Calculate the total spent for each category (Withdrawals only)
    spent_amounts = []
    for category in categories:
        spent = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        # Note: spent is a negative number, use abs() for comparisons
        spent_amounts.append(abs(spent))
        
    total_spent_all = sum(spent_amounts)
    
    # 2. Calculate the percentage spent for each category, rounded down to the nearest 10
    percent_spent = []
    for amount in spent_amounts:
        if total_spent_all == 0:
            percent = 0
        else:
            percent = (amount / total_spent_all) * 100
        # Round down to the nearest 10
        percent_spent.append(int(percent // 10) * 10)

    # 3. Build the Chart String
    
    chart_output = "Percentage spent by category\n"
    
    # Build the vertical axis and bars
    for i in range(100, -1, -10):
        # Y-axis label (right-aligned, 3 chars, padded with space)
        line = str(i).rjust(3) + "|"
        
        for percent in percent_spent:
            if percent >= i:
                line += " o " # Bar present
            else:
                line += "   " # No bar
        
        chart_output += line + " \n" # Add extra space for the horizontal line to pass

    # Build the horizontal line
    # (3 spaces for '100', 1 for '|', and 3*N categories for the bars, 1 extra space)
    num_categories = len(categories)
    dash_line = "    " + ("---" * num_categories) + "-"
    chart_output += dash_line + "\n"

    # 4. Build the Category Names (Vertical)
    
    category_names = [category.name for category in categories]
    max_name_length = max(len(name) for name in category_names) if category_names else 0
    
    name_lines = []
    for i in range(max_name_length):
        name_line = "    " # Padding to align with the start of the bars
        for name in category_names:
            if i < len(name):
                name_line += f" {name[i]} "
            else:
                name_line += "   "
        
        name_lines.append(name_line + " ") # Add final space for alignment

    chart_output += "\n".join(name_lines)
    
    return chart_output
