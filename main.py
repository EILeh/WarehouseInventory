"""
COMP.CS.100 Ohjelmointi 1 / Programming 1

Writers of the program:

writer 1: ehkuitti

writer 2: EILeh

This program saves information about different products to a dictionary. This
dictionary contains key-value pairs. The keys are product ID's and the values
are objects that contain the rest of the information about the products. This
data is read by parsing a text file which is formatted according to
pre-determined rules.

The program goes through the dictionary in a loop. It uses the Product ID:s to
find appropriate values and go through the dictionaries behind them. The
program can print information about stocks (compare them,
tell their size etc.), do the same to product categories
and set products on sale. The data is processed within
the dictionary. The text file isn't used once it's been
parsed into the dictionary for processing.
"""

# +--------------------------------------------------------------+
# | This template file requires at minimum Python version 3.8 to |
# | work correctly. If your Python version is older, you really  |
# | should get yourself a newer version.                         |
# +--------------------------------------------------------------+


LOW_STOCK_LIMIT = 30
HUNDRED_PERCENTAGE = 100
REQUIRED_AMOUNT_OF_PARAMETERS = 2
MINIMUM_STOCK_LIMIT = 0


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock, original_price=0):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        self.__original_price = original_price
        self.__has_price_been_changed = False

    def __str__(self):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests.
        """
        lines = [

            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def print_with_parameters(self, product_code):
        """
        Takes a product_code as a parameter and prints the attributes
        of only that product. Doesn't return anything (= implicitly
        returns a None)
        """
        lines = [

            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            if lines[i] == product_code:
                lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests since the read_database function will
        stop working correctly.
        """
        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        YOU SHOULD NOT MODIFY THIS METHOD since read_database
        relies on its behavior and might stop working as a result.

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """
        self.__stock += amount

    def get_stock_size(self):
        """
        Returns the stock size of a product based on its product ID.
        Doesn't take any external parameters, returns the value from
        the object attributes to the caller.
        """
        return self.__stock

    def get_product_category(self):
        """
        Returns the category of a product based on its product ID.
        Doesn't take any external parameters, returns the value from
        the object attributes to the caller.
        """
        return self.__category

    def get_product_price(self):
        """
        Returns the price of a product based on its product ID.
        Doesn't take any external parameters, returns the value from
        the object attributes to the caller.
        """
        return self.__price

    def combine_stock(self, other):
        """
        Takes another object as a parameter and uses the
        modify_stock_size() method of the first object to combine
        the stocks of the products.
        """
        self.modify_stock_size(other.get_stock_size())

    def compare_product_categories(self, other):
        """
        Takes another object as a parameter. Uses the
        get_product_category() method of both to return
        the product categories and then compares them.
        Returns a boolean to the caller based on whether
        the comparison evaluates to True or False
        (True = the same category, False = categories
        are different)
        """
        if self.get_product_category() == other.get_product_category():
            return True

        return False

    def compare_product_prices(self, other):
        """
        Takes another object as a parameter. Uses the
        get_product_price() method of both to return
        the product prices and then compares them.
        Returns a boolean to the caller based on whether
        the comparison evaluates to True or False
        (True = the same price, False = prices
        are different)
        """
        if self.get_product_price() == other.get_product_price():
            return True

        return False

    def set_product_on_sale(self, sale_percentage):
        """
        Checks how much is the product's price lowered and lowers the
        product's price.
        :param sale_percentage: The percentage that the price is reduced by
        from the product's original price.
        """
        # If zero is given as a sale_percentage, the ongoing sale is stopped.
        if sale_percentage == 0.0:
            self.__price = self.__original_price

        else:
            # If the __has_price_been_changed value is true, the new sale
            # percentage is taken from the original price, not the current
            # price.
            if self.__has_price_been_changed:
                # Counts a new price for the product.
                self.__price = self.__original_price - \
                               ((sale_percentage / HUNDRED_PERCENTAGE) *
                                self.__original_price)

            else:
                # Stores the original price.
                self.__original_price = self.__price

                # Counts a new price for the product.
                self.__price = self.__original_price - \
                               ((sale_percentage / HUNDRED_PERCENTAGE) *
                                self.__original_price)

                # Sets the __has_price_been_changed value as True.
                self.__has_price_been_changed = True


def _read_lines_until(fd, last_line):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION since read_database
    relies on its behavior and might stop working as a result.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """
    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION as it is ready.

    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    You don't necessarily need to understand how this function
    works as long as you understand what the return value is.
    You can probably learn something new though, if you examine the
    implementation.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """
    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(
                        f"Error: premature end of file while reading "
                        f"'{filename}'.")
                    return None

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(
                        maxsplit=1)  # ValueError possible

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(
                        f"Error: a product block is missing one or "
                        f"more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(
                            f"Error: product code '{product_code}' "
                            f"conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def is_product_found(warehouse, product_id):
    """
    This function checks if a desired product is found in the warehouse
    dictionary.
    :param warehouse: dict, stores product_id-product_object pairs
    :param product_id: integer, the product_id of the desired product
    :return: boolean, the answer to the question "was product found"
    """
    if product_id not in warehouse:
        return False

    return True


def command_print_with_parameters(warehouse, str_product_id):
    """
    Checks if a desired product is found in the warehouse dictionary. If the
    product is found, prints all the information about it.
    :param warehouse: dict, stores product_id-product_object pairs
    :param str_product_id: str, the product_id of the desired product
    :return: doesn't return anything (= returns None implicitly)
    """
    product_id = 0

    # Tries to change the string to integer, if it can't be done, raises a
    # ValueError and returns to the caller.
    try:
        product_id = int(str_product_id)

    except ValueError:
        print(
            f"Error: product '{str_product_id}' can not be printed as it does "
            f"not exist.")
        return

    # If function is_product_found returns false, prints an error and returns
    # to the caller.
    if not is_product_found(warehouse, product_id):
        print(
            f"Error: product '{product_id}' can not be printed as it does "
            f"not exist.")
        return

    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Prints product details if the product is found.
    for key, word in warehouse.items():
        if product_id == key:
            print(word)


def command_change(warehouse, parameters):
    """
    Adds or subtracts the amount of a product from the warehouse.

    :param warehouse: dict, stores product_id-product_object pairs
    :param parameters: str, contains the amount to be processed
    :return: doesn't return anything (= returns None implicitly)
    """
    product_id = 0
    amount_of_change = 0

    split_parameters = parameters.split()

    if len(split_parameters) != REQUIRED_AMOUNT_OF_PARAMETERS:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for change command.")
        return

    str_product_id = split_parameters[0]
    str_amount_of_change = split_parameters[1]

    # Tries to convert product_id into an integer. If this fails,
    # the product_id is invalid because it can only contain numbers.
    try:
        product_id = int(str_product_id)

    except ValueError:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for change command.")
        return

    # An error is printed if change cannot be converted into an integer
    try:
        amount_of_change = int(str_amount_of_change)

    except ValueError:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for change command.")
        return

    if not is_product_found(warehouse, product_id):
        print(f"Error: stock for '{product_id}' can not be changed as it does "
              f"not exist.")
        return

    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Calls the method modify_stock_size to change the
    # amount of stock of the current product.
    for key, word in warehouse.items():
        if product_id == key:
            word.modify_stock_size(amount_of_change)


def command_delete(warehouse, parameters):
    """
    The function deletes a product based on its product id.
    Prints an error if the product isn't found or if the
    parameters are invalid, i.e there are too many or too
    little values given.
    :param warehouse: dict, product_id-product_object pairs
    :param parameters: str, the product to be deleted
    :return: None (implicitly)
    """
    product_id = 0

    # Tries to convert product_id into an integer. If this fails,
    # the product_id is invalid because it can only contain numbers.
    try:
        product_id = int(parameters)

    except ValueError:
        print(f"Error: product '{parameters}' can not be deleted as it does "
              f"not exist.")
        return

    if not is_product_found(warehouse, product_id):
        print(f"Error: product '{product_id}' can not be deleted as it does "
              f"not exist.")
        return

    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Calls the method get_stock_size to check that the
    # stock isn't less than zero. Removes the product if its stock is empty.
    for key, value in warehouse.items():
        if product_id == key:
            if value.get_stock_size() > MINIMUM_STOCK_LIMIT:
                print(f"Error: product '{product_id}' can not be deleted as "
                      f"stock remains.")
                break

            else:
                warehouse.pop(key)
                break


def command_low(warehouse):
    """
    Prints products whose stocks are below a critical limit.
    :param warehouse: dict, product_id-product_object pairs
    :return: None (implicitly)
    """
    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Calls the method get_stock_size to inform the user if
    # the stock is less than 30 and prints the value.
    for key, value in sorted(warehouse.items()):
        if value.get_stock_size() < LOW_STOCK_LIMIT:
            print(value)


def command_print(warehouse):
    """
    Prints though the object dictionary. Prints
    product ID's (key) and product_object
    attributes (payload).
    :param warehouse: dict, product_id-product_object pairs
    :return: None (implicitly)
    """
    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Prints the products.
    for key, product in sorted(warehouse.items()):
        print(product)


def command_combine(warehouse, parameters):
    """
    Uses the object comparison methods to
    compare specified products. Checks if the
    parameter amount is correct and tries to
    convert product_id into an integer. Checks
    also if both products are found. If
    everything succeeds, combines the products
    using their respective methods.
    :param warehouse: dict, product_id-product_object pairs
    :param parameters: str, includes the second product_id
    :return: None (implicitly)
    """
    split_parameters = parameters.split()

    product_id_1 = 0
    product_id_2 = 0

    if len(split_parameters) != REQUIRED_AMOUNT_OF_PARAMETERS:
        print(
            f"Error: bad command line 'combine {parameters}' "
            f"for combine command.")
        return

    str_product_id_1 = split_parameters[0]
    str_product_id_2 = split_parameters[1]

    # Tries to convert product_id into an integer. If this fails,
    # the product_id is invalid because it can only contain numbers.
    try:
        product_id_1 = int(str_product_id_1)

    except ValueError:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for combine command.")
        return

    # An error is printed if change cannot be converted into an integer
    try:
        product_id_2 = int(str_product_id_2)

    except ValueError:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for combine command.")
        return

    if not is_product_found(warehouse, product_id_1):
        print(
            f"Error: bad parameters '{parameters}' "
            f"for combine command.")
        return

    if not is_product_found(warehouse, product_id_2):
        print(
            f"Error: bad parameters '{parameters}' "
            f"for combine command.")
        return

    product_id_1 = int(split_parameters[0])
    product_id_2 = int(split_parameters[1])

    if product_id_1 == product_id_2:
        print(f"Error: bad parameters '{parameters}' "
              f"for combine command.")
        return

    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID.
    for key, value in warehouse.items():

        # Uses the product category comparison method to compare whether the
        # product in question has the same category as the caller object.
        if not warehouse[product_id_1] \
                .compare_product_categories(warehouse[product_id_2]):
            print(f"Error: combining items of different categories "
                  f"'{warehouse[product_id_1].get_product_category()}' "
                  f"and "
                  f"'"
                  f"{warehouse[product_id_2].get_product_category()}'.")
            break

        # Uses the price comparison method to compare whether the
        # product in question has the same price as the caller object.
        if not warehouse[product_id_1] \
                .compare_product_prices(warehouse[product_id_2]):
            print(f"Error: combining items with different prices "
                  f"{warehouse[product_id_1].get_product_price()}€ "
                  f"and "
                  f"{warehouse[product_id_2].get_product_price()}€.")
            break

        else:
            # Calls the method modify_stock_size to combine the products'
            # stocks together. Calls the method get_stock_size to get the
            # stock size of a product from the index of product_id_2 in the
            # warehouse dictionary. Once the value has been gotten, adds it to
            # product_id_1's stock. Removes the product_id_2 from the
            # warehouse dictionary.

            warehouse[product_id_1].modify_stock_size(
                warehouse[product_id_2].get_stock_size())
            warehouse.pop(product_id_2)
            break


def command_sale(warehouse, parameters):
    """
    Sets a product on sale.
    :param warehouse: dict, product_id-product_object pairs
    :param parameters: str, includes the second product_id
    :return: None (implicitly)
    """
    split_parameters = parameters.split()

    product_category = split_parameters[0]
    str_product_sale_percentage = split_parameters[1]
    product_sale_percentage = 0.0

    # If sale percentage cannot be converted into a float,
    # it includes letters and is thus invalid.
    try:
        product_sale_percentage = float(str_product_sale_percentage)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for sale command.")
        return

    i = 0

    # Goes through the warehouse dictionary and tries to find a product based
    # on a product ID. Calls the method get_product_category to check that
    # the products to be combined have the same category.
    for key, value in warehouse.items():
        if product_category == value.get_product_category():
            # Calls the method set_product_on_sale to set a new price for the
            # product.
            value.set_product_on_sale(product_sale_percentage)
            i += 1

    print(f"Sale price set for {i} items.")


def main():
    filename = input("Enter database name: ")

    warehouse = read_database(filename)
    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        if "print".startswith(command) and parameters == "":
            command_print(warehouse)

        elif "print".startswith(command) and parameters != "":
            command_print_with_parameters(warehouse, parameters)

        elif "delete".startswith(command) and parameters != "":
            command_delete(warehouse, parameters)

        elif "change".startswith(command) and parameters != "":
            command_change(warehouse, parameters)

        elif "low".startswith(command) and parameters == "":
            command_low(warehouse)

        elif "combine".startswith(command) and parameters != "":
            command_combine(warehouse, parameters)

        elif "sale".startswith(command) and parameters != "":
            command_sale(warehouse, parameters)

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
