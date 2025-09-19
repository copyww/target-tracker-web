# -*- coding: utf-8 -*-
# import cv2
# import numpy as np
# from TargetTracker import TargetTracker

# # ��������
# key_esc = 27
# key_space = 32

# class HybridTracker:
#     def __init__(self):
#         self.tracker = None
#         self.detector = TargetTracker()
#         self.tracking = False
#         self.lost_count = 0
#         self.max_lost_frames = 1  # ������������֡����ȫֹͣ
#         self.current_roi = (0, 0, 0, 0)
#         self.model_frame = None
#         self.frame_count = 0
#         self.detection_interval = 30  # ÿ30֡�Զ����һ��
#         self.auto_detection_mode = True  # �Զ����ģʽ
        
#     def initialize_tracker(self, frame, bbox):
#         """��ʼ��������"""
#         self.tracker = cv2.TrackerCSRT.create()
#         self.tracker.init(frame,bbox)
        
#         # print(f"Tracker init success: {success}")
        
#         self.tracking = True
#         self.lost_count = 0
#         self.frame_count = 0
#         self.current_roi = bbox
#         self.model_frame = frame.copy()
#         # ���ü������Ŀ������
#         self.detector.set_target(frame, bbox)
#         print(f"Tracker initialized with ROI: {bbox}")
#         return True
    
#     def update(self, frame):
#         """���¸���״̬"""
#         if not self.tracking:
#             return False, None
            
#         # ���¸�����
#         success, bbox = self.tracker.update(frame)
        
#         if success:
#             self.lost_count = 0
#             self.frame_count += 1
#             return True, bbox
#         else:
#             self.lost_count += 1
#             self.frame_count += 1
#             print(f"Tracking lost! Lost count: {self.lost_count}")
            
#             # �������������֡����ȫֹͣ����
#             if self.lost_count >= self.max_lost_frames:
#                 self.tracking = False
#                 print("Tracking completely lost. Waiting for auto re-detection...")
            
#             return False, None
    
#     def auto_re_detect(self, frame):
#         """�Զ����¼��Ŀ��"""
#         print("Auto re-detection in progress...")
#         result = self.detector.match_features(frame)
        
#         if result is not None:
#             dst, matches_mask = result
#             if dst is not None:
#                 # �����µ�bbox
#                 dst_points = dst.reshape(4, 2)
#                 x = int(np.min(dst_points[:, 0]))
#                 y = int(np.min(dst_points[:, 1]))
#                 w = int(np.max(dst_points[:, 0]) - x)
#                 h = int(np.max(dst_points[:, 1]) - y)

#                 #�����bbox̫С�򳬳��߽������
#                 if  x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
#                     print("Auto re-detected bbox is invalid, ignoring.")
#                     return False, None
                
#                 new_bbox = (x, y, w, h)
#                 print(f"Auto re-detected target at: {new_bbox}")
                
#                 # ���³�ʼ��������
#                 if self.initialize_tracker(frame, new_bbox):
#                     return True, new_bbox
        
#         print("Auto re-detection failed")
#         return False, None
    
#     def should_auto_detect(self):
#         """�ж��Ƿ�Ӧ�ý����Զ����"""
#         if not self.auto_detection_mode:
#             return False
            
#         # ���������ȫ��ʧ�����ڳ������¼��
#         if not self.tracking:
#             return self.frame_count % 15 == 0  # ÿ15֡����һ��
        
#         # ������ڸ��٣����ڽ�����֤�Լ�⣨��ֹƯ�ƣ�
#         return self.frame_count % self.detection_interval == 0

# def videoPlay():
#     # global pause
#     tracker = HybridTracker()
#     pause = False
    
#     vc = cv2.VideoCapture(r"F:\opencvTest\video\��.mp4")
#     if not vc.isOpened():
#         print("Video not found")
#         exit()

#     while True:
#         if not pause:
#             open, frame = vc.read()
#             # print(f'tracking: {tracker.tracking}, lost_count: {tracker.lost_count}')
#             if not open:
#                 break
#             if frame is None:
#                 break
            
#             display_frame = frame.copy()
#             status_text = ""
#             status_color = (0, 0, 0)
            
#             if tracker.tracking:
#                 # ��������ģʽ
#                 success, bbox = tracker.update(frame)
#                 # print(f"Update success: {success}, bbox: {bbox}")
                
#                 if success:
#                     # ���Ƹ��ٿ�
#                     p1 = (int(bbox[0]), int(bbox[1]))
#                     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#                     cv2.rectangle(display_frame, p1, p2, (0, 255, 0), 2, 1)
#                     status_text = "Tracking"
#                     status_color = (0, 255, 0)
#                 else:
#                     # ����ʧ��
#                     status_text = f"Tracking lost ({tracker.lost_count}/{tracker.max_lost_frames})"
#                     status_color = (0, 0, 255)
#             else:
#                 # ��ȫֹͣ״̬
#                 status_text = "Tracker stopped - Auto detecting..."
#                 status_color = (0, 0, 255)
            
#             # �Զ�����߼�
#             # print(tracker.should_auto_detect())
#             if tracker.should_auto_detect():
#                 # print(f'trackering: {tracker.tracking}, frame_count: {tracker.frame_count}')
#                 if  tracker.tracking:
#                     # �������¼��
#                     success, bbox = tracker.auto_re_detect(frame)
#                     if success:
#                         # �������¼�⵽��Ŀ��
#                         p1 = (int(bbox[0]), int(bbox[1]))
#                         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#                         cv2.rectangle(display_frame, p1, p2, (255, 0, 0), 2, 1)
#                         # status_text = "Auto re-detected!"
#                         # status_color = (255, 0, 0)
#                         print("Auto re-detection successful!")
            
