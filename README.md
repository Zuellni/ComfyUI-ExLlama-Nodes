# ComfyUI ExLlama Nodes
A simple text generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlamaV2](https://github.com/turboderp/exllamav2).

## Installation
Clone the repository to `custom_nodes` and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r requirements.txt
```
Optionally, you can install [flash-attention](https://github.com/Dao-AILab/flash-attention) by uncommenting the relevant lines in the requirements file.
If you see any ExLlama-related errors while loading the nodes, install it manually following the instructions [here](https://github.com/turboderp/exllamav2#method-2-install-from-release-with-prebuilt-extension).

## Usage
ExLlamaV2 supports EXL2 and 4-bit GPTQ models. You can find a lot of them on [Hugging Face](https://huggingface.co/TheBloke).
Refer to the model card in each repository for details about quant differences and instruction formats.

To use a model with the nodes, you should clone its repository with git or manually download all the files and place them in `models/llm`.
You can also add your own `llm` path to [extra_model_paths.yaml](https://github.com/comfyanonymous/ComfyUI/blob/master/extra_model_paths.yaml.example) and place the models there instead.

For instance, if you want to download the 4-bit 32g branch of [Zephyr 7B Beta](https://huggingface.co/TheBloke/zephyr-7B-beta-GPTQ), use the following command:
```
git clone https://huggingface.co/TheBloke/zephyr-7B-beta-GPTQ -b gptq-4bit-32g-actorder_True models/llm/zephyr-7b-gptq-32g
```

## Nodes
Name | Description
:--- | :---
Loader | Used to load EXL2/GPTQ Llama models.
Generator | Generates a `string` based on the given input.
Preview | Displays generated outputs in the UI.
Replace | Replaces variables enclosed in brackets, such as `[a]`, with their values.

## Workflow
The image below can be opened in ComfyUI.

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/cb20b040-9856-4dab-aed0-4b318bc2d805)
