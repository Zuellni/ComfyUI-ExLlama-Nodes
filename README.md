# [ExLlama](https://github.com/turboderp/exllama) nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI).

## Installation
Clone or download the repository to `custom_nodes` in your ComfyUI directory:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama
```

Install the latest ExLlama package from https://github.com/jllllll/exllama/releases. Choose the version matching your platform, Python, and PyTorch CUDA/ROCm. Example for Windows with Python 3.10 and CUDA 11.7:
```
pip install https://github.com/jllllll/exllama/releases/download/0.0.17/exllama-0.0.17+cu117-cp310-cp310-win_amd64.whl
```

## Nodes
### ExLlama Loader
Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them over at https://huggingface.co/TheBloke. Specify the model directory in `model_dir`. ExLlama allocates memory according to `max_seq_len`, setting it lower is a good way to save on VRAM. Currently it's not possible to offload the model to CPU RAM.

### ExLlama Generator
Generates a `string` based on the given `prompt` and max `tokens` for use with other nodes. Default values correspond to the `simple-1` preset from https://github.com/oobabooga/text-generation-webui. ExLlama isn't deterministic so the outputs may differ even with the same seed.

## Workflow
![example](https://github.com/Zuellni/ComfyUI-ExLlama/assets/123005779/44a85d68-387d-438b-bef7-3c3409ce21e8)

The example above can be loaded in ComfyUI. Model used: https://huggingface.co/TheBloke/MythoLogic-Mini-7B-GPTQ. Total VRAM usage hovering just below 5GB without any SD model loaded.

Some random outputs:
- A vibrant underwater cityscape filled with colorful marine life, surrounded by sunken ruins from ancient civilizations.
- A romantic scene between two lovers during sunset, with flowers around them and birds flying overhead.
- A steampunk-inspired portrait of Jane Austen, dressed in Victorian era clothing and holding a parasol.
