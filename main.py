from InputOutput.log import Log


def main():
    log = Log("log")
    log.debug("Debug")
    log.info("Info")
    log.error("Error")
    log.critical("Critical")


if __name__ == "__main__":
    main()
