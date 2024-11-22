import json
import yfinance as yf


class StockPortfolio:
    def __init__(self, file="portfolio.json"):
        self.file = file
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_portfolio(self):
        with open(self.file, "w") as f:
            json.dump(self.portfolio, f, indent=4)

    def add_stock(self, ticker, shares, purchase_price):
        if ticker in self.portfolio:
            print(f"{ticker} already exists in your portfolio. Updating shares and price.")
            self.portfolio[ticker]["shares"] += shares
            self.portfolio[ticker]["purchase_price"] = (
                self.portfolio[ticker]["purchase_price"] + purchase_price
            ) / 2
        else:
            self.portfolio[ticker] = {"shares": shares, "purchase_price": purchase_price}
        self.save_portfolio()
        print(f"Added {ticker} to your portfolio.")

    def remove_stock(self, ticker):
        if ticker in self.portfolio:
            del self.portfolio[ticker]
            self.save_portfolio()
            print(f"Removed {ticker} from your portfolio.")
        else:
            print(f"{ticker} not found in your portfolio.")

    def get_stock_performance(self):
        if not self.portfolio:
            print("Your portfolio is empty.")
            return

        print(f"{'Ticker':<10}{'Shares':<10}{'Purchase Price':<15}{'Current Price':<15}{'Profit/Loss':<15}")
        print("-" * 65)

        for ticker, details in self.portfolio.items():
            shares = details["shares"]
            purchase_price = details["purchase_price"]
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.history(period="1d")["Close"].iloc[-1]
                profit_loss = (current_price - purchase_price) * shares
                print(
                    f"{ticker:<10}{shares:<10}{purchase_price:<15.2f}{current_price:<15.2f}{profit_loss:<15.2f}"
                )
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

    def menu(self):
        while True:
            print("\n--- Stock Portfolio Tracker ---")
            print("1. Add Stock")
            print("2. Remove Stock")
            print("3. View Performance")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                ticker = input("Enter stock ticker: ").upper()
                shares = int(input("Enter number of shares: "))
                purchase_price = float(input("Enter purchase price per share: "))
                self.add_stock(ticker, shares, purchase_price)
            elif choice == "2":
                ticker = input("Enter stock ticker to remove: ").upper()
                self.remove_stock(ticker)
            elif choice == "3":
                self.get_stock_performance()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    portfolio = StockPortfolio()
    portfolio.menu()
