# -*- coding: utf-8 -*-
import os
import datetime
def dir_exists(path, flg):
    """ディレクトリ存在確認する関数"""
    filepath_list = []
    dt_now = datetime.datetime.now()

    if flg:
        dir_names = ["T_P_", "F_N_","F_P_", "T_N_"]
    else:
        dir_names = ["T_P_", "T_N_"]

    for i in dir_names:
      filepath = path + i + dt_now.strftime('%Y%m%d%H%M')
      if not os.path.exists(filepath):
              os.mkdir(filepath)
      filepath_list.append(filepath)

    return filepath_list

if __name__ == "__main__":
    pass

"""
    dir_exist("/Users/okayamashoya/", "shom", "shoyam")
"""
