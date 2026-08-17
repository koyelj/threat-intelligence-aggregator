import subprocess
import sys


def run_module(module_name):

    print("\n")
    print("=" * 60)
    print(f"RUNNING: {module_name}")
    print("=" * 60)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module_name
        ]
    )

    if result.returncode != 0:

        print(
            f"\nERROR: {module_name} failed."
        )

        sys.exit(
            result.returncode
        )


def main():

    print(
        "\n"
        "============================================\n"
        "   THREAT INTELLIGENCE AGGREGATOR\n"
        "        COMPLETE PIPELINE\n"
        "============================================"
    )

    run_module(
        "processing.process_feed"
    )

    run_module(
        "correlation.correlate"
    )

    run_module(
        "correlation.blocklist_generator"
    )

    run_module(
        "reports.report_generator"
    )

    print(
        "\n"
        "============================================\n"
        "       PIPELINE COMPLETED SUCCESSFULLY\n"
        "============================================"
    )


if __name__ == "__main__":

    main()