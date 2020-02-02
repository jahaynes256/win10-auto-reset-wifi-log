import socket, time, datetime, os, re

#SETTINGS
SECS_BETWEEN_PINGS = 20.0
REMOTE_SERVER = "www.google.com"
LOG_FILE = "log\\log.txt"

def wifiProperties(key):
    """
    Parses the "netsh wlan show interfaces" command into a dictionary.
    """
    lines = os.popen("netsh wlan show interfaces").read().splitlines()

    #It makes me laugh, but it works. Removes empty strings from list and the first line too.    
    lines = [line.strip() for line in lines if line][1::] 
    
    "Group 1 is the Key and Group 4 is the Value"
    regex = r"(\w*\s?\w*\s?\S*)(\s*)(:\W)(.*$)" 
    
    keys = [re.search(regex, line).group(1).strip() for line in lines]
    values = [re.search(regex, line).group(4).strip() for line in lines]
    properties = dict(zip(keys,values))
    return properties[key]

def resetAdapter(delay=0.0):

    """
    Resets the wireless device specified with an optional delay between
    being disabled and enabled.
    """
    wifiAdapter = wifiProperties('Name')
    os.system(f"netsh interface set interface \"{wifiAdapter}\" disabled")
    time.sleep(delay)
    os.system(f"netsh interface set interface \"{wifiAdapter}\" enabled")

def logMSG(message):

    """
    Logs a message to LOG_FILE and terminal.
    """

    with open(LOG_FILE,'a+') as f:
        f.write(message + "\n")
    print(message)

def logStatus(failed=True,verbose=True):

    """
    Logs wireless status to LOG_FILE and terminal.
    """
    logTime = datetime.datetime.now()
    
    if failed:
        status = f'FAILED at {logTime}'
    else:
        status = f'+ {logTime}'
    if verbose:
        properties = f"\
        \n\tAdapater         : {wifiProperties('Name')}\
        \n\tSSID             : {wifiProperties('SSID')}\
        \n\tSignal Strength  : {wifiProperties('Signal')}"
        status += properties
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


def statusLoop(verbose=True):
    """
    Main Loop
    """
    print("----------------------James's Connection Manager-------------------")
    print(f"REMOTE_SERVER = {REMOTE_SERVER}\t SECS_BETWEEN_PINGS: {SECS_BETWEEN_PINGS}")
    while True:
        if(is_connected(REMOTE_SERVER)):
            logStatus(failed=False)
        else:
            logStatus()
            logMSG("\tReseting Connection...")
            resetAdapter()
            logMSG("\tConnection Reset")
        time.sleep(SECS_BETWEEN_PINGS)



if __name__ == '__main__':
    statusLoop()




