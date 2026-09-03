import cv2
import socket
import math
import time
import struct

# --- CONFIGURATION ---
# Replace with the exact Local IP address of Laptop B (the Client)
CLIENT_IP = "192.176.0.254"
PORT = 5000
# Safe UDP payload size (Max is 65535, we use 60000 to leave room for headers)
MAX_IMAGE_DGRAM = 60000

def main():
    # 1. Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
    # 2. Open the video file
    cap = cv2.VideoCapture('sample_video.mp4')
   
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps: # Fallback if FPS cannot be read
        fps = 30
    sleep_time = 1 / fps

    print(f"Streaming to {CLIENT_IP}:{PORT} at {fps} FPS...")

    # 3. For each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break
           
        # 3(a). Resize and encode into JPEG
        frame = cv2.resize(frame, (640, 480))
        _, encoded_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        data = encoded_frame.tobytes()
       
        # 3(b). Split frame into chunks of fixed size
        total_chunks = math.ceil(len(data) / MAX_IMAGE_DGRAM)
       
        for i in range(total_chunks):
            start = i * MAX_IMAGE_DGRAM
            end = start + MAX_IMAGE_DGRAM
            chunk = data[start:end]
           
            # 3(c). Marker bit: 1 if last packet of frame, 0 otherwise
            marker = 1 if i == total_chunks - 1 else 0
           
            # Pack the marker as an unsigned char (1 byte) and prepend it
            packet = struct.pack('B', marker) + chunk
           
            # Send chunk
            sock.sendto(packet, (CLIENT_IP, PORT))
           
        # 4. Sleep for frame interval (maintain FPS)
        time.sleep(sleep_time)

    cap.release()
    sock.close()

if __name__ == "__main__":
    main()