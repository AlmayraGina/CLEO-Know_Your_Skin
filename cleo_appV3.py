
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from inference_sdk import InferenceHTTPClient
import io
import tempfile

st.title("CLEO - Know Your Skin")

uploaded_file = st.file_uploader("Upload foto wajah dengan pencahayaan cukup dan tanpa riasan", type=["jpg", "jpeg", "png"])

if uploaded_file:
    
    image_bytes = uploaded_file.read()

    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption="Gambar yang diupload", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(image_bytes)
        tmp_file_path = tmp_file.name

    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="BstUvYe2O3KZuLFe1IZb" 
    )

    result = client.run_workflow(
        workspace_name="cleo-know-your-skin",
        workflow_id="custom-workflow-4",
        images={"image": tmp_file_path},
        use_cache=True
    )

    import matplotlib.font_manager as fm

    for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):

        draw = ImageDraw.Draw(image)
    try:
        f_ont = ImageFont.truetype("LiberationSans-Italic.ttf", 50)
    except IOError:
        f_ont = ImageFont.load_default()

    predictions = result[0]['predictions']['predictions']
    for pred in predictions:
        x, y, w, h = pred['x'], pred['y'], pred['width'], pred['height']
        left = x - w / 2
        top = y - h / 2
        right = x + w / 2
        bottom = y + h / 2

        draw.rectangle([left, top, right, bottom], outline="purple", width=2)
        confidence_percent = max(int(pred['confidence'] * 100), 40)
        label = f"{pred['class']} ({confidence_percent}%)"
        draw.text((left, top - 20), label, fill="red", font=f_ont)
    st.image(image, caption="Annotated Image", use_container_width=True)
