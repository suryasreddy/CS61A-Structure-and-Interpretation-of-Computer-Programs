def convert_link(link):
    """Takes a linked list and returns a Python list with the same elements.

    >>> link = Link(1, Link(2, Link(3, Link(4))))
    >>> convert_link(link)
    [1, 2, 3, 4]
    >>> convert_link(Link.empty)
    []
    """
    if link == Link.empty:
        return []
    return [link.first] + convert_link(link.rest)


def every_other(s):
    """Mutates a linked list so that all the odd-indiced elements are removed
    (using 0-based indexing).

    >>> s = Link(1, Link(2, Link(3, Link(4))))
    >>> every_other(s)
    >>> s
    Link(1, Link(3))
    >>> odd_length = Link(5, Link(3, Link(1)))
    >>> every_other(odd_length)
    >>> odd_length
    Link(5, Link(1))
    >>> singleton = Link(4)
    >>> every_other(singleton)
    >>> singleton
    Link(4)
    """
    if s is Link.empty or s.rest is Link.empty:
        return
    else:
        s.rest = s.rest.rest
        every_other(s.rest)



def label_squarer(t):
    """Mutates a Tree t by squaring all its elements.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> label_squarer(t)
    >>> t
    Tree(1, [Tree(9, [Tree(25)]), Tree(49)])
    """
    t.label = t.label ** 2
    for b in t.branches:
        label_squarer(b)



def cumulative_mul(t):
    """Mutates t so that each node's label becomes the product of all labels in
    the corresponding subtree rooted at t.

    >>> t = Tree(1, [Tree(3, [Tree(5)]), Tree(7)])
    >>> cumulative_mul(t)
    >>> t
    Tree(105, [Tree(15, [Tree(5)]), Tree(7)])
    """
    for b in t.branches:
        cumulative_mul(b)
    total = t.label
    for b in t.branches:
        total *= b.label
    t.label = total



def has_cycle(link):
    """Return whether link contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle(t)
    False
    >>> u = Link(2, Link(2, Link(2)))
    >>> has_cycle(u)
    False
    """
    links = []
    while link is not Link.empty:
        if link in links:
            return True
        links.append(link)
        link = link.rest
    return False

def has_cycle_constant(link):
    """Return whether link contains a cycle.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle_constant(s)
    True
    >>> t = Link(1, Link(2, Link(3)))
    >>> has_cycle_constant(t)
    False
    """
    if link is Link.empty:
        return False
    slow, fast = link, link.rest
    while fast is not Link.empty:
        if fast.rest == Link.empty:
            return False
        elif fast is slow or fast.rest is slow:
            return True
        else:
            slow, fast = slow.rest, fast.rest.rest
    return False


def reverse_other(t):
    """Mutates the tree such that nodes on every other (odd-depth) level
    have the labels of their branches all reversed.

    >>> t = Tree(1, [Tree(2), Tree(3), Tree(4)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(4), Tree(3), Tree(2)])
    >>> t = Tree(1, [Tree(2, [Tree(3, [Tree(4), Tree(5)]), Tree(6, [Tree(7)])]), Tree(8)])
    >>> reverse_other(t)
    >>> t
    Tree(1, [Tree(8, [Tree(3, [Tree(5), Tree(4)]), Tree(6, [Tree(7)])]), Tree(2)])
    """
    def reverse_helper(t, reverse):
        if t.is_leaf():
            return
        new_labs = [child.label for child in t.branches][::-1]
        for i in range(len(t.branches)):
            child = t.branches[i]
            reverse_helper(child, not reverse)
            if reverse:
                child.label = new_labs[i]
    reverse_helper(t, True)

class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'


