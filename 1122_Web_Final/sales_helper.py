import pandas as pd


class SalesHelper:
    def __init__(self):
        self.df = pd.read_csv(
            'static/BillLastMonth.csv'
        )

        _set = self.df.iloc[0:18, 3:].sum()  # underscore is used to avoid naming conflict
        noodle = self.df.iloc[18:31, 3:].sum()
        rice = self.df.iloc[31:40, 3:].sum()
        burger = self.df.iloc[40:58, 3:].sum()
        toast = self.df.iloc[58:70, 3:].sum()
        salad = self.df.iloc[70:72, 3:].sum()
        sandwich = self.df.iloc[72:75, 3:].sum()
        pancake = self.df.iloc[75:102, 3:].sum()

        self.df1 = pd.DataFrame({
            '套餐': _set,
            '麵': noodle,
            '飯': rice,
            '潛艇堡': burger,
            '吐司': toast,
            '沙拉': salad,
            '三明治': sandwich,
            '鬆餅': pancake
        })

        self.df2 = self.df.copy()

    def get_df1(self):
        return self.df1

    def get_df2(self):
        return self.df2
