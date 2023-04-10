import re
import pandas as pd

def preprocess(data):
    messages = re.findall('(\d+/\d+/\d+, \d+:\d+\d)+ ([a-z]*) - (.*?): (.*)', data)
    df = pd.DataFrame(messages,columns=['date_time',"time_format",'name','message'])
    df['date'] = pd.to_datetime(df['date_time'],format="%d/%m/%y, %H:%M")
    df["date_num"] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []

    for hour in df[['day_name','hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + "-" + str('00'))

        else:
            period.append(str(hour) + "-" + str(hour+1))

    df["period"] = period

    return df