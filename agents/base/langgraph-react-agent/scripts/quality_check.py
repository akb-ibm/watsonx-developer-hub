import importlib.util

# Validate whether `unitxt`
if not importlib.util.find_spec("unitxt"):
    raise ModuleNotFoundError(
        f"ModuleNotFoundError: unitxt is not installed. Please install it using `pip install unitxt`."
    )

import json
from pathlib import Path
import warnings

from unitxt import get_logger
from unitxt.api import create_dataset, evaluate
import ibm_watsonx_ai
from utils import load_config

deployment_id = "PLACEHOLDER FOR YOUR DEPLOYMENT ID"
stream = True

SCORE_THRESHOLD = 0.3


def retrieve_generated_answer(chat_completions: dict) -> str:
    return chat_completions["choices"][0]["message"]["content"]


def load_benchmarking_data(benchmarking_data_path: str) -> list[dict]:
    with open(benchmarking_data_path, "r") as f:
        benchmarking_data = [json.loads(line) for line in f]

    return benchmarking_data


def generate_answers(
    input_data: list[dict], ids: list[str]
) -> tuple[list[str], list[str]]:
    results = []
    final_ids = []

    for payload, payload_id in zip(input_data, ids):
        try:
            results.append(
                retrieve_generated_answer(
                    api_client.deployments.run_ai_service(
                        deployment_id=deployment_id, ai_service_payload=payload
                    )
                )
            )
            final_ids.append(payload_id)
        except Exception as e:
            warnings.warn(f"Skipping sample: {payload_id}. Reason: {e}")

    return final_ids, results


def evaluate_agent(
    evaluation_data: list[dict], predictions: list[str], metrics: list[str]
) -> float:

    dataset = [
        {
            "question": eval_data["payload"]["messages"][-1]["content"],
            "answers": [eval_data["correct_answer"]],
        }
        for eval_data in evaluation_data
    ]

    dataset = create_dataset(
        task="tasks.qa.open",
        test_set=dataset,
        metrics=metrics,
    )

    results = evaluate(predictions, dataset["test"])

    df_results = results.global_scores.to_df()
    print(df_results)

    return df_results.to_dict().get("score", {}).get("score", 0)


if __name__ == "__main__":
    config = load_config("deployment")

    deployment_id = config["deployment_id"]

    api_client = ibm_watsonx_ai.APIClient(
        credentials=ibm_watsonx_ai.Credentials(
            url=config["watsonx_url"], api_key=config["watsonx_apikey"]
        ),
        space_id=config["space_id"],
    )

    # Load benchmarking data
    benchmarking_filename = "benchmarking_data.json"
    benchmarking_data_path = (
        Path(__file__).parents[1] / Path("./benchmarking_data") / benchmarking_filename
    )

    benchmarking_data = load_benchmarking_data(
        benchmarking_data_path=str(benchmarking_data_path)
    )

    # Executing deployed AI service with provided scoring data
    payloads_list = [data["payload"] for data in benchmarking_data]
    correct_answer_list = [data["correct_answer"] for data in benchmarking_data]

    final_ids, answers = generate_answers(
        payloads_list, [data["id"] for data in benchmarking_data]
    )

    metrics = ["metrics.qa.open.recommended_no_gpu"]

    # Check whether QA metric score is larger than acceptable threshold
    assert (
        evaluate_agent(
            evaluation_data=[
                _data for _data in benchmarking_data if _data["id"] in final_ids
            ],
            predictions=answers,
            metrics=metrics,
        )
        > SCORE_THRESHOLD
    ), f"Agent does not pass quality check. Used metrics: {metrics}, threshold: {SCORE_THRESHOLD}"
