from pywinauto.application import Application
import os
from dotenv import load_dotenv

def login():
    # make your own .env file, copy the contents from "sample.env", paste into .env, change the values in your new .env file to your actual values
    # define path to .env file
    load_dotenv(dotenv_path="C:\\Path\\to\\.env")

    ip_address = os.getenv("IP_ADDRESS")
    sudo_password = os.getenv("SUDO_PASSWORD")
    user_name = os.getenv("USER_NAME")
    port = os.getenv("PORT")

    # Initial login
    app = Application().start(cmd_line=u"putty -ssh " f"{user_name}@{ip_address} -P {port}")
    putty = app.PuTTY
    putty.wait('ready')
    putty.type_keys(sudo_password)
    putty.type_keys("{ENTER}")

if __name__ == "__main__":
    login()
