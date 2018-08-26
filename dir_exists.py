# -*- coding: utf-8 -*-
import os

def dir_exists(path, *args):
      """ディレクトリ存在確認する関数"""
      filepath_list = []
      for dir0 in args:
          for i in ["P_P_", "N_P_"]:
              filepath = path + i + dir0
              if not os.path.exists(filepath):
                      os.mkdir(filepath)
              filepath_list.append(filepath)
      return filepath_list

if __name__ == "__main__":
    pass

"""
    dir_exist("/Users/okayamashoya/", "shom", "shoyam")
"""
