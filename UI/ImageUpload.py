import gradio as gr
from PIL import Image
from rembg import remove
import numpy as np
import os
import cv2
import io

def process_image(file):

    if file is None:
        return "No file uploaded. Please upload an image.", None

    # Extract file extension and validate
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension not in ['.jpg', '.png']:
        return "Invalid file format. Please upload a JPG or PNG image.", None

    try:
        # Open and validate the image using Pillow
        img = Image.open(file.name)
        if img.format not in ['JPEG', 'PNG']:
            return "Invalid file format. Please upload a valid JPG or PNG image.", None

        # Resize the image to 512x512
        img = img.resize((512, 512))

        # Perform background removal
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')  # Ensure compatibility before background removal
        img_byte_array.seek(0)

        output_image = remove(img_byte_array.getvalue())

        # Convert the output back to a PIL image
        output_image_io = io.BytesIO(output_image)
        result_img = Image.open(output_image_io).convert('RGB')  # Ensure final image is RGB

        # Save the result
        output_path = "output.jpg"
        result_img.save(output_path, "JPEG")

        return "Background removed successfully!", output_path

    except Exception as e:
        return f"Error processing image: {e}", None

with gr.Blocks() as app:
    gr.Markdown("## Image Upload and Background Removal")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Input")
            file_input = gr.File(label="Upload Image", file_types=["image"], type="filepath")
            submit_button = gr.Button("Cut Background")
            status_output = gr.Textbox(label="Status")
        
        with gr.Column():
            gr.Markdown("### Output")
            image_output = gr.Image(label="Processed Image", type="filepath")

    submit_button.click(fn=process_image, inputs=file_input, outputs=[status_output, image_output])

if __name__ == "__main__":
    app.launch(debug=True)
