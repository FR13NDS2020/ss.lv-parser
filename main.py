from products_parser import parse_pages
from visualize_data import visualize


def main():
    link = input("Please insert link : ")
    parse_pages(link)
    videocards = input("print 0 or 1 if you want enable filter for videocards: ")
    visualize(int(videocards))


if __name__ == '__main__':
    main()


