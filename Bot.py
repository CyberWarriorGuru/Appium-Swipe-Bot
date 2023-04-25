from functions import *
import config
class BumbleBot:

    def __init__(self, cycle_number, desirced_cap, port) -> None:
        self.elements = fnReadJsonData()
        self.desirced_cap = desirced_cap
        self.port = port
        self.server_url = f"http://localhost:{str(self.port)}/wd/hub"
        print(self.desirced_cap, "-------------------")
        self.driver = fnCreateBotInstance(self.desirced_cap, self.server_url)
        self.cycle_number = cycle_number
        self.flag = True
        self.st_time = datetime.now()
        self.ed_time = datetime.now()
        self.refreshtime = random.randint(30, 60)

    def fnSelectBox(self):
        el_selected_boxes = []
        try:
            el_onepage = self.driver.find_element(AppiumBy.XPATH, self.elements["OnePageXpath"])
            self.flag = False
        except:
            el_onepage = self.driver.find_element(AppiumBy.XPATH, self.elements["OnePage1Xpath"])
            self.flag = True

        self.el_boxes = self.driver.find_elements(AppiumBy.XPATH, self.elements["BoxXpath"])
        if len(self.el_boxes) == 0:
            print("Please make full screen size")
            el_selected_boxes = []
            return el_selected_boxes
        action_number = random.randint(0, 9)
        # Swipe 2 box
        try:
            if RANDOM_NUMBER[action_number] == 10:
                selected_numbers = fnGenerateNonRepeatNumber()
                el_selected_boxes.append(self.el_boxes[selected_numbers[0]])
                el_selected_boxes.append(self.el_boxes[selected_numbers[1]])
            # Swipe None
            elif RANDOM_NUMBER[action_number] == -1:
                print("Non select Box...")
                el_selected_boxes = []
            # Swipe One Box
            else:
                el_selected_boxes.append(self.el_boxes[RANDOM_NUMBER[action_number]])
        except:
            print("Non select Box...")
            el_selected_boxes = []
        return el_selected_boxes
    
    def fnSwipeBox(self, st_x, st_y, w_box, h_box):
        st_x = st_x + 10
        st_y = st_y + int(h_box / 2)
        ed_x = st_x + w_box - 30
        ed_y = st_y
        self.driver.swipe(start_x=st_x, start_y=st_y, end_x=ed_x, end_y=ed_y, duration=550)

    def fnScrollDown(self):
        el_parent = self.driver.find_element(AppiumBy.XPATH, self.elements["ParentXpath"])
        try:
            st_x = self.el_boxes[3].location["x"] + self.el_boxes[3].size["width"] + 10
            st_y = self.el_boxes[3].location["y"] + self.el_boxes[3].size["height"] -10
        except:
            print("Scroll ended...")
            return
        ed_x = el_parent.location['x']
        ed_y = el_parent.location['y']
        if self.flag == False:
            self.driver.swipe(start_x=st_x, start_y=st_y, end_x=0, end_y=0, duration=600)
        else:
            self.driver.swipe(start_x=st_x, start_y=st_y, end_x=ed_x, end_y=ed_y, duration=800)

    def fnRefresh(self):
        self.driver.find_element(AppiumBy.XPATH, self.elements["PeopleXpath"]).click()
        time.sleep(1)
        self.driver.find_element(AppiumBy.XPATH, self.elements["LikeXpath"]).click()
        time.sleep(3)
    
    def fnMakeFullScreen(self):
        print(1)
        header = self.driver.find_element(AppiumBy.XPATH, self.elements["ParentXpath"])
        print(2)
        header_size = header.size
        header_position = header.location
        header_w = header_size['width']
        header_h = header_size['height']
        if header_w > header_h:
            st_x = header_position['x'] + header_w - 20
            st_y = header_position['y'] + header_h + 200
            ed_x = header_position['x'] + header_w
            ed_y = header_position['y']
            self.driver.swipe(start_x=st_x, start_y=st_y, end_x=ed_x, end_y=ed_y, duration=600)



    def runBot(self):
        try:
            for k in range(0, self.cycle_number):
                try:
                    print("MakeScreen")
                    self.fnMakeFullScreen()
                    selected_boxes = self.fnSelectBox()
                    for i in range(0, len(selected_boxes)):
                        temp_box = selected_boxes[i]
                        temp_box_location = temp_box.location
                        temp_box_size = temp_box.size
                        self.fnSwipeBox(temp_box_location['x'], temp_box_location['y'], temp_box_size['width'], temp_box_size['height'])
                        time.sleep(random.randint(2500, 5000) / (1000*config.SPEED))
                        print(f"Current Speed is {config.SPEED}x")
                        print("Current Sleep Time is ", random.randint(2500, 5000) / (1000*config.SPEED))
                        self.ed_time = datetime.now()
                        if (self.ed_time - self.st_time).total_seconds() > self.refreshtime:
                            self.st_time = datetime.now()
                            self.fnRefresh()
                            time.sleep(3)
                    self.fnScrollDown()
                        
                except:
                    continue
        except:
            print("skip")

        print("This Instance is finished.")
                    

            


# if __name__ == "__main__":
#     # load_dotenv()
#     config.init()
#     config.SPEED = 1
#     service = AppiumService()
#     args = [
#         "--address", "127.0.0.1", 
#         "--port", PORT,
#         "--log-no-colors",
#         "--allow-cors",
#         "--base-path", '/wd/hub'
#     ]
#     print(f"starting cmd = appium {' '.join(args)}")
#     service.start(args=args)
#     print(f"service.is_running={service.is_running}")
#     print(f"service.is_listening={service.is_listening}")
#     bot = BumbleBot(cycle_number=10)
#     bot.runBot()