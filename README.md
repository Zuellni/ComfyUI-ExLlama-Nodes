# ExLlama nodes for ComfyUI
A simple prompt generator for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) utilizing [ExLlama](https://github.com/turboderp/exllama).  
Outputs are printed in the console, if you'd like to see them in the UI you can use the `Show Text` node from [here](https://github.com/pythongosssss/ComfyUI-Custom-Scripts).

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

### ExLlama Loader
Used to load 4-bit GPTQ Llama/2 models. You can find a lot of them over at [Hugging Face](https://huggingface.co/TheBloke).  
ExLlama allocates [memory](https://github.com/turboderp/exllama/issues/259) according to `max_seq_len`. Lowering it is a good way to save on GPU RAM.  
It's currently not possible to [offload](https://github.com/turboderp/exllama/issues/177) the model to CPU RAM.

### ExLlama Generator
Generates a `string` based on the given `prompt` for use with other nodes.  
Default values correspond to the `simple-1` preset from [text-generation-webui](https://github.com/oobabooga/text-generation-webui).  
ExLlama isn't [deterministic](https://github.com/turboderp/exllama/issues/201), so the outputs may differ even with the same seed.

## Example
The workflow can be opened directly in ComfyUI.  
Model used: [MythoLogic-Mini-7B](https://huggingface.co/TheBloke/MythoLogic-Mini-7B-GPTQ).

Generated output:
```
A serene Japanese garden inspired by Zen philosophy, featuring intricate stonework and minimalist design elements.
```

![workflow](https://github.com/Zuellni/ComfyUI-ExLlama-Nodes/assets/123005779/e5956c9a-36f7-4674-9737-2589727bf73d)
