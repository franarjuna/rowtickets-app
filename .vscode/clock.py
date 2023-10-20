from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=1)
def scheduled_job():
    import requests
    r = requests.get('https://rowticket-app.herokuapp.com/api/cron')

sched.start()