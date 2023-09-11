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
Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them over at https://huggingface.co/TheBloke. ExLlama allocates memory according to `max_seq_len`, setting it lower is a good way to save VRAM. Currently it's not possible to offload the model to CPU RAM.

### ExLlama Generator
Generates a `string` based on the given `prompt` and max `tokens` for use with other nodes. Default values correspond to the `simple-1` preset from https://github.com/oobabooga/text-generation-webui. ExLlama isn't deterministic so the outputs may differ even with the same seed.

## Workflow
![workflow](https://github.com/Zuellni/ComfyUI-ExLlama/assets/123005779/005df502-9986-444c-b736-448b305e329c)
