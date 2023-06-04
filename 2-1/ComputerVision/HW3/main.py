# pip install opencv-contrib-python
import cv2
import numpy as np
import math
# from functions import calculate_position_orientation

# my cv version is 4.7.0

# 이동거리 계산 함수
def calculate_distance(position):
    return np.linalg.norm(position)

# 이동거리 오차 계산 함수
def calculate_distance_error(position, actual_distance):
    actual_distance = np.array(actual_distance)
    calculated_distance = calculate_distance(position)
    error = np.linalg.norm(calculated_distance - actual_distance)
    return error

# 라디안 값을 각도로 변환
def radians_to_degrees(angles):
    degrees = []
    for angle in angles:
        degrees.append(tuple(math.degrees(a) for a in angle))
    return degrees

# 물체의 각도 계산
def calculate_orientation(rvecs):
    orientations = []

    for rvec in rvecs:
        # 회전 매개 변수(rvecs)를 회전 행렬로 변환
        R, _ = cv2.Rodrigues(rvec)

        # 회전 행렬을 이용하여 각도 계산
        # 여기에서는 회전 행렬에서 오일러 각으로 변환하는 방식을 사용합니다.
        # 참고: 이 방식은 각도를 제한하지 않으므로 일부 문제가 발생할 수 있습니다.
        # 필요에 따라 다른 방식을 사용하실 수 있습니다.
        pitch = math.asin(R[1, 0])
        roll = math.atan2(-R[1, 2], R[1, 1])
        yaw = math.atan2(-R[2, 0], R[0, 0])

        orientations.append((roll, pitch, yaw))

    return orientations

# 물체의 위치와 각도 측정
def calculate_position_orientation(M, rvecs, tvecs):
    # 카메라의 외부 파라미터를 이용하여 물체의 위치와 각도 계산

    # 카메라의 회전 매개 변수(rvecs)를 회전 행렬로 변환
    R, _ = cv2.Rodrigues(rvecs)

    # 카메라의 위치(tvecs) 계산
    position = -np.matrix(R).T * np.matrix(tvecs)

    # 카메라의 각도 계산
    angles, _ = cv2.Rodrigues(R)

    return position, angles

# 물체의 위치 오차 측정
def calculate_position_error(objpoints, imgpoints, rvecs, tvecs, M, D):
    position_errors = []

    for i in range(len(objpoints)):
        objpoint = objpoints[i]
        imgpoint = imgpoints[i]
        rvec = rvecs[i]
        tvec = tvecs[i]

        # 투영된 이미지 포인트 계산
        imgpoints_proj, _ = cv2.projectPoints(objpoint, rvec, tvec, M, D)

        # 3D 특징점의 위치와 재투영된 2D 이미지 포인트의 위치 비교하여 위치 오차 계산
        error = cv2.norm(objpoint.astype(np.float32), imgpoints_proj, cv2.NORM_L2) / len(objpoint)
        position_errors.append(error)

    return position_errors


np.set_printoptions(precision=2, suppress=True)

# input: 사용된 calibration pattern 정보, 촬영된 calibration pattern 사진
wp = 6        # calibration pattern 가로점 수
hp = 5       # calibration pattern 세로점 수
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

print("===========================================")

print(f'Distorsion coefficient:\n{D}')
print(f"Reprojection error: {rt}")
print("===================================")
print("Calculating position and orientation")

print("=============================================")

# 0번째 사진을 기준으로 나머지 사진들의 이동 거리 계산
real_degrees = [0, 0, 0, 30, 45]
distances = []

for i, no in enumerate(findImages):
    rvec = rvecs[i]
    tvec = tvecs[i]
    orientations = calculate_orientation(rvecs)
    orientations_degrees = radians_to_degrees(orientations)

    position, angles = calculate_position_orientation(M, rvec, tvec)

    if i == 0:
        reference_position = position  # 0번째 사진의 위치를 기준으로 설정
        print(f"{no}th Image - Reference Position: {reference_position.T}")
    if i == 2:
        reference_position2 = position

    # 유클리드 거리 계산
    distance = np.linalg.norm(position - reference_position)
    _calculated_distance = float(distance) / 291 * 10
    distances.append(distance)

    degree = round(abs(orientations_degrees[i][1]), 2)
    real_degree = real_degrees[i]
    
    print(f"{no}th Image - X: {position[0][0]}, Y: {position[1][0]}, Z: {position[2][0]}")
    print(f"{no}th Image - Distance from Reference: about {int(_calculated_distance)}cm")
    print(f"{no}th Image - Orientation (degrees): {degree}°")
    if real_degree == 0:
        print(f"{no}th Image's real degree is 0, and the error is {degree}\n")
    else:
        print(f"{no}th Image - Error rate of degree : {round(abs(real_degree - degree) / degree * 100, 1)}%\n")

print(f"\n약 10cm는 {abs(int(reference_position[0]) - int(reference_position2[0]))}")

# 이동거리 평균 출력
mean_distance = np.mean(distances)
print(f"Mean Distance from Reference: {mean_distance}")

# 오차율 계산
reprojection_errors = []
for i, objpoint in enumerate(objpoints):
    imgpoint = imgpoints[i]

    # 투영된 이미지 포인트 계산
    imgpoints_proj, _ = cv2.projectPoints(objpoint, rvecs[i], tvecs[i], M, D)

    # 재투영 오차 계산
    error = cv2.norm(imgpoint, imgpoints_proj, cv2.NORM_L2) / len(imgpoints_proj)
    reprojection_errors.append(error)
    

mean_error = np.mean(reprojection_errors)

print(f"Mean reprojection error: {mean_error * 100} %") # ?