class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def map(self, fn):
        """
        Apply a function `fn` to each node in the tree and mutate the tree.

        >>> t1 = Tree(1)
        >>> t1.map(lambda x: x + 2)
        >>> t1.map(lambda x : x * 4)
        >>> t1.label
        12
        >>> t2 = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
        >>> t2.map(lambda x: x * x)
        >>> t2
        Tree(9, [Tree(4, [Tree(25)]), Tree(16)])
        """
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)

    def __contains__(self, e):
        """
        Determine whether an element exists in the tree.

        >>> t1 = Tree(1)
        >>> 1 in t1
        True
        >>> 8 in t1
        False
        >>> t2 = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
        >>> 6 in t2
        False
        >>> 5 in t2
        True
        """
        if self.label == e:
            return True
        for b in self.branches:
            if e in b:
                return True
        return False

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    def __str__(self):
        def print_tree(t, indent=0):
            tree_str = '  ' * indent + str(t.label) + "\n"
            for b in t.branches:
                tree_str += print_tree(b, indent + 1)
            return tree_str
        return print_tree(self).rstrip()



 def __init__(self, product, price):
        self.product = product
        self.price = price
        self.stock = 0
        self.balance = 0

    def restock(self, n):
        self.stock += n
        return 'Current {0} stock: {1}'.format(self.product, self.stock)

    def deposit(self, n):
        if self.stock == 0:
            return 'Machine is out of stock. Here is your ${0}.'.format(n)
        self.balance += n
        return 'Current balance: ${0}'.format(self.balance)

    def vend(self):
        if self.stock == 0:
            return 'Machine is out of stock.'
        difference = self.price - self.balance
        if difference > 0:
            return 'You must deposit ${0} more.'.format(difference)
        message = 'Here is your {0}'.format(self.product)
        if difference != 0:
            message += ' and ${0} change'.format(-difference)
        self.balance = 0
        self.stock -= 1
        return message + '.'

def __init__(self, product, price):
        self.product = product
        self.price = price
        self.stock = 0
        self.balance = 0
         
    def restock(self, amount):
        self.stock += amount
        return 'Current {0} stock: {1}'.format(self.product, self.stock)
         
         
    def deposit(self, amount):
        if self.stock == 0:
            return 'Machine is out of stock. Here is your ${0}.'.format(amount)
        else:
            self.balance += amount
            return 'Current balance: ${0}'.format(self.balance)
 
    def vend(self):
        if self.stock == 0:
            return 'Machine is out of stock.'
        elif self.balance < self.price:
            return 'You must deposit ${0} more.'.format(self.price - self.balance)
        elif self.balance == self.price:
            self.balance = 0
            self.stock -= 1
            return 'Here is your {0}.'.format(self.product)
        else:
            money = self.balance
            self.balance = 0
            self.stock -= 1
            return 'Here is your {0} and ${1} change.'.format(self.product, money - self.price)

#Mint
def __init__(self):
        self.update()

    def create(self, kind):
        return kind(self.year)

    def update(self):
        self.year = Mint.current_year

class Coin:
    def __init__(self, year):
        self.year = year

    def worth(self):
        "The worth is a coin's face value + 1 cent for each year over age 50."
        return self.cents + max(0, Mint.current_year - self.year - 50)

class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10


#is_bst
def bst_max(t):
    if t.is_leaf():
        return t.label
    return max(t.label, bst_max(t.branches[-1]))
def bst_min(t):
    if t.is_leaf():
        return t.label
    return min(t.label, bst_min(t.branches[0]))
if t.is_leaf():
    return True
if len(t.branches) == 1:
    return is_bst(t.branches[0]) and (t.label >= bst_min(t.branches[0]) or t.label < bst_max(t.branches[0]))
if len(t.branches) == 2:
    return is_bst(t.branches[0]) and is_bst(t.branches[1]) and bst_max(t.branches[0]) <= t.label and bst_min(t.branches[1]) > t.label
else:
    return False


#store_digits(n)
if n < 10:
    return Link(n)
else:
    string_n = str(n)
    first, all_but_first = int(string_n[0]), int(string_n[1:])
    return Link(first, store_digits(all_but_first))

store = Link.empty
while n > 0:
    store= Link(n % 10, store)
    n //= 10
return store


#def generate paths(t, x)
if label(t) == x:
        yield [x]
    for b in branches(t):
        for path in generate_paths(b, x):
            yield [label(t)] + path


#remove_all
p1, p2 = link, link.rest
while p2 is not Link.empty:
    if p2.first == value:
        p1.rest = p2.rest
    else:
        p1 = p1.rest
    p2 = p2.rest

if link is Link.empty or link.rest is Link.empty:
    return
if link.rest.first == value:
    link.rest = link.rest.rest
    remove_all(link, value)
else:
    remove_all(link.rest, value)


#deep_map
 if s is Link.empty:
    return s
else:
    if isinstance(s.first, Link):
        return Link(deep_map(f, s.first), deep_map(f, s.rest))
    else:
        return Link(f(s.first), deep_map(f, s.rest))

if link is Link.empty:
    return
elif isinstance(link.first, Link):
    deep_map_mut(fn, link.first)
else:
    link.first = fn(link.first)
deep_map_mut(fn, link.rest)