#!/usr/bin/env python3
"""
Autonomous Content Engine - Visual Carousel Renderer
Renders high-definition (1080x1350) social media carousel slides using Pillow.
"""

import os
import sys
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

# Default styling constants
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1350
BG_COLOR = (10, 15, 29)         # #0A0F1D (Dark tech navy)
CARD_BG = (22, 31, 54)          # #161F36
CARD_BORDER = (40, 56, 92)      # #28385C
ACCENT_COLOR = (74, 179, 216)   # #4AB3D8 (Sky cyan)
TEXT_WHITE = (255, 255, 255)
TEXT_DIM = (148, 163, 184)      # #94A3B8

def find_font(font_name, fallback_paths):
    for path in fallback_paths:
        if os.path.exists(path):
            return path
    return None

FONT_BOLD = find_font("bold", [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc"
])

FONT_REGULAR = find_font("regular", [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Helvetica.ttc"
])

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        bbox = font.getbbox(" ".join(current_line))
        line_w = bbox[2] - bbox[0]
        if line_w > max_width:
            current_line.pop()
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render_slide(slide_data, slide_num, total_slides, brand_handle="@nusantaraai00001"):
    img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_badge = ImageFont.truetype(FONT_BOLD, 22) if FONT_BOLD else ImageFont.load_default()
    f_title = ImageFont.truetype(FONT_BOLD, 52) if FONT_BOLD else ImageFont.load_default()
    f_subtitle = ImageFont.truetype(FONT_REGULAR, 32) if FONT_REGULAR else ImageFont.load_default()
    f_card_title = ImageFont.truetype(FONT_BOLD, 30) if FONT_BOLD else ImageFont.load_default()
    f_card_body = ImageFont.truetype(FONT_REGULAR, 26) if FONT_REGULAR else ImageFont.load_default()
    f_footer = ImageFont.truetype(FONT_REGULAR, 22) if FONT_REGULAR else ImageFont.load_default()

    # Top Header: Badge + Counter
    badge_text = slide_data.get("badge", "AI BREAKTHROUGH").upper()
    draw.rounded_rectangle([70, 70, 70 + len(badge_text) * 14 + 30, 115], radius=8, fill=CARD_BG, outline=ACCENT_COLOR, width=2)
    draw.text((85, 80), badge_text, fill=ACCENT_COLOR, font=f_badge)

    counter_text = f"{slide_num}/{total_slides}"
    draw.text((CANVAS_WIDTH - 140, 80), counter_text, fill=TEXT_DIM, font=f_badge)

    # Title
    title = slide_data.get("title", "")
    y_cursor = 180
    for line in wrap_text(title, f_title, CANVAS_WIDTH - 140):
        draw.text((70, y_cursor), line, fill=TEXT_WHITE, font=f_title)
        y_cursor += 65

    # Subtitle / Hook description
    subtitle = slide_data.get("subtitle", "")
    if subtitle:
        y_cursor += 15
        for line in wrap_text(subtitle, f_subtitle, CANVAS_WIDTH - 140):
            draw.text((70, y_cursor), line, fill=TEXT_DIM, font=f_subtitle)
            y_cursor += 42

    # Content Cards / Bullets
    cards = slide_data.get("cards", [])
    y_cursor += 40

    for card in cards:
        card_title = card.get("title", "")
        card_body = card.get("desc", "")
        
        body_lines = wrap_text(card_body, f_card_body, CANVAS_WIDTH - 220)
        card_h = 60 + (len(body_lines) * 36) + (40 if card_title else 0)
        
        # Draw card container
        draw.rounded_rectangle([70, y_cursor, CANVAS_WIDTH - 70, y_cursor + card_h], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
        
        # Left accent pill
        draw.rounded_rectangle([70, y_cursor, 78, y_cursor + card_h], radius=4, fill=ACCENT_COLOR)

        # Card Text
        text_y = y_cursor + 25
        if card_title:
            draw.text((110, text_y), card_title, fill=TEXT_WHITE, font=f_card_title)
            text_y += 44
            
        for line in body_lines:
            draw.text((110, text_y), line, fill=TEXT_DIM, font=f_card_body)
            text_y += 36

        y_cursor += card_h + 25

    # Footer: Branding & Swipe Prompt
    draw.line([70, CANVAS_HEIGHT - 100, CANVAS_WIDTH - 70, CANVAS_HEIGHT - 100], fill=CARD_BORDER, width=1)
    draw.text((70, CANVAS_HEIGHT - 70), brand_handle, fill=TEXT_DIM, font=f_footer)
    
    prompt_text = "SWIPE TO EXPLORE →" if slide_num < total_slides else "SAVE & SHARE ✦"
    draw.text((CANVAS_WIDTH - 280, CANVAS_HEIGHT - 70), prompt_text, fill=ACCENT_COLOR, font=f_footer)

    return img

def main():
    parser = argparse.ArgumentParser(description="Render social carousel slides")
    parser.add_argument("--input", required=True, help="Path to carousel JSON file")
    parser.add_argument("--out-dir", default="./output_slides", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.input, "r") as f:
        data = json.load(f)

    slides = data.get("slides", [])
    brand = data.get("brand_handle", "@nusantaraai00001")
    total = len(slides)

    print(f"[+] Rendering {total} slides to {args.out_dir}...")
    for idx, slide in enumerate(slides, start=1):
        img = render_slide(slide, idx, total, brand)
        out_path = os.path.join(args.out_dir, f"slide_{idx}.png")
        img.save(out_path, "PNG", quality=95)
        print(f"  ✓ Saved {out_path}")

    print("[✔] All slides successfully generated!")

if __name__ == "__main__":
    main()
