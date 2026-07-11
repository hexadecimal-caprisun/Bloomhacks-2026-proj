import cv2
import queue
import threading
import numpy as np
from tensorflow import keras

class recycle_detector():
    # class definition
    def __init__(self, model_path, classes):
        self.model = keras.models.load_model(model_path) #load model
        self.classes = classes 

        self.frame_queue = queue.Queue(maxsize=1) #queue init with maxsize 1

        self.predictions = None
        self.lock = threading.Lock()
        self.running = True

    def preprocess(self, frame):
        img = cv2.resize(frame, (256, 256))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img 
    def infer_loop(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=5)
                input_data = self.preprocess(frame)

                with self.lock:
                    self.predictions = preds

                self.frame_queue.task_done()
            except queue.Empty:
                continue


def main():
    class_labels = ["battery", "biological", "cardboard", "clothes", "glass", "metal", "paper", "plastic", "shoes", "trash"]
    detector = recycle_detector('./model.h5', class_labels)
    inference_thread = threading.Thread(target=detector.infer_loop)
    inference_thread.daemon = True
    inference_thread.start()

    cap = cv2.VideoCapture(0)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1
        
        if frame_count%5 == 0:
            try:
                if detector.frame_queue.full():
                    detector.frame_queue.get_nowait()

                detector.frame_queue.put_nowait(frame.copy())
            except:
                pass
        with detector.lock:
            current_preds = detector.predictions
        if current_preds is not None:
            class_id = np.argmax(current_preds)
            confidence = current_preds[class_id]

            if confidence > 0.6:
                label = f"{class_labels[class_id]}: {confidence*100}Z%", cv2.putText(frame, label, (30,50), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Live Video', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
