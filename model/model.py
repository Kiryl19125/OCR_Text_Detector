"""
Text detection and highlighting using EasyOCR and OpenCV.
Detects text in images and draws green rectangles around detected text regions.
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


class Model:
    """A class for detecting and highlighting text in images using EasyOCR."""

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
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        return self.reader.readtext(image)

    def detect_and_highlight(
        self,
        image_path: str,
        output_path: str | None = None,
        line_color: tuple[int, int, int] = (0, 255, 0),
        line_thickness: int = 2,
        show_result: bool = False,
    ) -> list[tuple[list, str, float]]:
        """
        Detect text in an image and draw polylines around detected text.

        Args:
            image_path: Path to the input image.
            output_path: Path to save the output image. If None, won't save.
            line_color: BGR color tuple for the polylines. Defaults to green.
            line_thickness: Thickness of the polylines.
            show_result: Whether to display the result in a window.

        Returns:
            List of tuples containing (bounding_box, text, confidence).
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        results = self.reader.readtext(image)

        # Draw polylines around detected text
        for bbox, text, confidence in results:
            points = np.array(bbox, dtype=np.int32)
            cv2.polylines(
                image,
                [points],
                isClosed=True,
                color=line_color,
                thickness=line_thickness,
            )

        if output_path:
            cv2.imwrite(output_path, image)
            print(f"Result saved to: {output_path}")

        if show_result:
            cv2.imshow("Text Detection Result", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return results

    def print_results(self, results: list[tuple[list, str, float]]) -> None:
        """
        Print detected text with confidence scores.

        Args:
            results: List of detection results from detect() or detect_and_highlight().
        """
        print("\n--- Detected Text ---")
        for i, (bbox, text, confidence) in enumerate(results, 1):
            print(f"{i}. Text: '{text}' (Confidence: {confidence:.2%})")
        print("---------------------\n")

    def get_texture_data(
        self,
        image_path: str,
        line_color: tuple[int, int, int] = (0, 255, 0),
        line_thickness: int = 2,
        text_separator: str = "\n",
    ) -> TextureResult:
        """
        Detect text and return texture data compatible with DearPyGui.

        The texture data is a flat list of floats (RGBA values normalized to 0-1)
        that can be used directly with dpg.add_static_texture() or dpg.add_dynamic_texture().

        Args:
            image_path: Path to the input image.
            line_color: BGR color tuple for the polylines. Defaults to green.
            line_thickness: Thickness of the polylines.
            text_separator: Separator for joining detected text strings.

        Returns:
            TextureResult containing texture_data, width, height, and detected_text.

        Example usage with DearPyGui:
            result = detector.get_texture_data("image.png")

            with dpg.texture_registry():
                dpg.add_static_texture(
                    width=result.width,
                    height=result.height,
                    default_value=result.texture_data,
                    tag="ocr_texture"
                )

            with dpg.window(label="OCR Result"):
                dpg.add_image("ocr_texture")
                dpg.add_text(result.detected_text)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        results = self.reader.readtext(image)

        # Draw polylines around detected text
        for bbox, text, confidence in results:
            points = np.array(bbox, dtype=np.int32)
            cv2.polylines(
                image,
                [points],
                isClosed=True,
                color=line_color,
                thickness=line_thickness,
            )

        # Convert BGR to RGBA
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

        # Get dimensions
        height, width = image_rgba.shape[:2]

        # Normalize to 0-1 range and flatten for DearPyGui
        texture_data = (image_rgba.astype(np.float32) / 255.0).flatten().tolist()

        # Extract detected text
        detected_texts = [text for bbox, text, confidence in results]
        combined_text = text_separator.join(detected_texts)

        return TextureResult(
            texture_data=texture_data,
            width=width,
            height=height,
            detected_text=combined_text,
        )