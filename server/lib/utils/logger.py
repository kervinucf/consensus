import random


def status_logger(
        non_status_text="",
        status_text="",
        yellow=False,
        green=False,
        red=False,

        cyan=False,
        purple=False,
        blue=False,
        pink=False,
        multi=False,
        orange=False,
        inline=True,

) -> None:
    """Log the status of the application."""
    if inline:
        ending = '\n'
    else:
        ending = '\n'
    if yellow:
        print(non_status_text +
                      '\033[1;33m' + status_text + '\033[0m', end=ending)
    elif red:
        print(non_status_text +
                      '\033[1;31m' + status_text + '\033[0m', end=ending)
    elif green:
        print(non_status_text +
                      '\033[1;32m' + status_text + '\033[0m', end=ending)
    elif cyan:
        print(non_status_text +
                      '\033[1;36m' + status_text + '\033[0m', end=ending)
    elif purple:
        print(non_status_text +
                      '\033[1;35m' + status_text + '\033[0m', end=ending)
    elif blue:
        print(non_status_text +
                      '\033[1;34m' + status_text + '\033[0m', end=ending)
    elif pink:
        print(non_status_text +
                      '\033[1;95m' + status_text + '\033[0m', end=ending)
    elif orange:
        print(non_status_text +
                      '\033[1;33m' + status_text + '\033[0m', end=ending)
    elif multi:
        random_color = random.choice([36, 35, 34, 95])
        print(non_status_text + '\033[1;' + str(
            random_color) + 'm' + status_text + '\033[0m', end=ending)
    else:
        print(non_status_text + status_text)

