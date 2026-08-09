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
            base = Image.open(thumb_path).convert("RGB")
            bg = base.resize((CANVAS_W, CANVAS_H))
            bg = bg.filter(ImageFilter.GaussianBlur(15))
            bg = ImageEnhance.Brightness(bg).enhance(0.18)
            canvas = bg.convert("RGBA")

            overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (25, 0, 0, 180))
            canvas = Image.alpha_composite(canvas, overlay)

            draw = ImageDraw.Draw(canvas)

            box_x = 60
            box_y = 33
            box_w = 1160
            box_h = 393

            draw.rounded_rectangle(
                (box_x, box_y, box_x + box_w, box_y + box_h),
                radius=10,
                fill=(255, 255, 255, 55),
                outline=(255, 255, 255),
                width=3
            )

            thumb = base.resize((633, 326))
            thumb_x = 323
            thumb_y = 43
            canvas.paste(thumb, (thumb_x, thumb_y))

            fade = Image.new("RGBA", (box_w, 116), (0, 0, 0, 0))
            fd = ImageDraw.Draw(fade)
            for y in range(116):
                alpha = int((y / 116) * 255)
                fd.line([(0, y), (box_w, y)], fill=(0, 0, 0, alpha))
            canvas.paste(fade, (box_x, box_y + 277), fade)

            c = (255, 255, 255)
            # TOP LEFT
            draw.line([(60, 33), (100, 33)], fill=c, width=3)
            draw.line([(60, 33), (60, 73)], fill=c, width=3)
            # TOP RIGHT
            draw.line([(1220, 33), (1180, 33)], fill=c, width=3)
            draw.line([(1220, 33), (1220, 73)], fill=c, width=3)
            # BOTTOM LEFT
            draw.line([(60, 426), (100, 426)], fill=c, width=3)
            draw.line([(60, 426), (60, 386)], fill=c, width=3)
            # BOTTOM RIGHT
            draw.line([(1220, 426), (1180, 426)], fill=c, width=3)
            draw.line([(1220, 426), (1220, 386)], fill=c, width=3)

            try:
                medium_font = ImageFont.truetype(FONT_BOLD, 32)
                small_font = ImageFont.truetype(FONT_REGULAR, 20)
            except:
                medium_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            draw.text((983, 340), "ELINA MUSIC", font=medium_font, fill=(255, 0, 0))

            wave_y = 580
            for x in range(100, 1133, 8):
                h = random.randint(10, 40)
                draw.line([(x, wave_y - h // 2), (x, wave_y + h // 2)], fill=(255, 255, 255), width=3)

            line_y = 630
            draw.line([(100, line_y), (1150, line_y)], fill=(140, 140, 140), width=5)
            draw.line([(100, line_y), (433, line_y)], fill=(255, 255, 255), width=6)
            draw.ellipse((423, line_y - 8, 440, line_y + 8), fill="white")

            draw.text((100, 646), "00:00", font=small_font, fill="white")
            draw.text((1083, 646), duration, font=small_font, fill="white")

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
        import config
        return config.YOUTUBE_IMG_URL
