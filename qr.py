import qrcode

# Ask user for the hyperlink
link = input("Enter your website link: ")

# Generate QR code
qr = qrcode.QRCode(
    version=1,  # 1 = smallest size (21x21)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=6,  # controls how big each box is
    border=2,    # smaller border for mini QR
)

qr.add_data(link)
qr.make(fit=True)

# Create the image (black on white)
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("mini_qr_code.png")

print("✅ QR code generated successfully! Saved as 'mini_qr_code.png'")
