import pandas as pd
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def formPage():
    df = pd.read_csv(
        "https://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates",
        encoding="cp950",
    )
    df.isnull().sum()
    df.drop(df.iloc[:, 5:], axis=1, inplace=True)
    df.drop(df.iloc[:, 2:4], axis=1, inplace=True)
    df.columns = ["date", "usd-twd", "usd-jpy"]
    df["twd-jpy"] = df["usd-twd"] / df["usd-jpy"]
    df["twd-usd"] = 1 / df["usd-twd"]
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['date'] = df["date"].astype(str)
    twd_usd_data = df[["date", "twd-usd"]]
    twd_jpy_data = df[["date", "twd-jpy"]]
    result_twd_usd = twd_usd_data.to_json(orient="records")
    result_twd_jpy = twd_jpy_data.to_json(orient="records")
    return render_template("index.html", exchangeData=result_twd_jpy, exchangeData2=result_twd_usd)

if __name__ == '__main__':
    app.run()
