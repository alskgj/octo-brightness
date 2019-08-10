import subprocess


def dmenu_wrapper(items):
    items = map(str, items)

    # start the dmenu process
    proc = subprocess.Popen(
        ['dmenu'],
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )

    # write items over to dmenu
    with proc.stdin:
        for item in items:
            proc.stdin.write(item)
            proc.stdin.write('\n')

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')


def get_monitors():
    """:returns a list of monitors"""
    outputs = []
    for line in subprocess.check_output(["xrandr", "--listmonitors"]).decode("utf-8").split('\n')[1:]:
        if line: outputs.append(line.split(' ')[-1])
    return outputs


def set_brightness(output, brightness):
    subprocess.run(["xrandr", "--output", output, "--brightness", brightness])


def main():
    """Asks for an output and a brightness, and applies it"""
    outputs = get_monitors()
    output = dmenu_wrapper(outputs)

    # safety, so we don't accidentally turn of the screen (brightness = 0)
    brightness_values = [str(i / 10) for i in range(1, 11)]
    brightness = dmenu_wrapper(brightness_values)
    if brightness not in brightness_values:
        print("got", brightness)
        print(brightness_values)
        brightness = "1"

    set_brightness(output, brightness)


if __name__ == '__main__':
    main()
