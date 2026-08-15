import os
import aiohttp
import aiofiles
import traceback
import random

from pathlib import Path

from PIL import (
    Image,
    ImageDraw,
    ImageFilter,
    ImageFont,
    ImageEnhance
)

from py_yt import VideosSearch

# =====================================
# CACHE
# =====================================

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# =====================================
# 4K SIZE
# =====================================

CANVAS_W = 1280
CANVAS_H = 720

# =====================================
# FONTS
# =====================================

FONT_BOLD = "ShrutiMusic/assets/font3.ttf"
FONT_REGULAR = "ShrutiMusic/assets/font2.ttf"

BOT_NAME = "XTR MUSIC"

# =====================================
# THUMB GENERATOR
# =====================================

async def gen_thumb(videoid: str):
    try:
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]
        duration = result.get("duration", "3:20")
        title = result.get("title", BOT_NAME)
        thumburl = result["thumbnails"][0]["url"].split("?")[0]

        thumb_path = CACHE_DIR / f"{videoid}.jpg"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumburl) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
                else:
                    # Fallback to hqdefault
                    fallback_url = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
                    async with session.get(fallback_url) as resp2:
                        if resp2.status == 200:
                            async with aiofiles.open(thumb_path, "wb") as f:
                                await f.write(await resp2.read())

        if not os.path.exists(thumb_path):
            import config
            return config.YOUTUBE_IMG_URL

        output = CACHE_DIR / f"{videoid}_final.png"

        def _draw_thumb():
            # Open the base downloaded youtube thumbnail
            base = Image.open(thumb_path).convert("RGB")
            
            # Open our template background image
            bg_base = Image.open("ShrutiMusic/assets/elina_thumb_bg.jpg").convert("RGBA")
            
            # Select a random hue shift (0 to 255) to rotate background colors (40+ colors)
            hue_shift = random.randint(0, 255)
            hsv = bg_base.convert("HSV")
            h_band, s_band, v_band = hsv.split()
            h_band = h_band.point(lambda p: (p + hue_shift) % 256)
            bg = Image.merge("HSV", (h_band, s_band, v_band)).convert("RGBA")
            
            canvas = bg.copy()
            draw = ImageDraw.Draw(canvas)
            
            # Cover the default top-left branding
            draw.rectangle((0, 0, 296, 150), fill=(0, 0, 0, 255))
            
            # Calculate theme color matching the shifted hue
            import colorsys
            orig_r, orig_g, orig_b = 236 / 255.0, 40 / 255.0, 112 / 255.0
            orig_h, orig_s, orig_v = colorsys.rgb_to_hsv(orig_r, orig_g, orig_b)
            new_h = (orig_h + (hue_shift / 256.0)) % 1.0
            new_r, new_g, new_b = colorsys.hsv_to_rgb(new_h, orig_s, orig_v)
            theme_color = (int(new_r * 255), int(new_g * 255), int(new_b * 255), 255)
            
            # Load fonts
            try:
                title_font = ImageFont.truetype(FONT_BOLD, 38)
                subtitle_font = ImageFont.truetype(FONT_REGULAR, 20)
                player_title_font = ImageFont.truetype(FONT_BOLD, 18)
                player_sub_font = ImageFont.truetype(FONT_REGULAR, 13)
                small_font = ImageFont.truetype(FONT_REGULAR, 16)
                logo_title_font = ImageFont.truetype(FONT_BOLD, 24)
                logo_sub_font = ImageFont.truetype(FONT_REGULAR, 12)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                player_title_font = ImageFont.load_default()
                player_sub_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                logo_title_font = ImageFont.load_default()
                logo_sub_font = ImageFont.load_default()
                
            # Helper to get text width
            def get_text_width(text, font):
                try:
                    return draw.textlength(text, font=font)
                except AttributeError:
                    try:
                        return draw.textsize(text, font=font)[0]
                    except:
                        return len(text) * 12

            # Draw the Elina Music branding dynamically on the top right
            icon_x, icon_y = 1000, 30
            # Circle
            draw.ellipse((icon_x, icon_y, icon_x + 50, icon_y + 50), fill=theme_color)
            # Music note lines inside circle
            draw.ellipse((icon_x + 12, icon_y + 25, icon_x + 24, icon_y + 37), fill=(0, 0, 0, 255))
            draw.ellipse((icon_x + 26, icon_y + 22, icon_x + 38, icon_y + 34), fill=(0, 0, 0, 255))
            draw.line([(icon_x + 24, icon_y + 12), (icon_x + 24, icon_y + 30)], fill=(0, 0, 0, 255), width=3)
            draw.line([(icon_x + 38, icon_y + 9), (icon_x + 38, icon_y + 27)], fill=(0, 0, 0, 255), width=3)
            draw.line([(icon_x + 24, icon_y + 12), (icon_x + 38, icon_y + 9)], fill=(0, 0, 0, 255), width=4)
            # Text
            draw.text((1065, 30), "ELINA MUSIC", font=logo_title_font, fill="white")
            draw.text((1065, 58), "FEEL THE MUSIC", font=logo_sub_font, fill=theme_color)

            # 1. Overlay resized and rounded YouTube thumbnail in the center
            # Center thumbnail size: 688 x 387 (16:9 ratio)
            thumb_w, thumb_h = 688, 387
            thumb = base.resize((thumb_w, thumb_h))
            
            # Create rounded corners mask
            radius = 24
            mask = Image.new('L', (thumb_w, thumb_h), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, thumb_w, thumb_h), radius=radius, fill=255)
            
            # Paste the thumbnail onto canvas using mask
            thumb_x = (CANVAS_W - thumb_w) // 2 # 296
            thumb_y = 60
            canvas.paste(thumb, (thumb_x, thumb_y), mask)
            
            # Draw themed glowing rounded border around the thumbnail
            draw.rounded_rectangle(
                (thumb_x - 3, thumb_y - 3, thumb_x + thumb_w + 3, thumb_y + thumb_h + 3),
                radius=radius + 3,
                outline=theme_color,
                width=4
            )
            
            # 2. Draw Title & Subtitle (below the card, centered)
            clean_title = title.title()
            if len(clean_title) > 36:
                clean_title = clean_title[:33] + "..."
                
            title_w = get_text_width(clean_title, font=title_font)
            title_x = (CANVAS_W - title_w) // 2
            title_y = 465
            draw.text((title_x, title_y), clean_title, font=title_font, fill="white")
            
            # Subtitle
            channel = result.get("channel", {}).get("name", "YOUTUBE")
            subtitle_text = f"{channel.upper()} • HD AUDIO"
            if len(subtitle_text) > 40:
                subtitle_text = subtitle_text[:37] + "..."
                
            sub_w = get_text_width(subtitle_text, font=subtitle_font)
            sub_x = (CANVAS_W - sub_w) // 2
            sub_y = 515
            draw.text((sub_x, sub_y), subtitle_text, font=subtitle_font, fill=theme_color)
            
            # 3. Draw player bar contents (bottom overlay)
            player_title = clean_title
            if len(player_title) > 16:
                player_title = player_title[:13] + "..."
            draw.text((315, 575), player_title, font=player_title_font, fill="white")
            draw.text((315, 603), "ELINA MUSIC", font=player_sub_font, fill=(180, 180, 180))
            
            # Progress bar lines
            bar_start_x = 490
            bar_end_x = 990
            bar_y = 598
            # Gray background line
            draw.line([(bar_start_x, bar_y), (bar_end_x, bar_y)], fill=(80, 80, 80), width=4)
            # Active themed progress line (random progress, e.g. 35%)
            progress_pct = random.uniform(0.25, 0.55)
            active_end_x = int(bar_start_x + (bar_end_x - bar_start_x) * progress_pct)
            draw.line([(bar_start_x, bar_y), (active_end_x, bar_y)], fill=theme_color, width=5)
            # Handle dot
            draw.ellipse((active_end_x - 6, bar_y - 6, active_end_x + 6, bar_y + 6), fill="white")
            
            # Duration texts
            draw.text((bar_start_x, 615), "00:00", font=small_font, fill=(180, 180, 180))
            draw.text((bar_end_x - 45, 615), duration, font=small_font, fill=(180, 180, 180))
            
            # Dynamic Equalizer lines
            eq_start_x = 1025
            for i in range(5):
                h = random.randint(10, 30)
                line_x = eq_start_x + i * 8
                draw.line([(line_x, bar_y - h // 2), (line_x, bar_y + h // 2)], fill=theme_color, width=3)
                
            # Save the final image
            canvas.save(output, format="PNG", quality=95)
            try:
                os.remove(thumb_path)
            except:
                pass

        import asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _draw_thumb)

        return str(output)

    except Exception as e:
        print(f"[THUMB ERROR] {e}")
        traceback.print_exc()
        import config
        return config.YOUTUBE_IMG_URL
