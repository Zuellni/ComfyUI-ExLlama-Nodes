// Copied from https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/web/js/showText.js

import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "Zuellni.ExLlama.Generator",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "ZuellniExLlamaGenerator") {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);

				if (this.widgets) {
					const pos = this.widgets.findIndex((w) => w.name === "text");

					if (pos !== -1) {
						for (let i = pos; i < this.widgets.length; i++) {
							this.widgets[i].onRemove?.();
						}

						this.widgets.length = pos;
					}

					const string = ["STRING", { multiline: true }]
					const widget = ComfyWidgets["STRING"](this, "text", string, app).widget;

					widget.inputEl.readOnly = true;
					widget.inputEl.style.opacity = 0.7;
					widget.value = message.text;

					requestAnimationFrame(() => {
						const size = this.computeSize();

						if (size[0] < this.size[0]) {
							size[0] = this.size[0];
						}

						if (size[1] < this.size[1]) {
							size[1] = this.size[1];
						}

						this.onResize?.(size);
						app.graph.setDirtyCanvas(true, false);
					});
				}
			};
		}
	},
});
