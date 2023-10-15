from PIL import ImageFont, Image, ImageDraw
import numpy as np
import cv2 as cv


def show_logo():
    print("""
   ##  #     ##       ###    ##  ##      ##    ##  ## 
  ### ##     ##      ## ##   ##  ##     ###    ##  ## 
  ## ##      ##     ##       ##  ##    ## ##   ### ## 
 ####       ##      ##      #######   ##  ##   ###### 
 ####       ##      ##      ##  ##   #######  ##  ##  
##  ##      ##      ##  ##  ##  ##   ##   ##  ##  ##  
##   ##     ##       ####   ##  ##   ##   ##  ##  ##  



[가위바위보] : 모델 로딩중
""")

def show_title_pil(text, color, img_):
    global width, height

    font_title = ImageFont.truetype("./font/Pretendard-Regular.otf", 40)
    BOX_PADDING = 5

    img_np = np.array(img_)
    img_pil = Image.fromarray(img_np) # numpy를 PIL 이미지로 변경

    draw = ImageDraw.Draw(img_pil) # 이미지에 글씨를 쓸 객체

    x1, y1, x2, y2 = draw.textbbox((50, 50), text, font_title)
    size_width, size_height = x2 - x1, y2 - y1

    box_width = size_width + 10
    box_height = size_height + 10

    box_x = (img_.shape[1] - box_width) // 2
    box_y = (img_.shape[0] - box_height) // 2

    draw.rectangle(
        [(box_x - BOX_PADDING, box_y - BOX_PADDING),
         (box_x + size_width + BOX_PADDING, box_y + size_height + BOX_PADDING + 5)
         ],
        (255, 255, 255)
    )

    draw.text((box_x, box_y), text, color, font_title)


    return np.array(img_pil)

def show_header_pil(text, img_):
    BOX_PADDING = 5
    font_header = ImageFont.truetype("./font/Pretendard-Regular.otf", 30)

    img_np = np.array(img_)
    img_pil = Image.fromarray(img_np) # numpy를 PIL 이미지로 변경

    draw = ImageDraw.Draw(img_pil) # 이미지에 글씨를 쓸 객체

    x1, y1, x2, y2 = draw.textbbox((5, 5), text, font_header)
    size_width, size_height = x2 - x1, y2 - y1

    box_width = size_width + 10
    box_height = size_height + 10


    draw.rectangle(
        [8, 10, BOX_PADDING + box_width, BOX_PADDING + box_height],
        (255, 255, 255)
    )
    draw.text((10, 10), text, (0, 0, 255), font_header)

    return np.array(img_pil)


if __name__ == '__main__':
    cam = cv.VideoCapture(0)
    cv.namedWindow("webcam", cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("webcam", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

    while True:
        sucess, img = cam.read()

        img = cv.flip(img, 1)

        if(not sucess):
            continue

        img = show_header_pil("안녕", img)

        cv.imshow("webcam", img)

        if cv.waitKey(1) & 0xff == 27:  # esc키 누르면 종료
            exit(0)