# ComfyUI ExLlama Nodes
A simple text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Make sure your ComfyUI is up to date. Clone the repository to `custom_nodes` and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r requirements.txt
```

If you see any ExLlama-related errors while loading, install it manually following the instructions from [here](https://github.com/turboderp/exllamav2#method-2-install-from-release-with-prebuilt-extension).

## Nodes
Name | Description
:--- | :---
Model | Used to load EXL2/GPTQ Llama models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke). Clone the model repository or download all the files in it and place them in an empty directory, then specify the path in `model_dir`. The `model.safetensors` file won't work on its own.<br><br>ExLlama allocates memory based on `max_seq_len`. Lowering it is a good way to save on VRAM.
LoRA | Used to load LoRAs. The directory should contain `adapter_model.bin` or `.safetensors` and `adapter_config.json`. LoRA parameter count has to match the model.
Generator | Generates a `string` based on the given input for use with other nodes. Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui).
Condition | Checks if the input meets some condition, interrupts processing otherwise.
Format | Replaces variables enclosed in brackets, such as `[a]`, with their values.
Preview | Displays generated outputs in the UI.

## Workflow
The image below can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/a4c980ac-281c-41fd-8fa7-b4c1d0419bea)
