import qrcode
import pandas as pd
from PIL import Image
import cv2

def generate_qr(data, file_name="qrcode.png", fill_color="black", bg_color="white", logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill=fill_color, back_color=bg_color)
    
    if logo_path:
        logo = Image.open(logo_path)
        logo_size = min(img.size) // 5
        logo = logo.resize((logo_size, logo_size))
        
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo, pos, logo.convert("RGBA"))
    
    img.save(file_name)
    print(f"QR Code saved as {file_name}")

def generate_bulk_qr(file_path):
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        generate_qr(row['data'], f"qr_{index}.png")

def scan_qr(image_path):
    detector = cv2.QRCodeDetector()
    image = cv2.imread(image_path)
    data, _, _ = detector.detectAndDecode(image)
    
    if data:
        print("Scanned QR Code Data:", data)
    else:
        print("No QR code found.")

if __name__ == "__main__":
    choice = input("Choose an option: 1) Generate QR 2) Bulk Generate QR 3) Scan QR: ")
    
    if choice == "1":
        data = input("Enter the text or URL to generate a QR code: ")
        file_name = input("Enter file name to save (default: qrcode.png): ") or "qrcode.png"
        fill_color = input("Enter the QR color (default: black): ") or "black"
        bg_color = input("Enter the background color (default: white): ") or "white"
        logo_path = input("Enter logo path (or press Enter to skip): ") or None
        generate_qr(data, file_name, fill_color, bg_color, logo_path)
    elif choice == "2":
        file_path = input("Enter CSV file path for bulk QR generation: ")
        generate_bulk_qr(file_path)
    elif choice == "3":
        image_path = input("Enter the path of the QR code image to scan: ")
        scan_qr(image_path)
    else:
        print("Invalid choice!")
