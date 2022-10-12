from pywinauto.application import Application
import os
import time
import pandas as pd
from dotenv import load_dotenv

# change the values in your new .env file to your actual values
# change path below in line #10

load_dotenv(dotenv_path="C:\\path\\to\\.env")

# Setting variables defined in .env
ip_address = os.getenv("IP_ADDRESS")
sudo_password = os.getenv("SUDO_PASSWORD")
temp_password = os.getenv("TEMP_PASSWORD")
user_name = os.getenv("USER_NAME")
port = os.getenv("PORT")

sp = "{SPACE}"
e = "{ENTER}"

app = Application().start(cmd_line=u"putty -ssh " f"{user_name}@{ip_address} -P {port}")
putty = app.PuTTY

# resets and forces the expiration of user's password
# users are defined within "user-reset.xlsx" with a temporary password of "temp_password" defined in the .env 
# that pre-defined password will have to be used and changed upon the user's next login
def autoReset():
    df = pd.read_excel("C:\\path\\to\\user-reset.xlsx") 
    user_list = df['username'].tolist()
    putty.type_keys("sudo" + sp + "passwd " + sp + str(user_list[0]))
    putty.type_keys(e)
    putty.type_keys(sudo_password)
    putty.type_keys(e)
    putty.type_keys(temp_password)
    putty.type_keys(e)
    putty.type_keys(temp_password)
    putty.type_keys(e)
    time.sleep(.2)
    putty.type_keys("sudo" + sp + "passwd" + sp + "-e" + sp + str(user_list[0]))
    putty.type_keys(e)

    for i in user_list[1:]:
        putty.type_keys("sudo" + sp + "passwd " + sp + str(i))
        putty.type_keys(e)
        putty.type_keys(temp_password)
        putty.type_keys(e)
        putty.type_keys(temp_password)
        putty.type_keys(e)
        time.sleep(.2)
        putty.type_keys("sudo" + sp + "passwd" + sp + "-e" + sp + str(i))
        putty.type_keys(e) 

#  **USE WITH CAUTION** auto-deletes users as defined in userdel.xlsx  
def autoDelete():
    df = pd.read_excel("C:\\path\\to\\userdel.xlsx") 
    user_list = df['username'].tolist()
    putty.type_keys("vim" + sp + "userdel.txt" + e)
    putty.type_keys("i")
    for i in user_list:
        time.sleep(.5)
        putty.type_keys(i + sp + e)
    putty.type_keys("{ESC}")
    putty.type_keys("{VK_SHIFT down}" "ZZ" "{VK_SHIFT up}")
    putty.type_keys("cat userdel.txt" + e, with_spaces=True)
    putty.type_keys("for user in `cat userdel.txt`;do userdel $user;done" + e, with_spaces=True)
    print(user_list)

# bulk creation of users based on useradd.xlsx, to be added
def addUsers():
    pass

# Initial login
def login():
    putty.wait('ready')
    putty.type_keys(sudo_password)
    putty.type_keys("{ENTER}")

if __name__ == "__main__":
    login()
