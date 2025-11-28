from comfy_api.latest import io


class SeedBasedOutputSelector(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GR85_SeedBasedOutputSelector",
            display_name="Seed Based Output Selector",
            category="GR85/Prompt/Selection",
            inputs=[
                io.Int.Input(
                    "seed_number",
                    default=0,
                    min=0,
                    max=0xFFFFFFFFFFFFFFFF,
                ),
                io.String.Input("input_1", default=""),
                io.String.Input("input_2", default=""),
                io.String.Input("input_3", default=""),
                io.String.Input("input_4", default=""),
                io.String.Input("input_5", default=""),
                io.String.Input("input_6", default=""),
                io.String.Input("input_7", default=""),
                io.String.Input("input_8", default=""),
                io.String.Input("input_9", default=""),
                io.String.Input("input_10", default=""),
            ],
            outputs=[
                io.String.Output(),
            ],
        )

    @classmethod
    def execute(
        cls,
        seed_number: int,
        input_1: str = "",
        input_2: str = "",
        input_3: str = "",
        input_4: str = "",
        input_5: str = "",
        input_6: str = "",
        input_7: str = "",
        input_8: str = "",
        input_9: str = "",
        input_10: str = "",
    ) -> io.NodeOutput:
        """Select an output based on the seed number and available non-null inputs."""

        inputs = [
            input_1,
            input_2,
            input_3,
            input_4,
            input_5,
            input_6,
            input_7,
            input_8,
            input_9,
            input_10,
        ]

        # Treat both None and empty strings as "no value" for optional inputs
        non_empty_inputs = [value for value in inputs if value not in (None, "")]
        num_outputs = len(non_empty_inputs)

        if num_outputs == 0:
            return io.NodeOutput("")

        output_index = seed_number % num_outputs
        final_output = non_empty_inputs[output_index]

        return io.NodeOutput(final_output)
