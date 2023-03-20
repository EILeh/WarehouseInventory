"""
COMP.CS.100 Ohjelmointi 1 / Programming 1

StudentId: 150541820
Name:      Eetu Kuittinen
Email:     eetu.kuittinen@tuni.fi

StudentId: 151309919
Name:      Elli Lehtimäki
Email:     elli.i.lehtimaki@tuni.fi
"""

# +--------------------------------------------------------------+
# | This template file requires at minimum Python version 3.8 to |
# | work correctly. If your Python version is older, you really  |
# | should get yourself a newer version.                         |
# +--------------------------------------------------------------+


LOW_STOCK_LIMIT = 30


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock

        # TODO (MAYBE): You might want to add more attributes here. :) Ö == :0

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

        # Halutaan tulostaa vain ne tiedot, jotka löytyvät product_coden "takaa"

        # for product_code in

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

    # TODO: Multiple methods need to be written here to allow
    #       all the required commands to be implemented.


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

    # MUISTA POISTAA SEURAAVA KOMMENTTI!!!!!!!!
    """
    Tämä koodi lukee tiedoston nimeltä filename, joka sisältää tietoja tuotteista. 
    Tiedoston oletetaan olevan UTF-8 -koodattu ja sen oletetaan sisältävän tuotetietoja, 
    joita on eroteltu merkkijonoilla "BEGIN PRODUCT" ja "END PRODUCT". Koodi 
    käsittelee kukin tuote blokkina, jossa kukin rivi edustaa yhtä tietoa tuotteesta. 
    Tuotteen tietoja ovat "CODE", "NAME", "CATEGORY", "PRICE" ja "STOCK". Koodi 
    yrittää parsia jokaisen tuotteen tiedot ja luoda niistä Product-olion, joka 
    lisätään sanakirjaan nimeltä data. Sanakirjan avaimena käytetään tuotekoodia
    ("CODE"). Koodi yrittää myös käsitellä virhetilanteita, kuten tiedoston avaamisen
    epäonnistuminen (OSError) tai tiedostosta lukemisen aikana tapahtuvat virheet 
    (ValueError). Jos mikään virheistä tapahtuu, koodi palauttaa None. Muussa 
    tapauksessa koodi palauttaa sanakirjan data, joka sisältää kaikkien luettujen
    tuotteiden tiedot.
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
                        f"Error: premature end of file while reading '{filename}'.")
                    return None

                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(
                        maxsplit=1)  # ValueError possible

                    # print(f"TEST: {keyword=} {value=}")

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
                        f"Error: a product block is missing one or more data lines.")
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

                # print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(
                            f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def example_function_for_example_purposes(warehouse, parameters):
    """
    This function is an example of how to deal with the extra
    text user entered on the command line after the actual
    command word.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, all the text that the user entered after the command word.
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be one int and one float) in
        # the <parameters> string.
        code, number = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        number = float(number)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for example command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in warehouse:
        print(f"Error: unknown product code '{code}'.")
        return

    # All the errors were checked above, so everything should be
    # smooth sailing from this point onward. Of course, the other
    # commands might require more or less error/sanity checks, this
    # is just a simple example.

    print("Seems like everything is good.")
    print(f"Parameters are: {code=} and {number=}.")


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



def limit_values_to_a_desired_product(warehouse, str_product_id):
    """
    Checks if a desired product is found in the warehouse dictionary. If the
    product is found, prints all the information about it.
    :param warehouse: dict, stores product_id-product_object pairs
    :param str_product_id: str, the product_id of the desired product
    :return: doesn't return anything (= returns None implicitely)
    """

    product_id = 0

    try:
        product_id = int(str_product_id)

    except ValueError:
        print(
            f"Error: product '{str_product_id}' can not be printed as it does "
            f"not exist.")
        return

    if not is_product_found(warehouse, product_id):
        print(
            f"Error: product '{product_id}' can not be printed as it does "
            f"not exist.")
        return

    for key, word in warehouse.items():
        if product_id == key:
            print(word)


def change(warehouse, parameters):
    """
    Adds or subtracts the amount of a product from the warehouse.
    :param warehouse: dict, stores product_id-product_object pairs
    :param parameters: str, contains the amount to be processed
    :return: doesn't return anything (= returns None implicitely)
    """

    product_id = 0
    amount_of_change = 0

    splitted_parameters = parameters.split()

    if len(splitted_parameters) != 2:
        print(
            f"Error: bad parameters '{parameters}' "
            f"for change command.")
        return

    str_product_id = splitted_parameters[0]
    str_amount_of_change = splitted_parameters[1]

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

    for key, word in warehouse.items():
        if product_id == key:
            word.modify_stock_size(amount_of_change)


def main():
    # filename = input("Enter database name: ")

    filename = "simpleproducts.txt"
    # filename = "products.txt"

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

        # If you have trouble undestanding what the values
        # in the variables <command> and <parameters> are,
        # remove the '#' comment character from the next line.
        #    print(f"TEST: {command=} {parameters=}")

        if "example".startswith(command) and parameters != "":
            """
            'Example' is not an actual command in the program. It is
            implemented only to allow you to get ideas how to handle
            the contents of the variable <parameters>.

            Example command expects user to enter two values after the
            command name: an integer and a float:

                Enter command: example 123456 1.23

            In this case the variable <parameters> would refer to
            the value "123456 1.23". In other words, everything that
            was entered after the actual command name as a single string.
            """

            example_function_for_example_purposes(warehouse, parameters)

        elif "print".startswith(command) and parameters == "":

            for key, product in sorted(warehouse.items()):
                print(product)

        elif "print".startswith(command) and parameters != "":

            limit_values_to_a_desired_product(warehouse, parameters)

        elif "delete".startswith(command) and parameters != "":
            # TODO: Implement delete command for removing
            #       a product from the inventory.
            ...

        elif "change".startswith(command) and parameters != "":
            change(warehouse, parameters)


        elif "low".startswith(command) and parameters == "":
            # TODO: Implement low command which can be used to
            #       alert the user when the amount of items
            #       drop below <LOW_STOCK_LIMIT> i.e. 30.
            ...

        elif "combine".startswith(command) and parameters != "":
            # TODO: Implement combine command which allows
            #       the combining of two products into one.
            ...

        elif "sale".startswith(command) and parameters != "":
            # TODO: Implement sale command which allows the user to set
            #       a sale price for all the products in a specific category.
            ...

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
