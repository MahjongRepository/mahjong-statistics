from optparse import OptionParser

from statistics import Statistics


def main():
    parser = OptionParser()
    parser.add_option("-p", "--db_path", type="string", help="Path to sqlite database with logs")
    opts, _ = parser.parse_args()

    if not opts.db_path:
        parser.error("Set the db path as argument")

    Statistics(opts.db_path).calculate_statistics()


if __name__ == "__main__":
    main()
