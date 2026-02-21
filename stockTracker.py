def stock_portfolio_tracker():
    # Hardcoded dictionary of stock prices (in USD)
    stock_prices = {
        "AAPL": 180.25,    # Apple Inc.
        "TSLA": 250.75,    # Tesla Inc.
        "GOOGL": 135.50,   # Alphabet Inc.
        "MSFT": 330.20,    # Microsoft
        "AMZN": 145.80,    # Amazon
        "NVDA": 450.30,    # NVIDIA
        "META": 365.40,    # Meta Platforms
        "BRK-B": 400.15    # Berkshire Hathaway
    }
    
    print("=" * 50)
    print("STOCK PORTFOLIO TRACKER")
    print("=" * 50)
    print("\nAvailable stocks and current prices:")
    for stock, price in stock_prices.items():
        print(f"  {stock}: ${price:.2f}")
    
    portfolio = {}
    total_investment = 0.0
    
    print("\n" + "-" * 50)
    print("ENTER YOUR PORTFOLIO")
    print("-" * 50)
    
    while True:
        print("\nEnter stock symbol (or type 'done' to finish):")
        stock_symbol = input("Stock symbol: ").upper()
        
        if stock_symbol == 'DONE':
            break
        
        if stock_symbol not in stock_prices:
            print(f"Error: '{stock_symbol}' is not in our database.")
            print("Available stocks:", ", ".join(stock_prices.keys()))
            continue
        
        try:
            quantity = int(input(f"Quantity of {stock_symbol}: "))
            if quantity <= 0:
                print("Error: Quantity must be positive.")
                continue
        except ValueError:
            print("Error: Please enter a valid number.")
            continue
        
        # Calculate value for this stock
        price = stock_prices[stock_symbol]
        value = price * quantity
        
        # Add to portfolio
        portfolio[stock_symbol] = {
            'quantity': quantity,
            'price': price,
            'value': value
        }
        
        print(f"Added: {quantity} shares of {stock_symbol} at ${price:.2f} = ${value:.2f}")
    
    # Calculate total investment
    total_investment = sum(item['value'] for item in portfolio.values())
    
    # Display results
    print("\n" + "=" * 50)
    print("PORTFOLIO SUMMARY")
    print("=" * 50)
    
    if not portfolio:
        print("Your portfolio is empty.")
        return
    
    print(f"\n{'Stock':<8} {'Quantity':<10} {'Price':<12} {'Value':<12}")
    print("-" * 50)
    
    for stock, data in portfolio.items():
        print(f"{stock:<8} {data['quantity']:<10} ${data['price']:<11.2f} ${data['value']:<11.2f}")
    
    print("-" * 50)
    print(f"{'TOTAL INVESTMENT':<30} ${total_investment:>15.2f}")
    print("=" * 50)
    
    # Ask if user wants to save results
    save_option = input("\nDo you want to save the results to a file? (yes/no): ").lower()
    
    if save_option in ['yes', 'y']:
        save_results(portfolio, total_investment)

def save_results(portfolio, total_investment):
    """Save portfolio results to file"""
    
    print("\nChoose file format:")
    print("1. Text file (.txt)")
    print("2. CSV file (.csv)")
    
    choice = input("Enter 1 or 2: ")
    
    if choice == '1':
        filename = "portfolio_summary.txt"
        with open(filename, 'w') as file:
            file.write("=" * 50 + "\n")
            file.write("STOCK PORTFOLIO SUMMARY\n")
            file.write("=" * 50 + "\n\n")
            file.write(f"{'Stock':<8} {'Quantity':<10} {'Price':<12} {'Value':<12}\n")
            file.write("-" * 50 + "\n")
            
            for stock, data in portfolio.items():
                file.write(f"{stock:<8} {data['quantity']:<10} ${data['price']:<11.2f} ${data['value']:<11.2f}\n")
            
            file.write("-" * 50 + "\n")
            file.write(f"{'TOTAL INVESTMENT':<30} ${total_investment:>15.2f}\n")
            file.write("=" * 50 + "\n")
        
        print(f"\nPortfolio summary saved to '{filename}'")
        
    elif choice == '2':
        filename = "portfolio_summary.csv"
        with open(filename, 'w') as file:
            file.write("Stock,Quantity,Price,Value\n")
            
            for stock, data in portfolio.items():
                file.write(f"{stock},{data['quantity']},{data['price']:.2f},{data['value']:.2f}\n")
            
            file.write(f"TOTAL,,,{total_investment:.2f}\n")
        
        print(f"\nPortfolio summary saved to '{filename}'")
    else:
        print("Invalid choice. File not saved.")

def view_saved_portfolio():
    """View previously saved portfolio from file"""
    
    print("\n" + "=" * 50)
    print("VIEW SAVED PORTFOLIO")
    print("=" * 50)
    
    files = ["portfolio_summary.txt", "portfolio_summary.csv"]
    found_files = []
    
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
                found_files.append(file)
                print(f"\n--- Content of {file} ---")
                print(content)
        except FileNotFoundError:
            pass
    
    if not found_files:
        print("\nNo saved portfolio files found.")

def main():
    """Main program with menu"""
    
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Create new portfolio")
        print("2. View saved portfolio files")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            stock_portfolio_tracker()
        elif choice == '2':
            view_saved_portfolio()
        elif choice == '3':
            print("\nThank you for using Stock Portfolio Tracker!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the program
if __name__ == "__main__":
    main()
