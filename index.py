from config import *
from Bot import *
import config
from concurrent.futures import ThreadPoolExecutor
import subprocess

class Main(QDialog, ui_main.Ui_Dialog):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        header = self.table_device.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.btn_start.setProperty('class', 'success')
        self.btn_refresh.setProperty('class', 'danger')
        self.btn_refresh.clicked.connect(self.fnRefresh)
        self.btn_start.clicked.connect(self.fnStart)
        self.horizontalSlider.valueChanged.connect(self.fnAdjustSpeed)
        config.init()
        config.SPEED =  int(self.horizontalSlider.value())

    def fnAdjustSpeed(self):
        config.SPEED = int(self.horizontalSlider.value())
    def fnRefresh(self):
        self.table_device.setRowCount(0)
        # os.popen("adb kill-server")
        # time.sleep(3) 
        device_list = os.popen("adb devices").readlines()
        n_device = len(device_list)-2
        for i in range(0, n_device):
            rowPosition = self.table_device.rowCount()
            self.table_device.insertRow(rowPosition)
            self.table_device.setItem(rowPosition , 0, QTableWidgetItem(device_list[i+1].split("\t")[0]))

    def fnStart(self):
        try:
            data = []
            for row in range(self.table_device.rowCount()):
                try:
                    device_name = self.table_device.item(row, 0).text()
                    swipe_number = self.table_device.item(row, 1).text()
                    data.append([device_name, swipe_number])
                except:
                    self.fnShowMessageBox(title="Warning", text_body="Please refresh the device and input their IP address")
                    return
            if data == []:
                self.fnShowMessageBox(title="Warning", text_body="Please refresh the device and input their IP address")
                return
            # with ThreadPoolExecutor(max_workers=2) as executor:
            #     tasks = []
            #     results = []
            for i in range(0, len(data)):
                try:
                    udid_cmd = f"adb -s {data[i][0]} shell getprop ro.serialno"
                    udid_output = subprocess.check_output(udid_cmd.split()).decode()
                    temp_udid = udid_output.strip()
                    temp_desired_cap = {
                        "platformName": 'Android',
                        "deviceName": f"{data[i][0]}",
                        "newCommandTimeout": "99999",
                        "uiautomator2ServerInstallTimeout": "99999",

                        # "udid": f"{temp_udid}",
                    }

                    port = str(int(PORT) + (i*2))
                    hubport = 2254 + (i*2)

                    # os.system(f"start /B start cmd.exe @cmd /k appium -a 127.0.0.1 -p {port} -bp {hubport} --udid {data[i]} --session-override")
                    time.sleep(3)
                    # cycle_number = self.spinBox.value()
                    # task1 = executor.submit(self.fnThread, port, cycle_number,  temp_desired_cap)
                    # tasks.append(task1)
                    m_thread = threading.Thread(target=self.fnThread, args=(port, data[i][0], int(data[i][1]),  hubport, temp_desired_cap))
                    m_thread.start()
                    time.sleep(3)
                except:
                    continue
                # for i in range(0, len(tasks)):
                #     results.append(tasks[i].result())
        except:
            return
    
    def fnShowMessageBox(self, title, text_body):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text_body)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def fnThread(self, port, udid, swipe_number, hubport, temp_desired_cap):
        service = AppiumService()
        args = [
            "--address", "127.0.0.1", 
            "--port", port,
            # "--log-no-colors",
            # "--session-override",
            # "--log-timestamp",
            # "--hubPort", str(hubport),
            "--session-override",
            "--udid", udid,
            "-bp", str(hubport),
            # "--allow-cors",
            "--base-path", '/wd/hub',
            # "-nodeconfig", str(config)
        ]
        print(args)
        print(f"starting cmd = appium {' '.join(args)}")
        service.start(args=args)
        # print(f"service.is_running={service.is_running}")
        # print(f"service.is_listening={service.is_listening}")
        bot = BumbleBot(cycle_number=swipe_number, desirced_cap = temp_desired_cap, port=port)
        bot.runBot()
        # service.stop()


app = QApplication(argv)
form = Main()
apply_stylesheet(app, theme='dark_teal.xml')
form.show()
app.exec_()