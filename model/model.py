"""
Text detection and highlighting using EasyOCR and OpenCV.
Detects text in icons and draws green rectangles around detected text regions.
Compatible with DearPyGui for desktop application integration.
"""

from dataclasses import dataclass

import cv2
import easyocr
import numpy as np


@dataclass
class TextureResult:
    """Result containing texture data for DearPyGui and detected text."""

    texture_data: list[float]
    width: int
    height: int
    detected_text: str


@dataclass
class HighlightOptions:
    """Options for highlighting detected text."""

    line_color: tuple[int, int, int] = (0, 255, 0)
    line_thickness: int = 2
    show_result: bool = False


class Model:
    """A class for detecting and highlighting text in icons using EasyOCR."""

    def __init__(
        self,
        languages: list[str] | None = None,
        use_gpu: bool = False,
    ) -> None:
        """
        Initialize the TextDetector.

        Args:
            languages: List of languages to detect (e.g., ['en', 'pl']).
                       Defaults to ['en'] if not specified.
            use_gpu: Whether to use GPU for OCR processing.
        """
        if languages is None:
            languages = ["en"]

        self.languages = languages
        self.reader = easyocr.Reader(languages, gpu=use_gpu)

    def detect(self, image_path: str) -> list[tuple[list, str, float]]:
        """
        Detect text in an image.

        Args:
            image_path: Path to the input image.

        Returns:
            List of tuples containing (bounding_box, text, confidence).
        """
        image = cv2.imread(image_path)  # pylint: disable=no-member
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        return self.reader.readtext(image)

    def detect_and_highlight(
        self,
        image_path: str,
        output_path: str | None = None,
        options: HighlightOptions | None = None,
    ) -> list[tuple[list, str, float]]:
        """
        Detect text in an image and draw polylines around detected text.

        Args:
            image_path: Path to the input image.
            output_path: Path to save the output image. If None, won't save.
            options: HighlightOptions for customizing the output.

        Returns:
            List of tuples containing (bounding_box, text, confidence).
        """
        if options is None:
            options = HighlightOptions()

        image = cv2.imread(image_path)  # pylint: disable=no-member
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        results = self.reader.readtext(image)

        # Draw polylines around detected text
        for bbox, _, _ in results:
            points = np.array(bbox, dtype=np.int32)
            cv2.polylines(  # pylint: disable=no-member
                image,
                [points],
                isClosed=True,
                color=options.line_color,
                thickness=options.line_thickness,
            )

        if output_path:
            cv2.imwrite(output_path, image)  # pylint: disable=no-member
            print(f"Result saved to: {output_path}")

        if options.show_result:
            cv2.imshow("Text Detection Result", image)  # pylint: disable=no-member
            cv2.waitKey(0)  # pylint: disable=no-member
            cv2.destroyAllWindows()  # pylint: disable=no-member

        return results

    def print_results(self, results: list[tuple[list, str, float]]) -> None:
        """
        Print detected text with confidence scores.

        Args:
            results: List of detection results from detect() or detect_and_highlight().
        """
        print("\n--- Detected Text ---")
        for i, (_, text, confidence) in enumerate(results, 1):
            print(f"{i}. Text: '{text}' (Confidence: {confidence:.2%})")
        print("---------------------\n")

    def _group_text_by_lines(
        self,
        results: list[tuple[list, str, float]],
        line_threshold: float = 0.5,
    ) -> str:
        """
        Group detected text into lines based on vertical position.

        Args:
            results: List of OCR results (bounding_box, text, confidence).
            line_threshold: Threshold for grouping text into same line.
                            Expressed as a fraction of average text height.

        Returns:
            Text grouped by lines, with lines separated by newlines.
        """
        if not results:
            return ""

        text_items = self._extract_text_positions(results)
        avg_height = np.mean([item["height"] for item in text_items])
        y_threshold = avg_height * line_threshold

        lines = self._group_items_into_lines(text_items, y_threshold)

        return self._join_lines(lines)

    def _extract_text_positions(
        self,
        results: list[tuple[list, str, float]],
    ) -> list[dict]:
        """Extract text with position info from OCR results."""
        text_items: list[dict] = []
        for bbox, text, _ in results:
            points = np.array(bbox)
            text_items.append({
                "text": text,
                "center_y": np.mean(points[:, 1]),
                "left_x": np.min(points[:, 0]),
                "height": np.max(points[:, 1]) - np.min(points[:, 1]),
            })
        return text_items

    def _group_items_into_lines(
        self,
        text_items: list[dict],
        y_threshold: float,
    ) -> list[list[dict]]:
        """Group text items into lines based on vertical proximity."""
        text_items.sort(key=lambda item: item["center_y"])

        lines: list[list[dict]] = []
        current_line: list[dict] = [text_items[0]]

        for item in text_items[1:]:
            if abs(item["center_y"] - current_line[0]["center_y"]) <= y_threshold:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]
        lines.append(current_line)

        return lines

    def _join_lines(self, lines: list[list[dict]]) -> str:
        """Sort each line by horizontal position and join into string."""
        result_lines: list[str] = []
        for line in lines:
            line.sort(key=lambda item: item["left_x"])
            line_text = " ".join(item["text"] for item in line)
            result_lines.append(line_text)
        return "\n".join(result_lines)

    def get_texture_data(
        self,
        image_path: str,
        line_color: tuple[int, int, int] = (0, 255, 0),
        line_thickness: int = 2,
        line_threshold: float = 0.5,
    ) -> TextureResult:
        """
        Detect text and return texture data compatible with DearPyGui.

        The texture data is a flat list of floats (RGBA values normalized to 0-1)
        that can be used directly with dpg.add_static_texture().

        Text is automatically grouped into lines based on vertical position,
        making it suitable for reading documents and books.

        Args:
            image_path: Path to the input image.
            line_color: BGR color tuple for the polylines. Defaults to green.
            line_thickness: Thickness of the polylines.
            line_threshold: Threshold for grouping text into same line.

        Returns:
            TextureResult containing texture_data, width, height, and detected_text.
        """
        image = cv2.imread(image_path)  # pylint: disable=no-member
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        results = self.reader.readtext(image)
        image = self._draw_polylines(image, results, line_color, line_thickness)
        texture_data, width, height = self._convert_to_texture(image)
        combined_text = self._group_text_by_lines(results, line_threshold)

        return TextureResult(
            texture_data=texture_data,
            width=width,
            height=height,
            detected_text=combined_text,
        )

    def _draw_polylines(
        self,
        image: np.ndarray,
        results: list[tuple[list, str, float]],
        line_color: tuple[int, int, int],
        line_thickness: int,
    ) -> np.ndarray:
        """Draw polylines around detected text regions."""
        for bbox, _, _ in results:
            points = np.array(bbox, dtype=np.int32)
            cv2.polylines(  # pylint: disable=no-member
                image,
                [points],
                isClosed=True,
                color=line_color,
                thickness=line_thickness,
            )
        return image

    def _convert_to_texture(
        self,
        image: np.ndarray,
    ) -> tuple[list[float], int, int]:
        """Convert BGR image to RGBA texture data for DearPyGui."""
        # pylint: disable=no-member
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        height, width = image_rgba.shape[:2]
        texture_data = (image_rgba.astype(np.float32) / 255.0).flatten().tolist()
        return texture_data, width, height