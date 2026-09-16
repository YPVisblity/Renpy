import cloudinary
import cloudinary.uploader
from django.conf import settings
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)
def upload_avatar_to_cloudinary(file_obj,public_id):
    """
    把上傳的圖片檔案推到Cloudinary，回傳圖片的公開網址。
    file_obj:Django的 UploadedFile物件(request.FILES 拿到的那個）
    public_id:要存到Cloudinary上的識別碼(建議帶使用者id避免重複覆蓋)
    """
    result = cloudinary.uploader.upload(
        file_obj,
        folder="codequest_avatars",
        public_id=public_id,
        overwrite=True,
        transformation=[{"width": 200, "height": 200, "crop": "fill"}]
    )
    return result["secure_url"]