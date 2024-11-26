import torch
import numpy as np
import cv2
import networkx as nx
from scipy.spatial.distance import pdist, squareform
from skimage.morphology import skeletonize
import comfy
import folder_paths
import nodes

class MaskConnectMST:
    """
    MaskConnectMST is a custom node for ComfyUI designed to connect disconnected regions within a binary mask
    using the Minimum Spanning Tree (MST) approach. Additionally, it supports an optional split_mask to divide
    the primary mask into smaller sections (islands) for VRAM conservation by processing each section individually.
    An optional skeletonization step can further refine the connections.

    ## Features:
    - **Connect Disconnected Regions:** Utilizes MST to establish minimal connections between separated mask regions.
    - **Mask Splitting:** Optionally splits the primary mask into smaller sections based on a secondary split_mask to manage VRAM usage efficiently.
    - **Skeletonization:** Optionally skeletonizes the connected mask to produce refined, thin connections.

    ## Usage:
    - **Inputs:**
        - `mask` (MASK): The primary binary mask to process.
        - `to_skeletonize` (BOOLEAN): Flag to enable or disable skeletonization of the connected mask.
        - `line_thickness` (INT): Thickness of the connecting lines.
        - `split_mask` (MASK, optional): Secondary mask defining how to split the primary mask into sections.
    - **Output:**
        - Returns a processed mask with connected regions, maintaining the same shape as input.

    ## Example:
    ```python
    processed_mask = MaskConnectMST.connect_with_mst(
        mask=primary_mask_tensor,
        to_skeletonize=True,
        line_thickness=2,
        split_mask=secondary_split_mask_tensor
    )
    ```
    """

    # Define a display name for better identification in the UI
    display_name = "Mask Connect MST"

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the input types for the node. 'mask', 'to_skeletonize', and 'line_thickness' are required inputs.
        'split_mask' is an optional input that defines how to split the primary mask into sections.
        """
        return {
            "required": {
                "mask": ("MASK",),  # Primary binary mask to process
                "to_skeletonize": ("BOOLEAN", {  # Boolean flag to enable/disable skeletonization
                    "default": False,
                    "label_on": "Enable Skeletonization",
                    "label_off": "Disable Skeletonization",
                    "tooltip": "Enable skeletonization of the connected mask."
                }),
                "line_thickness": ("INT", {  # Thickness of the connecting lines
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "tooltip": "Thickness of the connecting lines."
                }),
            },
            "optional": {
                "split_mask": ("MASK",),  # Optional secondary mask to define splitting into sections
            }
        }

    RETURN_TYPES = ("MASK",)  # Defines the output type
    FUNCTION = "connect_with_mst"  # Specifies the method to be called
    CATEGORY = "GR85/Mask"  # Category under which the node will appear in ComfyUI

    @staticmethod
    def connect_with_mst(mask, to_skeletonize=False, line_thickness=1, split_mask=None):
        """
        Connects disconnected regions in a binary mask using the Minimum Spanning Tree (MST) approach.
        Optionally splits the mask into sections based on a split_mask, processes each section individually,
        and merges them back into a single mask. An optional skeletonization step can refine the connections.

        Parameters:
            mask (torch.Tensor): Primary input mask tensor with shape (1, H, W), (C, H, W), (Batch, C, H, W), or (H, W).
            to_skeletonize (bool): If True, skeletonizes the connected lines after MST connections.
            line_thickness (int): Thickness of the connecting lines drawn based on MST.
            split_mask (torch.Tensor, optional): Secondary mask defining how to split the primary mask into sections.
                                                 Must have the same dimensions as 'mask'. Defaults to None.

        Returns:
            torch.Tensor: Processed mask tensor with connected regions, maintaining the same shape as input.
        """
        # Debug: Log the shapes and data types of the input masks
        print(f"[MaskConnectMST] Input mask shape: {mask.shape}, dtype: {mask.dtype}")
        if split_mask is not None:
            print(f"[MaskConnectMST] Split mask shape: {split_mask.shape}, dtype: {split_mask.dtype}")
        else:
            print(f"[MaskConnectMST] No split_mask provided. Processing entire mask.")

        # Ensure the primary mask is on CPU and detached from any computation graph
        mask_cpu = mask.detach().cpu()

        # Convert the primary mask to a NumPy array based on its dimensions
        if mask_cpu.ndim == 4:
            # Assuming shape (Batch, C, H, W)
            if mask_cpu.size(0) == 1 and mask_cpu.size(1) == 1:
                mask_np = mask_cpu.squeeze(0).squeeze(0).numpy()
                print(f"[MaskConnectMST] Squeezed mask shape from 4D: {mask_np.shape}")
            else:
                raise ValueError(f"[MaskConnectMST] Unsupported mask shape: {mask_cpu.shape} (Batch and Channel dimensions must be 1)")
        elif mask_cpu.ndim == 3:
            # Assuming shape (C, H, W), where C=1 for grayscale
            if mask_cpu.size(0) == 1:
                mask_np = mask_cpu.squeeze(0).numpy()
                print(f"[MaskConnectMST] Squeezed mask shape from 3D: {mask_np.shape}")
            else:
                raise ValueError(f"[MaskConnectMST] Unsupported mask shape: {mask_cpu.shape} (Channel dimension must be 1)")
        elif mask_cpu.ndim == 2:
            # Shape (H, W)
            mask_np = mask_cpu.numpy()
            print(f"[MaskConnectMST] Mask shape: {mask_np.shape}")
        else:
            raise ValueError(f"[MaskConnectMST] Unsupported mask dimensions: {mask_cpu.ndim}")

        # Initialize split_mask_np as None
        split_mask_np = None

        # Process the split_mask if provided
        if split_mask is not None:
            # Ensure the split_mask is on CPU and detached
            split_mask_cpu = split_mask.detach().cpu()

            # Handle different dimensions of split_mask
            if split_mask_cpu.ndim == 4:
                # Assuming shape (Batch, C, H, W)
                if split_mask_cpu.size(0) == 1 and split_mask_cpu.size(1) == 1:
                    split_mask_np = split_mask_cpu.squeeze(0).squeeze(0).numpy()
                    print(f"[MaskConnectMST] Squeezed split mask shape from 4D: {split_mask_np.shape}")
                else:
                    raise ValueError(f"[MaskConnectMST] Unsupported split_mask shape: {split_mask_cpu.shape} (Batch and Channel dimensions must be 1)")
            elif split_mask_cpu.ndim == 3:
                # Assuming shape (C, H, W), where C=1 for grayscale
                if split_mask_cpu.size(0) == 1:
                    split_mask_np = split_mask_cpu.squeeze(0).numpy()
                    print(f"[MaskConnectMST] Squeezed split mask shape from 3D: {split_mask_np.shape}")
                else:
                    raise ValueError(f"[MaskConnectMST] Unsupported split_mask shape: {split_mask_cpu.shape} (Channel dimension must be 1)")
            elif split_mask_cpu.ndim == 2:
                # Shape (H, W)
                split_mask_np = split_mask_cpu.numpy()
                print(f"[MaskConnectMST] Split mask shape: {split_mask_np.shape}")
            else:
                raise ValueError(f"[MaskConnectMST] Unsupported split_mask dimensions: {split_mask_cpu.ndim}")

            # Validate that both masks have the same dimensions
            if mask_np.shape != split_mask_np.shape:
                raise ValueError(f"[MaskConnectMST] 'mask' and 'split_mask' must have the same dimensions. "
                                 f"Got mask: {mask_np.shape}, split_mask: {split_mask_np.shape}")

            # Convert split_mask to binary (0 and 255)
            binary_split_mask = (split_mask_np > 0).astype(np.uint8) * 255
            print(f"[MaskConnectMST] Binary split mask created with shape: {binary_split_mask.shape}")

        # Convert the primary mask to binary (0 and 255)
        binary_mask = (mask_np > 0).astype(np.uint8) * 255
        print(f"[MaskConnectMST] Binary mask created with shape: {binary_mask.shape}")

        if split_mask_np is not None:
            # Process the mask in sections defined by split_mask
            # Step 1: Find connected components in split_mask to define sections
            num_sections, section_labels = cv2.connectedComponents(binary_split_mask)
            print(f"[MaskConnectMST] Number of sections found in split_mask: {num_sections - 1}")  # Exclude background

            if num_sections <= 1:
                # If only background is present in split_mask, process the entire mask as a single section
                print("[MaskConnectMST] Only background found in split_mask. Processing entire mask.")
                processed_mask = MaskConnectMST.process_section(binary_mask, to_skeletonize, line_thickness)
            else:
                # Initialize an empty canvas to accumulate processed sections
                processed_mask = np.zeros_like(binary_mask)

                # Iterate through each section (connected component) in split_mask
                for section in range(1, num_sections):  # Start from 1 to exclude background
                    # Create a mask for the current section by isolating its pixels
                    section_mask = np.where(section_labels == section, binary_mask, 0).astype(np.uint8)
                    section_size = np.sum(section_mask > 0)
                    print(f"[MaskConnectMST] Processing section {section} with size: {section_size} pixels")

                    if section_size == 0:
                        # Skip empty sections
                        print(f"[MaskConnectMST] Section {section} is empty. Skipping.")
                        continue

                    # Apply MST-based connectivity to the current section
                    connected_section = MaskConnectMST.process_section(section_mask, to_skeletonize, line_thickness)

                    # Merge the processed section back into the main processed_mask at the same position
                    processed_mask = cv2.bitwise_or(processed_mask, connected_section)
                    print(f"[MaskConnectMST] Section {section} connected and merged.")
        else:
            # If no split_mask is provided, process the entire mask as a single section
            processed_mask = MaskConnectMST.process_section(binary_mask, to_skeletonize, line_thickness)

        # Optional Skeletonization:
        # If split_mask was not provided and skeletonization is enabled, apply skeletonization to the entire mask
        if split_mask_np is None and to_skeletonize:
            processed_mask = skeletonize(processed_mask > 0).astype(np.uint8) * 255
            print("[MaskConnectMST] Applied skeletonization to the entire connected mask.")

        # Convert the processed mask back to a PyTorch tensor
        # The shape is (1, H, W) to maintain consistency with input
        binary_mask_tensor = torch.from_numpy(processed_mask).float().unsqueeze(0).to(mask.device)
        print(f"[MaskConnectMST] Output tensor shape: {binary_mask_tensor.shape}, dtype: {binary_mask_tensor.dtype}")

        return (binary_mask_tensor, )

    @staticmethod
    def process_section(section_mask, to_skeletonize, line_thickness):
        """
        Processes a single section of the mask by connecting its regions using MST and optionally skeletonizing.

        Parameters:
            section_mask (np.ndarray): Binary mask of the section to process.
            to_skeletonize (bool): If True, skeletonizes the connected mask after MST connections.
            line_thickness (int): Thickness of the connecting lines drawn based on MST.

        Returns:
            np.ndarray: Processed section mask with connected regions.
        """
        # Debug: Log the number of connected components in the section
        num_labels, labels = cv2.connectedComponents(section_mask)
        print(f"[MaskConnectMST] Section has {num_labels - 1} connected components.")

        if num_labels <= 2:
            # If only background and one region are present, return the section as is
            print("[MaskConnectMST] Only one connected component in section. Returning section as is.")
            return section_mask

        # Step 1: Calculate centroids of each connected component within the section
        centroids = []
        for i in range(1, num_labels):  # Start from 1 to exclude background
            y, x = np.where(labels == i)
            if len(x) == 0 or len(y) == 0:
                # Skip empty components
                continue
            centroid = (np.mean(x), np.mean(y))
            centroids.append(centroid)
            print(f"[MaskConnectMST] Centroid {i}: {centroid}")

        if len(centroids) < 2:
            # Not enough centroids to form an MST; return the section as is
            print("[MaskConnectMST] Not enough centroids to form MST in section. Returning section as is.")
            return section_mask

        # Step 2: Create a graph where each centroid is a node
        distances = pdist(centroids)  # Compute pairwise Euclidean distances between centroids
        distance_matrix = squareform(distances)
        graph = nx.Graph()
        for idx, centroid in enumerate(centroids):
            graph.add_node(idx, pos=centroid)
            print(f"[MaskConnectMST] Added node {idx} to graph with position {centroid}")

        # Step 3: Add edges between all pairs of nodes with weights equal to their Euclidean distances
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                graph.add_edge(i, j, weight=distance_matrix[i, j])
                print(f"[MaskConnectMST] Added edge ({i}, {j}) with weight {distance_matrix[i, j]:.2f}")

        # Step 4: Compute the Minimum Spanning Tree (MST) of the graph
        mst = nx.minimum_spanning_tree(graph)
        print(f"[MaskConnectMST] MST for section has {mst.number_of_edges()} edges.")

        # Step 5: Draw lines between centroids based on the MST edges
        for edge in mst.edges():
            start_centroid = centroids[edge[0]]
            end_centroid = centroids[edge[1]]

            # Convert centroids to integer pixel coordinates
            start = (int(round(start_centroid[0])), int(round(start_centroid[1])))
            end = (int(round(end_centroid[0])), int(round(end_centroid[1])))

            # Clamp coordinates to be within image bounds
            height, width = section_mask.shape
            start_clamped = (max(0, min(start[0], width - 1)), max(0, min(start[1], height - 1)))
            end_clamped = (max(0, min(end[0], width - 1)), max(0, min(end[1], height - 1)))

            # Draw the connecting line on the section_mask
            cv2.line(section_mask, start_clamped, end_clamped, color=255, thickness=line_thickness)
            print(f"[MaskConnectMST] Drew line from {start_clamped} to {end_clamped} with thickness {line_thickness}")

        # Optional Skeletonization:
        # If enabled, apply skeletonization to the connected section to refine the connections
        if to_skeletonize:
            section_mask = skeletonize(section_mask > 0).astype(np.uint8) * 255
            print("[MaskConnectMST] Applied skeletonization to the section mask.")

        return section_mask
