from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_architecture_diagram():
    width, height = 1200, 800
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Colors
    bg_header = "#1E3A8A"
    box_blue = "#DBEAFE"
    border_blue = "#1E40AF"
    box_green = "#DCFCE7"
    border_green = "#15803D"
    box_orange = "#FFEDD5"
    border_orange = "#C2410C"
    text_dark = "#1F2937"

    # Draw Header Banner
    draw.rectangle([0, 0, width, 80], fill=bg_header)
    draw.text((30, 25), "BMW Service Knowledge RAG - Technical Architecture", fill="#FFFFFF", font_size=28)

    # Box Definitions (x1, y1, x2, y2, label, sublabel, color_bg, color_border)
    boxes = [
        (80, 140, 320, 210, "Service Documents", "PDF, TXT, DOCX, CSV", box_blue, border_blue),
        (80, 250, 320, 320, "Document Loader", "Multi-format Extraction", box_blue, border_blue),
        (80, 360, 320, 430, "Text Processing", "Clean Whitespace & Lines", box_blue, border_blue),
        (80, 470, 320, 540, "Chunker Module", "800 Chars / 100 Overlap", box_blue, border_blue),
        (80, 580, 320, 650, "SentenceTransformers", "all-MiniLM-L6-v2 Embeddings", box_blue, border_blue),
        (450, 580, 690, 650, "FAISS Vector Store", "Local Index Persistence", box_green, border_green),
        (450, 470, 690, 540, "Retriever Module", "Similarity Threshold (0.35)", box_green, border_green),
        (450, 360, 690, 430, "LangChain RAG Pipeline", "Strict Grounding System Prompt", box_green, border_green),
        (820, 360, 1060, 430, "Ollama Local LLM", "qwen2.5:1.5b @ localhost:11434", box_orange, border_orange),
        (450, 250, 690, 320, "FastAPI Backend", "Uvicorn REST API Services", box_blue, border_blue),
        (450, 140, 690, 210, "Streamlit Frontend", "Technician Web Interface", box_blue, border_blue),
    ]

    for x1, y1, x2, y2, label, subtext, bg, border in boxes:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=bg, outline=border, width=2)
        draw.text((x1 + 15, y1 + 15), label, fill=text_dark, font_size=16)
        draw.text((x1 + 15, y1 + 40), subtext, fill="#4B5563", font_size=12)

    # Arrow definitions (x1, y1, x2, y2)
    arrows = [
        (200, 210, 200, 250), # Docs -> Loader
        (200, 320, 200, 360), # Loader -> Cleaner
        (200, 430, 200, 470), # Cleaner -> Chunker
        (200, 540, 200, 580), # Chunker -> Embeddings
        (320, 615, 450, 615), # Embeddings -> FAISS
        (570, 580, 570, 540), # FAISS -> Retriever
        (570, 470, 570, 430), # Retriever -> RAG
        (690, 395, 820, 395), # RAG <-> Ollama
        (570, 360, 570, 320), # RAG -> FastAPI
        (570, 250, 570, 210), # FastAPI -> Streamlit
    ]

    for x1, y1, x2, y2 in arrows:
        draw.line([x1, y1, x2, y2], fill="#1E40AF", width=3)

    output_path = Path(__file__).parent / "architecture.png"
    img.save(output_path)
    static_path = Path(__file__).parent / "source" / "_static" / "architecture.png"
    static_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(static_path)
    print(f"Architecture diagram generated at: {output_path} and {static_path}")

if __name__ == "__main__":
    create_architecture_diagram()
