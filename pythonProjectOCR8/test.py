from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Export the model to PaddlePaddle format
model.export(format="paddle")  # creates '/yolov8n_paddle_model'

# Load the exported PaddlePaddle model
paddle_model = YOLO("./yolov8n_paddle_model")

# Run inference
results = paddle_model("D://savecode/pythonProjectOCR8/image5/1.jpg")

# Convert the image from BGR (OpenCV default) to RGB for plotting
image = results[0].plot()  # Plot the detection results

# Display the image
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis("off")  # Turn off axis
plt.show()