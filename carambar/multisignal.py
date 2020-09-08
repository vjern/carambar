import signal

# https://stackoverflow.com/questions/10856926/sigwinch-equivalent-on-windows


if __name__ == "__main__":
    
    def f():
        print(1)
    def g():
        print(2)

    signal.signal(signal.SIGTERM, f)
    signal.signal(signal.SIGTERM, g)

    input()