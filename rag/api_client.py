"""
Streamlit 前端使用的后端 API client。
"""

from collections.abc import Mapping
from typing import Any, Optional
from urllib.parse import quote

import requests


def build_api_headers(api_token: str = "") -> dict[str, str]:
    """配置 API_TOKEN 时返回认证请求头。"""
    if not api_token:
        return {}
    return {"Authorization": f"Bearer {api_token}"}


class RagApiClient:
    """封装前端到 FastAPI 后端的 HTTP 请求。"""

    def __init__(self, api_base_url: str, api_token: str = ""):
        self.api_base_url = api_base_url.rstrip("/")
        self.api_token = api_token
        self.last_response_meta: dict[str, Any] = {}

    @property
    def headers(self) -> dict[str, str]:
        return build_api_headers(self.api_token)

    def _collection_path(self, collection_name: str) -> str:
        return quote(str(collection_name or ""), safe="")

    def _capture_response_meta(self, response) -> None:
        """Capture request diagnostics from backend response headers."""
        headers = getattr(response, "headers", {}) or {}
        if not isinstance(headers, Mapping):
            headers = {}
        self.last_response_meta = {
            "request_id": headers.get("X-Request-ID", ""),
            "process_time_ms": headers.get("X-Process-Time-Ms", ""),
            "status_code": getattr(response, "status_code", None),
        }

    def _capture_exception_meta(self, error: Exception) -> None:
        """Capture a short diagnostics record for failed HTTP calls."""
        self.last_response_meta = {
            "request_id": "",
            "process_time_ms": "",
            "status_code": None,
            "error": str(error)[:200],
        }

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            self._capture_response_meta(response)
            return response.status_code == 200
        except Exception as e:
            self._capture_exception_meta(e)
            return False

    def list_collections(self) -> list:
        try:
            response = requests.get(
                f"{self.api_base_url}/collections",
                headers=self.headers,
                timeout=10,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self._capture_exception_meta(e)
            return []
        return []

    def upload_file(
        self,
        file: Any,
        collection_name: str,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        enable_multimodal: Optional[bool] = None,
    ) -> dict:
        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            data = {"collection_name": collection_name}
            if chunk_size:
                data["chunk_size"] = str(chunk_size)
            if chunk_overlap is not None:
                data["chunk_overlap"] = str(chunk_overlap)
            if enable_multimodal is not None:
                data["enable_multimodal"] = str(bool(enable_multimodal)).lower()
            response = requests.post(
                f"{self.api_base_url}/upload",
                files=files,
                data=data,
                headers=self.headers,
                timeout=120,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": f"上传失败：{response.status_code}"}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": f"上传异常：{str(e)}"}

    def ask(
        self,
        question: str,
        collection_name: str,
        chat_history: Optional[list] = None,
        enable_query_rewrite: Optional[bool] = None,
        enable_contextual_compression: Optional[bool] = None,
    ) -> dict:
        payload = {
            "question": question,
            "collection_name": collection_name,
            "chat_history": chat_history or [],
            "enable_query_rewrite": enable_query_rewrite,
            "enable_contextual_compression": enable_contextual_compression,
        }
        return self._post_json(
            "/ask",
            payload,
            timeout=120,
            error_key="error",
            fallback={"success": False, "error": "请求失败", "answer": "", "sources": []},
        )

    def retrieve(
        self,
        question: str,
        collection_name: str,
        chat_history: Optional[list] = None,
        top_k: Optional[int] = None,
        temperature: Optional[float] = None,
        enable_query_rewrite: Optional[bool] = None,
        enable_contextual_compression: Optional[bool] = None,
    ) -> dict:
        payload = {
            "question": question,
            "collection_name": collection_name,
            "chat_history": chat_history or [],
            "top_k": top_k,
            "temperature": temperature,
            "enable_query_rewrite": enable_query_rewrite,
            "enable_contextual_compression": enable_contextual_compression,
        }
        return self._post_json(
            "/retrieve",
            payload,
            timeout=120,
            error_key="error",
            fallback={
                "success": False,
                "error": "检索失败",
                "documents": [],
                "sources": [],
                "retrieved_count": 0,
                "selected_count": 0,
            },
        )

    def generate(
        self,
        question: str,
        collection_name: str,
        documents: list,
        chat_history: Optional[list] = None,
        temperature: Optional[float] = None,
    ) -> dict:
        payload = {
            "question": question,
            "collection_name": collection_name,
            "chat_history": chat_history or [],
            "documents": documents or [],
            "temperature": temperature,
        }
        return self._post_json(
            "/generate",
            payload,
            timeout=120,
            error_key="error",
            fallback={"success": False, "error": "生成失败", "answer": "", "sources": []},
        )

    def agent(
        self,
        question: str,
        collection_name: str,
        chat_history: Optional[list] = None,
        debug: Optional[bool] = None,
    ) -> dict:
        payload = {
            "question": question,
            "collection_name": collection_name,
            "chat_history": chat_history or [],
            "debug": debug,
        }
        return self._post_json(
            "/agent",
            payload,
            timeout=180,
            error_key="error",
            fallback={"success": False, "error": "Agent 请求失败", "answer": "", "agent_steps": [], "debug_info": {}},
        )

    def create_collection(self, collection_name: str) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.post(
                f"{self.api_base_url}/collections/{collection_path}",
                headers=self.headers,
                timeout=10,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": f"创建失败：{response.status_code}"}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": f"创建异常：{str(e)}"}

    def delete_collection(self, collection_name: str) -> bool:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.delete(
                f"{self.api_base_url}/collections/{collection_path}",
                headers=self.headers,
                timeout=10,
            )
            self._capture_response_meta(response)
            return response.status_code == 200
        except Exception as e:
            self._capture_exception_meta(e)
            return False

    def rename_collection(self, collection_name: str, new_name: str) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.post(
                f"{self.api_base_url}/collections/{collection_path}/rename",
                headers=self.headers,
                json={"new_name": new_name},
                timeout=10,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": response.text}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": f"重命名异常：{str(e)}"}

    def list_documents(self, collection_name: str) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.get(
                f"{self.api_base_url}/collections/{collection_path}/documents",
                headers=self.headers,
                timeout=20,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "documents": [], "message": response.text}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "documents": [], "message": str(e)}

    def delete_document(self, collection_name: str, source: str) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.delete(
                f"{self.api_base_url}/collections/{collection_path}/documents",
                headers=self.headers,
                params={"source": source},
                timeout=20,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": response.text}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": str(e)}

    def batch_delete_documents(self, collection_name: str, sources: list) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.post(
                f"{self.api_base_url}/collections/{collection_path}/documents/batch_delete",
                headers=self.headers,
                json={"sources": sources},
                timeout=30,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": response.text}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": str(e)}

    def toggle_document_enabled(self, collection_name: str, source: str, enabled: bool) -> dict:
        try:
            collection_path = self._collection_path(collection_name)
            response = requests.patch(
                f"{self.api_base_url}/collections/{collection_path}/documents/enabled",
                headers=self.headers,
                json={"source": source, "enabled": enabled},
                timeout=20,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            return {"success": False, "message": response.text}
        except Exception as e:
            self._capture_exception_meta(e)
            return {"success": False, "message": str(e)}

    def _post_json(
        self,
        endpoint: str,
        payload: dict,
        timeout: int,
        error_key: str,
        fallback: dict,
    ) -> dict:
        try:
            response = requests.post(
                f"{self.api_base_url}{endpoint}",
                headers=self.headers,
                json=payload,
                timeout=timeout,
            )
            self._capture_response_meta(response)
            if response.status_code == 200:
                return response.json()
            result = dict(fallback)
            result[error_key] = f"请求失败：{response.status_code}"
            return result
        except Exception as e:
            self._capture_exception_meta(e)
            result = dict(fallback)
            result[error_key] = f"请求异常：{str(e)}"
            return result
