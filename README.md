# OpenCVを用いたダーツの刺さった場所検知

# 概要
ダーツボードに扮したクッションの中心にカメラをセットします。
<img src="img\darts2.jpg" width="500px">

クションの中心にダーツが当たると音の再生と得点を表示を行います。
<img src="img\darts1.gif" width="500px">
## 作成の経緯
ひょんなことから作成してみました。
1. 足の骨折を機にダーツにはまる。
2. 家でもダーツをしたくなる。
3. うるさいとの理由で妻からのダーツボード設置許可がおりない。
4. ダーツボード代わりにクッション壁に貼り付けてダーツを投げ始める。
5. クッションではダーツが刺さらないので、ダーツが真ん中に刺さったどうかを検知したくなる。

# 仕組み
ざっくりと説明すると、読み込まれた動画の最新フレームと少し前のフレームを比較します。
比較はブル（ダーツの真ん中）の範囲で行われます。その範囲で設定した閾値以上の変化があれば、得点（ブルに入った）とみなしています。
## 比較用のフレームを取得
aveにフレームを代入した後にcontinueしてループを抜けるので、aveには少し前のフレームの情報が入ることになります。
```
        if avg is None:
            avg = gray.copy().astype("float")
            continue
```
## 現在のフレームと移動平均との差を計算
最新のフレームblurと少し前のフレームaveを比較します。
```
        # accumulateWeighted関数の第三引数は「どれくらいの早さで以前の画像を忘れるか」。小さければ小さいほど「最新の画像」を重視する。
        cv2.accumulateWeighted(blur, avg, 0.8)
        frameDelta = cv2.absdiff(blur, cv2.convertScaleAbs(avg))
        # デルタ画像を閾値処理を行う（閾値を設定し、フレームを2値化）
```
## 指定の範囲で閾値以上の変化があるかどうか確認
比較した結果が指定した閾値よりも大きければ、次に指定の範囲でその結果（フレームの差）があったのかどうかを確認します。
範囲内でのフレーム差であれば、得点とし音の再生と得点を表示を行います。
```
for i in range(0, len(contours)):
            if len(contours[i]) > 0:
                # しきい値より小さい領域は無視する
                if cv2.contourArea(contours[i]) < 300:
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
```

## 環境
- windows10
- Python 3.10.8
- OpenCV 4.6.0
