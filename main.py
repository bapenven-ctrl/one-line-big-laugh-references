"""One Line, Big Laugh entry: write one funny line to /output/entry.txt.

Deterministic: the same bytes on every run. No network, no environment
reads, no timestamps. The output file's 0644 mode is achieved with
os.open and os.umask(0o022) at creation time -- never by changing modes
afterwards: the grading sandbox runs the program as a non-root user, and
changing modes on /output or on the output file fails there.
"""

import os

LINE = "The job interview asked for three references, and all three were the same man in different wigs \u2014 Dave, Dave with a moustache, and Dave's identical twin, Dave \u2014 vouching loudly for himself."


def main() -> None:
    os.umask(0o022)
    os.makedirs("/output", exist_ok=True)
    data = LINE.encode("utf-8")
    fd = os.open("/output/entry.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
    try:
        # os.write may write only part of the buffer; loop until all bytes land.
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            view = view[written:]
    finally:
        os.close(fd)


if __name__ == "__main__":
    main()
