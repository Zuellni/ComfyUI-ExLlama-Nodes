import { app } from "../../../scripts/app.js"

app.registerExtension({
	name: "ZuellniText",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.category != "Zuellni/Text")
			return

		const onNodeCreated = nodeType.prototype.onNodeCreated
		const onExecuted = nodeType.prototype.onExecuted

		if (nodeData.name == "ZuellniTextPreview") {
			nodeType.prototype.onNodeCreated = function () {
				const output = this.widgets.find(w => w.name == "output")

				if (output) {
					output.inputEl.placeholder = ""
					output.inputEl.readOnly = true
					output.inputEl.style.cursor = "default"
					output.inputEl.style.opacity = 0.7
				}

				this.setSize(this.computeSize())
				return onNodeCreated?.apply(this, arguments)
			}

			nodeType.prototype.onExecuted = function (message) {
				const output = this.widgets.find(w => w.name == "output")
				output && (output.value = message.text)
				return onExecuted?.apply(this, arguments)
			}
		} else if (nodeData.name == "ZuellniTextReplace") {
			nodeType.prototype.onNodeCreated = function () {
				const count = this.widgets.find(w => w.name == "count")

				if (count) {
					count.callback = () => this.onChanged(count.value)
					this.onChanged(count.value)
				}

				return onNodeCreated?.apply(this, arguments)
			}

			nodeType.prototype.onChanged = function (count) {
				!this.inputs && (this.inputs = [])
				const current = this.inputs.length

				if (current == count)
					return

				if (current < count)
					for (let i = current; i < count; i++)
						this.addInput(String.fromCharCode(i + 97), "STRING")
				else
					for (let i = current - 1; i >= count; i--)
						this.removeInput(i)
			}
		}
	}
})
