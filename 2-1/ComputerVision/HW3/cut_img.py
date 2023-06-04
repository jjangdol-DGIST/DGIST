from PIL import Image
import matplotlib.pyplot as plt

def crop_image(image_path, x, y, width, height, output_path):
    # 이미지 파일 열기
    image = Image.open(image_path)
    
    # 이미지 crop
    cropped_image = image.crop((x, y, x + width, y + height))
    
    # crop된 이미지 저장
    cropped_image.save(output_path)
    
    print(f"이미지가 성공적으로 잘려진 후 저장되었습니다: {output_path}")

# crop할 이미지 파일 경로 지정
directory = '/home/dgist/2-1/ComputerVision/HW3/images/'

# 이미지 crop 함수 호출
# crop_image(image_path, x, y, width, height, output_path)
for n in range(1, 6):
    image = Image.open(directory+f'{n}.jpg')
    cropimg = image.crop((0, 250, 2000, 2000))
    cropimg.save(directory+f'crop{n}.jpg')

plt.imshow(cropimg)
plt.show()