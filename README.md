# ISWS 2024 Project Idea - What do Large Language Models know and remember?

The [Open LLM Leaderboard by Huggingface](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) is very often used to evaluate large language models (LLMs).
It covers various datasets such as:

- ARC - AI2 Reasoning Challenge (7,787 grade-school science questions)
    - [paper](https://arxiv.org/abs/1803.05457), [eval config](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/arc), [dataset](https://huggingface.co/datasets/allenai/ai2_arc)
- HellaSwag (multiple choice questions on how to end a sentence) 
    - [paper](https://arxiv.org/abs/1905.07830), [eval config](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/hellaswag), [dataset](https://huggingface.co/datasets/hellaswag)
- TruthfulQA (model's propensity to reproduce falsehoods commonly found online)
    - [paper](https://arxiv.org/abs/2109.07958), [eval config](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/truthfulqa), [dataset](https://huggingface.co/datasets/truthful_qa)
- Winogrande (multiple choice questions on machine intelligence)
    - [paper](https://arxiv.org/abs/1907.10641), [eval config](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/winogrande), [dataset](https://huggingface.co/datasets/winogrande)
- GSM8k (diverse grade school math word problems)
    - [paper](https://arxiv.org/abs/2110.14168), [eval config](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks/gsm8k), [dataset](https://huggingface.co/datasets/gsm8k)


In this project, you will analyze what information LLMs will correctly remember.
The idea is to generate questions based on a KG of your choice (e.g., Wikidata, DBpedia, etc.) to see if they can be correctly answered.
When executed on many models, one can see which models can remember many facts.
More specifically, different kinds of questions can be generated out of the KG, e.g. 

- do LLMs remember more information on persons, rather than places?
- do LLMs remember more information about cities in the US than in other countries?
- do LLMs remember more information about entities that are more popular (according to Wiki page views reported by [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Popular_pages) or [WikiMedia](https://stats.wikimedia.org/)) than long-tail entities
- do LLMs remember dates (e.g., birthdate) better than locations (e.g., birthplace) or vice versa
- can LLMs decide on types of instances or on subclass relations? Which one works better?

One possible way would be to generate multiple-choice questions (similar to HellaSwag).
The difficulty level of those questions is something to be explored.
Similarly, the question remains how wrong answers (which still make sense) can be generated.
In a successful project, we can see which models remember factual information and how biased they are.
Depending on the questions asked, such an evaluation dataset can also be used to check which models are suitable for ontology construction (see the last question above).

## Research Questions
- RQ1: How well do different pretrained LLMs memorize different topics?
- RQ2: How well can pretrained LLMs decide on knowledge engineering tasks? 
- RQ2: How can KGs be leveraged for the evaluation of pretrained LLMs?
- RQ3: How can we automatically create reference datasets from KGs for the evaluation of pretrained LLMs?

## Implementation Details

- One possible framework to be used is called [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness). It is the framework used by the [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- To create a new task/dataset, [the framework provide a useful introduction](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/new_task_guide.md) 
- All implemented [tasks are available in GitHub](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks)
    - To find the corresponding dataset mentioned in the dataset_path attribute (e.g. [hellaswag example](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/hellaswag/hellaswag.yaml)), you can **append** the dataset name to the following URI `https://huggingface.co/datasets/` (in the example this will be [https://huggingface.co/datasets/hellaswag](https://huggingface.co/datasets/hellaswag))
- All possible parameters for the eval config file are reported [in the task guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md)


## How to run

- To install the evaluation framework, run 
```
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e .
```
(also explained on the [eval framework homepage](https://github.com/EleutherAI/lm-evaluation-harness))

- Creating a task involves creating a config file (an example is provided as kg_g.yaml and kg_mc.yaml)

- If the task configuration file (the yaml file) is not in the tasks folder, then provide a folder containing all tasks files by `--include_path` argument ([see the task guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/new_task_guide.md#task-name--groups-registering-a-task))

- A possible run command looks like the following (it will run the kg_g task for the gpt3.5 model):
    - to check detail run the tool with `-w --verbosity DEBUG`
    - `--log_samples` can be used to get further detailed results 
    - for all options, execute `lm_eval --help` 
```
lm_eval --model openai-chat-completions --model_args model=gpt-3.5-turbo --include_path ./ --tasks kg_g  --output_path ./results
```



## OpenAI Models and the Multiple Choice Questions
The tasks can have different output types ([see scoring details](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md#parameters)) like
- `generate_until`, `loglikelihood`, `loglikelihood_rolling`, and `multiple_choice`
    - `generate_until` works with all models (inlcuding proprietary models like ChatGPT)
    - all others do usually only work with open source models because it requires to get access to the logits of the model. In case you are further interested, see issues [#1196](https://github.com/EleutherAI/lm-evaluation-harness/issues/1196) and [#1704](https://github.com/EleutherAI/lm-evaluation-harness/issues/1704)
- thus e.g. the Polish PPC dataset has both variants ([`ppc_mc` for `multiple choice` version and `polish_ppc_regex` for `generate_until` version](https://github.com/speakleash/lm-evaluation-harness/tree/polish2/lm_eval/tasks/polish_ppc))


## Contact information
- Harald Sack ([mail](mailto:Harald.Sack@fiz-Karlsruhe.de))
- Sven Hertling ([mail](mailto:Sven.Hertling@fiz-Karlsruhe.de))
