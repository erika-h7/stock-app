# Flet Stock App with Live Data & Charts - Alpha Vantage API
import os
import flet as ft
import requests

def get_api_key():
    api_key = os.getenv("ALPHAVANTAGE_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        return None
    return api_key

API_KEY = get_api_key()
if not API_KEY:
    # show a friendly message in your Flet UI instead of crashing
    print("Warning: ALPHAVANTAGE_API_KEY not set. Set it or create a .env file.")
    # optionally continue with limited functionality or exit

# Example usage: load the key once and reuse it.
API_KEY = get_api_key()

# Main Flet Interface -> Function based
def main(page: ft.Page):
    # App settings
    page.title = "My Stock!"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 900
    page.window_height = 700

    # Sate Variables - Widgets in our App
    stock_symbol = ft.Ref[ft.TextField()] #GOOGL, APPL, MSFT
    chart_container = ft.Ref[ft.Container()]
    price_info = ft.Ref[ft.Container()]
    price_text_below = ft.Ref[ft.Container()]
    error_message = ft.Ref[ft.Container()]
    time_rage_dropdown = ft.Ref[ft.Dropdown()]

    # Time range for the stock
    def get_days_for_range(range_name):
        ranges = {
            "1 week":7,
            "2 weeks":14,
            "30 days":30,
            "90 days":90,
            "1 year":365,
            "5 years":1825
        }

        return ranges.get(range_name, 30)  # Default to 30 days if not found
    
    def get_range_label(range_name):
        return range_name

    
    # Fetch the Stock with our API
    def fetch_stock_data(e):
        symbol = stock_symbol.current.value.strip().upper()
        time_range = time_rage_dropdown.current.value or "30 days"
        days = get_days_for_range(time_range) #365

        if not symbol:
            error_message.current.content = ft.Text("Please enter a stock symbol.", color=ft.Colors.RED, size=14)
            