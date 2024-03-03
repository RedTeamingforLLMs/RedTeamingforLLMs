
# Red Teaming for Large Language Models At Scale: Tackling Hallucinations on Mathematics Tasks

This project provides a framework designed for executing positive red-teaming experiments on large language models. More information about the nature of this project can be found in our [paper](https://aclanthology.org/2023.artofsafety-1.1/).

## Prerequisites

1. **Python Version**: Ensure you have Python 3.9 installed on your machine.
2. **Dependencies**: Install the required libraries using the following command:
    ```bash
    pip install -r requirements.txt
    ```

3. **API Key**: Ensure the `key.txt` file is located in the root directory of the project. This file should house the OpenAI API key.

## Running the Experiments

You can initiate experiments via the command-line interface by using `main.py` with appropriate arguments.

### Arguments

- `--name`: Specifies the name of the experiment. This creates a folder with results. By default, it uses the current date and time.
  
- `--contexts`: Determines the contexts for the experiments. Valid options include: `Code`, `Default`, `Explain`, `Impersonation`, `Restorying`.
    By default, the `Default` context is chosen.
  
- `--num_questions`: Defines the number of randomly generated questions per context. If only one number is provided, it assigns that number to each context. The default value is 100.

- `--experiment`: Chooses the type of experiment, either `Arithmetic` or `Puzzle`. The default is `Arithmetic`.

- `--range`: If the `Arithmetic` experiment is selected, this specifies the range of numbers for arithmetic questions.

### Usage Examples

1. **Default Call**: 
    ```bash
    python main.py
    ```
   This initiates the script with default argument values.

2. **Custom Call**:
    ```bash
    python main.py --name first_experiment --contexts Code Explain --num_questions 100 200 --experiment Arithmetic --range 5 100
    ```
   This example demonstrates the script execution with custom arguments.

## Results

- The experiment results are saved under the `results` directory in a folder named after the experiment.
  
- The data is stored as JSON files:
  - Each experiment directory contains a JSON file for every context type. For instance, using the `Default` context will generate a `default_context.json` file. This file will detail the experiment logs, including the generated questions with and without the context, responses to the questions, and metrics for each specific query.
  - The `results.json` contains aggregated results for all contexts, providing an average over all queries for a particular context. 

**Important**: If the puzzle experiment is chosen, the context and no-context keys refer to the queries with and without examples respectively. 
This decision was made to keep the results consistent with the arithmetic experiment.

## Project File Structure

### Main Files

- `main.py`: Initiates the experiments.

### Contexts

Directory dedicated to generating various contexts.

- `context.py`: Base class for all contexts.
- `code_context.py`: Prompts the LLM to generate code for a given input before responding.
- `explain_context.py`: Directs the LLM to elucidate its reasoning for the posed query.
- `impersonation_context.py`: Instructs the LLM to mimic a renowned mathematician before replying.
- `restorying_context.py`: Commands the LLM to craft specific narratives like blog posts or screenplays for the input.
- `default_context.py`: Represents the standard context.

### Experiments

Directory responsible for the experiment's execution.

- `experiment.py`: Base class for all experiments.
- `arithmetic_experiment.py`: Manages arithmetic questions, from generation to execution.
- `puzzle_experiment.py`: Manages puzzle-related questions and their execution.

### Utilities

Directory with utility functions.

- `metrics.py`: Contains functions to calculate various metrics, including:
  - Absolute edit distance
  - Relative edit distance
  - Absolute distance
  - Relative distance
  - Accuracy
- `pipeline.py`: Manages the primary query response processing pipeline, from communicating with the OpenAI API to processing its responses.
- `puzzles.py`: Core logic for puzzle question generation.
- `question_generation.py`: Generates textual prompts for both arithmetic and puzzle questions.

## OpenAI Language Model Configuration

To alter the OpenAI language model and its parameters, edit the `config.json` file. For a deeper dive into the parameters, consult the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/chat).

## Extending the Framework

The framework is designed for adaptability and expansion. Here are some ideas to broaden its capabilities:

### 1. Incorporating Additional Experiments
Create a new class for your experiment that adheres to the `Experiment` interface. Further, update the Experiment enum class within `main.py`.  Inspect the existing experiments for implementation insights.

### 2. Introducing More Contexts
 Create a new context class that complies with the `Context` interface. Also, remember to update the Context enum class in `main.py`.
Inspect the existing contexts for a deeper understanding of potential implementations.
