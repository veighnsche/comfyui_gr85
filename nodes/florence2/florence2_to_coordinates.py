import json
from typing import Tuple, List, Dict, Any, Optional


class Florence2toCoordinatesGR85:
    """
    Converts JSON data containing bounding boxes into center coordinates,
    optionally filtering out bounding boxes that are too large relative to the image dimensions.

    Inputs:
        - data (STRING): JSON string representing bounding boxes.
        - index (STRING): Comma-separated indices indicating which bounding boxes to process (default "0").
        - batch (BOOLEAN): If True, processes all data in batch mode (default False).
        - image_width (INT, optional): Width of the image in pixels.
        - image_height (INT, optional): Height of the image in pixels.
        - max_bbox_area_percentage (FLOAT, optional): Maximum allowed area of a bounding box as a percentage of the image area.

    Outputs:
        - center_coordinates (STRING): JSON string of extracted center coordinates.
        - bboxes (LIST): List of processed bounding boxes.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("JSON",),  # Accept JSON objects (which are parsed to lists in Python)
                "index": ("STRING", {"default": "0"}),
                "batch": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image_width": ("INT", {"default": None, "min": 1, "max": 10000, "step": 1}),
                "image_height": ("INT", {"default": None, "min": 1, "max": 10000, "step": 1}),
                "max_bbox_area_percentage": ("FLOAT", {"default": 90.0, "min": 0.0, "max": 100.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("STRING", "BBOX")  # Aligned with source class
    RETURN_NAMES = ("center_coordinates", "bboxes")
    FUNCTION = "segment"
    CATEGORY = "GR85/Florence2"


    def log(self, message: str, data: Any = None):
        """
        Logs messages with an optional data payload.
        """
        print(f"[Florence2toCoordinatesGR85]: {message}")
        if data is not None:
            print(f"  -> Data: {data}")


    def segment(
            self,
            data,
            index,
            batch=False,
            image_width=None,
            image_height=None,
            max_bbox_area_percentage=90.0
    ) -> Tuple[Optional[str], Optional[List[List[float]]]]:
        """
        Processes data containing bounding boxes to extract center coordinates,
        optionally filtering out bounding boxes that are too large,
        and computes centroids based on geometric calculations.

        Args:
            data: List of bounding boxes or JSON string representing bounding boxes.
            index: Comma-separated indices indicating which bounding boxes to process.
            batch: If True, processes all data in batch mode.
            image_width: Width of the image in pixels.
            image_height: Height of the image in pixels.
            max_bbox_area_percentage: Maximum allowed area of a bounding box as a percentage of the image area.

        Returns:
            Tuple[Optional[str], Optional[List[List[float]]]]: A tuple containing a JSON string of center coordinates and a list of bounding boxes.
        """
        self.log("Execution started.")

        # Check if data is a string or a list
        if isinstance(data, str):
            # Sanitize and parse JSON data
            try:
                sanitized_data = data.replace("'", '"')  # Replace single quotes with double quotes
                data_parsed = json.loads(sanitized_data)
                self.log("Parsed data successfully.", data_parsed)
            except json.JSONDecodeError:
                self.log("Invalid JSON data provided.")
                raise ValueError("Invalid JSON data provided.")
            except Exception as e:
                self.log("An unexpected error occurred while parsing JSON data.", str(e))
                raise RuntimeError(f"An unexpected error occurred: {e}")
        elif isinstance(data, list):
            # Data is already a list
            data_parsed = data
            self.log("Data is already a list.", data_parsed)
        else:
            self.log("Data must be a string or a list.")
            raise TypeError("Data must be a JSON string or a list.")

        # Validate data structure
        if not isinstance(data_parsed, list) or not all(isinstance(item, list) for item in data_parsed):
            self.log("Data validation failed. Data must be a list of lists containing bounding boxes.")
            raise TypeError("Data must be a list of lists containing bounding boxes.")

        if len(data_parsed) == 0:
            self.log("Empty data received. No valid data to process.")
            return (None, None)

        # Determine indices to process
        if index.strip():
            try:
                indexes = [int(i) for i in index.split(",")]
                self.log(f"Processing specified indices: {indexes}")
            except ValueError:
                self.log("Index string must contain comma-separated integers.")
                raise ValueError("Index string must contain comma-separated integers.")
        else:
            indexes = list(range(len(data_parsed[0])))
            self.log(f"No indices specified. Processing all indices: {indexes}")

        center_points = []
        bboxes = []

        # Check if optional parameters are provided
        filter_bboxes = image_width is not None and image_height is not None

        if filter_bboxes:
            image_area = image_width * image_height
            max_bbox_area = (max_bbox_area_percentage / 100.0) * image_area
            self.log(f"Image area: {image_area}, Max BBOX area allowed: {max_bbox_area}")
        else:
            self.log("Image dimensions not provided. Skipping BBOX filtering based on size.")

        if batch:
            self.log("Batch mode enabled. Processing all data in batch.")
            for idx in indexes:
                if 0 <= idx < len(data_parsed[0]):
                    for sublist_idx, sublist in enumerate(data_parsed):
                        bbox = sublist[idx]
                        if not self._validate_bbox(bbox):
                            self.log(f"Invalid bbox format at data[{sublist_idx}][{idx}]: {bbox}")
                            continue  # Skip invalid bbox
                        if filter_bboxes:
                            bbox_area = self._calculate_bbox_area(bbox)
                            if bbox_area > max_bbox_area:
                                self.log(f"BBOX at data[{sublist_idx}][{idx}] is too large (Area: {bbox_area}). Skipping.")
                                continue  # Skip large bbox
                        center = self._calculate_center(bbox)
                        center_points.append(center)
                        bboxes.append(bbox)
                        self.log(f"Processed bbox at data[{sublist_idx}][{idx}]: {bbox} -> Center: {center}")
                else:
                    self.log(f"Index {idx} is out of range. Skipping.")
            self.log("Batch processing completed.")
        else:
            self.log("Batch mode disabled. Processing single batch.")
            for idx in indexes:
                if 0 <= idx < len(data_parsed[0]):
                    bbox = data_parsed[0][idx]
                    if not self._validate_bbox(bbox):
                        self.log(f"Invalid bbox format at data[0][{idx}]: {bbox}")
                        continue  # Skip invalid bbox
                    if filter_bboxes:
                        bbox_area = self._calculate_bbox_area(bbox)
                        if bbox_area > max_bbox_area:
                            self.log(f"BBOX at data[0][{idx}] is too large (Area: {bbox_area}). Skipping.")
                            continue  # Skip large bbox
                    center = self._calculate_center(bbox)
                    center_points.append(center)
                    bboxes.append(bbox)
                    self.log(f"Processed bbox at data[0][{idx}]: {bbox} -> Center: {center}")
                else:
                    self.log(f"Index {idx} is out of range for the bounding boxes.")
                    continue  # Skip out-of-range index
            self.log("Single batch processing completed.")

        if not center_points:
            self.log("No valid center coordinates extracted. Returning None.")
            return (None, None)

        coordinates_json = json.dumps(center_points)
        self.log("Extracted center coordinates successfully.", coordinates_json)
        return (coordinates_json, bboxes)


    def _validate_bbox(self, bbox: Any) -> bool:
        """
        Validates the bounding box format.

        Args:
            bbox (Any): The bounding box to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return isinstance(bbox, (list, tuple)) and len(bbox) == 4 and all(isinstance(coord, (int, float)) for coord in bbox)


    def _calculate_center(self, bbox: List[float]) -> Dict[str, int]:
        """
        Calculates the center coordinates of a bounding box.

        Args:
            bbox (List[float]): Bounding box in the format [min_x, min_y, max_x, max_y].

        Returns:
            Dict[str, int]: Center coordinates as {"x": center_x, "y": center_y}.
        """
        min_x, min_y, max_x, max_y = bbox
        center_x = int((min_x + max_x) / 2)
        center_y = int((min_y + max_y) / 2)
        return {"x": center_x, "y": center_y}


    def _calculate_bbox_area(self, bbox: List[float]) -> float:
        """
        Calculates the area of a bounding box.

        Args:
            bbox (List[float]): Bounding box in the format [min_x, min_y, max_x, max_y].

        Returns:
            float: Area of the bounding box.
        """
        min_x, min_y, max_x, max_y = bbox
        width = max_x - min_x
        height = max_y - min_y
        return width * height
