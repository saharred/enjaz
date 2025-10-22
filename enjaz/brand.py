"""
Brand System Module for Enjaz Application.
Extracts brand colors from logo and generates comprehensive palette.
"""

import colorsys
from typing import Tuple, Dict
import streamlit as st


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    """Convert RGB to HSL."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s * 100, l * 100)


def hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """Convert HSL to RGB."""
    h, s, l = hsl[0] / 360, hsl[1] / 100, hsl[2] / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def lighten_color(hex_color: str, percent: float) -> str:
    """Lighten a color by percentage in HSL space."""
    rgb = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(rgb)
    
    # Increase lightness
    new_l = min(100, l + percent)
    
    new_rgb = hsl_to_rgb((h, s, new_l))
    return rgb_to_hex(new_rgb)


def darken_color(hex_color: str, percent: float) -> str:
    """Darken a color by percentage in HSL space."""
    rgb = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(rgb)
    
    # Decrease lightness
    new_l = max(0, l - percent)
    
    new_rgb = hsl_to_rgb((h, s, new_l))
    return rgb_to_hex(new_rgb)


def get_luminance(hex_color: str) -> float:
    """Calculate relative luminance of a color (WCAG formula)."""
    rgb = hex_to_rgb(hex_color)
    r, g, b = [x / 255.0 for x in rgb]
    
    # Apply gamma correction
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Calculate contrast ratio between two colors (WCAG)."""
    l1 = get_luminance(fg_hex)
    l2 = get_luminance(bg_hex)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def ensure_contrast(fg_hex: str, bg_hex: str, level: str = "AA") -> Tuple[str, str]:
    """
    Ensure sufficient contrast between foreground and background colors.
    
    Args:
        fg_hex: Foreground color (hex)
        bg_hex: Background color (hex)
        level: "AA" (4.5:1) or "AAA" (7:1)
    
    Returns:
        Tuple of (foreground, background) with sufficient contrast
    """
    min_ratio = 4.5 if level == "AA" else 7.0
    current_ratio = get_contrast_ratio(fg_hex, bg_hex)
    
    if current_ratio >= min_ratio:
        return (fg_hex, bg_hex)
    
    # If contrast is insufficient, use white on dark or dark on white
    bg_luminance = get_luminance(bg_hex)
    
    if bg_luminance > 0.5:
        # Light background, use dark text
        return ("#222222", bg_hex)
    else:
        # Dark background, use light text
        return ("#FFFFFF", bg_hex)


