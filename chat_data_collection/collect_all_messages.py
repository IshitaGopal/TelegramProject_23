#!/usr/bin/env python3

from telethon.sync import TelegramClient
import argparse
import os
import time
from config import Config
from data_utils import write_json
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel_input", type=str, required=True)
    # parser.add_argument("--type", type=str, required=True)

    args = parser.parse_args()

    start_time = time.time()

    channel_input = args.channel_input

    # Output dir -  json_chat_data or json_channel_data based on type of input
    # if type == "group chat":
    #     output_dir = Config.json_chat_dir
    # else:
    #     output_dir = Config.json_channel_dir

    output_dir = "new_data"
    Path(os.path.join(output_dir, channel_input)).mkdir(parents=True, exist_ok=True)
    # Connect to the API
    with TelegramClient(Config.session_name, Config.api_id, Config.api_hash) as client:
        print("starting collection")
        new_messages = client.get_messages(channel_input, limit=10000)
        oldest_msg_id = new_messages[-1].id
        print(oldest_msg_id)

        # If there are non zero messages, collect them in a list
        if len(new_messages) > 0:

            msg_list = [msg.to_dict() for msg in new_messages]

            output_file = channel_input + f"_{oldest_msg_id}" + ".json"

            # save in a json file
            write_json(
                data=msg_list,
                output_dir=output_dir,
                output_subdir=channel_input,
                output_file=output_file,
            )

            # Keep grabbing messages
            while len(new_messages) > 0:
                new_messages = client.get_messages(
                    channel_input, offset_id=oldest_msg_id, limit=10000
                )
                if len(new_messages) > 0:
                    oldest_msg_id = new_messages[-1].id
                    print("getting messages before %s" % (oldest_msg_id))

                    msg_list = [msg.to_dict() for msg in new_messages]
                    # write it to file
                    output_file = channel_input + f"_{oldest_msg_id}" + ".json"
                    write_json(
                        data=msg_list,
                        output_dir=output_dir,
                        output_subdir=channel_input,
                        output_file=output_file,
                    )

    print("--- %s seconds ---" % (time.time() - start_time))
