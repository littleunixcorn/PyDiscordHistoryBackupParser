import sys, os, json, requests

from argparse import ArgumentParser
from urllib.parse import urlparse
from os.path import splitext

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-b", "--backupfile", dest="backupfile", required=True,
                        help="The backup file created by DiscordHistoryBackup.")
    parser.add_argument("-f", "--folder", dest="foldername", required=True,
                        help="Destination folder where the parsed backup will be saved.")

    args = parser.parse_args()
    
    # The specified backup file does not exist
    if os.path.exists(args.backupfile) != True:
        print("The specified backup file does not exist.")
        sys.exit()

    # The specified backup file is not a file
    if os.path.isfile(args.backupfile) != True:
        print("The specified backup file is not a file.")
        sys.exit()

    # The directory specified to backup does not exist
    if os.path.exists(args.foldername) != True:
        print("The directory specified not exist.")
        sys.exit()
    
    # The directory specified to backup is not a directory
    if os.path.isdir(args.foldername) != True:
        print("The directory specified is not a directory.")
        sys.exit()

    # Parsing the file
    with open(args.backupfile, encoding='utf8', errors='ignore') as f:
        data = json.load(f)
        print("Starting to parse the backup file.")
        for channel_id, channel_content in data["data"].items():
            # Create a folder per channel
            try:
                os.mkdir(args.foldername + "/channel_" + data["meta"]["channels"][channel_id]["name"])
            except FileExistsError:
                pass
            
            for message_id, message_content in channel_content.items():
                # Create a folder per message
                try:
                    os.mkdir(args.foldername + "/channel_" + data["meta"]["channels"][channel_id]["name"] + "/messageid_" + message_id)
                except FileExistsError:
                    pass
                # If the message have a written content it is put in messagecontent.txt
                try:
                    message_text = message_content["m"]
                    message = open(args.foldername + "/channel_" + data["meta"]["channels"][channel_id]["name"] + "/messageid_" + message_id + "/messagecontent.txt", "w")
                    message.write(message_text)
                    message.close()
                except:
                    pass
                # If the message have files uploaded with it is downloaded on the message folder
                try:
                    url_content = message_content["a"]
                    for url in url_content:
                        r = requests.get(url["url"], allow_redirects=True)
                        # Get the extension of the file
                        parsed = urlparse(url["url"])
                        root, extension = splitext(parsed.path)
                        open(args.foldername + "/channel_" + data["meta"]["channels"][channel_id]["name"] + "/messageid_" + message_id + "/" + "file" + extension, 'wb').write(r.content)
                except:
                    pass
            print("Parsed the channel " + data["meta"]["channels"][channel_id]["name"] + ".")
    print("Backup file sucessfully parsed.")