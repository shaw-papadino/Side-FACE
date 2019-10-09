import shutil

def copy_all_img(path):
    """
    交差検証の為に画像ファイルコピーする
    
    これいる？
    """
    filepathP = path + "positiveImage"
    filepathN = path + "negativeImage"
    shutil.copytree(filepathP , path + "Positive")
    shutil.copytree(filepathN , path + "Negative")
