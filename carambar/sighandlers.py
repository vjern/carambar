import signal


# def also()


def handler(*sigs):
    """A simple decorator to set a signal handler."""
    def decorator(fn):
        for sig in sigs:
            signal.signal(sig, fn)
        return fn
    return decorator


@handler(signal.SIGWINCH)
def sigwinch_handler(*a):

    """React to the terminal window changing size."""

    global TERMSIZE
    previous_termsize = TERMSIZE
    TERMSIZE = get_terminal_size()

    setup_scroll_area(TERMSIZE.lines)

    coldiff = previous_termsize.columns // TERMSIZE.columns
    if coldiff > 0:
        FILENO.write('\033[%dA' % coldiff)

    FILENO.write('\033[J')
    FILENO.flush()

    for i in ctxb.get_instances():
        if i.running:
            i.refresh()


@handler(signal.SIGTSTP)
def sigtstp_handler(*a):

    global TERMSIZE
    TERMSIZE = get_terminal_size()

    setup_scroll_area(TERMSIZE.lines + 1)

    # Erase the terminal after & below the cursor
    FILENO.write('\033[J')
    FILENO.flush()

    # Show cursor in case it was hidden
    FILENO.write('\033[?25h')
    FILENO.flush()

    # Disable SIGTSTP handler; replace by default handler
    signal.signal(signal.SIGTSTP, signal.SIG_DFL)

    # Resend signal to self
    os.kill(os.getpid(), signal.SIGTSTP)


@handler(signal.SIGCONT)
def sigcont_handler(*a):

    global TERMSIZE
    TERMSIZE = get_terminal_size()

    setup_scroll_area(TERMSIZE.lines)

    # Erase the terminal after & below the cursor
    FILENO.write('\033[J')
    FILENO.flush()

    # Refresh running ctxb instances
    i = None
    for i in ctxb.get_instances():
        if i.running:
            i.refresh()

    # Hide cursor in case it was hidden by the most nested ctxb
    if i is not None and i.hide_cursor:
        FILENO.write('\033[?25l')
        FILENO.flush()

    # Re-enable SIGTSTP handler
    signal.signal(signal.SIGTSTP, sigtstp_handler)


@handler(signal.SIGTERM, signal.SIGINT)
def sigterm_handler(*a):

    global TERMSIZE
    TERMSIZE = get_terminal_size()

    setup_scroll_area(TERMSIZE.lines + 1)

    # Erase the terminal after & below the cursor
    FILENO.write('\033[J')
    FILENO.flush()

    # Show cursor in case it was hidden
    FILENO.write('\033[?25h')
    FILENO.flush()

    exit()
