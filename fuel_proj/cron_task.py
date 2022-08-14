from datetime import datetime
from adapter_wog import WogScrapper
def cron_task():
    scrapper_wog = WogScrapper()
    scrapper_wog.save_stations_data()
    scrapper_wog.save_fuel_type_data()
    scrapper_wog.save_fuel_price_data()
    scrapper_wog.save_fuel_avaiability_data()

    print(f"Last database update - {datetime.now()}")

cron_task()
