import cv2

# filepath = "sample.mov"
filepath = "C:\\Users\\ino\\Desktop\\20221023_215533.mp4"
UploadPath = "C:\\Users\\ino\\Desktop\\test.jpg"
# cap = cv2.VideoCapture(filepath)
cap = cv2.VideoCapture(0)
avg = None

while True:
    # 1フレームずつ取得する。
    ret, frame = cap.read()
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
    cv2.accumulateWeighted(blur, avg, 0.7)
    frameDelta = cv2.absdiff(blur, cv2.convertScaleAbs(avg))
    # デルタ画像を閾値処理を行う
    thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
    # 画像の閾値に輪郭線を入れる
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    maxY = 0


    cv2.circle(frame, (211, 101), 10, (0, 255, 0), 1, cv2.LINE_4, 0)
    for i in range(0, len(contours)):
        if len(contours[i]) > 0:
            # しきい値より小さい領域は無視する
            if cv2.contourArea(contours[i]) < 100:
                continue
            # 面積が閾値未満の輪郭の削除する
            # todo 使えそう
            # contours2 = list(filter(lambda x: cv2.contourArea(x) >= 5000, contours))
            print(i)
            print(contours[i][0])
            print(contours[i][1])
            print(contours[i][0][0])
            print(contours[i][0][0][1])
            
            for contour in contours[i]:
                for index in contour:
                    if (maxY < index[1]):
                        maxX = index[0]
                        maxY = index[1]
            
            if (100 <= maxY < 120) :
                print('120point')


            # 短形で領域を囲む
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)
            # 長方形の描画
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
            # cv2.circle(frame, (x, y), 60, (0, 255, 0), 1, cv2.LINE_4, 0)
            
            # frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    # 結果を出力

    cv2.imshow("Frame", frame)
    # Escキーで終わる
    key = cv2.waitKey(30)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()