import cv2

# #画像をグレースケールで読み込む
# img = cv2.imread("splatoonimage.png", 0)
# temp = cv2.imread("template.png", 0)
# #マッチングテンプレートを実行
# #比較方法はcv2.TM_CCOEFF_NORMEDを選択
# result = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)

# #検出結果から検出領域の位置を取得
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# top_left = max_loc
# w, h = temp.shape[::-1]
# bottom_right = (top_left[0] + w, top_left[1] + h)

# #検出領域を四角で囲んで保存
# result = cv2.imread("splatoonimage.png")
# cv2.rectangle(result,top_left, bottom_right, (255, 0, 0), 2)
# cv2.imwrite("result.png", result)

# opencvのmachiTemplateで画像比較
def match(img_gray , temp):
#比較方法はcv2.TM_CCOEFF_NORMEDを選択
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    #結果のmax_valが欲しい　0-1 1に近いほど似てる
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return (max_val)

#ここから
video = cv2.VideoCapture("C:\\Users\\ino/\\\Desktop\\20230109_203519.mp4")
templateDead = cv2.imread("C:\\Users\\ino\\Desktop\\template.PNG")
frame_count = int(video.get(7)) #フレーム数を取得
frame_rate = int(video.get(5)) #フレームレート(1フレームの時間単位はミリ秒)の取得 splatoon2は60
deadTime = 0 # 前回のチェックとの比較時間用。近いフレームは無視するようにする
dead = [] # 取得タイミングをリストに入れる。秒単位
n=3 #n秒ごと

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

for i in range(int((frame_count / frame_rate)/n)): #動画の秒数を取得し、回す
    video.set(1 ,frame_rate * n * i)
    _, frame = video.read() #動画をフレームに読み込み
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #比較用にグレー画像を作る
    # checkVal = match(framegray,templateStart) #関数呼び出し

    if match(framegray,templateDead) > 0.7 and deadTime < (i-1) *n - 10 :
        deadTime = (i-1) * (n)
        print ("deadTime : "+str(deadTime))
        dead.append(deadTime)

if len(dead)>0 :
    #動画作成
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    newVideo = cv2.VideoWriter('C:\\Users\\ino\\\Desktop\\deadonlyvideo.mp4', fourcc, frame_rate, (width, height))

    for i in dead:
        sFrame = i * frame_rate - frame_rate * 1 #n秒前
        eFrame = i * frame_rate + frame_rate * 10
        video.set(1 ,sFrame)
        for no in range(sFrame,eFrame):
            _, frame = video.read()
            # newVideo.write(frame)
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            newVideo.write(frame)