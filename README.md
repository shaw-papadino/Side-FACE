# Smile-Camera_v2
Smile-camera_v2

肩乗り型ロボットから真横笑顔を識別する,その時の周囲状況を記録するためのプログラム
    - todo:CNNモデルを追記
    - todo:

1. demoディレクトリにUSBカメラとラズパイカメラが接続されたRaspberryPiを用いて、同時に動画撮影を行うプログラムがあります。
    1. OUTPUT1 -> 
        1. 横顔動画  
        1. 周囲状況動画

1. ffmpegで[o1-1]を、フレーム毎に画像として保存する
    1. OUTPUT2 -> 
        1. 横顔画像

1. アノテーションツールを用いて、[o2]の笑顔部分にバウンディングボックスを付け記録
    1. OUTPUT3 -> 
        1. positive.dat(ファイル名とバウンディングボックスの座標)  
        1. negative.dat(ファイル名)  
    ※のちにサンプルとして追加予定
             
1. positive画像にData augmentationを行い、増やした画像を[o3-1]に追記

1. opencv_createsample, opencv_traincascadeで識別器作成
    1. OUTPUT -> - models/side_smile_default_ver1.xml
        1. adaboost
        1. 59813枚を2分割交差検証*10回
        1. 再現率89.8%
        1. 適合率70.9%  
    ※CNNモデルも追加予定
            
1. detection/side_smile.pyで識別を行う

1. detection/cut_video.pyで笑顔区間を算出し、[o1-2]から切り取り保存を行う。
