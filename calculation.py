import cv2
# import numpy as np
# for playing effect sound
from playsound import playsound

# filepath = "sample.mov"
filepath = "C:\\Users\\ino\\Desktop\\20221030_152351.mp4"
# filepath = "C:\\Users\\ino\\Desktop\\20221023_215533.mp4"
UploadPath = "C:\\Users\\ino\\Desktop\\test.jpg"
# cap = cv2.VideoCapture(filepath)
cap = cv2.VideoCapture(1)
# 解像度変更
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
fps = round(cap.get(cv2.CAP_PROP_FPS))

avg = None
detectFlg = False

#画像サイズ取得し、Centerを割り出す
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
centerX = round(width/2)
centerY = round(height/2)

# debug
print(height)
print(width)
print(cap.get(cv2.CAP_PROP_FPS))


secCnt = 0
while True:
    # 何度も音がなるので、初期検出から１秒間は何もしない
    if detectFlg and secCnt >= fps:
        detectFlg = False
    if detectFlg:
        secCnt += 1
        continue
    # 1フレームずつ取得する。
    ret, frame = cap.read()

    cv2.circle(frame, (centerX, centerY), 15, (0, 255, 0), 1, cv2.LINE_4, 0)
    cv2.circle(frame, (centerX, centerY), 135, (0, 255, 0), 1, cv2.LINE_4, 0)

    if not ret:
        break
    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 比較用のフレームを取得する
    if avg is None:
        avg = gray.copy().astype("float")
        continue

    # ブラーを掛けてノイズを軽減する
    blur = cv2.GaussianBlur(gray, (1, 1), 1)
    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(blur, avg, 0.8)
    frameDelta = cv2.absdiff(blur, cv2.convertScaleAbs(avg))
    # デルタ画像を閾値処理を行う
    thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
    # 画像の閾値に輪郭線を入れる
    # contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    # 面積が閾値未満の輪郭の削除する
    contours = list(filter(lambda x: cv2.contourArea(x) >= 200, contours))
    maxY = 0

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:
            # しきい値より小さい領域は無視する
            if cv2.contourArea(contours[i]) <200:
                continue

            # 下から見下ろす感じで取ることを想定、変化があった座標の中で、一番下の座標が得点となる
            for contour in contours[i]:
                for index in contour:
                    if (maxY < index[1]):
                        maxX = index[0]
                        maxY = index[1]
            # bull
            # todo 関数化
            bullRange = 15
            if (centerX - bullRange <= maxX < centerX + bullRange
                and centerY - bullRange <= maxY < centerY + bullRange) :
                print('50oint')
                playsound("sounds/和太鼓でドン.mp3")
                detectFlg = True
                break


            # 短形で領域を囲む
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)

            # ささったDarts描画
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            # cv2.circle(frame, (x, y), 60, (0, 255, 0), 1, cv2.LINE_4, 0)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    # 結果を出力
    cv2.imshow("Frame", frame)
    # Escキーで終わる
    key = cv2.waitKey(30)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()