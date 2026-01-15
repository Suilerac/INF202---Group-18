from InputOutput.commandlineParser import commandlineParser


def main():
    clp = commandlineParser()
    clp.setConfigList()
    print(clp.configs)


if __name__ == "__main__":
    main()
