import argparse
from data.loader import load_stories_from_excel
from evaluation.evaluator import Evaluator
from improvement.improver import Improver
from output.evaluator_writer import save_evaluator_results
from output.writer import save_evaluation_results
from output.improver_writer import save_improver_results

def main():
    parser = argparse.ArgumentParser(description="Evaluate and improve user stories.")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of stories to process")
    parser.add_argument("--only", choices=["evaluator", "improver"], help="Run only evaluator or improver")
    args = parser.parse_args()

    # Load stories
    stories = load_stories_from_excel("datasets/us_neodataset_sample.xlsx")
    if args.limit:
        stories = stories[:args.limit]

    evaluator = Evaluator()
    improver = Improver()
    results = []

    for i, story in enumerate(stories):
        print(f"\n📝 Story {i+1}/{len(stories)}")

        result = {"original": story}

        if args.only in [None, "evaluator"]:
            print("🔍 Evaluating...")
            eval_result = evaluator.evaluate_story(story)
            result.update(eval_result)

        if args.only in [None, "improver"]:
            if "scores" in result and "explanations" in result:
                print("✍️ Improving...")
                improved = improver.improve_story(
                    result["original"],
                    result.get("scores", {}),
                    result.get("explanations", {})
                )
                result.update(improved)
            else:
                print("⚠️ Skipping improvement due to missing evaluation data.")

        results.append(result)

    if args.only == "evaluator":
        save_evaluator_results(results, "output/evaluator_results.xlsx")
    elif args.only == "improver":
        save_improver_results(results, "output/improver_results.xlsx")
    else:
        save_evaluation_results(results, "output/full_results.xlsx")
        save_evaluator_results(results, "output/evaluator_results.xlsx")

    print("✅ Done.")

if __name__ == "__main__":
    main()
