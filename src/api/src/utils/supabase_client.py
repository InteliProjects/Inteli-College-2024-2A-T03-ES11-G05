from supabase import create_client, Client
import os
from configs.settings import settings

# Load environment variables
SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY


class SupabaseClient:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def create_bucket_if_not_exists(self, bucket_name):
        print(f"Creating bucket '{bucket_name}'...")
        try:
            self.supabase.storage.create_bucket(bucket_name)

            self.supabase.rpc('set_rls_policy', {
                'table': 'buckets',
                'permissions': 'insert'
            })

            self.supabase.rpc('set_rls_policy', {
                'table': 'objects',
                'permissions': 'none'
            })
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, bucket_name, file_path):
        try:
            file_name = os.path.basename(file_path)

            # Open the file in binary mode
            with open(file_path, 'rb') as file_data:
                # Upload the file
                response = self.supabase.storage.from_(bucket_name).upload(
                    path=file_name,
                    file=file_data,
                    # Define MIME type
                    file_options={"content-type": "application/octet-stream"}
                )

            if response.error:
                raise Exception(f"Error uploading file: {response.error.message}")

            print(f"File '{file_name}' uploaded successfully to bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_file(self, bucket_name, file_name, local_file_path):
        try:
            # Download the file
            response = self.supabase.storage.from_(
                bucket_name).download(file_name)

            # Save the downloaded content to a local file
            with open(local_file_path, 'wb+') as file:
                file.write(response)
                print(f"File '{file_name}' downloaded successfully to '{local_file_path}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")
