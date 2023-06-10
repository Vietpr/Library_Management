import os
import shutil
import PyPDF2
from gtts import gTTS
from playsound import playsound
import pygame


class Node:
    def __init__(self, bid, title, author, status, borrower=None):
        self.bid = bid
        self.title = title
        self.author = author
        self.status = status
        self.borrower = borrower
        self.next = None


class LinkedListLibrary:
    def __init__(self):
        self.head = None
        self.bid_set = set()
        self.borrowers = {}
        self.pdf_folder = "pdf_books"

        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder)

    def AddBook(self, bid, title, author, status, path):
        if bid in self.bid_set:
            print(f'book with id {bid} already exists.')
        else:
            new_node = Node(bid, title, author, status)
            if self.head is None:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
            self.bid_set.add(bid)
            new_node.borrower = None
            file_name = f'{bid}.pdf'
            new_path = os.path.join(self.pdf_folder, file_name)
            shutil.move(path, new_path)
            new_node.path = new_path

    def display_list(self):
        if self.head is None:
            print("The list is empty.")
        else:
            current = self.head
            print("Book List:")
            print("{:<5} | {:<25} | {:<20} | {:<10}".format("Bid", "Title", "Author", "status (0 - available)"))
            print("------------------------------------------------------------------------------------------")
            while current:
                print("{:<5} | {:<25} | {:<20} | {:<10}".format(current.bid, current.title, current.author, current.status))
                current = current.next

    def delete_book(self, bid):
        if self.head is None:
            print("The list is empty.")
        else:
            current = self.head
            prev = None
            found = False
            while current:
                if current.bid == bid:
                    found = True
                    break
                prev = current
                current = current.next
            if found:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                print(f"Book with id {bid} has been deleted.")
            else:
                print(f"Book with id {bid} not found.")

    def borrow_book(self, bid, borrower, borrowed_books):
        if self.head is None:
            print("The list is empty.")
        else:
            current = self.head
            found = False

            while current:
                if current.bid == bid:
                    found = True
                    if current.status == "0":
                        current.status == "1"
                        borrowed_books.add_node(current.bid, current.title, borrower)
                        self.borrowers[current.bid] = borrower
                        print(f'Book with ID {bid} has been borrowed.')
                    else:
                        print(f"Book with ID {bid} is not available")
                current = current.next
            if not found:
                print(f"Book with id {bid} is not found.")

    def return_book(self, bid, borrowed_books):
        if borrowed_books.head is None:
            print("No books are currently borrowed.")
        else:
            current = borrowed_books.head
            prev = None
            found = False
            while current:
                if current.bid == bid:
                    found = True
                    break
                prev = current
                current = current.next
            if found:
                if prev:
                    prev.next = current.next
                else:
                    borrowed_books.head = current.next
                current = self.head
                while current:
                    if current.bid == bid:
                        current.status = "0"
                        break
                    current = current.next
                borrower = self.borrowers.get(bid)  # Get borrower information from dictionary
                print(f"Book with id {bid} - {current.title} has been returned by {borrower}.")  # The minus sign (-) is used to create a space between two parts of a string.
            else:
                print(f"Book with id {bid} not found in borrowed books.")

    def search_book_by_title(self, title):
        current = self.head
        found_books = []
        while current:
            if title.lower() in current.title.lower():
                found_books.append(current.bid)
            current = current.next
        return found_books

    def print_book_id(self, title):
        found_books = self.search_book_by_title(title)
        if found_books:
            print(f"Books with title '{title}' found with the following IDs:")
            for bid in found_books:
                print(bid)
        else:
            print(f"No books found with title '{title}'.")

    def read_pdf(self, file_path):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            content = ''
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                content += page.extract_text()  # extract: extract Content
            return content

    def read_book_with_voice(self, bid):
        current = self.head
        found = False
        while current:
            if current.bid == bid:
                found = True
                break
            current = current.next
        if found:
            content = self.read_pdf(current.path)  # use path of book
            if content:
                tts = gTTS(text=content, lang='vi')
                tts.save("output.mp3")
                pygame.mixer.init()
                pygame.mixer.music.load("output.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
                pygame.mixer.quit()
                os.remove("output.mp3")
            else:
                print(f"Book with id {bid} not found in the library.")
        else:
            print(f"Book with id {bid} not found in the library.")


class BorrowedLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, bid, title, borrower):
        new_node = Node(bid, title, borrower, None)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
