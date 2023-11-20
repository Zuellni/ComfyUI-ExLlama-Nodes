import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "ZuellniText",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "ZuellniTextPreview") {
			nodeType.prototype.onExecuted = function(message) {
				if (this.widgets) {
					const index = this.widgets.findIndex((w) => w.name === "output");

					if (index !== -1) {
						for (let i = index; i < this.widgets.length; i++)
							this.widgets[i].onRemove?.();

						this.widgets.length = index;
					}

					this.widgets.length = 1;
					const options = ["STRING", {multiline: true }]
					const widget = ComfyWidgets["STRING"](this, "output", options, app).widget;
					widget.inputEl.readOnly = true;
					widget.inputEl.style.opacity = 0.7;
					widget.value = message.text;
				}
			};
		}
	},
});
