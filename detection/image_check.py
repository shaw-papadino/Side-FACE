import os

class Checker():

    def img_size(self, num):
        try:
            if isinstance(num, int):
                return num
            elif isinstance(num, float):
                return int(num)
            elif num.isdecimal():
                return int(num)

        except ValueError:
            print("Wはintで指定してください。")

    def store_path(self, path):

        if not os.path.isdir(path):
            return False
        else:
            return True
