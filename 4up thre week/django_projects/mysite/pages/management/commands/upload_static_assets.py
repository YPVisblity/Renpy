import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class Command(BaseCommand):
    help = "把 static 資料夾裡的固定素材（BGM、頭像、商店圖）批次上傳到 Cloudinary"

    def handle(self, *args, **options):
        # 上傳 BGM
        bgm_path = Path(settings.BASE_DIR) / "pages/static/pages/audio/BGM.mp3"
        if bgm_path.exists():
            result = cloudinary.uploader.upload(
                str(bgm_path),
                resource_type="video",
                public_id="codequest/audio/bgm",
                overwrite=True,
            )
            self.stdout.write(self.style.SUCCESS(f"BGM 上傳成功：{result['secure_url']}"))

        # 上傳預設頭像
        avatar_dir = Path(settings.BASE_DIR) / "pages/static/pages/images/avatars"
        for avatar_file in avatar_dir.glob("*.png"):
            public_id = f"codequest/avatars/{avatar_file.stem}"
            result = cloudinary.uploader.upload(
                str(avatar_file),
                public_id=public_id,
                overwrite=True,
            )
            self.stdout.write(self.style.SUCCESS(f"{avatar_file.name} 上傳成功：{result['secure_url']}"))

        # 上傳商店圖片
        shop_dir = Path(settings.BASE_DIR) / "pages/static/pages/images/shop"
        if shop_dir.exists():
            for shop_file in shop_dir.glob("*.png"):
                public_id = f"codequest/shop/{shop_file.stem}"
                result = cloudinary.uploader.upload(
                    str(shop_file),
                    public_id=public_id,
                    overwrite=True,
                )
                self.stdout.write(self.style.SUCCESS(f"{shop_file.name} 上傳成功：{result['secure_url']}"))