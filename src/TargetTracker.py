import cv2
import numpy as np
class TargetTracker:
    def __init__(self):
        #初始化orbb特征检测器
        self.SIFT = cv2.SIFT.create(nfeatures=1000)
        #FlANN参数
        index_params = dict(algorithm=1,  # FLANN_INDEX_LSH
                            table_number=6,  # 12)
                            key_size=12,  # 20)
                            multi_probe_level=1)  # 2)
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        self.target_kp = None
        self.target_des = None
        self.target_shape = None

    #设置目标图像
    def set_target(self, flame,bbox):
        flame_gray = cv2.cvtColor(flame, cv2.COLOR_BGR2GRAY)
        x,y,w,h = map(int, bbox)
        print(f"Selected ROI: x={x}, y={y}, w={w}, h={h}")
        self.target_shape = (h,w)
        target_roi = flame_gray[y:y+h, x:x+w]
        self.target_kp, self.target_des = self.SIFT.detectAndCompute(target_roi, None)
        # 检查特征提取结果
        if self.target_kp is None or self.target_des is None:
            print("Error: No features extracted from ROI!")
            return False
    
        print(f"Successfully extracted {len(self.target_kp)} keypoints")
        return target_roi, self.target_kp, self.target_des

    #在新图像中匹配目标特征
    def match_features(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.target_des is None:
            print("Target not set. Call set_target() first.")
            return None, None
        kp, des = self.SIFT.detectAndCompute(frame_gray, None)
        if des is not None and len(des) >= 2:
            matches = self.flann.knnMatch(self.target_des, des, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < 0.85 * n.distance:
                    good_matches.append(m)
        if len(good_matches) > 4:
            #获取匹配点坐标
            src_pts = np.float32([self.target_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            #计算单应性矩阵
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            matches_mask = mask.ravel().tolist()
            h, w = self.target_shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            if M is not None:
                dst = cv2.perspectiveTransform(pts, M)
                return dst, matches_mask
        return None, None

#测试 main函数
#读取两张图片对比
if __name__ == "__main__":
    tracker = TargetTracker()
    img1 = cv2.imread(r'F:\opencvTest\image\car.png')
    img2 = cv2.imread(r'F:\opencvTest\image\car.png')
    # img1 = cv2.resize(img1, fx=2, fy=2, dsize=None)
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    img1 = cv2.filter2D(img1, -1, kernel)
    #鼠标选取目标区域
    bbox = cv2.selectROI("Select Target", img1, False, False)
    target_roi, target_kp, target_des = tracker.set_target(img1, bbox)
    print(f"Target Keypoints: {len(target_kp)}")
    dst, matches_mask = tracker.match_features(img2)
    print(f'dst: {dst}')
    if dst is not None:
        # img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Matched Result', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No sufficient matches found.")

