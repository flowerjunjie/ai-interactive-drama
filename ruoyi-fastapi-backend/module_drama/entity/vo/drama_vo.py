from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip_html(s: str | None) -> str | None:
    """Remove HTML tags to prevent stored XSS in title/description fields."""
    if s is None:
        return None
    return re.sub(r'<[^>]*>', '', s)


# --- App auth ---
class AppRegisterModel(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=64)
    nick_name: str | None = Field(default=None, max_length=64)


class AppLoginModel(BaseModel):
    user_name: str
    password: str


class AppUserBrief(BaseModel):
    user_id: int
    user_name: str
    nick_name: str
    avatar: str | None = None


class AppTokenResponse(BaseModel):
    token: str
    token_type: str = 'Bearer'


# --- Drama / feed ---
class DramaPublicModel(BaseModel):
    drama_id: int
    title: str
    cover_url: str | None = None
    description: str | None = None
    drama_type: str
    tags: str | None = None
    heat: int | None = None
    model_config = ConfigDict(from_attributes=True)


class VideoNodePublicModel(BaseModel):
    node_id: int
    drama_id: int
    title: str | None = None
    video_url: str | None = None
    cover_url: str | None = None
    duration_sec: int | None = None
    is_entry: str | None = None
    model_config = ConfigDict(from_attributes=True)


class VideoChoicePublicModel(BaseModel):
    choice_id: int
    node_id: int
    label: str
    next_node_id: int
    sort: int
    model_config = ConfigDict(from_attributes=True)


class FeedItemModel(BaseModel):
    kind: str  # drama | ad
    drama: DramaPublicModel | None = None
    ad: dict | None = None


class WatchHistoryIn(BaseModel):
    drama_id: int
    node_id: int | None = None
    progress_sec: int = 0


class LikeIn(BaseModel):
    target_type: str  # drama | node
    target_id: int


class FavoriteIn(BaseModel):
    drama_id: int


class SubscribeIn(BaseModel):
    drama_id: int
    notify_enabled: bool = True


class CommentCreateModel(BaseModel):
    drama_id: int
    node_id: int | None = None
    content: str = Field(..., min_length=1, max_length=2000)


class ChoiceLogIn(BaseModel):
    drama_id: int
    from_node_id: int | None = None
    choice_id: int
    to_node_id: int


class ReviewCreateModel(BaseModel):
    drama_id: int
    node_id: int | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    content: str | None = Field(default=None, max_length=2000)


# --- Admin ---
class DramaSaveModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    cover_url: str | None = None
    description: str | None = None
    drama_type: str = 'comic_drama'
    status: str = 'draft'
    sort: int = 0
    tags: str | None = Field(default=None, max_length=512, description='JSON 数组字符串或逗号分隔')
    heat: int = 0

    @field_validator('title', 'description')
    @classmethod
    def _sanitize(cls, v: str | None) -> str | None:
        return _strip_html(v)


class VideoNodeSaveModel(BaseModel):
    drama_id: int
    parent_node_id: int | None = None
    title: str | None = None
    video_url: str | None = None
    cover_url: str | None = None
    tos_key: str | None = None
    duration_sec: int | None = None
    episode_no: int | None = None
    sort: int = 0
    is_entry: str = '0'
    is_interactive: str = '0'
    choice_trigger_sec: float | None = None
    status: str = 'draft'
    review_status: str = 'pending'
    reject_reason: str | None = None

    @field_validator('title', 'reject_reason')
    @classmethod
    def _sanitize(cls, v: str | None) -> str | None:
        return _strip_html(v)


class VideoChoiceSaveModel(BaseModel):
    node_id: int
    choice_code: str | None = Field(default=None, max_length=8)
    label: str
    next_node_id: int
    sort: int = 0


class DramaAdSaveModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str
    media_type: str = Field(default='image', description='image | video')
    media_url: str | None = None
    image_url: str | None = None
    cover_url: str | None = None
    link_url: str | None = None
    slot_type: str = Field(default='feed', validation_alias='slotType')
    weight: int = 0
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str = '0'


class UploadCompleteIn(BaseModel):
    file_id: int
    size_bytes: int | None = None
    video_url: str | None = None
    cover_url: str | None = None
    tos_key: str | None = None


class UploadSignQuery(BaseModel):
    drama_id: int | None = None
    node_id: int | None = None
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str | None = Field(default='video/mp4', max_length=128)


class ReviewAuditModel(BaseModel):
    status: str  # approved | rejected
    admin_remark: str | None = None


class NodeModerationRejectModel(BaseModel):
    reject_reason: str | None = Field(default=None, max_length=500)


class PageQuery(BaseModel):
    page_num: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class DramalistQuery(BaseModel):
    drama_type: str | None = None
    keyword: str | None = None
    sort: str | None = Field(default=None, description='recommend|latest|heat')
    page_num: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=50)
