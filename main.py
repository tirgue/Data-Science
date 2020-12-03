from datascience.ui.commandLine import CommandLine

if __name__ == '__main__':
    ui = CommandLine()
    try:
        ui.cmdloop()
    except KeyboardInterrupt:
        print("\nQuitting...")
