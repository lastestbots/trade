from core.job.alert_price import AlertPriceTask

task = AlertPriceTask()
task.symbols = ['ETHUSDT', 'BNBUSDT']
task.target_prices = [1770, 350]
task.run()