def extract_brand_maroon(logo_path: str) -> str:
    """
    Extract dominant maroon color from logo image.
    
    Args:
        logo_path: Path to logo image file
    
    Returns:
        Hex color string (e.g., "#6d3a46")
    """
    try:
        from PIL import Image
        import numpy as np
        from sklearn.cluster import KMeans
        
        # Load image
        img = Image.open(logo_path)
        img = img.convert('RGB')
        
        # Resize for faster processing
        img.thumbnail((200, 200))
        
        # Convert to numpy array
        pixels = np.array(img).reshape(-1, 3)
        
        # Filter out near-white and near-black pixels
        mask = np.all([
            np.sum(pixels, axis=1) > 100,  # Not too dark
            np.sum(pixels, axis=1) < 700,  # Not too light
        ], axis=0)
        
        filtered_pixels = pixels[mask]
        
        if len(filtered_pixels) < 10:
            # Fallback if filtering removed too many pixels
            filtered_pixels = pixels
        
        # Cluster colors
        n_clusters = min(6, len(filtered_pixels) // 100)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(filtered_pixels)
        
        # Get cluster centers and their frequencies
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        counts = np.bincount(labels)
        
        # Find the most prominent non-neutral color (maroon)
        best_idx = 0
        best_score = 0
        
        for i, (center, count) in enumerate(zip(centers, counts)):
            r, g, b = center
            
            # Calculate saturation
            h, s, l = rgb_to_hsl((int(r), int(g), int(b)))
            
            # Score: prefer high saturation and high frequency
            # Maroon should have moderate lightness and high saturation
            if 20 < l < 50 and s > 30:
                score = count * s
                if score > best_score:
                    best_score = score
                    best_idx = i
        
        # Get the maroon color
        maroon_rgb = centers[best_idx]
        maroon_hex = rgb_to_hex(tuple(maroon_rgb.astype(int)))
        
        return maroon_hex
        
    except Exception as e:
        print(f"Warning: Could not extract color from logo: {e}")
        # Fallback to Qatar maroon
        return "#6d3a46"


def build_palette(base_hex: str) -> Dict[str, any]:
    """
    Build comprehensive color palette from base maroon color.
    
    Args:
        base_hex: Base maroon color (hex)
    
    Returns:
        Dictionary with all palette colors
    """
    palette = {
        "maroon": base_hex,
        "maroon_900": darken_color(base_hex, 14),
        "maroon_700": darken_color(base_hex, 9),
        "maroon_300": lighten_color(base_hex, 12),
        "maroon_100": lighten_color(base_hex, 20),
        "gold": "#C9A227",
        "gold_light": "#E5C563",
        "light": "#FFFFFF",
        "muted": "#E9EDF2",
        "dark": "#222222",
        "gradient": {
            "start": base_hex,
            "end": darken_color(base_hex, 14)
        }
    }
    
    return palette


def get_brand_palette(logo_path: str) -> Dict[str, any]:
    """
    High-level function to extract brand colors and build palette.
    
    Args:
        logo_path: Path to logo image
    
    Returns:
        Complete brand palette dictionary
    """
    base_maroon = extract_brand_maroon(logo_path)
    palette = build_palette(base_maroon)
    return palette


def inject_css(palette: Dict[str, any]):
    """
    Inject CSS variables and styles from palette into Streamlit app.
    
    Args:
        palette: Brand palette dictionary
    """
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* CSS Variables */
    :root {{
        --maroon: {palette['maroon']};
        --maroon-900: {palette['maroon_900']};
        --maroon-700: {palette['maroon_700']};
        --maroon-300: {palette['maroon_300']};
        --maroon-100: {palette['maroon_100']};
        --gold: {palette['gold']};
        --gold-light: {palette['gold_light']};
        --light: {palette['light']};
        --muted: {palette['muted']};
        --dark: {palette['dark']};
    }}
    
    /* RTL Support */
    * {{
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    
    /* Main Container */
    .main {{
        background-color: #F8F9FA;
    }}
    
    /* Hero Section */
    .hero {{
        background: linear-gradient(160deg, var(--maroon), var(--maroon-900));
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        color: var(--light);
        box-shadow: 0 10px 30px rgba(138, 21, 56, 0.2);
    }}
    
    /* Buttons */
    .stButton>button {{
        background: var(--maroon);
        color: var(--light);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(138, 21, 56, 0.15);
    }}
    
    .stButton>button:hover {{
        background: var(--maroon-700);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(138, 21, 56, 0.25);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
    }}
    
    /* Cards */
    .card {{
        background: var(--light);
        border: 1px solid var(--muted);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }}
    
    .card:hover {{
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    /* Metrics */
    .stMetric {{
        background: var(--light);
        border-radius: 12px;
        padding: 1rem;
        border-right: 4px solid var(--maroon);
    }}
    
    /* Tables */
    table thead th {{
        background: var(--maroon-100) !important;
        color: var(--dark) !important;
        font-weight: 700 !important;
        border-bottom: 2px solid var(--maroon) !important;
    }}
    
    table tbody tr:hover {{
        background: var(--muted) !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: var(--light);
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 1px solid var(--muted);
        border-bottom: none;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: var(--maroon);
        color: var(--light) !important;
        border-color: var(--maroon);
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: linear-gradient(180deg, var(--maroon-100), var(--light));
    }}
    
    /* File Uploader */
    .stFileUploader {{
        border: 2px dashed var(--maroon-300);
        border-radius: 12px;
        background: var(--maroon-100);
        padding: 1.5rem;
    }}
    
    /* Success/Error Messages */
    .stSuccess {{
        background: #D4EDDA;
        border-right: 4px solid #28A745;
        border-radius: 8px;
    }}
    
    .stError {{
        background: #F8D7DA;
        border-right: 4px solid #DC3545;
        border-radius: 8px;
    }}
    
    .stWarning {{
        background: #FFF3CD;
        border-right: 4px solid #FFC107;
        border-radius: 8px;
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: var(--maroon);
        font-weight: 700;
    }}
    
    /* Links */
    a {{
        color: var(--maroon);
        text-decoration: none;
        font-weight: 600;
    }}
    
    a:hover {{
        color: var(--maroon-700);
        text-decoration: underline;
    }}
    
    /* Gold Accents */
    .gold-text {{
        color: var(--gold);
        font-weight: 700;
    }}
    
    /* Custom Header */
    .custom-header {{
        background: linear-gradient(160deg, var(--maroon), var(--maroon-900));
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: var(--light);
        box-shadow: 0 10px 30px rgba(138, 21, 56, 0.2);
    }}
    
    /* Custom Footer */
    .custom-footer {{
        background: var(--maroon);
        color: var(--light);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 3rem;
        text-align: center;
        line-height: 1.8;
    }}
    
    .custom-footer a {{
        color: var(--gold);
        text-decoration: none;
    }}
    
    .custom-footer a:hover {{
        text-decoration: underline;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