#             # ��ʾ״̬��Ϣ
#             cv2.putText(display_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
#             # ��ʾ֡�����ͼ����Ϣ
#             info_text = f"Frame: {tracker.frame_count}, AutoDetect: {'ON' if tracker.auto_detection_mode else 'OFF'}"
#             cv2.putText(display_frame, info_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
#             if not tracker.tracking:
#                 next_detect = 15 - (tracker.frame_count % 15)
#                 detect_text = f"Next auto detect in: {next_detect} frames"
#                 cv2.putText(display_frame, detect_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

#             cv2.imshow('video', display_frame)

#         # ���̿���
#         key = cv2.waitKeyEx(30) & 0xff
        
#         if key == key_esc:
#             break
#         elif key == key_space:
#             pause = not pause
#             print("Pause:", pause)
#         elif key == ord('s'):  # ѡ����Ŀ��
#             pause = True
#             roi = cv2.selectROI('video', frame, False, False)
#             if roi != (0, 0, 0, 0):
#                 tracker.initialize_tracker(frame, roi)
#             pause = False
#         elif key == ord('a'):  # �л��Զ����ģʽ
#             tracker.auto_detection_mode = not tracker.auto_detection_mode
#             mode = "ON" if tracker.auto_detection_mode else "OFF"
#             print(f"Auto detection mode: {mode}")
#         elif key == ord('r'):  # �ֶ��������¼��
#             if not tracker.tracking:
#                 success, bbox = tracker.auto_re_detect(frame)
#                 if success:
#                     print("Manual re-detection successful!")
#                 else:
#                     print("Manual re-detection failed")

#     vc.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     videoPlay()




# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from TargetTracker import TargetTracker


class HybridTracker:
    def __init__(self, max_templates=5):
        self.tracker = None
        self.detector = TargetTracker()
        self.tracking = False
        self.lost_count = 0
        self.max_lost_frames = 3  # 容忍3帧丢失
        self.current_roi = (0, 0, 0, 0)
        self.model_frame = None
        self.frame_count = 0
        self.detection_interval = 30  # 每30帧尝试自动重检测
        self.auto_detection_mode = True

        # 模板库
        self.template_pool = []      # [(roi_img, bbox), ...]
        self.max_templates = max_templates

    def initialize_tracker(self, frame, bbox):
        """初始化跟踪器"""
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, bbox)
        self.tracking = True
        self.lost_count = 0
        self.frame_count = 0
        self.current_roi = bbox
        self.model_frame = frame.copy()

        # 保存模板
        self.save_template(frame, bbox)

        # 同步 detector
        self.detector.set_target(frame, bbox)
        print(f"[Tracker] 初始化成功 ROI: {bbox}")
        return True

    def save_template(self, frame, bbox):
        """保存当前ROI到模板库"""
        x, y, w, h = map(int, bbox)
        if w <= 0 or h <= 0:
            return
        roi_img = frame[y:y+h, x:x+w].copy()
        self.template_pool.append((roi_img, bbox))
        if len(self.template_pool) > self.max_templates:
            self.template_pool.pop(0)
        print(f"[Tracker] 模板库大小: {len(self.template_pool)}")

    def update(self, frame):
        """更新跟踪"""
        if not self.tracking:
            return False, None

        success, bbox = self.tracker.update(frame)

        if success:
            self.lost_count = 0
            self.frame_count += 1

            # 定期存模板
            if self.frame_count % 50 == 0:
                self.save_template(frame, bbox)

            return True, bbox
        else:
            self.lost_count += 1
            self.frame_count += 1
            print(f"[Tracker] 跟踪失败，lost_count={self.lost_count}")

            if self.lost_count >= self.max_lost_frames:
                self.tracking = False
                print("[Tracker] 完全丢失，等待自动重检测")

            return False, None

    def auto_re_detect(self, frame):
        """用模板库尝试自动找回"""
        print("[Tracker] 开始自动重检测...")
        best_match = None
        best_score = -1

        for tpl_img, tpl_bbox in self.template_pool:
            result = self.detector.match_features(frame, tpl_img)
            if result is not None:
                dst, matches_mask, score = result
                if dst is not None and score > best_score:
                    best_match = dst
                    best_score = score

        if best_match is not None:
            dst_points = best_match.reshape(4, 2)
            x = int(np.min(dst_points[:, 0]))
            y = int(np.min(dst_points[:, 1]))
            w = int(np.max(dst_points[:, 0]) - x)
            h = int(np.max(dst_points[:, 1]) - y)

            if w <= 0 or h <= 0:
                print("[Tracker] 重检测得到无效bbox，丢弃")
                return False, None

            new_bbox = (x, y, w, h)
            print(f"[Tracker] 自动重检测成功，bbox={new_bbox}")

            self.initialize_tracker(frame, new_bbox)
            return True, new_bbox

        print("[Tracker] 自动重检测失败")
        return False, None

    def should_auto_detect(self):
        """是否要触发自动重检测"""
        if not self.auto_detection_mode:
            return False

        if not self.tracking:
            return self.frame_count % 15 == 0

        return self.frame_count % self.detection_interval == 0
