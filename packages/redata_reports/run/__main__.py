# Entry point for DO functions

import main as m
from os import environ


def main(event, context):
    # Only allow authenticated requests
    accesstoken = event.get("t", "")
    if accesstoken != environ["TOKEN"]:
        return {
            "headers": {"Content-Type": "text/html"},
            "statusCode": 403,
            "body": "Forbidden. Invalid token."
        }

    args = m.init_argparse().parse_args()
    args.sync_to_dashboard = True

    result = m.run(args)

    return {
        "headers": {"Content-Type": "text/html"},
        "statusCode": 200,
        "body": f"{result}"
    }
