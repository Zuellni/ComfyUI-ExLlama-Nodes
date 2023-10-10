import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "ZuellniTextPreview",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "ZuellniTextPreview") {
			const onExecuted = nodeType.prototype.onExecuted;

			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);

				if (this.widgets) {
					const position = this.widgets.findIndex((w) => w.name === "text");

					if (position !== -1) {
						for (let i = position; i < this.widgets.length; i++) {
							this.widgets[i].onRemove?.();
						}
						this.widgets.length = position;
					}

					const type = ["STRING", { multiline: true }];
					const widget = ComfyWidgets["STRING"](this, "text", type, app).widget;

					widget.inputEl.readOnly = true;
					widget.inputEl.style.opacity = 0.7;
					widget.value = message.text;
				}
			};
		}
	},
});
