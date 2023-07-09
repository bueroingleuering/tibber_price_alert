'''@author: robin leuering'''

import tibber
import tibber_credentials
import pandas as pd
from time import sleep

# current time value
now_time = pd.Timestamp.now().tz_localize('Europe/Berlin')
# tibber object
account = tibber.Account(tibber_credentials.token)
home = account.homes[0]
# price object
price_today = home.current_subscription.price_info.today
price_today_index = []
price_today_value = []
# price object to price lists
for price in price_today:
    price_today_index.append(price.starts_at)
    price_today_value.append(price.total)
# price lists to time bases series
ts_price_today = pd.Series(index=pd.to_datetime(price_today_index), data=price_today_value)
# get all prices below today's average price
ts_price_today_affordable = ts_price_today[ts_price_today.values < ts_price_today.mean()]
# get all prices below today's average price since now
ts_price_today_affordable_usable = ts_price_today_affordable[
    ts_price_today_affordable.index >= now_time - pd.Timedelta(hours=1)]
for index_affordable in ts_price_today_affordable_usable.index:
    # current time
    now_time = pd.Timestamp.now().tz_localize('Europe/Berlin')
    if index_affordable > now_time:
        delta_seconds = (index_affordable - now_time).seconds
        print("sleep for the next %s seconds" % delta_seconds)
        # sleep until next affordable price time
        sleep(delta_seconds)
    # push notification with current price
    account.send_push_notification("Cheap price alert", "Price: %s €" % (ts_price_today[index_affordable]))

