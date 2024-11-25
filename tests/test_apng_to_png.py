import pytest
from unittest.mock import patch, MagicMock

from apng_to_png.apng_to_png import (
    ensure_folder_exists,
    extract_frames,
    process_apng_files,
)


@pytest.fixture
def temp_folder(tmp_path):
    return tmp_path


def test_ensure_folder_exists(temp_folder):
    test_path = temp_folder / "test_folder"
    ensure_folder_exists(test_path)

    assert test_path.exists() and test_path.is_dir()


def test_extract_frames(temp_folder):
    apng_mock = MagicMock()
    apng_mock.frames = [
        (MagicMock(to_bytes=MagicMock(return_value=b"fake_png_data")), None)
    ] * 3

    input_apng = temp_folder / "test.apng"
    input_apng.touch()

    output_folder = temp_folder / "output"

    with (
        patch(
            "apng_to_png.apng_to_png.ensure_folder_exists"
        ) as mock_ensure_folder_exists,
        patch("apng_to_png.apng_to_png.APNG.open", return_value=apng_mock),
        patch("builtins.open", new_callable=MagicMock) as mock_open,
    ):
        extract_frames(input_apng, output_folder)

        # Ensure output folder creation was attempted
        mock_ensure_folder_exists.assert_called_once_with(output_folder)

        # Ensure that the `to_bytes` method was called and files were written
        assert mock_open.call_count == 3
        for i in range(3):
            output_file = output_folder / f"frame_{i:03}.png"
            mock_open.assert_any_call(output_file, "wb")


def test_process_apng_files(temp_folder):
    input_folder = temp_folder / "input"
    output_folder = temp_folder / "output"

    apng_file = input_folder / "test1.apng"
    non_apng_file = input_folder / "test.txt"

    input_folder.mkdir()
    apng_file.touch()
    non_apng_file.touch()

    with (
        patch("apng_to_png.apng_to_png.extract_frames") as mock_extract_frames,
        patch(
            "apng_to_png.apng_to_png.ensure_folder_exists"
        ) as mock_ensure_folder_exists,
    ):
        process_apng_files(input_folder, output_folder)

        # Ensure output folder creation was attempted
        mock_ensure_folder_exists.assert_called_once_with(output_folder)

        # Ensure extract_frames was called only for the APNG file
        mock_extract_frames.assert_called_once_with(apng_file, output_folder / "test1")

        # Ensure non-APNG files are ignored
        assert mock_extract_frames.call_count == 1
