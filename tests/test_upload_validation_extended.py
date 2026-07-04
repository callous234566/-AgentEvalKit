"""Extended edge-case tests for rag.upload_validation."""

import tempfile
import unittest
from pathlib import Path

from rag.upload_validation import validate_uploaded_file_content


class EmptyFileTest(unittest.TestCase):
    def test_empty_file_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(path, ".txt", "text/plain")
        finally:
            Path(path).unlink()


class PdfValidationTest(unittest.TestCase):
    def test_valid_pdf_header(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4 some content")
            path = f.name
        try:
            validate_uploaded_file_content(path, ".pdf", "application/pdf")
        finally:
            Path(path).unlink()

    def test_wrong_header_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"NOT_A_PDF")
            path = f.name
        try:
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(path, ".pdf", "application/pdf")
        finally:
            Path(path).unlink()


class DocxValidationTest(unittest.TestCase):
    def test_valid_zip_header(self):
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            f.write(b"PK\x03\x04rest of file")
            path = f.name
        try:
            validate_uploaded_file_content(path, ".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        finally:
            Path(path).unlink()

    def test_wrong_header_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            f.write(b"NOT_ZIP")
            path = f.name
        try:
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(path, ".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        finally:
            Path(path).unlink()


class TextValidationTest(unittest.TestCase):
    def test_clean_text_passes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("正常的文本内容\n第二行")
            path = f.name
        try:
            validate_uploaded_file_content(path, ".txt", "text/plain")
        finally:
            Path(path).unlink()

    def test_binary_null_byte_raises(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"text\x00binary")
            path = f.name
        try:
            with self.assertRaises(ValueError):
                validate_uploaded_file_content(path, ".txt", "text/plain")
        finally:
            Path(path).unlink()

    def test_md_validation(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("# Markdown标题\n\n内容")
            path = f.name
        try:
            validate_uploaded_file_content(path, ".md", "text/markdown")
        finally:
            Path(path).unlink()

    def test_tab_and_newline_allowed(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"col1\tcol2\nrow1\trow2\r\n")
            path = f.name
        try:
            validate_uploaded_file_content(path, ".txt", "text/plain")
        finally:
            Path(path).unlink()


class MimeMismatchTest(unittest.TestCase):
    def test_mismatch_warns_but_does_not_raise(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("content")
            path = f.name
        try:
            # application/octet-stream is in allowed MIME for .txt, so no warning
            validate_uploaded_file_content(path, ".txt", "application/octet-stream")
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
