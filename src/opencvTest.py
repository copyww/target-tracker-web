# -*- coding: gbk -*-
import cv2
import numpy as np
from TargetTracker import TargetTracker

# 按键定义
key_esc = 27
key_space = 32

class HybridTracker:
    def __init__(self):
        self.tracker = None
        self.detector = TargetTracker()
        self.tracking = False
        self.lost_count = 0
        self.max_lost_frames = 1  # 连续跟丢多少帧后完全停止
        self.current_roi = (0, 0, 0, 0)
        self.model_frame = None
        self.frame_count = 0
        self.detection_interval = 30  # 每30帧自动检测一次
        self.auto_detection_mode = True  # 自动检测模式
        
    def initialize_tracker(self, frame, bbox):
        """初始化跟踪器"""
        self.tracker = cv2.TrackerCSRT.create()
        self.tracker.init(frame,bbox)
        
        # print(f"Tracker init success: {success}")
        
        self.tracking = True
        self.lost_count = 0
        self.frame_count = 0
        self.current_roi = bbox
        self.model_frame = frame.copy()
        # 设置检测器的目标特征
        self.detector.set_target(frame, bbox)
        print(f"Tracker initialized with ROI: {bbox}")
        return True
    
    def update(self, frame):
        """更新跟踪状态"""
        if not self.tracking:
            return False, None
            
        # 更新跟踪器
        success, bbox = self.tracker.update(frame)
        
        if success:
            self.lost_count = 0
            self.frame_count += 1
            return True, bbox
        else:
            self.lost_count += 1
            self.frame_count += 1
            print(f"Tracking lost! Lost count: {self.lost_count}")
            
            # 如果连续跟丢多帧，完全停止跟踪
            if self.lost_count >= self.max_lost_frames:
                self.tracking = False
                print("Tracking completely lost. Waiting for auto re-detection...")
            
            return False, None
    
    def auto_re_detect(self, frame):
        """自动重新检测目标"""
        print("Auto re-detection in progress...")
        result = self.detector.match_features(frame)
        
        if result is not None:
            dst, matches_mask = result
            if dst is not None:
                # 计算新的bbox
                dst_points = dst.reshape(4, 2)
                x = int(np.min(dst_points[:, 0]))
                y = int(np.min(dst_points[:, 1]))
                w = int(np.max(dst_points[:, 0]) - x)
                h = int(np.max(dst_points[:, 1]) - y)

                #如果新bbox太小或超出边界则忽略
                if  x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
                    print("Auto re-detected bbox is invalid, ignoring.")
                    return False, None
                
                new_bbox = (x, y, w, h)
                print(f"Auto re-detected target at: {new_bbox}")
                
                # 重新初始化跟踪器
                if self.initialize_tracker(frame, new_bbox):
                    return True, new_bbox
        
        print("Auto re-detection failed")
        return False, None
    
    def should_auto_detect(self):
        """判断是否应该进行自动检测"""
        if not self.auto_detection_mode:
            return False
            
        # 如果跟踪完全丢失，定期尝试重新检测
        if not self.tracking:
            return self.frame_count % 15 == 0  # 每15帧尝试一次
        
        # 如果正在跟踪，定期进行验证性检测（防止漂移）
        return self.frame_count % self.detection_interval == 0

def videoPlay():
    # global pause
    tracker = HybridTracker()
    pause = False
    
    vc = cv2.VideoCapture(r"F:\opencvTest\video\车.mp4")
    if not vc.isOpened():
        print("Video not found")
        exit()

    while True:
        if not pause:
            open, frame = vc.read()
            # print(f'tracking: {tracker.tracking}, lost_count: {tracker.lost_count}')
            if not open:
                break
            if frame is None:
                break
            
            display_frame = frame.copy()
            status_text = ""
            status_color = (0, 0, 0)
            
            if tracker.tracking:
                # 正常跟踪模式
                success, bbox = tracker.update(frame)
                # print(f"Update success: {success}, bbox: {bbox}")
                
                if success:
                    # 绘制跟踪框
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(display_frame, p1, p2, (0, 255, 0), 2, 1)
                    status_text = "Tracking"
                    status_color = (0, 255, 0)
                else:
                    # 跟踪失败
                    status_text = f"Tracking lost ({tracker.lost_count}/{tracker.max_lost_frames})"
                    status_color = (0, 0, 255)
            else:
                # 完全停止状态
                status_text = "Tracker stopped - Auto detecting..."
                status_color = (0, 0, 255)
            
            # 自动检测逻辑
            # print(tracker.should_auto_detect())
            if tracker.should_auto_detect():
                # print(f'trackering: {tracker.tracking}, frame_count: {tracker.frame_count}')
                if  tracker.tracking:
                    # 尝试重新检测
                    success, bbox = tracker.auto_re_detect(frame)
                    if success:
                        # 绘制重新检测到的目标
                        p1 = (int(bbox[0]), int(bbox[1]))
                        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                        cv2.rectangle(display_frame, p1, p2, (255, 0, 0), 2, 1)
                        # status_text = "Auto re-detected!"
                        # status_color = (255, 0, 0)
                        print("Auto re-detection successful!")
            
            # 显示状态信息
            cv2.putText(display_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # 显示帧计数和检测信息
            info_text = f"Frame: {tracker.frame_count}, AutoDetect: {'ON' if tracker.auto_detection_mode else 'OFF'}"
            cv2.putText(display_frame, info_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            if not tracker.tracking:
                next_detect = 15 - (tracker.frame_count % 15)
                detect_text = f"Next auto detect in: {next_detect} frames"
                cv2.putText(display_frame, detect_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            cv2.imshow('video', display_frame)

        # 键盘控制
        key = cv2.waitKeyEx(30) & 0xff
        
        if key == key_esc:
            break
        elif key == key_space:
            pause = not pause
            print("Pause:", pause)
        elif key == ord('s'):  # 选择新目标
            pause = True
            roi = cv2.selectROI('video', frame, False, False)
            if roi != (0, 0, 0, 0):
                tracker.initialize_tracker(frame, roi)
            pause = False
        elif key == ord('a'):  # 切换自动检测模式
            tracker.auto_detection_mode = not tracker.auto_detection_mode
            mode = "ON" if tracker.auto_detection_mode else "OFF"
            print(f"Auto detection mode: {mode}")
        elif key == ord('r'):  # 手动触发重新检测
            if not tracker.tracking:
                success, bbox = tracker.auto_re_detect(frame)
                if success:
                    print("Manual re-detection successful!")
                else:
                    print("Manual re-detection failed")

    vc.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    videoPlay()