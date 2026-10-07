"""Bounded, non-redirecting transport for the scoped Dot tool API.

This module uses only the standard library and never loads credentials itself.
Callers translate ScopedRequestError into their own user-facing error class.
"""
import json
import urllib.error
import urllib.request

SITE = "https://reminder.geniusqi.com"
MAX_BUNDLE_BYTES = 32 * 1024 * 1024
HTTP_USER_AGENT = "Mozilla/5.0"


class ScopedRequestError(Exception):
    """Safe diagnostic: excludes credentials, response bodies and network URLs."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def scoped_request(list_id, tool, arguments, token):
    """Send an existing scoped tool payload; reading/writing depends on tool."""
    try:
        request = urllib.request.Request(
            SITE + "/api/dot/agent",
            data=json.dumps({"listId": list_id, "tool": tool, "arguments": arguments},
                            ensure_ascii=False).encode("utf-8"),
            headers={"Authorization": "Bearer " + token,
                     "Content-Type": "application/json", "User-Agent": HTTP_USER_AGENT},
            method="POST")
        with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
            raw = response.read(MAX_BUNDLE_BYTES + 1)
        if len(raw) > MAX_BUNDLE_BYTES:
            raise ScopedRequestError("网站标签接口响应过大，未读取截断内容。")
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ScopedRequestError("网站标签接口响应 JSON 不是对象，未采用响应。")
        return result
    except ScopedRequestError:
        raise
    except urllib.error.HTTPError as error:
        status = error.code
        try:
            error.close()
        except Exception:
            pass
        raise ScopedRequestError(
            f"网站标签接口拒绝请求 HTTP {status}；未把本地缓存当本次网站结果。") from None
    except (OSError, TimeoutError):
        raise ScopedRequestError(
            "网站标签接口网络读取失败；未把本地缓存当本次网站结果。") from None
    except (ValueError, UnicodeError):
        raise ScopedRequestError("网站标签接口响应 JSON 无效，未采用响应。") from None
    except Exception:
        raise ScopedRequestError("网站标签接口读取失败，未采用响应。") from None
