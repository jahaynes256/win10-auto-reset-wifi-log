import socket, time, datetime, os

#SETTINGS
SECS_BETWEEN_PINGS = 20.0
REMOTE_SERVER = "www.google.com"
LOG_FILE = "log\\log.txt"
WIFI_ADAPTER = "WIFI"


def resetAdapter(wifiAdapter= WIFI_ADAPTER, delay=0.0):

    """
    Resets the wireless device specified with an optional delay between
    being disabled and enabled.
    """

    os.system(f"netsh interface set interface \"{wifiAdapter}\" disabled")
    time.sleep(delay)
    os.system(f"netsh interface set interface \"{wifiAdapter}\" enabled")


def log(status):

    """
    Logs wireless status to LOG_FILE and terminal.
    """

    with open(LOG_FILE,'a+') as f:
        f.write(status + "\n")
    print(status)


def is_connected(hostname):

    """
    Checks if it can establish a connection with host. If so,
    returns True. Otherwise, False
    """

    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


if __name__ == '__main__':
    print("----------------------James's Connection Manager-------------------")
    print(f"REMOTE_SERVER = {REMOTE_SERVER}\t SECS_BETWEEN_PINGS: {SECS_BETWEEN_PINGS}")
    while True:
        currentTime = str(datetime.datetime.now())
        if(is_connected(REMOTE_SERVER)):
            status = f'(+) {currentTime}'
            log(status)
        else:
            status = f'(-) {currentTime}'
            log(status)
            log("\tReseting Connection...")
            resetAdapter()
            log("\tConnection Reset")
        time.sleep(SECS_BETWEEN_PINGS)



