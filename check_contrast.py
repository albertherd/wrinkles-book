import math

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(hex1, hex2):
    lum1 = get_luminance(hex_to_rgb(hex1))
    lum2 = get_luminance(hex_to_rgb(hex2))
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

def find_accessible_color_fg(fg_hex, bg_hex, target_ratio=4.5):
    # Simplistic iterative approach to lighten FG
    ratio = get_contrast_ratio(fg_hex, bg_hex)
    if ratio >= target_ratio:
        return fg_hex, ratio
    
    fg_rgb = list(hex_to_rgb(fg_hex))
    
    # Try adjusting significantly to find a safe value
    for i in range(255):
        # Lighten FG
        fg_rgb = [min(255, c + 1) for c in fg_rgb]
            
        new_fg = '#{:02x}{:02x}{:02x}'.format(*fg_rgb)
        new_ratio = get_contrast_ratio(new_fg, bg_hex)
        
        if new_ratio >= target_ratio:
            return new_fg, new_ratio
            
    return fg_hex, ratio

def find_accessible_color_bg(fg_hex, bg_hex, target_ratio=4.5):
    # Simplistic iterative approach to darken BG
    ratio = get_contrast_ratio(fg_hex, bg_hex)
    if ratio >= target_ratio:
        return bg_hex, ratio
        
    bg_rgb = list(hex_to_rgb(bg_hex))
    
    for i in range(255):
         # Darken BG
        bg_rgb = [max(0, c - 1) for c in bg_rgb]
        
        new_bg = '#{:02x}{:02x}{:02x}'.format(*bg_rgb)
        new_ratio = get_contrast_ratio(fg_hex, new_bg)
        
        if new_ratio >= target_ratio:
            return new_bg, new_ratio
    return bg_hex, ratio

# Colors from styles.css
bg_dark = "#1a1a1a"
bg_gradient_start = "#1a1a1a"
bg_gradient_end = "#2a2420" 
text_meta = "#c8c3be"
text_body = "#dcd7d2" # Not explicitly p tag color but body color
text_h1 = "#f2f0ed"
text_price = "#b8d4ff"

# Buttons
btn_paypal_bg = "#003087"
btn_revolut_bg = "#335DFF"
btn_offline_bg = "#444444"
btn_text = "#ffffff"

print("--- Contrast Check ---")

# 1. Check text color on details/p
ratio_meta_dark = get_contrast_ratio(text_meta, bg_dark)
ratio_meta_end = get_contrast_ratio(text_meta, bg_gradient_end)
print(f"Meta Text ({text_meta}) on BG Dark ({bg_dark}): {ratio_meta_dark:.2f}")
print(f"Meta Text ({text_meta}) on BG Gradient End ({bg_gradient_end}): {ratio_meta_end:.2f}")

# 2. Check Link Color (none explicit found in CSS, checking Price as similar heavy text)
ratio_price = get_contrast_ratio(text_price, bg_dark)
print(f"Price Text ({text_price}) on BG Dark ({bg_dark}): {ratio_price:.2f}")

# 3. Check Button Color
ratio_paypal = get_contrast_ratio(btn_text, btn_paypal_bg)
print(f"PayPal Button Text ({btn_text}) on BG ({btn_paypal_bg}): {ratio_paypal:.2f}")

ratio_revolut = get_contrast_ratio(btn_text, btn_revolut_bg)
print(f"Revolut Button Text ({btn_text}) on BG ({btn_revolut_bg}): {ratio_revolut:.2f}")

ratio_offline = get_contrast_ratio(btn_text, btn_offline_bg)
print(f"Offline Button Text ({btn_text}) on BG ({btn_offline_bg}): {ratio_offline:.2f}")

print("\n--- Suggestions ---")

if ratio_meta_dark < 4.5:
    new_fg, new_ratio = find_accessible_color_fg(text_meta, bg_dark)
    print(f"SUGGESTION: Change .meta color from {text_meta} to {new_fg} (ratio {new_ratio:.2f} on {bg_dark})")

if ratio_meta_end < 4.5:
     new_fg, new_ratio = find_accessible_color_fg(text_meta, bg_gradient_end)
     print(f"SUGGESTION: Change .meta color from {text_meta} to {new_fg} (ratio {new_ratio:.2f} on {bg_gradient_end})")

if ratio_revolut < 4.5:
    new_bg, new_ratio = find_accessible_color_bg(btn_text, btn_revolut_bg)
    print(f"SUGGESTION: Change .btn-revolut background from {btn_revolut_bg} to {new_bg} (ratio {new_ratio:.2f})")
if ratio_paypal < 4.5:
    new_bg, new_ratio = find_accessible_color_bg(btn_text, btn_paypal_bg)
    print(f"SUGGESTION: Change .btn-paypal background from {btn_paypal_bg} to {new_bg} (ratio {new_ratio:.2f})")
if ratio_offline < 4.5:
     new_bg, new_ratio = find_accessible_color_bg(btn_text, btn_offline_bg)
     print(f"SUGGESTION: Change .btn-offline background from {btn_offline_bg} to {new_bg} (ratio {new_ratio:.2f})")
