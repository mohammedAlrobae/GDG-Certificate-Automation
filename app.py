import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from streamlit_image_coordinates import streamlit_image_coordinates
import io
import zipfile
import os
import time
import random

# ─────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GDG Certificate Automation",
    page_icon="gdg_icon.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS — Clean Solid White Background, Black Titles
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Google Sans', 'Roboto', sans-serif;
}

/* ── Solid white background ── */
.stApp {
    background-color: #FFFFFF !important;
}

.main .block-container {
    background: #FFFFFF;
    padding: 2rem 3rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* ── Hide default Streamlit header/footer ── */
header {visibility: hidden;}
footer {visibility: hidden;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #F8F9FA;
}

/* ── All headings: Large, Bold, Solid Black ── */
h1, h2, h3, h4 {
    color: #000000 !important;
    font-weight: 700 !important;
}
h1 { font-size: 2.8rem !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.5rem !important; }

/* ── Labels / markdown text ── */
label, .stMarkdown p, .stTextInput label, .stSlider label,
.stFileUploader label, .stSelectbox label, .stColorPicker label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* ── Buttons — Material feel ── */
.stButton > button {
    background-color: #4285F4;
    color: white;
    border-radius: 24px;
    font-weight: 500;
    border: none;
    padding: 0.65rem 2rem;
    width: 100%;
    transition: all 0.25s ease;
    box-shadow: 0 1px 3px rgba(60,64,67,0.3), 0 1px 2px rgba(60,64,67,0.15);
}
.stButton > button:hover {
    background-color: #3367D6;
    box-shadow: 0 4px 12px rgba(60,64,67,0.25);
    transform: translateY(-1px);
}

/* ── Download button ── */
.stDownloadButton > button {
    background-color: #34A853;
    color: white;
    border-radius: 24px;
    font-weight: 500;
    border: none;
    padding: 0.65rem 2rem;
    width: 100%;
    transition: all 0.25s ease;
    box-shadow: 0 1px 3px rgba(60,64,67,0.3), 0 1px 2px rgba(60,64,67,0.15);
}
.stDownloadButton > button:hover {
    background-color: #2d9249;
    box-shadow: 0 4px 12px rgba(60,64,67,0.25);
    transform: translateY(-1px);
}

/* ── Inputs ── */
input { border-radius: 8px !important; }

/* ── Progress bar — Google gradient ── */
.stProgress > div > div > div > div {
    background-image: linear-gradient(to right, #4285F4, #EA4335, #FBBC05, #34A853);
}

/* ── Section headers ── */
.section-header {
    background: linear-gradient(135deg, #4285F4, #34A853);
    color: white;
    padding: 0.75rem 1.4rem;
    border-radius: 12px;
    font-size: 1.25rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.8rem;
}

/* ── Control Panel ── */
.control-panel {
    background: #F8F9FA;
    border: 2px solid #E8EAED;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1.2rem 0;
}
.control-panel-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 0.6rem;
}

/* ── Click instruction ── */
.click-instruction {
    font-size: 1.6rem;
    font-weight: 700;
    color: #4285F4;
    text-align: center;
    padding: 0.8rem 0;
    letter-spacing: 0.2px;
}

/* ── Footer ── */
.app-footer {
    text-align: center;
    padding: 1.6rem 0 0.6rem;
    color: #5f6368;
    font-size: 0.88rem;
    letter-spacing: 0.3px;
}
.app-footer span {
    color: #4285F4;
    font-weight: 500;
}

/* ── Balloon animation ── */
@keyframes floatUp {
    0%   { transform: translateY(0) scale(1); opacity: 1; }
    100% { transform: translateY(-120vh) scale(1.2); opacity: 0; }
}
.balloon-container {
    position: fixed; bottom: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 9999; overflow: hidden;
}
.balloon {
    position: absolute; bottom: -80px;
    font-size: 3rem;
    animation: floatUp 4s ease-out forwards;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────
def load_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType font, falling back to the built-in default."""
    try:
        if font_path:
            return ImageFont.truetype(font_path, size)
    except OSError:
        pass
    return ImageFont.load_default()


def process_certificate(template_image, name, font, color, x, y):
    """Stamp *name* onto a copy of *template_image* at (x, y)."""
    img = template_image.copy()
    draw = ImageDraw.Draw(img)
    draw.text((x, y), str(name), fill=color, font=font)
    return img


def show_balloon_effect():
    """Render a celebratory emoji balloon animation."""
    emojis = ["🎈", "🎉", "🥳", "✨", "🎊", "🏆", "⭐"]
    html = '<div class="balloon-container">'
    for _ in range(18):
        emoji = random.choice(emojis)
        left = random.randint(2, 95)
        delay = round(random.uniform(0, 2.5), 2)
        dur = round(random.uniform(3, 5.5), 2)
        html += (
            f'<span class="balloon" style="left:{left}%;'
            f'animation-delay:{delay}s;animation-duration:{dur}s;">'
            f'{emoji}</span>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def check_password() -> bool:
    """Gate the app behind a regional access key stored in st.secrets."""
    def _on_change():
        if st.session_state["password"] in st.secrets["regional_access_keys"].values():
            st.session_state["password_correct"] = True
            for region, key in st.secrets["regional_access_keys"].items():
                if key == st.session_state["password"]:
                    st.session_state["region"] = region
                    break
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Enter Regional Access Key", type="password",
            on_change=_on_change, key="password",
        )
        return False
    if not st.session_state["password_correct"]:
        st.text_input(
            "Enter Regional Access Key", type="password",
            on_change=_on_change, key="password",
        )
        st.error("😕 Access Permission Denied")
        return False
    return True


# ─────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────
def main():
    # ══════════════════════════════════════════════════════════
    # SIDEBAR — Region display & About
    # ══════════════════════════════════════════════════════════
    with st.sidebar:
        if os.path.exists("gdg_logo.png"):
            st.image("gdg_logo.png", width=140)
        else:
            st.title("GDG")

        if "region" in st.session_state:
            st.markdown(f"**🌐 Region:** `{st.session_state['region']}`")

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info("Built for GDG Chapter Leaders to automate certificate generation.")
        st.caption("v2.0.0 • Developed by Mohammed Robae")

    # ══════════════════════════════════════════════════════════
    # TOP — Centered GDG Logo
    # ══════════════════════════════════════════════════════════
    _, logo_col, _ = st.columns([1, 1, 1])
    with logo_col:
        if os.path.exists("gdg_logo_ZUJ.png"):
            st.image("gdg_logo_ZUJ.png", use_container_width=True)

    st.markdown(
        "<h1 style='text-align:center;margin:0.2rem 0 0.1rem;'>"
        "🎓 Certificate Automation</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;color:#5f6368;margin-bottom:1.5rem;'>"
        "Generate bulk certificates with <strong>pixel-perfect</strong> precision.</p>",
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════
    # UPLOAD SECTION — Centralized
    # ══════════════════════════════════════════════════════════
    _, upload_col, _ = st.columns([1, 2, 1])
    with upload_col:
        template_file = st.file_uploader(
            "📄 Certificate Template", type=["png", "jpg", "jpeg"],
        )
        data_file = st.file_uploader(
            "📊 Participants (Excel / CSV)", type=["csv", "xlsx"],
        )

    # ══════════════════════════════════════════════════════════
    # CONTROL PANEL — Font Size, Color Picker, Column Name
    # ══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div class="control-panel-title">⚙️ Control Panel</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        cp_col1, cp_col2, cp_col3 = st.columns(3, gap="large")

        with cp_col1:
            font_size = st.slider(
                "🖋️ Font Size", min_value=10, max_value=200, value=60,
            )

        with cp_col2:
            font_color_hex = st.color_picker("🎨 Font Color", value="#000000")

        with cp_col3:
            excel_col_name = st.text_input(
                "🗂️ Excel Column Name", value="Name",
            )

    # ─── Data loading ───
    df = None
    name_col = None

    if data_file:
        try:
            if data_file.name.endswith(".csv"):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)

            # Use the user-specified column name
            if excel_col_name in df.columns:
                name_col = excel_col_name
            else:
                # Fallback: fuzzy-match on "name" or "participant"
                possible = [
                    c for c in df.columns
                    if "name" in c.lower() or "participant" in c.lower()
                ]
                if possible:
                    name_col = possible[0]
                    st.warning(
                        f"Column **'{excel_col_name}'** not found. "
                        f"Using **'{name_col}'** instead."
                    )
                else:
                    name_col = df.columns[0]
                    st.warning(
                        f"Column **'{excel_col_name}'** not found. "
                        f"Falling back to first column: **'{name_col}'**."
                    )
        except Exception as e:
            st.error(f"Error reading data file: {e}")

    # ══════════════════════════════════════════════════════════
    # WORKSPACE — Two-Column Layout (Set Position + Preview)
    # ══════════════════════════════════════════════════════════
    if template_file:
        image = Image.open(template_file)
        orig_w, orig_h = image.size

        # ─── Bold blue click instruction ───
        st.markdown(
            '<p class="click-instruction">'
            '👆 Click where the name should appear on the certificate'
            '</p>',
            unsafe_allow_html=True,
        )

        ws_col, preview_col = st.columns(2, gap="large")

        # ─── Left: Set Name Position ───
        with ws_col:
            st.markdown(
                '<div class="section-header">📍 Set Name Position</div>',
                unsafe_allow_html=True,
            )

            # Fixed display width — NO use_container_width
            DISPLAY_WIDTH = 700
            display_h = int(DISPLAY_WIDTH * orig_h / orig_w)

            value = streamlit_image_coordinates(
                image, key="coord_picker", width=DISPLAY_WIDTH,
            )

            coords = None
            if value:
                # Scale click coords back to the original resolution
                scale_x = orig_w / DISPLAY_WIDTH
                scale_y = orig_h / display_h
                original_x = int(value["x"] * scale_x)
                original_y = int(value["y"] * scale_y)
                coords = (original_x, original_y)

                st.success(
                    f"✅ Position → **({original_x}, {original_y})** "
                    f"on original {orig_w}×{orig_h} image"
                )

        # ─── Right: Live Preview ───
        with preview_col:
            st.markdown(
                '<div class="section-header">👁️ Live Preview</div>',
                unsafe_allow_html=True,
            )

            if coords and df is not None and name_col:
                font_path = "Roboto-Bold.ttf" if os.path.exists("Roboto-Bold.ttf") else None
                font = load_font(font_path, font_size)

                first_name = df[name_col].iloc[0]
                preview_img = process_certificate(
                    image, first_name, font, font_color_hex,
                    coords[0], coords[1],
                )
                st.image(
                    preview_img,
                    caption=f"Preview: {first_name}",
                    use_container_width=True,
                )

                st.markdown(f"""
| Setting | Value |
|---|---|
| **Certificates** | {len(df)} |
| **Font Color** | `{font_color_hex}` |
| **Font Size** | {font_size}px |
| **Position** | ({coords[0]}, {coords[1]}) |
                """)
            else:
                if not coords:
                    st.info("👆 Click on the template to set the name position.")
                elif df is None:
                    st.info("📂 Upload a **Participants file** to see the preview.")
                else:
                    st.info("⏳ Configure settings to see the preview.")

        # ─── Centered Generate & Download Button ───
        if coords and df is not None and name_col:
            st.markdown("")  # spacer
            _, btn_col, _ = st.columns([1, 2, 1])
            with btn_col:
                if st.button(
                    "🚀 Generate & Download ZIP",
                    type="primary",
                    use_container_width=True,
                ):
                    font_path = (
                        "Roboto-Bold.ttf"
                        if os.path.exists("Roboto-Bold.ttf")
                        else None
                    )
                    font = load_font(font_path, font_size)

                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    zip_buffer = io.BytesIO()
                    start_time = time.time()

                    with zipfile.ZipFile(zip_buffer, "w") as zf:
                        total = len(df)
                        for i, row in df.iterrows():
                            name = row[name_col]
                            clean_name = "".join(
                                c for c in str(name)
                                if c.isalnum() or c in " _-"
                            ).strip() or f"participant_{i}"

                            cert_img = process_certificate(
                                image, name, font, font_color_hex,
                                coords[0], coords[1],
                            )

                            img_bytes = io.BytesIO()
                            cert_img.save(img_bytes, format="PNG")
                            zf.writestr(f"{clean_name}.png", img_bytes.getvalue())

                            progress_bar.progress((i + 1) / total)
                            status_text.text(f"⏳ Processing: {name}...")

                    duration = round(time.time() - start_time, 2)
                    status_text.empty()
                    progress_bar.empty()

                    show_balloon_effect()
                    st.success(
                        f"🎉 Processed **{len(df)}** certificates in **{duration}s**!"
                    )

                    st.download_button(
                        label="⬇️ Download Certificates (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name="certificates.zip",
                        mime="application/zip",
                    )
    else:
        st.info("📤 Upload a **Certificate Template** above to get started.")

    # ══════════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div class="app-footer">Developed by <span>Mohammed Robae</span></div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if check_password():
        main()
