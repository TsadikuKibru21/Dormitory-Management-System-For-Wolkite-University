from apscheduler.schedulers.background import BackgroundScheduler


scheduler=BackgroundScheduler()
job=None

def trik():
    print("gate")
def start_job():
    global job
    job=scheduler.add_job(trik, 'interval',seconds=10)
    try:
        scheduler.start()
    except:
        pass

