import boto3
from django.conf import settings


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
)


def upload_image(file, folder, username, post_id=None):
    try:
        if folder == "profile_images":
            file_name = f"{username}"
        elif folder == "post_images":
            file_name = f"{username}_{post_id}"
        s3_client.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            f"{folder}/{file_name}",
            ExtraArgs={"ContentType": "image/png"},
        )

        # Generar la url
        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{folder}/{file_name}"
        return file_url
    except Exception as e:
        return {"error": str(e), "message": "Upload image to s3 has been failed"}
