import os

source_path = r"C:\Users\vanda\OneDrive\Desktop\AML Miniproject\Automatic_Number_Plate_Detection_Recognition_YOLOv8\test\N4.jpeg"  # Replace with your actual image path

command = f"python predict.py source=\"{source_path}\""  
os.system(command)

print("Prediction completed!")
