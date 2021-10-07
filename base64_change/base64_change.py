import os
import base64

def base64_func():
    input_path = "./"
    all_file_list = os.listdir(input_path)
    print("all_file_list: ", all_file_list)
    base64_array = []
    for file in all_file_list:
        if file.endswith(".dcm"):
            img_name = os.path.splitext(file)[0]
            with open(input_path + "/" + img_name +'.dcm', "rb") as image_file:
                data = base64.b64encode(image_file.read())
                f = open(input_path + '/' + img_name+'.txt', 'w')
                f.write(data.decode("utf-8"))
                f.close()
    return "OK"

def test():
    return "Hello World"
