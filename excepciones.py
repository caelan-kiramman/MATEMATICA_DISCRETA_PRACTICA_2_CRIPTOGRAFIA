class Nop(Exception): pass
class IncompatibleEquationError(Exception): pass

class NonExistingUser(Exception):
    '''
    Indicates that a user does not exists, therefore, it has no key linked to it
    '''

    pass