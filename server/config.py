import os
from pydantic import BaseModel, Field

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)


class ReRankConfig(BaseModel):
    device: str = Field(default="cuda")
    release_year_fuzzy_value: int = Field(default=5)
    total_recommendations_required: int = Field(default=10)
    lance_db_path: int = Field(default=os.path.join(current_dir, "data", "movies-data"))


class RecSysConfig(BaseModel):
    model_id: str = Field(default=os.environ.get("HF_MODEL_ID", None))
    prem_api_key: str = Field(default=os.environ.get("PREM_API_KEY", None))
    prem_project_id: str = Field(default=os.environ.get("PREM_PROJECT_ID", None))
    mongo_connection_uri: str = Field(
        default=os.environ.get("MONGO_CONNECTION_URI", None)
    )

    # url and output paths
    drive_url: str = Field(
        default="https://drive.google.com/uc?id=1HpM0rWT9SZr8MTeJ_KMG9G9utWDVn0Qk"
    )
    zip_path: str = Field(default=os.path.join(current_dir, "data.zip"))
    output_folder: str = Field(default=current_dir)
    data_path: str = Field(default=os.path.join(current_dir, "data", "movies-data"))
