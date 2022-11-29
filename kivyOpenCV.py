from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import datetime
import calcDarts as cd

# アプリの定義
class MainApp(MDApp):
    # ビルド時に呼ばれる(constructor)
    def build(self):
        # レイアウトの生成
        layout = MDBoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.save_img_button = MDRaisedButton(
            text='CLICK HERE!',
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None))
        self.save_img_button.bind(on_press=self.take_picture)
        layout.add_widget(self.save_img_button)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        # Frame initilize
        self.image_frame = frame

        # selfはメンバ変数的な感じだと思われ
        #画像サイズ取得し、Centerを割り出す
        height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        centerX = round(width/2)
        centerY = round(height/2)

        cd.calcDarts(centerX, centerY, ret, frame)

        buffer = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        self.image.texture = texture

    def take_picture(self, *args):
        dt_now = datetime.datetime.now()
        image_name = dt_now.strftime('%Y%m%d%H%M%S')+".jpg"
        cv2.imwrite(image_name, self.image_frame)

if __name__ == '__main__':
    MainApp().run()