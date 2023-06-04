# 함수: 객체의 위치와 방향 계산
import cv2
import numpy as np

def calculate_position_orientation(objpoints, rvecs, tvecs):
    positions = []    # 객체 위치
    orientations = [] # 객체 방향

    for i in range(len(objpoints)):
        objp = objpoints[i]  # 3D 객체 특징점
        rvec = rvecs[i]      # 회전 벡터
        tvec = tvecs[i]      # 변위 벡터

        # 회전 벡터를 회전 행렬로 변환
        R, _ = cv2.Rodrigues(rvec)

        # 카메라 좌표계에서 객체 좌표계로 변환
        T = np.concatenate((R, tvec), axis=1)

        # 객체 좌표계에서 원점의 위치 계산
        position = -np.linalg.inv(R) @ tvec
        positions.append(position.flatten())

        # 객체 방향 계산 (Z축을 따라 회전하는 각도)
        orientation = np.arctan2(R[1, 0], R[0, 0])
        orientations.append(orientation)

    return positions, orientations