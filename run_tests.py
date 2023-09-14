import argparse

from tests import metrics_test, pipeline_test, prompt_test

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up experiment parameters')
    parser.add_argument('--api_tests', type=bool, required=False, default=False)
    parser.add_argument('--api_key', type=str, required=False)
    parser.add_argument('--verbose', type=bool, required=False, default=False)
    args = parser.parse_args()

    if args.api_tests and args.api_key is None:
        raise ValueError('API tests require an API key')

    metrics_test.run_metrics_tests()
    pipeline_test.run_pipeline_tests(api_tests=args.api_tests, api_key=args.api_key)
    prompt_test.run_prompt_tests(verbose=False)
