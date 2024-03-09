#!/bin/bash

python main.py --logic omegaBot --email=test@email.com --name=stima1 --password=123456 --team etimo &
python main.py --logic omegaBot --email=test1@email.com --name=stima1 --password=123456 --team etimo &
python main.py --logic random --email=test2@email.com --name=stima2 --password=123456 --team etimo &
python main.py --logic random --email=test3@email.com --name=stima3 --password=123456 --team etimo &