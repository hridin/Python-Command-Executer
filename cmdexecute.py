
# A very basic python script to login into multiple devices and execute number of commands 
# Logs will be recorded in the log file
# Output of each command will be written to a local folder under date directory
# by hridin@gmail.com, CenturyLink, Aug 2019




#!/usr/bin/env python2
import pexpect,os
import time
import logging
from datetime import date
def main():

    os.system('clear')
    print "***************************************************\nUse this script to execute cmds on Cisco routers\n*******************************************
********\n"
    print "For Example:\n"
    print "For Precheck                     |  For Execution\r"
    print "***************************************************************************"
    print "\rsh run int g9/38                   conf t"
    print "\rsh run int g9/37                   int g9/38"
    print "\rsh int g9/38 status                description Available"
    print "\rsh int g9/37 status                end"
    print "\rsh mac address-table int g9/38     wr me"
    print "\rsh mac address-table int g9/37"
    print "\rsh int g9/38 | inc packet"
    print "\rsh int g9/37 | inc packet\n"
     #print "
    global CA
    CA = raw_input("Enter CA/CRQ No: ").strip()								## Read Change number
    n=int(raw_input("Enter No of devices : "))									## Read Number of devices
    global output
    global command
    devlst = []
    tmplst = []
    cmdlst = []
    myDict = dict()
    for i in range(0,n):
        dev = raw_input("Enter Name of Device "+str(i+1)+": ").strip() 		## Read device name and appends to list
        print "Enter cmds in lines, end with \'quit\' :\n"
        devlst.append(dev) # adding the devices
        while True:
            cmd = str(raw_input())
            if 'quit' in cmd:
                break;
            tmplst.append(cmd)
            cmdlst.append(cmd)
            while('' in tmplst):
                tmplst.remove('')												## Clears any unwanted spaces in input
            myDict[dev]=tmplst													## Assigns device names as key and commands as value into a DICTIONARY
        tmplst = []

    while('' in cmdlst):
        cmdlst.remove('')
    for router in myDict:														## Confirmation to execute the commands entered
        print "\n\n### Commands for "+ router+" are:"
        for command in myDict[router]:
            print command
    today = str(date.today())
    CA = CA + "_" + str(today)
    createFolder(today)															## Creates a folder with date if not exists
    logging.basicConfig(filename=CA+'deletelog.log', filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') ## Writes logs
    output = open(CA +".txt", "a+")											## Opening file to write command outpts
    while True:
        go = raw_input("Enter y or n :").strip()
        if 'y'  in go:
            for deviceName in myDict:											## Iterates thru all devices and prompts for login.
                print "\nEnter credentials for "+ deviceName +"\n"
                username = raw_input( 'Username >> ').strip()
                output.write("\n\n## DEVICE: " + deviceName.upper() +" \n\n")
                password = raw_input( 'Password >> ').strip()
                try:
                    doSSH(deviceName,username,password)							## Calls function to login into device via SSH
                except:
                    print "\n Unable to Login\n"
                    break;
                for command in myDict[deviceName]:
                    exeCMD(command)												## Execute command
                   #ssh.waitnoecho(5)
                ssh.sendline("exit")
                print "\nExited"
                logging.warning('User ' + username + ' Logged out from ' + deviceName)
                ssh.expect(pexpect.EOF)
                ssh.close()
        else:
            break;
        output.close()
        print "\n====================\n OUTPUT   \n====================\n\n"
        s=open(CA+".txt").read()
        print s;
        return
def exeCMD(command):															## Sends command and receives ouput using Pexpect Module
    cmd=command.strip()+"\n"
    print(command)
    try:
        ssh.sendline("\n")
        ssh.expect(prompt)
        ssh.delaybeforesend = 1
        ssh.sendline(cmd)
        #ssh.waitnoecho()
        ssh.expect(prompt)
        result=ssh.after

        output.write(result)
        resultlist=result.split()
        logging.warning('Executed:' + cmd)
        #print result
        #searchOutput(resultlist)
    except:
        print "## Above command failed, retrying ##\n"
        ssh.sendline("\n")
        ssh.expect(prompt)
        ssh.delaybeforesend = 2
        ssh.sendline(cmd)
        #ssh.waitnoecho()
        ssh.expect(prompt)
        result=ssh.after
        output.write(result)

        resultlist=result.split()

        logging.warning('Executed:' + cmd)
        #print result
        #searchOutput(resultlist)

def searchOutput(resultlist):
        indices = [i+1 for i, x in enumerate(resultlist) if x == "route"]
        if indices != '':
            for m in indices:
                command="\nsh run | inc " + resultlist[m]
                print "in function" + command
                exeCMD(command)


def doSSH(deviceName,username,password):													## SSH ing into device
    global ssh
    global prompt
    prompt = '^.*#';
    hostname = deviceName
    cmd = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " + username + "@" + hostname
    print("\nLogging into " + hostname + " . . . ")
    try:
        ssh = pexpect.spawn(cmd)
    except:
        print("\n Unable to login into "+ hostname + ". Please retry")
    ssh.waitnoecho(5)
    i = ssh.expect_exact(['word:','(yes/no)?'])
    if i == 0:
            ssh.sendline(password)
    elif i == 1:
            ssh.sendline("yes\n")
            ssh.expect("word:")
            ssh.sendline(password)

    if(ssh.expect(['^.*>',prompt]) == 0):
        ssh.sendline("enable")
        ssh.expect("word:")
        ssh.sendline(password)
        ssh.expect(prompt)
        ssh.sendline("term len 0\n")
        ssh.expect(prompt)
        print ('User ' + username + ' Logged into ' + hostname)
        logging.warning('User ' + username + ' Logged into ' + hostname)
def createFolder(directory):																		## Creating folder if not exists
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir(os.getcwd()+"/"+directory)
        print "\n Output stored under Folder "+ directory
    except OSError:
        print "\nCant create Directory\n"
    return
if __name__ == "__main__":
    main()
	
	
