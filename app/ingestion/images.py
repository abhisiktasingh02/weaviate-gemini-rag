from PIL import Image
import fitz
import pytesseract

def extract_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    
    for page_index in range(len(doc)):
        page = doc[page_index]
        for img in page.get_images(full=True):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                img_pil = Image.frombytes(
                    "RGB", [pix.width, pix.height], pix.samples
                )
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img_pil = Image.frombytes(
                    "RGB", [pix.width, pix.height], pix.samples
                )
            images.append((page_index + 1, img_pil))
    return images

def orc_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)