import gradio as gr
import cv2
import numpy as np
from PIL import Image

def process_image_with_slider(image, x1, y1, x2, y2):
    # Resize image to 512x512
    image_np = cv2.resize(np.array(image), (512, 512), interpolation=cv2.INTER_LINEAR)

    # Ensure coordinates are valid and within bounds
    x1, x2 = max(0, x1), min(511, x2)
    y1, y2 = max(0, y1), min(511, y2)

    # Create mask and apply GrabCut algorithm
    mask = np.zeros(image_np.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (x1, y1, x2 - x1, y2 - y1)

    cv2.grabCut(image_np, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    result = image_np * mask2[:, :, np.newaxis]

    return Image.fromarray(result)

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("""
    # Image Background Remover with Sliders
    Upload an image and use the sliders to adjust the bounding box for background removal.
    """)

    with gr.Row():
        input_image = gr.Image(label="Upload Image", type="pil")

        with gr.Column():
            x1 = gr.Slider(0, 511, step=1, label="x1", value=50)
            y1 = gr.Slider(0, 511, step=1, label="y1", value=50)
            x2 = gr.Slider(0, 511, step=1, label="x2", value=400)
            y2 = gr.Slider(0, 511, step=1, label="y2", value=400)

    output_image = gr.Image(label="Processed Image")
    process_button = gr.Button("Process")

    process_button.click(
        process_image_with_slider, 
        inputs=[input_image, x1, y1, x2, y2], 
        outputs=output_image
    )

# Launch the Gradio app
demo.launch(debug=True)
