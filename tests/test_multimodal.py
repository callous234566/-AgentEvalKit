"""Tests for rag.multimodal helper functions."""

import base64
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image


def _make_test_image(width=100, height=100, color=(255, 0, 0), fmt="PNG"):
    """Create a small test image and return its bytes."""
    img = Image.new("RGB", (width, height), color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


class PrepareImageDataURLTest(unittest.TestCase):
    @patch("rag.multimodal.config")
    def test_valid_png(self, mock_config):
        mock_config.MULTIMODAL_IMAGE_MAX_SIDE = 1280
        from rag.multimodal import _prepare_image_data_url
        image_bytes = _make_test_image()
        result = _prepare_image_data_url(image_bytes)
        self.assertTrue(result.startswith("data:image/jpeg;base64,"))
        # Verify the base64 part decodes
        b64_part = result.split(",", 1)[1]
        decoded = base64.b64decode(b64_part)
        self.assertGreater(len(decoded), 0)

    @patch("rag.multimodal.config")
    def test_rgba_image_converted(self, mock_config):
        mock_config.MULTIMODAL_IMAGE_MAX_SIDE = 1280
        from rag.multimodal import _prepare_image_data_url
        img = Image.new("RGBA", (50, 50), (255, 0, 0, 128))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        result = _prepare_image_data_url(buf.getvalue())
        self.assertTrue(result.startswith("data:image/jpeg;base64,"))

    @patch("rag.multimodal.config")
    def test_palette_image_converted(self, mock_config):
        mock_config.MULTIMODAL_IMAGE_MAX_SIDE = 1280
        from rag.multimodal import _prepare_image_data_url
        img = Image.new("P", (50, 50))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        result = _prepare_image_data_url(buf.getvalue())
        self.assertTrue(result.startswith("data:image/jpeg;base64,"))

    @patch("rag.multimodal.config")
    def test_large_image_thumbnail(self, mock_config):
        mock_config.MULTIMODAL_IMAGE_MAX_SIDE = 128
        from rag.multimodal import _prepare_image_data_url
        image_bytes = _make_test_image(width=500, height=500)
        result = _prepare_image_data_url(image_bytes)
        self.assertTrue(result.startswith("data:image/jpeg;base64,"))

    def test_invalid_bytes_returns_empty(self):
        from rag.multimodal import _prepare_image_data_url
        with patch("rag.multimodal.config") as mock_config:
            mock_config.MULTIMODAL_IMAGE_MAX_SIDE = 1280
            result = _prepare_image_data_url(b"not an image")
            self.assertEqual(result, "")


class ExtractImageDocumentsTest(unittest.TestCase):
    @patch("config.check_api_key", return_value=False)
    @patch("rag.multimodal.config")
    def test_returns_empty_when_no_api_key(self, mock_config, mock_key):
        mock_config.ENABLE_MULTIMODAL_PARSING = True
        mock_config.check_api_key = mock_key
        from rag.multimodal import extract_image_documents
        result = extract_image_documents("/fake/path.pdf", ".pdf")
        self.assertEqual(result, [])

    @patch("rag.multimodal.config")
    def test_returns_empty_when_disabled(self, mock_config):
        mock_config.ENABLE_MULTIMODAL_PARSING = False
        from rag.multimodal import extract_image_documents
        result = extract_image_documents("/fake/path.pdf", ".pdf")
        self.assertEqual(result, [])

    @patch("config.check_api_key", return_value=True)
    @patch("rag.multimodal.config")
    def test_returns_empty_for_unsupported_suffix(self, mock_config, mock_key):
        mock_config.ENABLE_MULTIMODAL_PARSING = True
        mock_config.check_api_key = mock_key
        from rag.multimodal import extract_image_documents
        result = extract_image_documents("/fake/path.txt", ".txt")
        self.assertEqual(result, [])


class ExtractDocxImagesTest(unittest.TestCase):
    def test_returns_empty_for_non_zip(self):
        from rag.multimodal import _extract_docx_images
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            f.write(b"not a zip file")
            path = Path(f.name)
        try:
            result = _extract_docx_images(path)
            self.assertEqual(result, [])
        finally:
            path.unlink()

    def test_extracts_media_from_zip(self):
        import zipfile
        from rag.multimodal import _extract_docx_images

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            path = Path(f.name)

        try:
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("word/media/image1.png", _make_test_image())
                zf.writestr("word/document.xml", "<doc/>")
            result = _extract_docx_images(path)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "image1.png")
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
