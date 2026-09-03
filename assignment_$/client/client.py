import cv2
import socket
import numpy as np
import struct

# --- CONFIGURATION ---
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 9999

def main():
    # 1. Create a UDP socket and bind to listening port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
   
    print(f"Listening for video stream on port {PORT}...")
   
    frame_data = b''
   
    while True:
        # 2. Receive packets continuously
        # Max UDP packet size is 65535 bytes
        packet, addr = sock.recvfrom(65535)
       
        # Extract the 1-byte marker header and the video chunk payload
        marker = struct.unpack('B', packet[:1])[0]
        chunk = packet[1:]
       
        # 3. Append data
        frame_data += chunk
       
        # Check if it is the last packet of the frame
        if marker == 1:
            if len(frame_data) > 0:
                # 4. Decode frame and display using OpenCV
                np_data = np.frombuffer(frame_data, dtype=np.uint8)
                frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
               
                if frame is not None:
                    cv2.imshow("Video Stream", frame)
               
                # Clear buffer for the next incoming frame
                frame_data = b''
               
            # 5. Stop when user presses "q"
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    sock.close()

if __name__ == "__main__":
    main()