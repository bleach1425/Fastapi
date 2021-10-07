import sys
sys.path.append('../../')
from base64_change import base64_change
import requests
from datetime import datetime
import time

def check_type(param):
    """:type
    check param type and check
    """
    if param[0].split('.')[-1] == 'jpg' or param[0].split('.')[-1] == 'png':
        image_name = param
        return image_name


class time_object():
    def __init__(self):
        pass
    def time(self):
        t = datetime.now()
        return str(t)
    def calculate_time(self):
        t = datetime.now()
        return t
    def driver_time(self, start, end):
        driver_time = end - start
        return str(driver_time)


class api():
    def __init__(self, url, method, loop, **kwargs):
        """:type
        input url, method, loop
        output response text, status_code
        """
        self.url = url
        self.method = method
        self.loop = loop
        self.runtime = 0

    def main(self, *param):
        time_obj = time_object()
        Start_time = time_obj.calculate_time()
        print("Start Test in %s" % time_obj.time())
        if self.method == 'GET':
            for n in range(self.loop):
                self.runtime += 1
                print(f"Runtime No.{self.runtime}")
                print('')
                try:
                    r = requests.get(self.url, timeout=60)
                    driver_time = time_obj.driver_time(Start_time, time_obj.calculate_time())
                    Start_time = time_obj.calculate_time()
                    print('*' * 10)
                    print("Status Code: ", r.status_code)
                    print("Response Text: ", r.text)
                    print("Driver Time: ", driver_time)
                    print('*' * 10)
                    print('')
                except requests.exceptions.RequestException as e:
                    driver_time = time_obj.driver_time(Start_time, time_obj.calculate_time())
                    Start_time = time_obj.calculate_time()
                    print('*' * 10)
                    print('Request error')
                    print('Driver Time:', driver_time)
                    print('*' * 10)
                    print('')
                    raise SystemExit(e)
            print('waiting 10 second views result')
            time.sleep(10)
            self.runtime = 0
        elif self.method == 'POST':
            if param and 'base64' in param:
                for n in range(loop):
                    self.runtime += 1
                    print(f"Runtime No.{self.runtime}")
                    print('')
                    base64 = base64_change.base64_func()
                    check_type(param[0])
            elif param and 'base64' not in param:
                for n in range(loop):
                    self.runtime += 1
                    print(f"Runtime No.{self.runtime}")
                    print('')
                    r = requests.post(self.url, self.data, timeout=60)
                    driver_time = time_obj.driver_time(Start_time, time_obj.calculate_time())
                    Start_time = time_obj.calculate_time()
                    print('*' * 10)
                    print("Status Code: ", r.status_code)
                    print("Response Text: ", r.text)
                    print("Driver Time: ", driver_time)
                    print('*' * 10)
                    print('')
            else:
                for n in range(loop):
                    self.runtime += 1
                    print(f"Runtime No.{self.runtime}")
                    print('')
                    r = requests.post(self.url, timeout=60)
                    driver_time = time_obj.driver_time(Start_time, time_obj.calculate_time())
                    Start_time = time_obj.calculate_time()
                    print('*' * 10)
                    print("Status Code: ", r.status_code)
                    print("Response Text: ", r.text)
                    print("Driver Time: ", driver_time)
                    print('*' * 10)
                    print('')
            self.runtime = 0
            print('waiting 10 second views result')
            time.sleep(10)
        return "Test End"



url = sys.argv[1]
method = sys.argv[2]
loop = int(sys.argv[3])

func = api(url=url, method=method, loop=loop)
print(func.main())

