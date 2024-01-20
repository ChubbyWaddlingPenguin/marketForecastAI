A project using AI to attempt to predict stock trends :)

AI model is training separately, and will be integrated into the project when complete.

Uses Alpha Vantage Stock API, currently pulls intraday trading data at 5 mins intervals from December 2023.

Current status:
  Working website graphing trend of inputed stock symbol.
  (Behind the scenes):
    Training AI model, will be integrated into website soon.

Update 0.1 logs:
- Call Main.java responsible for API requests and populating database using Python subprocess through views.py instead of PHP script (callJavaAPI.php removed)
- Fixed issues occuring when submitting new stock symbols on website leading to chart reloading errors
- Add stopgap if API down

Updates coming (no specific order):
- Graph with different price points (high, low, open, close)
- Interactive graph
- Move away from plain html, integrate ReactJS into frontend
- Deprecate models.py, and use direct SQL queries to better manage a dynamic database
- Integrate AI model into website & graph
- etc.

Arthur
