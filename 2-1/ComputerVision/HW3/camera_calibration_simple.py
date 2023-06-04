# pip install opencv-contrib-python
import cv2
import numpy as np
from functions import calculate_position_orientation
# my cv version is 4.7.0
np.set_printoptions(precision=2, suppress=True)

# input: 사용된 calibration pattern 정보, 촬영된 calibration pattern 사진
wp = 6        # calibration pattern 가로점 수
hp = 6        # calibration pattern 세로점 수
length = 14   # calibration pattern 한 변 길이
directory = '/home/dgist/2-1/ComputerVision/HW3/images/'
imageExtension = '.jpeg'  # 파일 확장자
startImageNum = 0  # 읽기 시작하는 사진 번호
endImageNum = 5   # 읽기를 끝내는 사진 번호 + 1

objp = np.zeros((wp*hp, 3), np.float32)              # 가상의 3차원 공간에서 calibration pattern의 특징점 위치 (추후 2차원 사진 정보와 매칭됨)
objp[:, :2] = np.mgrid[0:wp, 0:hp].T.reshape(-1, 2)  # mgrid 사용하여 값 대입 (0, 0, 0) (1, 0, 0) ... (6, 7, 0)
objp[:, :2] *= length                                # 실제 크기 대입을 위해 length 곱함

objpoints = []   # 실제 세계에서의 3d 특징점 집합
imgpoints = []   # 촬영된 사진에서 2d 특징점 집합
findImages = []  # calibration pattern이 성공적으로 인식된 사진 번호 집합

print("Start ")
print("===========================================")

for i in range(startImageNum, endImageNum):       
    img = cv2.imread(directory + str(i) + imageExtension)              
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)           
    ret, corners = cv2.findChessboardCorners(gray, (wp, hp), None)  # 사진에서 calibration pattern의 특징점 찾음
    img_shape = gray.shape[::-1]  # 사진의 가로 및 세로 화소 크기

    # 특징점이 사진에서 찾아진 경우
    if ret == True:
        print(f'{i}번째 이미지에서 calibration pattern 특징점 인식 성공')
        objpoints.append(objp)     # 집합에 3d정보 추가
        imgpoints.append(corners)  # 집합에 2d정보 추가
        findImages.append(i)       # 집합에 특징점 찾아진 사진 번호 추가
             
    # 특징점을 사진에서 찾지 못한 경우
    else:
        print(f'{i}번째 이미지에서 calibration pattern 특징점 인식 실패')

print("Recognization Done")
print("Do camera calibration")
print("===========================================")
    
# camera calibration 수행
# M: intrinsic parameter, D: distortion parameter
# rvecs: camera와 calibration pattern의 좌표계 사이 rotation 정보
# rvecs: camera와 calibration pattern의 좌표계 사이 translation 정보
# rt: reprojection error,
rt, M, D, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_shape, None, None)

print(f'Intrinsic matrix M:\n{M}')
print("===========================================")
print("Saving...")
np.savetxt(directory + "\Cal_intrinsic.txt", M, fmt='%.2f')  # intrinsic matrix 저장
print("Done")
print("===========================================")

# 외부 파라미터는 패턴 또는 카메라가 움직일 때 마다 변경, 내부 파라미터는 카메라 내부 특성으로 고정
W = np.full((3,4),0.0)
R = np.full((3,3),0.0)

print("Save Extrinsic matrix...")

for i, no in enumerate(findImages):
    rvec = rvecs[i]
    tvec = tvecs[i]
    
    cv2.Rodrigues(rvec,R)
    W[0:3,0:3] = R
    W[0:3,3:4] = tvec # np.reshape(tvec,(3,1))
    print(f'{no}th Extrinsic matrix W:\n{W}')
    np.savetxt(directory + "\Cal_extrinsic"+str(no)+".txt", W, fmt='%.2f')  # extrinsic matrix 저장

print("Done")
print("===========================================")
print("\n") 
print(f'Distorsion coefficient:\n{D}')
print(f"Reprojection error: {rt}")

print('==============================================')
# 객체의 위치와 방향 계산
positions, orientations = calculate_position_orientation(objpoints, rvecs, tvecs)

# 결과 출력 및 저장
for i, (position, orientation) in enumerate(zip(positions, orientations)):
    print(f"{findImages[i]}th Object Position: {position}")
    print(f"{findImages[i]}th Object Orientation: {orientation}")

    # 위치와 방향 저장
    np.savetxt(directory + f"/Object_position_{findImages[i]}.txt", position, fmt="%.2f")
    np.savetxt(directory + f"/Object_orientation_{findImages[i]}.txt", [orientation], fmt="%.2f")

print("Done")
print("Calculate coordinate")
print("=================================")

M = np.loadtxt("/home/dgist/2-1/ComputerVision/HW3/images/\Cal_intrinsic.txt")
inv_M = np.linalg.inv(M)

# 이미지 픽셀 좌표 (x, y)
pixel_x = 1000
pixel_y = 2000

# 이미지 픽셀 좌표를 이미지 평면 좌표로 변환
image_coordinates = np.array([pixel_x, pixel_y, 1])

# 이미지 평면 좌표를 실제 3D 공간 좌표로 변환
world_coordinates = inv_M.dot(image_coordinates)

# 결과 출력
print("Image Pixel Coordinates:", image_coordinates[:2])
print("World 3D Coordinates:", world_coordinates)
print("Done")

print("Calculate accuracy")
print("=================================")

# Measure accuracy in terms of relative position and orientation
ground_truth_positions = world_coordinates  # List of ground truth positions
ground_truth_orientations = [...]  # List of ground truth orientations

position_errors = []
orientation_errors = []

for i, (position, orientation) in enumerate(zip(positions, orientations)):
    ground_truth_position = ground_truth_positions[i]
    # ground_truth_orientation = ground_truth_orientations[i]

    # Calculate position error as Euclidean distance
    position_error = np.linalg.norm((position - ground_truth_position) / position * 100)
    position_errors.append(position_error)

    # # Calculate orientation error as absolute angular difference
    # orientation_error = np.abs(orientation - ground_truth_orientation)
    # orientation_errors.append(orientation_error)

    print(f"W{i}'s position error : {position_errors[i]}")
    print("\n")

# Calculate average errors
avg_position_error = np.mean(position_errors)
avg_orientation_error = np.mean(orientation_errors)

# Print accuracy results
print("=====================================================")

print(f"약 10cm는 {positions[0] - positions[2]}")

print("Accuracy Metrics:")
print(f"Average Position Error: {avg_position_error}")
print(f"Average Orientation Error: {avg_orientation_error}")