import numpy as np
import cv2
import os

def generate_test_video(output_path, duration=5, fps=60, resolution=(1920, 1080)):
    width, height = resolution
    total_frames = duration * fps
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame_num in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        t = frame_num / fps
        
        bg_color = int(30 + 20 * np.sin(t * 0.5))
        frame[:] = (bg_color, bg_color + 10, bg_color + 20)
        
        ball_x = int(width * (0.1 + 0.8 * (0.5 + 0.5 * np.sin(t * 2))))
        ball_y = int(height * (0.3 + 0.2 * np.sin(t * 3)))
        cv2.circle(frame, (ball_x, ball_y), 50, (0, 100, 255), -1)
        cv2.circle(frame, (ball_x, ball_y), 50, (0, 50, 200), 3)
        
        rect_x = int(width * 0.7 + 100 * np.sin(t * 1.5))
        rect_y = int(height * 0.6 + 50 * np.cos(t * 2))
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + 120, rect_y + 80), (255, 150, 0), -1)
        
        for i in range(5):
            px = int(width * 0.5 + 200 * np.cos(t * 4 + i * 1.2))
            py = int(height * 0.5 + 200 * np.sin(t * 4 + i * 1.2))
            size = int(5 + 3 * np.sin(t * 10 + i))
            cv2.circle(frame, (px, py), size, (100, 255, 100), -1)
        
        cv2.putText(frame, f"Frame: {frame_num}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Time: {t:.2f}s", (50, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"FPS: {fps}", (50, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.rectangle(frame, (width - 220, 20), (width - 20, 100), (40, 40, 40), -1)
        cv2.putText(frame, "TEST HUD", (width - 200, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        out.write(frame)
    
    out.release()
    print(f"Generated: {output_path}")
    print(f"  Duration: {duration}s, FPS: {fps}, Frames: {total_frames}")
    print(f"  Resolution: {width}x{height}")

if __name__ == "__main__":
    os.makedirs("data/ground_truth", exist_ok=True)
    os.makedirs("data/input", exist_ok=True)
    
    generate_test_video("data/ground_truth/test_60fps.mp4", duration=5, fps=60)
    generate_test_video("data/input/test_30fps.mp4", duration=5, fps=30)
    
    print("\nTest videos generated successfully!")
