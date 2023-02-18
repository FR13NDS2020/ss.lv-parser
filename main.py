from products_parser import parse_pages
from visualize_data import visualize_parameter


def main():
    link = input("Please insert link : ")
    parse_pages(link)
    videocards = input("print 0 or 1 if you want enable filter for videocards: ")
    visualize_parameter(0 if videocards in {"", "0"} else 1)


if __name__ == '__main__':
    main()

