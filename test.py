
class D:
    path = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/"
    path_dir = path + "img_croppy/"
    P_N_dir = "P_N_0623/"
    P_P_dir = "P_P_0623/"
    N_P_dir = "N_P_0623/"
    def dir_exist(self):
        for dir0 in [self.P_P_dir, self.N_P_dir]:
            print(dir0)
##            filepath = path_dir + dir0
##            if not os.path.exists(filepath):
##                    os.mkdir(filepath)

d = D()

d.dir_exist()
