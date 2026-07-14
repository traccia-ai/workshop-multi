"""Pydantic models for structured multi-agent outputs."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ContentChannel(str, Enum):
    BLOG = "blog"
    SOCIAL = "social"
    SEO = "seo"


class Subtask(BaseModel):
    id: str = Field(description="Short id, e.g. blog-1")
    channel: ContentChannel
    title: str
    brief: str = Field(description="What the specialist should produce")
    priority: Literal["high", "medium", "low"] = "medium"


class CampaignPlan(BaseModel):
    campaign_name: str
    audience: str
    goal: str
    tone: str
    subtasks: list[Subtask]


class DraftPiece(BaseModel):
    channel: ContentChannel
    title: str
    body: str
    notes: str = ""


class EditedPiece(BaseModel):
    channel: ContentChannel
    title: str
    body: str
    changes_made: list[str] = Field(default_factory=list)


class SeoOptimizedPiece(BaseModel):
    channel: ContentChannel
    title: str
    body: str
    primary_keyword: str
    secondary_keywords: list[str] = Field(default_factory=list)
    meta_description: str = ""


class ReviewDecision(BaseModel):
    approved: bool
    feedback: str = ""
    revised_title: str | None = None


class CampaignPackage(BaseModel):
    plan: CampaignPlan
    drafts: list[DraftPiece] = Field(default_factory=list)
    edited: list[EditedPiece] = Field(default_factory=list)
    seo: list[SeoOptimizedPiece] = Field(default_factory=list)
    review: ReviewDecision | None = None
    published: bool = False
