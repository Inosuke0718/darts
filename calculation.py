import cv2
import time
# import numpy as np
# for playing effect sound
from playsound import playsound
bullRange = 30
secondRange = 30
thirdRange = 60
UploadPath = "C:\\Users\\ino\\Desktop\\"
mode = None

def main():
    if (mode == 'video'):
        filepath = "C:\\Users\\ino\\Desktop\\20221030_152351.mp4"
        cap = cv2.VideoCapture(filepath)
    else:
        cap = cv2.VideoCapture(0)

    # 解像度変更
    fps = round(cap.get(cv2.CAP_PROP_FPS))

    avg = None
    # detectFlg = False

    #画像サイズ取得し、Centerを割り出す
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    centerX = round(width/2)
    centerY = round(height/2)

    # debug
    print(fps)

    secCnt = 0
    # 1フレームずつ取得する。
    while True:
        # 何度も音がなるので、初期検出から１秒間は何もしない
        ret, frame = cap.read()

        # 円の描画
        cv2.circle(frame, (centerX, centerY), bullRange, (0, 255, 0), 1, cv2.LINE_4, 0)
        cv2.circle(frame, (centerX, centerY), secondRange, (0, 255, 0), 1, cv2.LINE_4, 0)
        cv2.circle(frame, (centerX, centerY), thirdRange, (0, 255, 0), 1, cv2.LINE_4, 0)
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
        # accumulateWeighted関数の第三引数は「どれくらいの早さで以前の画像を忘れるか」。小さければ小さいほど「最新の画像」を重視する。
        cv2.accumulateWeighted(blur, avg, 0.8)
        frameDelta = cv2.absdiff(blur, cv2.convertScaleAbs(avg))
        # デルタ画像を閾値処理を行う（閾値を設定し、フレームを2値化）
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        # 画像の閾値に輪郭線を入れる
        # contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        # 面積が閾値未満の輪郭の削除する
        contours = list(filter(lambda x: cv2.contourArea(x) >= 200, contours))

        # 輪郭を「ある程度以上の大きさのものだけ」に絞り込み
        maxY = 0

        for i in range(0, len(contours)):
            if len(contours[i]) > 0:
                # しきい値より小さい領域は無視する
                if cv2.contourArea(contours[i]) < 200:
                    continue

                # 下から見下ろす感じで取ることを想定、変化があった座標の中で、一番下の座標が得点となる
                for contour in contours[i]:
                    for index in contour:
                        if (maxY < index[1]):
                            maxX = index[0]
                            maxY = index[1]
                ret = detectPoint(centerX, centerY, maxX, maxY)
                if (ret > 0):
                    # frame_Num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    # print(frame_Num)
                    # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_Num + fps * 20)
                    avg = None
                    time.sleep(1)
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

def detectPoint(centerX, centerY, maxX, maxY):
    if (centerX - bullRange <= maxX < centerX + bullRange
        and centerY - bullRange <= maxY < centerY + bullRange) :
        print('50point')
        playsound("sounds/重いパンチ1.mp3")
        ret = 50
    elif (centerX - secondRange <= maxX < centerX + secondRange
        and centerY - secondRange <= maxY < centerY + secondRange) :
        print('25point')
        playsound("sounds/軽いキック1.mp3")
        ret = 25
    elif (centerX - thirdRange <= maxX < centerX + thirdRange
        and centerY - thirdRange <= maxY < centerY + thirdRange) :
        print('10point')
        playsound("sounds/軽いパンチ1.mp3")
        ret = 10
    else:
        ret = 0
    return ret

if __name__ == '__main__':
    main()
