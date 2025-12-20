import os
from google.cloud import storage
from django.conf import settings

def upload_to_gcs(file, destination_path):
    # settings.py의 BASE_DIR을 기준으로 키 파일 위치를 찾습니다.
    # 키 파일을 pawfecto-backend/ 루트 폴더에 두셨다면 아래와 같이 작성합니다.
    key_path = os.path.join(settings.BASE_DIR, "service-account-key.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    storage_client = storage.Client()
    bucket_name = "your-bucket-name"  # 실제 버킷 이름으로 수정
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(destination_path)
    blob.upload_from_file(file, content_type=file.content_type)
    
    return blob.public_url