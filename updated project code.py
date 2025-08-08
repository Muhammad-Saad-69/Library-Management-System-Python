import datetime
import re

class LibrarySystem:
    def __init__(self):
        self.library_books = {
            1: {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Fiction"},
            2: {"title": "1984", "author": "George Orwell", "genre": "Dystopian"},
            3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic"},
            4: {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic"},
            5: {"title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure"},
            6: {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance"},
            7: {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical"},
            8: {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Coming-of-age"},
            9: {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
            10: {"title": "Fahrenheit 451", "author": "Ray Bradbury", "genre": "Science Fiction"},
            11: {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Philosophical"},
            12: {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian"},
            13: {"title": "The Odyssey", "author": "Homer", "genre": "Epic Poetry"},
            14: {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "genre": "Drama"},
            15: {"title": "Dracula", "author": "Bram Stoker", "genre": "Gothic Horror"}
        }
        self.members = {}  # Normal users
        self.admins = {
            "afnan": "same",
            "saad": "same",
            "fayyaz": "same"
        }
        self.user_carts = {}  # {username: [book_ids]}
        self.user_borrowed_books = {}  # {username: {book_id: original_book_data}}
        self.undo_stack = []  # Tracks actions for undo functionality
        self.current_user = None  # Tracks logged-in user
        self.current_user_type = None  # 'admin', 'user', or 'guest'
        self.next_book_id = max(self.library_books.keys()) + 1 if self.library_books else 1
        self.guest_borrowed_books = {}  # Track guest borrows {username: book_id}
        self.payment_info = {}     # Stores user banking info
        self.payment_dates = {}    # Stores payment/registration date

    # ------------------- Authentication Functions ------------------- #
    def register(self):
        print("💰 Registration requires a monthly fee of RS: 1000 to access the library system.")
        proceed = input("Do you wish to continue? (yes/no): ").strip().lower()
        if proceed != "yes":
            print("❌ Registration cancelled.")
            return

        username = input("👤 Enter a new username: ")
        if username in self.members or username in self.admins:
            print("❌ Username already exists.")
            return
        password = input("🔑 Enter password: ")

        # Ask for banking info
        card = input("💳 Enter your card number: ")
        expiry = input("📅 Enter expiry date (MM/YY or MMYY): ")
        cvv = input("🔐 Enter CVV: ")

        self.members[username] = password
        self.user_carts[username] = []
        self.user_borrowed_books[username] = {}

        # Store banking info and registration/payment date
        self.payment_info[username] = {"card": card, "expiry": expiry, "cvv": cvv}
        self.payment_dates[username] = datetime.datetime.now()

        print(f"✅ Registered successfully as {username}. \n Payment Succesfull.")

        # Return to login menu if user registered from guest menu
        if self.current_user_type == "guest":
            self.current_user_type = None
            self.login_menu()



    def login_user(self):
        while True:
            username = input("👤 Enter username (or 'back' to return): ")
            if username.lower() == 'back':
                return
            
            password = input("🔑 Enter password: ")
            
            if username in self.members and self.members[username] == password:
                self.current_user = username
                self.current_user_type = "user"
                print(f"✅ Logged in as {username}.")
                self.user_menu()
                break
            else:
                print("❌ Invalid username or password.")

    def login_admin(self):
        while True:
            username = input("👤 Enter admin username (or 'back' to return): ")
            if username.lower() == 'back':
                return
            
            password = input("🔑 Enter admin password: ")
            
            if username in self.admins and self.admins[username] == password:
                self.current_user = username
                self.current_user_type = "admin"
                print(f"✅ Logged in as admin {username}.")
                self.admin_menu()
                break
            else:
                print("❌ Invalid admin credentials.")

    def logout(self):
        if self.current_user:
            print(f"👋 Logged out {self.current_user}.")
            self.current_user = None
            self.current_user_type = None
        else:
            print("⚠️ No user is currently logged in.")

    # ------------------- Member Functions ------------------- #
    def show_members(self):
        print("\n📋 Registered Members:")
        if not self.members:
            print("No members yet.")
        for user in self.members:
            print(f"👤 {user}")

    def add_member(self):
        username = input("👤 Enter new member username: ")
        if username in self.members or username in self.admins:
            print("❌ Username already exists.")
            return
        password = input("🔑 Enter password: ")
        self.members[username] = password
        self.user_carts[username] = []
        self.user_borrowed_books[username] = {}
        print(f"✅ Member '{username}' added successfully.")

    def remove_member(self):
        username = input("👤 Enter username to remove: ")
        if username in self.members:
            del self.members[username]
            if username in self.user_carts:
                del self.user_carts[username]
            if username in self.user_borrowed_books:
                del self.user_borrowed_books[username]
            print(f"✅ Member '{username}' removed successfully.")
        else:
            print("❌ Member not found.")

    # ------------------- Book Functions ------------------- #
    def add_book(self):
        title = input("📖 Enter book title: ")
        author = input("✍️ Enter author name: ")
        genre = input("🏷️ Enter genre: ")

        self.library_books[self.next_book_id] = {
            "title": title,
            "author": author,
            "genre": genre
        }
        print(f"✅ Book '{title}' added with ID {self.next_book_id}")
        self.next_book_id += 1

    def remove_book(self):
        self.show_books()
        try:
            book_id = int(input("Enter Book ID to remove (or 0 to cancel): "))
            if book_id == 0:
                return
            if book_id in self.library_books:
                del self.library_books[book_id]
                print(f"✅ Book with ID {book_id} removed.")
            else:
                print("❌ Invalid book ID.")
        except ValueError:
            print("❌ Please enter a valid number.")

    def show_books(self):
        if not self.library_books:
            print("📚 No books available right now.")
        else:
            print("\n📖 Available Books:")
            for book_id, book in self.library_books.items():
                print(f"ID: {book_id} | Title: {book['title']} | Author: {book['author']} | Genre: {book['genre']}")

    # ------------------- Cart Functions ------------------- #
    def add_to_cart(self):
        self.show_books()
        try:
            book_id = int(input("Enter Book ID to add to cart (or 0 to cancel): "))
            if book_id == 0:
                return
            if book_id in self.library_books:
                self.user_carts[self.current_user].append(book_id)
                self.undo_stack.append(("remove_from_cart", book_id))
                print(f"✅ '{self.library_books[book_id]['title']}' (ID: {book_id}) added to your cart.")
            else:
                print("❌ Invalid book ID.")
        except ValueError:
            print("❌ Please enter a valid number.")

    def remove_from_cart(self):
        if not self.user_carts[self.current_user]:
            print("📭 Your cart is empty.")
            return
        
        self.view_cart()
        try:
            book_id = int(input("Enter Book ID to remove from cart (or 0 to cancel): "))
            if book_id == 0:
                return
            if book_id in self.user_carts[self.current_user]:
                self.user_carts[self.current_user].remove(book_id)
                self.undo_stack.append(("add_to_cart", book_id))
                print(f"🗑️ Removed '{self.library_books[book_id]['title']}' (ID: {book_id}) from cart.")
            else:
                print("❌ That book isn't in your cart.")
        except ValueError:
            print("❌ Please enter a valid number.")

    def view_cart(self):
        cart = self.user_carts[self.current_user]
        if not cart:
            print("\n🛒 Your cart is empty.")
        else:
            print(f"\n🛒 Cart for {self.current_user}:")
            for book_id in cart:
                book = self.library_books[book_id]
                print(f"ID: {book_id} | Title: {book['title']} by {book['author']}")

    # ------------------- Borrow/Return Functions ------------------- #
    def borrow_books(self):
        if self.current_user_type == "guest":
            self.guest_borrow_book()
            return
            
        cart = self.user_carts[self.current_user]
        if not cart:
            print("❌ Your cart is empty.")
            return
        
        print(f"\n📦 Borrowing Books for {self.current_user}:")
        for book_id in cart.copy():
            book = self.library_books[book_id]
            print(f"📘 {book['title']} (ID: {book_id}) borrowed.")
            # Store the original book data
            self.user_borrowed_books[self.current_user][book_id] = book.copy()
            del self.library_books[book_id]
        
        self.user_carts[self.current_user] = []
        self.undo_stack.clear()  # Clear undo stack after borrowing
        print("✅ books borrowed! Extra fine of 200 will be applied if you donot return book in 30 days .")

    def guest_borrow_book(self):
        # Check if banking info is valid
        if not self.check_payment_validity(self.current_user):
            print("❌ Access expired or invalid banking info. You must re-register or update payment details.")
            return

        if self.current_user in self.guest_borrowed_books:
            print("❌ You already have a borrowed book. Please return it before borrowing another.")
            return

        self.show_books()
        try:
            book_id = int(input("Enter Book ID to borrow (or 0 to cancel): "))
            if book_id == 0:
                return
            if book_id in self.library_books:
                confirm = input("💸 This will charge RS:200 for a 1-week borrow. Extra fine of 200 will be applied if you donot return book in 1 week. Proceed? (yes/no): ").strip().lower()
                if confirm != "yes":
                    print("❌ Borrowing cancelled.")
                    return

                # Simulate payment
                print("Processing payment of RS:200...")
                print("✅ Payment successful.")

                # Proceed with borrowing
                book = self.library_books[book_id]
                print(f"📘 {book['title']} (ID: {book_id}) borrowed.")
                self.guest_borrowed_books[self.current_user] = book_id
                del self.library_books[book_id]
                print("Payment successfull.")
                print("✅ Book borrowed! Remember to return it before borrowing another.")
            else:
                print("❌ Invalid book ID.")
        except ValueError:
            print("❌ Please enter a valid number.")



    def return_books(self):
        if self.current_user_type == "guest":
            self.guest_return_book()
            return
            
        borrowed = self.user_borrowed_books.get(self.current_user, {})
        if not borrowed:
            print("❌ You have no borrowed books.")
            return
        
        print("\n📤 Your Borrowed Books:")
        for book_id, book in borrowed.items():
            print(f"ID: {book_id} | Title: {book['title']}")
        
        try:
            book_id = int(input("Enter Book ID to return (or 0 to cancel): "))
            if book_id == 0:
                return
            if book_id in borrowed:
                # Return the book with its original data
                self.library_books[book_id] = borrowed[book_id]
                del self.user_borrowed_books[self.current_user][book_id]
                print(f"✅ Returned: {self.library_books[book_id]['title']} (ID: {book_id})")
                # Clear undo stack when returning books
                self.undo_stack.clear()
                print("⚠️ Note: Undo is not available after returning books.")
            else:
                print("❌ You haven't borrowed a book with that ID.")
        except ValueError:
            print("❌ Please enter a valid number.")

    def guest_return_book(self):
        if self.current_user not in self.guest_borrowed_books:
            print("❌ You have no borrowed books.")
            return
            
        book_id = self.guest_borrowed_books[self.current_user]
        book = self.library_books.get(book_id, None)
        
        if not book:
            # Reconstruct book data if needed
            book = {"title": "Unknown", "author": "Unknown", "genre": "Unknown"}
        
        print(f"\n📤 Your Borrowed Book:")
        print(f"ID: {book_id} | Title: {book['title']}")
        
        confirm = input("Type 'return' to confirm returning this book: ")
        if confirm.lower() == 'return':
            self.library_books[book_id] = book
            del self.guest_borrowed_books[self.current_user]
            print(f"✅ Returned: {book['title']} (ID: {book_id})")
            print("You may now borrow another book.")
        else:
            print("❌ Return cancelled.")

    # ------------------- Undo Function ------------------- #
    def undo_last_action(self):
        if not self.undo_stack:
            print("⚠️ Nothing to undo.")
            return
        
        action, book_id = self.undo_stack.pop()
        
        if action == "add_to_cart":
            if book_id in self.library_books:
                self.user_carts[self.current_user].append(book_id)
                print(f"↩️ Undo: Re-added '{self.library_books[book_id]['title']}' (ID: {book_id}) to cart.")
            else:
                print("⚠️ Book no longer available to add back to cart.")
        elif action == "remove_from_cart":
            if book_id in self.user_carts[self.current_user]:
                self.user_carts[self.current_user].remove(book_id)
                print(f"↩️ Undo: Removed '{self.library_books[book_id]['title']}' (ID: {book_id}) from cart.")
            else:
                print("⚠️ Book not found in cart to remove.")

    # ------------------- Menu Functions ------------------- #
    def main_menu(self):
        while True:
            print("\n📚 Library Management System")
            print("1. Login")
            print("2. Register")
            print("3. Continue as Guest")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.login_menu()
            elif choice == '2':
                self.register()
            elif choice == '3':
                self.guest_login()
            else:
                print("❌ Invalid option. Please choose 1-3.")

    def guest_login(self):
        print("📚 As a guest, you can borrow books for RS: 200 per book (valid for 1 week).")
        proceed = input("Do you wish to continue? (yes/no): ").strip().lower()
        if proceed != "yes":
            print("❌ Guest login cancelled.")
            return

        username = input("👤 Enter a temporary username for your guest session: ")
        if username in self.members or username in self.admins:
            print("❌ Username already exists. Please choose another.")
            return
        password = input("🔑 Enter a temporary password: ")

        # Ask for banking info
        card = input("💳 Enter your card number: ")
        expiry = input("📅 Enter expiry date (MM/YY or MMYY): ")
        cvv = input("🔐 Enter CVV: ")

        self.current_user = username
        self.current_user_type = "guest"

        # Store banking info and payment date
        self.payment_info[username] = {"card": card, "expiry": expiry, "cvv": cvv}
        self.payment_dates[username] = datetime.datetime.now()

        print(f"✅ Logged in as guest {username}. Banking info saved.")
        self.guest_menu()


    def login_menu(self):
        while True:
            print("\n🔐 Login As:")
            print("1. User")
            print("2. Admin")
            
            choice = input("Enter your choice (1-2): ")
            
            if choice == '1':
                self.login_user()
                break
            elif choice == '2':
                self.login_admin()
                break
            else:
                print("❌ Invalid option. Please choose 1-2.")

    def user_menu(self):
        while self.current_user and self.current_user_type == "user":
            print(f"\n👤 User Menu ({self.current_user})")
            print("1. Show Books")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Borrow Books")
            print("6. Return Books")
            print("7. Undo Last Action")
            print("8. Logout")
            
            choice = input("Enter your choice (1-8): ")
            
            if choice == '1':
                self.show_books()
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.remove_from_cart()
            elif choice == '4':
                self.view_cart()
            elif choice == '5':
                self.borrow_books()
            elif choice == '6':
                self.return_books()
            elif choice == '7':
                self.undo_last_action()
            elif choice == '8':
                self.logout()
                break
            else:
                print("❌ Invalid option. Please choose 1-8.")

    def guest_menu(self):
        while self.current_user_type == "guest":
            print("\n👤 Guest Menu")
            print("1. Show Books")
            print("2. Borrow a Book")
            print("3. Return Book")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.show_books()
            elif choice == '2':
                self.borrow_books()
            elif choice == '3':
                self.return_books()
            elif choice == '4':
                self.current_user = None
                self.current_user_type = None
                return
            else:
                print("❌ Invalid option. Please choose 1-4.")

    def admin_menu(self):
        while self.current_user and self.current_user_type == "admin":
            print(f"\n👑 Admin Menu ({self.current_user})")
            print("1. Manage Books")
            print("2. Manage Members")
            print("3. Logout")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.manage_books_menu()
            elif choice == '2':
                self.manage_members_menu()
            elif choice == '3':
                self.logout()
            else:
                print("❌ Invalid option. Please choose 1-3.")

    def manage_books_menu(self):
        while self.current_user and self.current_user_type == "admin":
            print("\n📚 Manage Books")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. Show Books")
            print("4. Back to Admin Menu")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.remove_book()
            elif choice == '3':
                self.show_books()
            elif choice == '4':
                return
            else:
                print("❌ Invalid option. Please choose 1-4.")

    def manage_members_menu(self):
        while self.current_user and self.current_user_type == "admin":
            print("\n👥 Manage Members")
            print("1. Add Member")
            print("2. Remove Member")
            print("3. Show Members")
            print("4. Back to Admin Menu")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.remove_member()
            elif choice == '3':
                self.show_members()
            elif choice == '4':
                return
            else:
                print("❌ Invalid option. Please choose 1-4.")
    

    def check_payment_validity(self, username):
        # Check if payment date is within 30 days
        if username in self.payment_dates:
            register_date = self.payment_dates[username]
            days_passed = (datetime.datetime.now() - register_date).days
            if days_passed > 30:
                print("❌ Your payment has expired.")
                return False
        else:
            print("❌ No payment date found.")
            return False

        # Validate banking info
        info = self.payment_info.get(username)
        if not info:
            print("❌ No banking info found.")
            return False

        card = info.get("card", "")
        expiry = info.get("expiry", "")
        cvv = info.get("cvv", "")

        # Validate card number: 16 digits
        if not (card.isdigit() and len(card) == 16):
            print("❌ Invalid card number. Must be 16 digits.")
            return False

        # Validate CVV: 3 digits
        if not (cvv.isdigit() and len(cvv) == 3):
            print("❌ Invalid CVV. Must be 3 digits.")
            return False

        # Flexible expiry parsing: MM/YY or MMYY
        expiry = expiry.replace("/", "")
        if not (expiry.isdigit() and len(expiry) == 4):
            print("❌ Expiry must be 4 digits in MMYY or MM/YY format.")
            return False

        try:
            month = int(expiry[:2])
            year = int(expiry[2:]) + 2000  # Convert YY to YYYY
            if not 1 <= month <= 12:
                print("❌ Invalid expiry month.")
                return False

            now = datetime.datetime.now()
            expiry_date = datetime.datetime(year, month, 1)
            if expiry_date < now.replace(day=1):
                print("❌ Card has expired.")
                return False
        except ValueError:
            print("❌ Invalid expiry date.")
            return False

        return True  # All checks passed



# Start the library system
if __name__ == "__main__":
    library = LibrarySystem()
    library.main_menu()