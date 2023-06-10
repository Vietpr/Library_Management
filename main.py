from Library import LinkedListLibrary, BorrowedLinkedList

book_library = LinkedListLibrary()
borrowed_books = BorrowedLinkedList()

while True:
    print("Library Management System Menu:")
    print("1. Add Book")
    print("2. View Books")
    print("3. Delete Book")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. Search Book")
    print("7. Read Book with Voice")
    print("8. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        bid = input("Enter book id: ")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        status = "0"
        path = input("Enter file path: ")
        book_library.AddBook(bid, title, author, status, path)
    elif choice == '2':
        book_library.display_list()
    elif choice == '3':
        bid = input("Enter book id to delete: ")
        book_library.delete_book(bid)
    elif choice == '4':
        bid = input("Enter book id to borrow: ")
        borrower = input("Enter borrower name: ")
        book_library.borrow_book(bid, borrower, borrowed_books)
    elif choice == '5':
        bid = input("Enter book id to return: ")
        book_library.return_book(bid, borrowed_books)
    elif choice == '6':
        title = input("Enter book title to search: ")
        found_books = book_library.search_book_by_title(title)
        if found_books:
            print(f"Books with title '{title}' found with the following IDs:")
            for bid in found_books:
                print(bid)
        else:
            print(f"No books found with title '{title}'.")
    elif choice == '7':
        bid = input("Enter book id to read with voice: ")
        book_library.read_book_with_voice(bid)
    elif choice == '8':
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 8.")
    print()

