# ExLlama nodes for ComfyUI
A simple prompt generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlama](https://github.com/turboderp/exllama).

## Installation
Clone the repository to `custom_nodes` in your ComfyUI directory and install dependencies:
```
git clone https://github.com/Zuellni/ComfyUI-ExLlama-Nodes
pip install -r requirements.txt
```

Install the latest pre-built ExLlama wheel from [here](https://github.com/jllllll/exllama/releases/latest).  
Choose the version matching your platform, Python, and PyTorch CUDA/ROCm.

Example for Windows with Python 3.10 and CUDA 11.7:
```
pip install https://github.com/jllllll/exllama/releases/download/0.0.17/exllama-0.0.17+cu117-cp310-cp310-win_amd64.whl
```

## Nodes
Comes with the following nodes:

### Loader
Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them over at [Hugging Face](https://huggingface.co/TheBloke).

You should either clone the model repository or download all the files in it manually, then point to the directory in `model_dir`. The `model.safetensors` file on its own is not enough to work.

ExLlama allocates [memory](https://github.com/turboderp/exllama/issues/259) according to `max_seq_len`. Lowering it is a good way to save on GPU RAM.  
It's currently not possible to [offload](https://github.com/turboderp/exllama/issues/177) the models to CPU RAM.

### Generator
Generates a `string` based on the given `prompt` for use with other nodes.  
Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui).  
ExLlama isn't [deterministic](https://github.com/turboderp/exllama/issues/201), so the outputs may differ even with the same seed.

### Previewer
Displays generated outputs in the UI.

## Workflow
Can be opened directly in ComfyUI.  
Model used: [MythoLogic-Mini-7B](https://huggingface.co/TheBloke/MythoLogic-Mini-7B-GPTQ).

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/c47e84da-93b0-4d58-ba93-fbfa0ce08f85)
