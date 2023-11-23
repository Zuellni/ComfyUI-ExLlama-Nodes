# ComfyUI ExLlama Nodes
A simple text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r requirements.txt
```

Optionally, you can install [flash-attention](https://github.com/Dao-AILab/flash-attention) by uncommenting the relevant lines in the requirements file.<br>If you see any ExLlama-related errors while loading, install it manually following the instructions from [here](https://github.com/turboderp/exllamav2#method-2-install-from-release-with-prebuilt-extension).

## Nodes
Name | Description
:--- | :---
Loader | Used to load EXL2/GPTQ Llama models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke).<br>Clone the model repository and place it in `models/llm` or specify your own `llm` path in `extra_model_paths.yaml`.
Generator | Generates a `string` based on the given input for use with other nodes.
Preview | Displays generated outputs in the UI.
Replace | Replaces variables enclosed in brackets, such as `[a]`, with their values.

## Workflow
The image below can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/cb20b040-9856-4dab-aed0-4b318bc2d805)
