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

CANVAS_W = 3840
CANVAS_H = 2160

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

        output = CACHE_DIR / f"{videoid}_final.png"

        def _draw_thumb():
            base = Image.open(thumb_path).convert("RGB")
            bg = base.resize((1280, 720))
            bg = bg.filter(ImageFilter.GaussianBlur(15))
            bg = ImageEnhance.Brightness(bg).enhance(0.5)
            
            canvas = bg.convert("RGBA")
            
            thumb = base.resize((640, 360))
            canvas.paste(thumb, (320, 150))
            
            draw = ImageDraw.Draw(canvas)
            
            try:
                medium_font = ImageFont.truetype(FONT_BOLD, 40)
                small_font = ImageFont.truetype(FONT_REGULAR, 30)
            except:
                medium_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                
            draw.text((320, 540), title[:50], font=medium_font, fill="white")
            draw.text((320, 600), f"Duration: {duration}", font=small_font, fill="white")
            draw.text((800, 600), BOT_NAME, font=small_font, fill="red")
            
            canvas.save(output, format="PNG", quality=90)
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
        return None
