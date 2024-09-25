import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "GR85.FluxAttentionSeeker2",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (!nodeData?.category?.startsWith("GR85")) {
      return;
    }

    if (nodeData.name === "FluxAttentionSeeker2") {
      const onCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        // Call the original onNodeCreated if it exists
        if (onCreated) {
          onCreated.apply(this);
        }

        // Add buttons for CLIP layers
        this.addWidget("button", "RESET CLIP LAYERS", null, () => {
          this.widgets.forEach(w => {
            if (w.type === "slider" && w.name.startsWith('clip_l')) {
              w.value = 1.0;
              w.callback(w.value);
            }
          });
        });

        this.addWidget("button", "ZERO CLIP LAYERS", null, () => {
          this.widgets.forEach(w => {
            if (w.type === "slider" && w.name.startsWith('clip_l')) {
              w.value = 0.0;
              w.callback(w.value);
            }
          });
        });

        this.addWidget("button", "REPEAT FIRST CLIP LAYER", null, () => {
          var clip_value = undefined;
          this.widgets.forEach(w => {
            if (w.type === "slider" && w.name.startsWith('clip_l')) {
              if (clip_value === undefined) {
                clip_value = w.value;
              }
              w.value = clip_value;
              w.callback(w.value);
            }
          });
        });
      };
    }
  },
});
