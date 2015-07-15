# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions
import unittest, time, re , os , socket, sys, datetime , paramiko
from paramiko.sftp_client import SFTPClient


class Upgrade_Test():

    def Test(self):
       try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(30)
            server_ip = sys.argv[1]
            upgrade_version = sys.argv[2]
            fw_path = sys.argv[3]
            ssh_port_status = False
                       
            driver.get("http://"+ server_ip+"/")
            driver.find_element_by_name("user").clear()
            driver.find_element_by_name("user").send_keys("admin")
            driver.find_element_by_name("pass").clear()
            driver.find_element_by_name("pass").send_keys("admin")
            driver.find_element_by_name("login_btn").click()
            driver.find_element_by_xpath("//div[@id='masterdiv']/div[4]").click()
            driver.find_element_by_xpath("//span[@id='sub6']/div[3]").click()
            driver.switch_to_frame("mainContent")        
            #driver.find_element_by_xpath("//input[@id='upload_file']").send_keys("\\\\snow2\\Public\\RD\\beta\\Titan\\NUUO\\nt4040\\v03.00.00\\NT-4040_03.00.0000.0025_20150511_1905.bin")
            driver.find_element_by_xpath("//input[@id='upload_file']").send_keys(fw_path)
            driver.find_element_by_id("OKBTN").click()
            driver.find_element_by_id("fw_upgrade_confirm_ok").click()
            print("upload_status:" + self.upload_status_check(driver)[1]) 
            driver.quit()
            time.sleep(60)
            
            while sshport_check == True:
                ssh_port_status =self.sshport_check(server_ip)
                if ssh_port_status == True:
                    version_compara_status = self.ssh_check(server_ip,upgrade_version)[1]
                    print("verify_upgrade_version:" + version_compara_status)
                    if self.ssh_check(server_ip,upgrade_version)[1] == "fail":
                        print("get_err_log:" + self.download_file(server_ip))
                #else:
                #    print(ssh_port_status)

            sys.exit(0)
       except :
            sys.exit(1)
     

    def sshport_check(self,destip):
        _socket = socket.socket()
        _socket.settimeout(1)
        retry_time= 1
        sshport_status = False
        while retry_time < 11:
            try:
                _socket.connect((destip,22))
                sshport_status = True
                break
            except:
                retry_time= retry_time + 1
                time.sleep(5)
        
        return sshport_status  
      
       
    def ssh_check(self,destip,upgrade_version):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(destip, 22, "root", "xbbigheadluderzalestrong")
            stdin,stdout,stderr = ssh.exec_command("source /etc/titan.conf;echo $NVR")
            current_version=stdout.readline().strip('\t\n\r')
            
            if upgrade_version == current_version:
                return True,"pass"
            else: return False,"fail"       
            ssh.close()
        except :
            return "Ssh connect fail"

    def download_file(self,destip):
        try:
            t = paramiko.Transport((destip,22))
            t.connect(username = "root", password = "xbbigheadluderzalestrong")
            sftp = paramiko.SFTPClient.from_transport(t)
            local_path=os.getcwd()  + "eror.log"
            remote_path = "/mtd/block4/var/log/upgrade_err.log"
            sftp.get(remote_path,local_path)
            return "download file success"
        except:
<<<<<<< HEAD
            return "dowmload file fail"
=======
            #return "dowmload file fail"
>>>>>>> f925c66fae33d7175c7b9c1b0fc1b2487ef6f34d

        
    def upload_status_check(self,driver):
        upload_status = driver.find_element_by_id("new_upload_status")
        #status = driver.find_element_by_id("upgradineinfo")
        
        while True:
            
            #print(upload_status.text)
            if "Upload complete. Please wait while the system reboots." in upload_status.text:
                return True , upload_status.text
                break
            elif "Upload File Timeout !" in upload_status.text:
                return True , upload_status.text
                break
            elif "Firmware file has checksum error." in upload_status.text:
                return False , upload_status.text
                break
            
            time.sleep(5)

    def is_element_present(self, driver,id):
        try: driver.find_element_by_id(id)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True


    
   



_Upgrade_Test = Upgrade_Test()
_Upgrade_Test.Test()
#print(_Upgrade_Test.download_file("10.0.130.175"))