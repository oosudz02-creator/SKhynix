"""OpenDART API client for SK hynix project."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://opendart.fss.or.kr/api"


class DartApiError(RuntimeError):
    """Raised when OpenDART returns a non-success status."""


class DartClient:
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("DART_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DART_API_KEY가 없습니다. .env 또는 환경변수에 입력하세요."
            )
        self.timeout = timeout

    def get_company(self, corp_code: str) -> dict[str, Any]:
        return self._get(
            "/company.json",
            {"corp_code": corp_code},
        )

    def get_full_financial_statement(
        self,
        corp_code: str,
        bsns_year: int,
        reprt_code: str,
        fs_div: str = "CFS",
    ) -> dict[str, Any]:
        return self._get(
            "/fnlttSinglAcntAll.json",
            {
                "corp_code": corp_code,
                "bsns_year": str(bsns_year),
                "reprt_code": reprt_code,
                "fs_div": fs_div,
            },
        )

    def _get(self, path: str, params: dict[str, str]) -> dict[str, Any]:
        request_params = {"crtfc_key": self.api_key, **params}
        response = requests.get(
            f"{BASE_URL}{path}",
            params=request_params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()
        status = str(data.get("status", ""))

        if status != "000":
            message = data.get("message", "OpenDART API 오류")
            raise DartApiError(f"status={status}: {message}")

        return data
