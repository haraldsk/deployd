import logging

from deployd.webapp import webapp

def main():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(name)s:%(lineno)d:%(levelname)s:%(message)s")
    webapp.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )


if __name__ == "__main__":
    main()
