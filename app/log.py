import datetime

log = []

def log_msg(msg):
    msg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + " - " + msg
    print(msg)
    log.append(msg)